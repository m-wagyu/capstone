import subprocess as sp
import os.path
import psutil
import io
import json
import yaml


# Process => the NIDS(Suricata)

#LIST OF FEATURES ON THIS CLASS:
# - start process
# - stop process
# - reload process
# - add rule
# - get rule
# - get alert
# - get stats
# - get error

#EXCEPTION LIST:
# - ProcessLoadInvalidRuleEception


#class ProcessLoadInvalidRuleEception(Exception):
  # To be called when invalid rule exist
#  pass



class Controller():
  def __init__(self, conf_file: str, queue_num: int, af_pack: bool = False):
    self.conf_file = conf_file
    self.af_pack = af_pack
    self.queue_num = queue_num
 
    self.tmp_dir = '/tmp/Suricata_controller/'


  # return process id if the process is running, else False
  @staticmethod
  def proc_is_run():
    for proc in psutil.process_iter():
      if proc.name().lower().startswith("suricata"):
        return proc.pid
    return False

  def __proc_check_error(self) -> list:
    try:
      s = sp.check_output(['suricata', '-T', '-c', self.conf_file,])
      buf = io.StringIO(s.decode())
      err = []
      for line in buf:
        if ("<Warning>" in line) or ("<Error>" in line):
          err.append(line)
      return err
    except sp.CalledProcessError:
      pass

  def __build_rule(self, rule:dict) -> str:
    return "{} {} {} {} {} {} {} ( msg:\"{}\"; sid:{}; gid:{}; rev:{}; )".format(
      	rule["action"].strip(), rule["proto"].strip(),
      	rule["src"][0].strip(), rule["src"][1],
      	rule["dir"].strip(),
      	rule["dst"][0].strip(), rule["dst"][1],
      	rule['msg'].strip(), rule['sid'], rule['gid'], rule['rev'])


####### Publicly accessible methods ######

  def proc_start(self):
    #if NIDS.proc_is_run():
    #  ret = {'function':'proc_start',
    #    	'result':'NOK'}
    #  return json.dumps(ret)
    try:
      if not os.path.isdir(self.tmp_dir):
        sp.run(['mkdir','-p',self.tmp_dir])
      sp.run(['cp', self.conf_file, self.tmp_dir], stdout=sp.DEVNULL)
      err = self.__proc_check_error()
      #write error to $tmp_dir/runtime_err
      if err:
        with open(self.tmp_dir + 'runtime_err', 'w') as f:
          for line in err:
            f.write("%s\n" % line)
        raise ProcessLoadInvalidRuleException
      cmd = ['suricata','-D','-c',self.conf_file,'-q',str(self.queue_num)]
      sp.run(cmd,stdout=sp.DEVNULL)
    #except ProcessLoadInvalidRuleException:
    #  print('ProcessLoadInvalidRuleEception')
    except Exception:
      pass
    ret = {'function':'proc-start',
		'result':'OK' if Controller.proc_is_run() else 'NOK'}
    return json.dumps(ret)

  def proc_stop(self):
    pid = Controller.proc_is_run()
    if pid:
      sp.run(['kill','-15',str(pid)])	# send SIGTERM
    import time
    time.sleep(0.1)
    ret = {'function':'proc-stop',
		'result':'OK' if Controller.proc_is_run() else 'NOK'}
    return json.dumps(ret)

  def proc_restart(self):
    if Controller.proc_is_run():
      self.proc_stop()
    p_json = json.loads(self.proc_start())
    if p_json['result'] == 'OK':
      ret = {'function':'proc-restart',
		'result':'OK'}
    else:
      ret = {'function':'proc-restart',
		'result':'NOK'}
    return json.dumps(ret)

  # rule -> action,proto,src,dir,dst,msg,
  def rule_add(self, rule:dict):
    rule_str = self.__build_rule(rule)
    if not rule_str:
      return {'result':'NOK','function':'rule-add'}
    else:
      try:
        with open('/var/lib/suricata/rules/suricata.rules', 'ab') as f:
          f.write((rule_str+'\n').encode('ascii'))
          return json.dumps({'result':'OK','function':'rule-add','arg':rule_str})
      except Exception:
        pass
      return {'result':'NOK','function':'rule-add'}

  def rule_get(self, rule_file:str):
    ret = {'rules':[]}
    ret['function'] = 'rule-get'
    # add try catch block if file not exist
    try:
      with open(rule_file, 'r') as f:
        rule = f.readline()
        while rule:
          small = rule.split(' ',7)
          rule_obj = {'active': True if small[0][0] != '#' else False,
          		'action': small[0],
          		'protocol': small[1],
          		'src_ip': small[2],
          		'src_port': small[3],
          		'direction': small[4],
          		'dst_ip': small[5],
          		'dst_port': small[6]
          		}
          rule = f.readline()
          ret['rules'].append(rule_obj)
        ret['result'] = 'OK'
    except:
      ret['result'] = 'NOK'
    return json.dumps(ret)

  def rule_reload(self):
    pid = Controller.proc_is_run()
    try:
      if pid:
        sp.run(['kill','-12',pid])	# send SIGUSR2
      return {'result':'OK'}
    except:
      pass
    return {'result':'NOK'}

  def get_stat(self):
    pass

  def get_alert(self):
    pass
