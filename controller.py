import subprocess as sp
from os.path import isdir
import psutil
import io
from time import sleep
import consock
import re


# Process => the NIDS(Suricata)

#LIST OF FEATURES ON THIS CLASS:
# - start process
# - stop process
# - reload process
# - get alert
# - clear alert
# - get runtime log

#TODO:
# - add rule
# - get rule
# - get stats


class Controller():
  def __init__(self, conf_file: str):
    self.conf_file = conf_file
    self.default_cmd = ['suricata','-D','-c',self.conf_file,'-q','0']
    self.socket = consock.ConSock('/var/run/suricata/suricata-command.socket')

    self.files = {'eve':'/var/log/suricata/eve.json',
		'fast':'/var/log/suricata/fast.json',
		'rule':'/var/lib/suricata/rules/suricata.rules',
		'suricata':'/var/log/suricata/suricata.log'}
 
    self.tmp_dir = '/tmp/Suricata_controller/'


  # return process id if the process is running, else False
  @staticmethod
  def proc_is_run():
    for proc in psutil.process_iter():
      if proc.name().lower().startswith("suricata"):
        return proc.pid
    return False

  def __build_rule(self, rule:dict):
    return "{} {} {} {} {} {} {} ( msg:\"{}\"; sid:{}; gid:{}; rev:{}; )".format(
      	rule["action"].strip(), rule["proto"].strip(),
      	rule["src"][0].strip(), rule["src"][1],
      	rule["dir"].strip(),
      	rule["dst"][0].strip(), rule["dst"][1],
      	rule['msg'].strip(), rule['sid'], rule['gid'], rule['rev'])

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
      


####### Publicly accessible methods ######

### proc related ###

  def proc_start(self):
    try:
      if not isdir(self.tmp_dir):
        sp.run(['mkdir','-p',self.tmp_dir])
      sp.run(['cp', self.conf_file, self.tmp_dir], stdout=sp.DEVNULL)
      sp.run(self.default_cmd,stdout=sp.DEVNULL)
    except Exception:
      return {'f':'proc_start','result':'NOK','error':'Other error'}
    return {'f':'proc_start','result':'OK'}

  def proc_stop(self):
    try:
      self.socket.s_connect()
      r = self.socket.send_cmd('shutdown')
      self.socket.s_close()
      return {'f':'proc_stop','result':'OK'}
    except OSError:
      return {'f':'proc_stop','result':'NOK','error':'socket error'}

  def proc_reload(self):
    try:
      self.socket.s_connect()
      r = self.socket.send_cmd('reload-rules')
      self.socket.s_close()
      return {'f':'proc_reload','result':'OK'}
    except OSError:
      return {'f':'proc_reload','result':'NOK','error':'Socket error'}

  def log_get(self):
    out = self.__get_runtime_log()
    if out['result'] == "OK":
      return {'f':'log_get','result':'OK','msg':out['msg']}
    else:
      return {'f':'log_get','result':'NOK','error':out['error']}

  def alert_get(self,page_num=None,count_per_page=None):
    buf = []
    load = True
    if type(page_num) == int and type(count_per_page) == int:
      load = (page_num*count_per_page,
      	((page_num+1)*count_per_page)-1)
    try:
      i = 0
      with open(self.files['eve'],'r') as f:
        import json
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
      return {'f':'alert_get','result':'OK','msg':{'alerts':buf,'total':i}}
    except OSError:
      return {'f':'alert_get','result':'NOK','error':'File not exist'} 
    except json.JSONDecodeError:
      return {'f':'alert_get','result':'OK','msg':{'alerts':buf,'total':i}}

  def alert_clear(self):
    try:
      open_file = self.files['eve']
      with open(open_file,'w') as f:
        pass
      open_file = self.files['fast']
      with open(open_file,'w') as f2:
        pass
      return {'f':'alert_clear','result':'OK','msg':''}
    except OSError:
      return {'f':'alert_clear','result':'NOK','error':'File '+open_file+' not found.'}
