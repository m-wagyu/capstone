import subprocess as sp
from os.path import isdir
import psutil
import io
from time import sleep
import consock
import re
import json
import yaml
import config_collector as cc
import parser


# Process => the NIDS(Suricata)

#LIST OF FEATURES ON THIS CLASS:
# - start process
# - stop process
# - reload process
# - get alert
# - clear alert
# - get runtime log
# - get stats
# - get rule
# - make a method to populate self.var_group
# - make a method to check conf_file & populate self.files

#TODO:
# - add rule
# - refactor


class Controller():
  def __init__(self, conf_file: str):
    self.conf_file = conf_file
    self.default_cmd = ['suricata','-D','-c',self.conf_file,'-q','0']
    self.socket = consock.ConSock('/var/run/suricata/suricata-command.socket')

    self.files = cc.get_config_path(self.conf_file) 
    self.var_group = cc.get_config_group(self.conf_file)    # get valid address and port groups in config file

    self.tmp_dir = '/tmp/Suricata_controller/'

  

  # return process id if the process is running, else False
  @staticmethod
  def proc_is_run():
    for proc in psutil.process_iter():
      if proc.name().lower().startswith("suricata"):
        return proc.pid
    return False

  def __build_rule(self, rule):
    return "{}{} {} {} {} {} {} {} (msg:\"{}\"; sid:{}; gid:{};)".format('#' if not rule['enabled'] else '',
rule["action"], rule["proto"],
rule["src_addr"], rule["src_port"],
rule["direction"],
rule["dst_addr"], rule["dst_port"],
rule['msg'], rule['sid'], rule['gid'])

  def __get_runtime_log(self):
    regex = '^.*<Notice>.*running in .*mode$'
    buf = []
    try:
      with open(self.files['suricata'],'r') as f:
        for l in f:
          if re.match(regex,l):
            buf = []
          s = re.split(' - ',l.strip())
          if len(s) == 3:
            buf.append({'ts':s[0],'type':re.sub(r'[<>]','',s[1]),'msg':s[2]})
          else:
            buf.append({'ts':s[0],'type':re.sub(r'[<>]','',s[1]),'msg':s[3]})
      return {'result':"OK",'msg':buf}
    except OSError:
      return {'result':"NOK",'error':'File '+self.files['suricata']+' not found'}

  @staticmethod
  def __get_config_path(c_file):
    try:
      out = {}
      f = open(c_file,'r')
      buf = f.read()
      conf = yaml.load(buf)
      out['eve'] = conf['default-log-dir']+conf['outputs'][1]['eve-log']['filename']
      out['fast'] = conf['default-log-dir']+conf['outputs'][0]['fast']['filename']
      out['suricata'] = conf['default-log-dir']+conf['logging']['outputs'][1]['file']['filename']
      out['rule'] = '/var/lib/suricata/rules/suricata.rules'
      f.close()
      return out
    except OSError:
      return {'eve':'/var/log/suricata/eve.json',
	'fast':'/var/log/suricata/fast.json',
	'rule':'/var/lib/suricata/rules/suricata.rules',
	'suricata':'/var/log/suricata/suricata.log'}
 

####### Publicly accessible methods ######

### proc related ###

  def proc_start(self):
    #__get_config_path()
    #__get_config_group()
    try:
      if not isdir(self.tmp_dir):
        sp.run(['mkdir','-p',self.tmp_dir])
      sp.run(['cp', self.conf_file, self.tmp_dir], stdout=sp.DEVNULL)
      sp.run(self.default_cmd,stdout=sp.DEVNULL)
    except Exception:
      return {'result':'NOK','error':'Other error'}
    return {'result':'OK'}

  # for testing /api/server_action/start
  def proc_start2(self):
    try:
      self.files = cc.get_config_path(self.conf_file) 
      self.var_group = cc.get_config_group(self.conf_file) 
      sp.run(self.default_cmd,stdout=sp.DEVNULL)
      sleep(0.01)
    except Exception as e:
      return {'result':'not-success','error':str(e)}
    return {'result':'success'}

  def proc_stop(self):
    try:
      self.socket.s_connect()
      r = self.socket.send_cmd('shutdown')
      self.socket.s_close()
      if r['return'] == 'OK':
        return {'result':'OK'}
      else:
        return {'result':'NOK','error':'other error'}
    except OSError:
      return {'result':'NOK','error':'socket error'}

  def proc_reload(self):
    try:
      self.socket.s_connect()
      r = self.socket.send_cmd('reload-rules')
      self.socket.s_close()
      if r['return'] == 'OK':
        return {'result':'OK'}
      else:
        return {'result':'NOK','error':'other error'}
    except OSError:
      return {'result':'NOK','error':'Socket error'}

  def log_get(self):
    out = self.__get_runtime_log()
    if out['result'] == "OK":
      return {'result':'OK','msg':out['msg']}
    else:
      return {'result':'NOK','error':out['error']}

### Alerts related ###

  def alert_get(self,page_num=None,count_per_page=None):
    buf = []
    load = True
    if type(page_num) == int and type(count_per_page) == int:
      load = (page_num*count_per_page,
      	((page_num+1)*count_per_page)-1)
    try:
      i = 0
      with open(self.files['eve'],'r') as f:
        if load == True:
          alert = json.loads(f.readline())
          while alert:
            if alert['event_type'] == 'alert':
              ts = alert['timestamp'].split('T')
              date = ts[0]
              time = ts[1].split('.')[0]
              if 'src_port' in alert.keys():
                src = "{}:{}".format(alert['src_ip'],alert['src_port'])
              else:
                src = alert['src_ip']
              if 'dest_port' in alert.keys():
                dst = "{}:{}".format(alert['dest_ip'],alert['dest_port'])
              else:
                dst = alert['dest_ip']
              a = {'time':'{} {}'.format(date,time),
	  	'src_dst':'{} -> {}'.format(src,dst),
	  	'proto':alert['proto'],
	  	'action':alert['alert']['action'],
	  	'message':alert['alert']['signature']}
              buf.append(a)
              i += 1
            alert = json.loads(f.readline())
        else:
          alert = json.loads(f.readline())
          while alert:
            if alert['event_type'] == 'alert':
              #if i > load[1]:
              #  break
              if i >= load[0] and i <= load[1]:
                ts = alert['timestamp'].split('T')
                date = ts[0]
                time = ts[1].split('.')[0]
                if 'src_port' in alert.keys():
                  src = "{}:{}".format(alert['src_ip'],alert['src_port'])
                else:
                  src = alert['src_ip']
                if 'dest_port' in alert.keys():
                  dst = "{}:{}".format(alert['dest_ip'],alert['dest_port'])
                else:
                  dst = alert['dest_ip']
                a = {'time':'{} {}'.format(date,time),
	          'src_dst':'{} -> {}'.format(src,dst),
	          'proto':alert['proto'],
	          'action':alert['alert']['action'],
	          'message':alert['alert']['signature']}
                buf.append(a)
              i += 1
            alert = json.loads(f.readline())
      return {'result':'OK','msg':{'alerts':buf,'total':i}}
    except OSError:
      return {'result':'NOK','error':'File not exist'} 
    except json.JSONDecodeError:
      return {'result':'OK','msg':{'alerts':buf,'total':i}}

  def alert_clear(self):
    if Controller.proc_is_run():
      return {'result':'NOK','error':'Suricata is running'}
    try:
      open_file = self.files['eve']
      with open(open_file,'w') as f:
        pass
      open_file = self.files['fast']
      with open(open_file,'w') as f2:
        pass
      return {'result':'OK'}
    except OSError:
      return {'result':'NOK','error':'File '+open_file+' not found.'}


### Statss related ###

  # show uptime -> suricatasc['uptime'] (in seconds)
  # show interface list -> suricatasc['iface-list']['ifaces']
  # show packets received, dropped suricatasc['iface-stat'][<iface>]['pkts'] for each iface
  # show most frequent rule hit (in table)
    # select a rule and show the source ip and dest ip hits
  # show activity based on past 24 hr (divide by each hour)
  def stats_get(self):
    out = {'result':'OK','msg':{'uptime':None,'version':None,'iface-list':None}}

    try:
      ver = sp.check_output(['suricata','-V']).decode().strip()
      ver = re.search(r'[0-9](\.[0-9]){2}',ver).group(0)
      out['msg']['version'] = ver
    except Exception:
      return out

    try:
      self.socket.s_connect()

      trying = 'uptime'
      r = self.socket.send_cmd('uptime')
      if r['return'] == 'OK':
        out['msg']['uptime'] = r['message']
      else:
        return out

      r = self.socket.send_cmd('iface-list')
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
        event = json.loads(f.readline())
        #line = 0
        while event:
          if event['event_type'] == 'alert':
            # populate tg
            ts = event['timestamp'].split('T')
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
            sid = event['alert']['signature_id']
            addr = event['src_ip']+'_'+event['dest_ip']
            if sid in sg.keys():
              if addr in sg[sid].keys():
                sg[sid][addr] += 1
              else:
                sg[sid][addr] = 1
            else:
              sg[sid] = {}
              sg[sid][addr] = 1
          #line += 1
          event = json.loads(f.readline())
        out['msg']['counter'] = sg
        out['msg']['per_hour'] = tg
    except OSError:
      out['result'] = 'NOK'
      out['error'] = 'File eve.json not found'
    except json.decoder.JSONDecodeError:
      out['msg']['counter'] = sg
      out['msg']['time_group'] = tg
    finally:
      return out

  # by default reading the first 30 rules
  def rule_get(self,page_num,count):
    out = {'result':'OK','msg':{'rules':[],'total':None}}
    try:
      with open(self.files['rule'],'r') as f:
        rule = f.readline()
        i = 0
        while rule:
          if (i >= page_num * count) and (i < (page_num + 1)*count):
            if re.match('^[ \t]*$',rule):
              rule = f.readline()
              continue
            try:
              p = parser.Parser(rule,
		var_port=self.var_group['port'],
		var_addr=self.var_group['addr'],
                line_num=i+1)
              out['msg']['rules'].append(p.get_rule())
            except parser.InvalidRuleError as e:
              out['msg']['rules'].append({'error':str(e)})
            rule = f.readline()
            i += 1
          elif (i < page_num*count) or (i >= (page_num+1)*count) :
            rule = f.readline()
            i += 1
            continue
      out['msg']['total'] = i
      return out
    except OSError: 
      return {'result':'NOK','error':'File '+ self.files['rule']+' not found.'}


  # NOT WORKING YET
  def rule_add(self,rule:dict):
    try:
      p = parser.Validator(rule,self.var_group['port'],self.var_group['addr'])
      return {'result':'OK','msg':self.__build_rule(rule)}
    except parser.InvalidRuleError as e:
      return {'result':'NOK','error':str(e)}
