import re

class InvalidRuleError(Exception):
    pass

#
# This class is used to validate rule input. To be used by /api/rule_add
#
class RuleValidator():
  def __init__(self,rule:dict, var_addr:list , var_port:list):
    self.rule = rule
    self.vp = var_port
    self.va = var_addr
    if not validate_action(self.rule['action']):                    raise InvalidRuleError('Invalid action '+self.rule['action'])
    if not validate_protocol(self.rule['proto']):                   raise InvalidRuleError('Invalid protocol '+self.rule['proto'])
    if not validate_address(self.rule['src_addr'],group=self.va):   raise InvalidRuleError('Invalid source address '+self.rule['src_addr'])
    if not validate_address(self.rule['dst_addr'],group=self.va):   raise InvalidRuleError('Invalid destination address '+self.rule['dst_addr'])
    if not validate_port(self.rule['src_port'],group=self.vp):      raise InvalidRuleError('Invalid source port '+self.rule['src_port'])
    if not validate_port(self.rule['dst_port'],group=self.vp):      raise InvalidRuleError('Invalid destination port '+self.rule['dst_port'])
    if not validate_direction(self.rule['direction']):              raise InvalidRuleError('Invalid direction '+self.rule['direction'])
    if not validate_sid(self.rule['sid']):                          raise InvalidRuleError('Invalid SID '+self.rule['sid'])
    if not validate_gid(self.rule['gid']):                          raise InvalidRuleError('Invalid GID '+self.rule['gid'])

def build_rule(rule:dict):
    return '{}{} {} {} {} {} {} {} (msg:"{}";sid:{};gid:{};)' .format(
          '' if rule['enabled'] == "True" else '#',
          rule['action'], rule['proto'],
          rule['src_addr'], rule['src_port'],
          rule['direction'],
          rule['dst_addr'], rule['dst_port'],
          rule['msg'], rule['sid'], rule['gid']
          )

def validate_action(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf in ['drop','pass','reject']:
        return True
    return False

def validate_protocol(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf in ['icmp','ip','tcp']:
        return True
    return False

def validate_direction(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf in ['->','<>']:
        return True
    return False

def validate_single_address(s:str,group:list):
    if re.match('^!',s):
        s = re.split('^!',s,maxsplit=1)[0]
        if s == "any": return False
    else:
        if s == "any": return True

    if re.fullmatch(regex.ipv4_re,s): return True

    if re.fullmatch(regex.ipv6_re,s): return True

    for i in group:
        if s == i:
            return True

    return False

def validate_address(s:str, group:list):
    header = s.lstrip()
    is_negative = False

    if not re.match('^!?\[',header):
        buf = header.split(' ',1)
        return validate_single_address(buf[0], group)
    else:
        if re.match('^!',header): is_negative = True

        header = re.sub('^!?\[','',header)
        header = re.split('\]',header,maxsplit=1)   

        if len(header) == 2:
            h = header[0]

            if ',' not in h:
                return validate_single_address(h,group)
            else:
                tmp = h.split(',')
                for i in tmp:
                    if re.fullmatch(' *',i.strip()): continue
                    if not validate_single_address(i.strip(),group): return False
                return True
        else:
            return False

def validate_single_port(s:str, group:list):
    if re.match('^!',s):
        s = re.split('^!',s,maxsplit=1)[0]
        if s == "any": return False
    else:
        if s == "any": return True
     
    for i in group:
        if s == i:
            return True

    if ':' in s:
        p = s.split(':')
        try:
            if not (int(p[0]) <= 65535 and int(p[0]) >=0): return False

            if not (int(p[0]) <= 65535 and int(p[0]) >=0):
                return False
            else:
                if p[0]>p[1]:
                    return False
                else:
                    return True
        except(ValueError):
            return False
    else:
        if int(s) <= 65535 and int(s) >=0:
            return True
        return False 

def validate_port(s:str, group:list):
    header = s.lstrip()
    is_negative = False

    if not re.match('^!?\[',header):
        buf = header.split(' ',1)
        return validate_single_port(buf[0], group)
    else:
        if re.match('^!',header): is_negative = True

        header = re.sub('^!?\[','',header)
        header = re.split('\]',header,maxsplit=1)   

        if len(header) == 2:
            h = header[0]

            if ',' not in h:
                return check_single_port(h,group)
            else:
                tmp = h.split(',')
                for i in tmp:
                    if re.fullmatch(' *',i.strip()): continue
                    if validate_single_port(i.strip(),group): return True
                return False
        else:
            return False

def validate_sid(sid:int):
  try:
    s = int(sid)
    if s < 0:
      return False
    else:
      return True
  except Exception:
    return False
  
def validate_gid(gid:int):
  try:
    g = int(gid)
    if g < 0:
      return False
    else:
      return True
  except Exception:
    return False

