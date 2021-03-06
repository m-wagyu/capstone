import psutil
import json
import subprocess as sp
import time
import re

from .sccontrol_helper.alert import alert as alert_mod
from .sccontrol_helper.rule import rule_parser as rp_mod, rule_validator as rv_mod
from .sccontrol_helper.scsocket import control_socket
from .sccontrol_helper import sc_config_reader as cc
from . import config_reader as cr


class Controller():
    
    def __init__(self):
        self.sc_conf_file = cr.get_sc_config()
        cmd_addition = cr.get_sc_param()
        self.default_cmd = ['suricata','-D','-c',self.sc_conf_file] + cmd_addition
        
        self.files = cc.get_config_path(self.sc_conf_file)
        self.var_group = cc.get_config_group(self.sc_conf_file)
        
        self.socket = control_socket.ControlSocket(self.files['sc_socket'])
    
    def __proc_pid(self):
        for proc in psutil.process_iter():
          if proc.name().lower().startswith('suricata'):
            return proc.pid
        return None


###### Public Accessible ######

    def proc_is_run(self):
        if self.__proc_pid():
          return {'result':'success'}
        return {'result':'not-success'}

    def proc_start(self):
        try:
            self.files = cc.get_config_path(self.sc_conf_file)
            self.var_group = cc.get_config_group(self.sc_conf_file)
            sp.run(self.default_cmd, stdout=sp.DEVNULL, stderr= sp.DEVNULL)
            time.sleep(0.01)
        except Exception as e:
            return {'result': 'not-success', 'error':str(e)}
        return {'result':'success'}

    def proc_stop(self):
        try:
            self.socket.s_connect()
            r = self.socket.send_cmd('shutdown')
            self.socket.s_close()
        except OSError:
            return {'result':'not-success', 'error':'Socket error'}
        if r['return'] == "OK":
            return {'result':'success'}
        else:
            for proc in psutil.process_iter():
                if proc.name().lower().startswith('suricata'):
                    proc.terminate()
            time.sleep(0.02)
            if __proc_pid():
                return {'result':'not-success', 'error':'Fail shutting down using psutil'}
            else:
                return {'result':'success'}
    
    def proc_reload(self):
        try:
            self.socket.s_connect()
            r = self.socket.send_cmd('reload-rules')
            self.socket.s_close()
        except OSError:
            return {'result':'not-success', 'error':'Socket error'}
        
        if r['return'] == "OK":
            return {'result': 'success'}
        else:
            return {'result':'not-success', 'error':'Other error'}
    
    def log_get(self):
        # rx message is generated when process is started
        rx = re.compile('.*<Notice>.*running in .*mode$')
        rx1 = re.compile(' - ')
        rx2 = re.compile('[<>]')
        buf = []
        
        try:
            with open(self.files['suricata'],'r') as f:
                for line in f:
                    if re.match(rx,line):
                        buf = []
                    s = re.split(rx1,line.strip())
                    
                    if len(s) == 3:
                        msg = {'ts':s[0], 'type':re.sub(rx2,'',s[1]), 'msg':s[2]}
                    else:
                        msg = {'ts':s[0], 'type':re.sub(rx2,'',s[1]), 'msg':s[3]}
                    buf.append(msg)
            return {'result':'success', 'msg':buf}
        
        except OSError:
            return {'result':'not-success', 'error':'File '+self.files['suricata']+' not found'}
    
    
    def alert_get(self, page_num, count):
        buf = []
        # i counts how many alerts
        i = 0
        
        try:
            with open(self.files['eve'],'r') as f:
                line = json.loads(f.readline())
                while line:
                    if line['event_type'] == 'alert':
                        if (i >=  page_num * count) and (i < (page_num + 1)*count):
                            a = alert_mod.alert_build(line)
                            if a:
                                buf.append(a)
                        i += 1
                    line = json.loads(f.readline())
            return {'result':'success', 'msg':{'alerts':buf,'total':i}}
        
        except OSError:
            return {'result':'not-success', 'error':'File '+self.files['eve']+' not exists'}
        except json.JSONDecodeError:
            return {'result':'success', 'msg':{'alerts':buf,'total':i}}
    
    
    def alert_clear(self):
        if self.__proc_pid():
            return {'resullt':'not-success', 'error':'Suricata is running'}
        
        try:
            open_file = self.files['eve']
            with open(open_file,'w') as f:
                pass
            open_file = self.files['fast']
            with open(open_file,'w') as f:
                pass
            return {'result':'success'}
        except OSError:
            return {'result':'not-success', 'error':'File '+open_file+' not found'}
    
    
    def stats_get(self):
        out = {'result':'success','msg':{'uptime':None,'version':None,'iface-list':None}}
        
        try:
            ver = sp.check_output(['suricata','-V']).decode().strip()
            ver = re.search(r'[0-9](\.[0-9]){2}',ver).group(0)
            out['msg']['version'] = ver
        except Exception:
            return out
        
        try:
            self.socket.s_connect()
            key = 'uptime'
            r = self.socket.send_cmd(key)
            if r['return'] == 'OK':
                out['msg']['uptime'] = r['message']
            else:
                return out
            
            key = 'iface-list'
            r = self.socket.send_cmd(key)
            out['msg']['iface-list'] = []
            if r['return'] == 'OK':
                for i in r['message']['ifaces']:
                    out['msg']['iface-list'].append({'name':i})
            else:
                return out
            
            for i, val in enumerate(out['msg']['iface-list']):
                r = self.socket.send_cmd('iface-stat',val['name'])
                if r['return'] == 'OK':
                    out['msg']['iface-list'][i]['pkts'] = r['message']['pkts']
                    out['msg']['iface-list'][i]['drop'] = r['message']['drop']
                    out['msg']['iface-list'][i]['invalid-checksums'] = r['message']['invalid-checksums']
                else:
                    return out
            self.socket.s_close()
        except OSError:
          self.socket.s_close()
    
        sg = {}
        tg = {}
        
        try:
            with open(self.files['eve'],'r') as f:
                line = json.loads(f.readline())
                while line:
                    if line['event_type'] == 'alert':
                        # populate tg
                        ts = line['timestamp'].split('T')
                        date = ts[0]
                        hr = ts[1].split(':')[0]
                        if not date in tg.keys():
                            tg[date] = {}
                            tg[date][hr] = 1
                        else:
                            if not hr in tg[date].keys():
                                tg[date][hr] = 1
                            else:
                                tg[date][hr] += 1
                        # populate sg
                        sid = line['alert']['signature_id']
                        addr = line['src_ip']+'_'+line['dest_ip']
                        if sid in sg.keys():
                            if addr in sg[sid].keys():
                                sg[sid][addr] += 1
                            else:
                                sg[sid][addr] = 1
                        else:
                            sg[sid] = {}
                            sg[sid][addr] = 1
                    
                    line = json.loads(f.readline())
                out['msg']['counter'] = sg
                out['msg']['per_hour'] = tg
        except OSError:
            out['result'] = 'not-success'
            out['error'] = 'File eve.json not found'
        except json.decoder.JSONDecodeError:
            out['msg']['counter'] = sg
            out['msg']['time_group'] = tg
        finally:
            return out
    
    
    def rule_get(self,page_num,count):
        out = {'result':'success','msg':{'rules':[],'total':None}}
        try:
            with open(self.files['rule'],'r') as f:
                rx = re.compile('^[ \t]*$')
                r = f.readline()
                i = 0
                while r:
                    if (i >= page_num * count) and (i < (page_num + 1)*count):
                        if re.match(rx,r):
                            r = f.readline()
                            continue
                        p = rp_mod.RuleParser(r,
                            var_port=self.var_group['port'],
                            var_addr=self.var_group['addr'],
                            line_num=i+1)
                        out['msg']['rules'].append(p.get_rule())
                        r = f.readline()
                        i += 1
                    elif (i < page_num*count) or (i >= (page_num+1)*count) :
                        r = f.readline()
                        i += 1
                        continue
            out['msg']['total'] = i
            return out
        except OSError: 
            return {'result':'not-success','error':'File '+ self.files['rule']+' not found.'}
    
    
    def rule_add(self,rule:dict):
        try:
            rv_mod.RuleValidator(rule, self.var_group['addr'], self.var_group['port'])
            r = rv_mod.build_rule(rule)+'\n'
            with open(self.files['rule'], 'a') as f:
                f.write(r)
            return {'result':'success','msg':r}
        except rv_mod.InvalidRuleError as e:
            return {'result':'not-success','error':str(e)}
        except OSError:
            return {'result':'not-success','error':'Error while appending rule'}
