from .. import regex
from . import rule_utils as ru
import re

class InvalidRuleError(Exception):
  def __init__(self,msg:str):
    self.m = msg
  def __str__(self):
    return self.m

#################### Parser class for 'rule_get' #####################

class RuleParser:
  def __init__(self, rule:str, var_port:list, var_addr:list, line_num:int):
    self.rule = re.split('\(',rule,maxsplit=1)	
    # rule[0] = action & header, rule[1] = options
    self.vp = var_port 
    self.va = var_addr 
    self.out = {'enable':None,'action':None,'header':None,'option':None}

    self.enable, self.rule[0] = self.is_enabled()
    self.action, self.rule[0] = ru.check_action(self.rule[0])

    h = self.parse_header()
    try:
        self.header = h['parsed_header']
    except KeyError as e:
        # self.parse_header returns empty
        self.option = {'msg':str(e),'sid':None,'gid':None}

    try:
        h['error']
        # self.parse_header returns 'parsed_rule' and 'error' field
        self.option = {'msg':str(h['error']),'sid':None,'gid':None}
    except KeyError:
        # self.parse_header returns 'parsed_rule' field only
        self.option = self.parse_option()
    finally:
        self.out = {'number':line_num,'enable':self.enable,'action':self.action,'header':self.header,'option':self.option}


  def is_enabled(self):
    regex = re.compile('^ *#+ *')
    if re.match(regex,self.rule[0]):
      return False, re.sub(regex,'',self.rule[0])
    else:
      return True, self.rule[0]

  def parse_header(self):
    full = {'proto':None,'src_addr':None,'src_port':None,
	'direction':None,'dst_addr':None,'dst_port':None}

    try:
        full['proto'], self.rule[0] =     ru.check_protocol(self.rule[0])
        full['src_addr'], self.rule[0] =  ru.check_address(self.rule[0], group=self.va)
        full['src_port'], self.rule[0] =  ru.check_port(self.rule[0], group=self.vp)
        full['direction'], self.rule[0] = ru.check_direction(self.rule[0])
        full['dst_addr'], self.rule[0] =  ru.check_address(self.rule[0], group=self.va)
        full['dst_port'], self.rule[0] =  ru.check_port(self.rule[0], group=self.vp)
        return {'parsed_header':full}
    except ru.RuleError as e:
        return {'parsed_header':full, 'error':str(e)}

  def parse_option(self):
    full = {'msg':None,'sid':None,'gid':1} # gid is 1 by default
    trimmed = re.sub('\)( *| *#+.*)$','',self.rule[1]).strip()
    opt_list = re.split('\ *;\ *',trimmed)

    for i in opt_list:
      if i:
        # catch single option tag
        try:
          l = i.split(':',1)
          key,val = l[0],l[1]
        except IndexError:
          key = l[0]
          val = ''

        if key == 'sid': 
          if not ru.check_sid(val):
            full['msg'] = "Invalid SID '{}'".format(val)
          else:
            full['sid'] = val
        if key == 'gid':
          if not ru.check_gid(val): 
            full['msg'] = "Invalid GID '{}'".format(val)
          else:
            full['gid'] = val
        if key == 'msg':
          full['msg'] = re.sub('(^\"|\"$)','',val)

    return full

  def get_rule(self):
    return self.out


#################### Validator class for 'rule_add' #####################


class RuleValidator():
  def __init__(self,rule:dict, var_addr:list , var_port:list):
    self.rule = rule
    self.vp = var_port
    self.va = var_addr
    if not validate_action(self.rule['action']):                     raise InvalidRuleError('Invalid action '+self.rule['action'])
    if not validate_proto(self.rule['proto']):                       raise InvalidRuleError('Invalid protocol '+self.rule['proto'])
    if not validate_address(self.rule['src_addr'],group=self.va):    raise InvalidRuleError('Invalid source address '+self.rule['src_addr'])
    if not validate_address(self.rule['dst_addr'],group=self.va):    raise InvalidRuleError('Invalid destination address '+self.rule['dst_addr'])
    if not validate_port(self.rule['src_port'],group=self.vp):       raise InvalidRuleError('Invalid source port '+self.rule['src_port'])
    if not validate_port(self.rule['dst_port'],group=self.vp):       raise InvalidRuleError('Invalid destination port '+self.rule['dst_port'])
    if not validate_direction(self.rule['direction']):               raise InvalidRuleError('Invalid direction '+self.rule['direction'])
    if not validate_sid(self.rule['sid']):          raise InvalidRuleError('Invalid SID '+self.rule['sid'])
    if not validate_gid(self.rule['gid']):          raise InvalidRuleError('Invalid GID '+self.rule['gid'])



def build_rule(rule:dict):
    return '{}{} {} {} {} {} {} {} (msg:"{}";sid:{};gid:{};)' .format(
          '' if rule['enabled'] == "True" else '#',
          rule['action'], rule['proto'],
          rule['src_addr'], rule['src_port'],
          rule['direction'],
          rule['dst_addr'], rule['dst_port'],
          rule['msg'], rule['sid'], rule['gid']
          )
