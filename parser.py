from const import * 
import re

class InvalidRuleError(Exception):
  def __init__(self,msg:str):
    self.m = msg
  def __str__(self):
    return self.m


#################### Parser class for 'rule_get' #####################

class Parser:
  def __init__(self, rule:str, var_port:list, var_addr:list, line_num:int):
    self.rule = re.split('\(',rule)	# rule[0] = action & header, rule[1] = options
    self.vp = var_port #self.esc_vars(var_port) #['$HOME_NET','$EXTERNAL_NET']
    self.va = var_addr #self.esc_vars(var_addr)  #['$HTTP_PORT','$TELNET_PORT']
    self.out = {'enable':None,'action':None,'header':None,'option':None}

    self.enable, self.rule[0] = self.is_enabled()
    self.action, self.rule[0] = check_action(self.rule[0])
    self.header = self.parse_header()
    self.option = self.parse_option()

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

    full['proto'], self.rule[0] = check_proto(self.rule[0])
    full['src_addr'], self.rule[0] = check_address(self.rule[0], group=self.va)
    full['src_port'], self.rule[0] = check_port(self.rule[0], group=self.vp)
    full['direction'], self.rule[0] = check_direction(self.rule[0])
    full['dst_addr'], self.rule[0] = check_address(self.rule[0], group=self.va)
    full['dst_port'], self.rule[0] = check_port(self.rule[0], group=self.vp, flag=True)

    return full

  def parse_option(self):
    full = {'msg':None,'sid':None,'gid':'1'} # gid is 1 by default
    trimmed = re.sub('\)( *| *#+.*)$','',self.rule[1]).strip()
    #opt_list = trimmed.split(';')
    opt_list = re.split('\ *;\ *',trimmed)

    for i in opt_list:
      if i:
        l = i.split(':',1)
        key,val = l[0],l[1]
        if key == 'sid': 
          if not check_sid(val): 
            raise InvalidRuleError('Invalid SID of \''+val+'\'')
          else:
            full['sid'] = val
        if key == 'gid': 
          if not check_gid(val): 
            raise InvalidRuleError('Invalid SID of \''+val+'\'')
          else:
            full['gid'] = val
        if key == 'msg':
          full['msg'] = re.sub('(^\"|\"$)','',val)

    return full

  def get_rule(self):
    return self.out


#################### Validator class for 'rule_add' #####################


class Validator():
  def __init__(self,rule:dict, var_port:list, var_addr:list):
    self.rule = rule
    self.vp = var_port #self.esc_vars(var_port) #['$HOME_NET','$EXTERNAL_NET']
    self.va = var_addr #self.esc_vars(var_addr)  #['$HTTP_PORT','$TELNET_PORT']
    if not check_action(self.rule['action'],validate=True): raise InvalidRuleError('Invalid action '+self.rule['action'])
    if not check_proto(self.rule['proto'],validate=True): raise InvalidRuleError('Invalid protocol '+self.rule['proto'])
    if not check_address(self.rule['src_addr'],validate=True,group=self.va): raise InvalidRuleError('Invalid source address '+self.rule['src_addr'])
    if not check_address(self.rule['dst_addr'],validate=True,group=self.va): raise InvalidRuleError('Invalid destination address '+self.rule['dst_addr'])
    if not check_port(self.rule['src_port'],validate=True,group=self.vp): raise InvalidRuleError('Invalid source port '+self.rule['src_port'])
    if not check_port(self.rule['dst_port'],validate=True,group=self.vp): raise InvalidRuleError('Invalid destination port '+self.rule['dst_port'])
    if not check_direction(self.rule['direction'],validate=True): raise InvalidRuleError('Invalid direction '+self.rule['direction'])
    if not check_sid(self.rule['sid']): raise InvalidRuleError('Invalid SID '+self.rule['sid'])
    if not check_gid(self.rule['gid']): raise InvalidRuleError('Invalid GID '+self.rule['gid'])
    self.rule['msg'] = re.escape(self.rule['msg'])
  
  def is_valid(self):
    return True


#################### Check functions #####################


# consider using 
# `act = starts_with(action_re,s,flag=validate)`
# for action,proto,direction,address.
# left the port like that.
def check_action(s:str, validate=False):
  if validate:
    act = starts_with(action_re,s,flag=True)
  else:
    act = starts_with(action_re,s)

  if act:
    if validate: return True
    return act, strip_beginning(action_re,s)
  else:
    if validate: return False
    raise InvalidRuleError('Invalid action on \''+s+'\'')

def check_proto(s:str, validate=False):
  if validate:
    proto = starts_with(proto_re,s,flag=True)
  else:
    proto = starts_with(proto_re,s)

  if proto:
    if validate: return True
    return proto, strip_beginning(proto_re,s)
  else:
    if validate: return False
    raise InvalidRuleError('Invalid protocol on \''+s+'\'')

def check_direction(s:str, validate=False):
  if validate:
    d = starts_with(dir_re,s,flag=True)
  else:
    d = starts_with(dir_re,s)
  if d:
    if validate: return True
    return d, strip_beginning(dir_re,s)
  else:
    if validate: return False
    raise InvalidRuleError('Invalid direction on \''+s+'\'')

# check if the frist word from `s` is a valid IP address 
# or IP group from `group` and remove
# return the matching ip & the remaining string
# Not yet support list of address (eg. [10.0.0.0/8, $HOME_NET])
def check_address(s:str, group=None, validate=False, depth=None):
  negate = False
  if re.match('^!{1}',s):
    negate = True
    s = re.sub('^!{1}','',s)

  # match ipv4
  if validate:
    add = starts_with(ipv4_re,s,flag=True)
  else:
    add = starts_with(ipv4_re,s)

  if add:
    if validate: return True
    return '!'+add if negate else add, strip_beginning(ipv4_re,s)

  #match ipv6
  if validate:
    add = starts_with(ipv6_re,s,flag=True)
  else:
    add = starts_with(ipv6_re,s)

  if add:
    if validate: return True
    return '!'+add if negate else add, strip_beginning(ipv6_re,s)

  #match group
  for i in group:
    if validate:
      add = starts_with(re.escape(i),s,flag=True)
    else:
      #add = starts_with('^!?'+re.escape(i)+'\ ',s)
      add = starts_with(re.escape(i),s)

    if add:
      if validate: return True
      #return '!'+add.strip() if negate else add.strip(), re.sub('^!?'+re.escape(i)+'\ +','',s)
      return '!'+add if negate else add, strip_beginning(re.escape(i),s)

  if validate: return False
  raise InvalidRuleError('Invalid address on \''+s+'\'')


# dont change this
def check_port(s:str, group=None, validate=False, flag=False):
  negate = False
  if re.match('^!{1}',s):
    negate = True
    s = re.sub('^!{1}','',s)

  # check if `s` is integer
  # flag is used to handle possible zero/multiple space(s) between rule dst_port and rule options
  if validate:
    port = starts_with('\d+',s,flag=True)
  else:
    port = starts_with('\d+',s,flag=flag)

  if port:
    try:
      p = int(port)
    except ValueError:
      raise InvalidRuleError('Invalid port number on \''+s+'\'')
    if p >= 0 and p <= 65535:
      if validate: return True
      #return '!'+str(p) if negate else str(p), re.sub('^(\d+)\ ','',s)
      return '!'+str(p) if negate else str(p), strip_beginning('\d+',s)

  # check if `s` is a port group
  for i in group:
    if validate:
      port = starts_with(re.escape(i),s,flag=True)
    else:
      port = starts_with(re.escape(i),s,flag=flag)

    if port:
      if validate: return True
      #return '!'+port.strip() if negate else port.strip(), re.sub('^'+re.escape(port)+'\ ','',s)
      return '!'+port.strip() if negate else port.strip(), strip_beginning(re.escape(port),s)

  if validate: return False
  raise InvalidRuleError('Invalid port on \''+s+'\'')


def check_sid(sid:int):
  try:
    if type(sid) != int:
      s = int(sid)
    else:
      s = sid
    if s < 0 or s > 65535:
      return False
    else:
      return True
  except Exception:
    return False
  
def check_gid(gid:int):
  try:
    if type(gid) != int:
      g = int(gid)
    else:
      g = gid
    if g < 0:
      return False
    else:
      return True
  except Exception:
    return False


# match a string against regex
# return the first occurence of regex if found
# else return none
# use flag if expect no space at the end
def starts_with(regx, string, flag=False):
  if flag:
    m = re.search(re.compile('^'+regx),string)
  else:
    m = re.search(re.compile('^'+regx+'\s+'),string)
  if m: return m.group(0).strip()
  return None

def strip_beginning(regx, string):
  return re.sub('^'+regx+' +','',string)
