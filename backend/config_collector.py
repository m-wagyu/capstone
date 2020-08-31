import yaml
# return eve log, fast log, suricata log, rule file and controller socket path
def get_config_path(cf:str):
  out = {}
  f = open(cf,'r')
  buf = f.read()
  conf = yaml.load(buf)
  out['eve'] = conf['default-log-dir']+conf['outputs'][1]['eve-log']['filename']
  out['fast'] = conf['default-log-dir']+conf['outputs'][0]['fast']['filename']
  out['suricata'] = conf['default-log-dir']+conf['logging']['outputs'][1]['file']['filename']
  out['rule'] = '/var/lib/suricata/rules/suricata.rules'
  out['consock'] = '/var/run/suricata/suricata-command.socket'
  f.close()
  return out


# return {'addr':[],'port':[]}
def get_config_group(cf:str):
  out = {'addr':['any'],'port':['any']}
  f = open(cf,'r')
  buf = f.read()
  conf = yaml.load(buf)
  for i in conf['vars']['address-groups'].keys():
    out['addr'].append('$'+i)
  for i in conf['vars']['port-groups'].keys():
    out['port'].append('$'+i)
  f.close()
  return out

