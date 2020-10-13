from .. import regex
import json
import re

class RuleError(Exception):
    pass

#
# This class is used to parse and validate the rule from suricata file.
#
class RuleParser:
  def __init__(self, rule:str, var_port:list, var_addr:list, line_num:int):
    self.rule = re.split('\(',rule,maxsplit=1)	
    # rule[0] = action & header, rule[1] = options
    self.vp = var_port 
    self.va = var_addr 
    self.out = {'enable':None,'action':None,'header':None,'option':None}

    self.enable, self.rule[0] = self.is_enabled()
    self.action, self.rule[0] = check_action(self.rule[0])

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
        full['proto'], self.rule[0] =     check_protocol(self.rule[0])
        full['src_addr'], self.rule[0] =  check_address(self.rule[0], group=self.va)
        full['src_port'], self.rule[0] =  check_port(self.rule[0], group=self.vp)
        full['direction'], self.rule[0] = check_direction(self.rule[0])
        full['dst_addr'], self.rule[0] =  check_address(self.rule[0], group=self.va)
        full['dst_port'], self.rule[0] =  check_port(self.rule[0], group=self.vp)
        return {'parsed_header':full}
    except RuleError as e:
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
          if not check_sid(val):
            full['msg'] = "Invalid SID '{}'".format(val)
          else:
            full['sid'] = val
        if key == 'gid':
          if not check_gid(val): 
            full['msg'] = "Invalid GID '{}'".format(val)
          else:
            full['gid'] = val
        if key == 'msg':
          full['msg'] = re.sub('(^\"|\"$)','',val)

    return full

  def get_rule(self):
    return self.out


################## Helper functions #####################

def list_to_string(l:list,is_negative=False):
    out = '!' if is_negative else ''
    out = out + '[' + l[0].strip()
    try:
        for i in range(1,len(l)):
            out = out +','+ l[i].strip()
    except IndexError:
        pass
    out = out + ']'
    return out

def check_action(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf not in regex.actions:
        raise RuleError("Invalid action '{}' on rule '{}'".format(buf,s))
    else:
        return buf, lbuf[1]

def check_protocol(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf not in regex.protos:
        raise RuleError("Invalid protocol '{}' on rule '{}'".format(buf,s))
    else:
        return buf, lbuf[1]

def check_direction(s:str):
    lbuf = s.lstrip().split(' ',1)
    buf = lbuf[0].strip().lower()
    if buf not in regex.directions:
        raise RuleError("Invalid direction '{}' on rule '{}'".format(buf,s))
    else:
        return buf, lbuf[1]

def check_single_address(s:str,group:list):
    if re.match('^!',s):
        s = re.split('^!',s,maxsplit=1)[0]
        if s == "any": raise "Invalid '!any' address"

    matched = re.fullmatch(regex.ipv4_re,s)
    if matched: return s

    matched = re.fullmatch(regex.ipv6_re,s)
    if matched: return s

    for i in group:
        if s == i:
            return s

    raise RuleError("Invalid Rule {}".format(s))

def check_address(s:str, group:list):
    header = s.lstrip()
    is_negative = False

    if not re.match('^!?\[',header):
        buf = header.split(' ',1)
        return check_single_address(buf[0], group), buf[1]
    else:
        addr_list = []

        if re.match('^!',header): is_negative = True

        header = re.sub('^!?\[','',header)            
        # header is still string
        header = re.split('\]',header,maxsplit=1)   
        # header is now list. [0] is addr, [1] is the rest of the rule header

        # if header[1] not exist, rule is missing ']', thus invalid
        if len(header) == 2:
            h = header[0]

            if ',' not in h:
                return check_single_address(h,group), header[1]
            else:
                tmp = h.split(',')
                for i in tmp:
                    if re.fullmatch(' *',i.strip()): continue
                    addr_list.append(check_single_address(i.strip(),group))
                return list_to_string(addr_list, is_negative), header[1]
        else:
            raise RuleError("Invalid address list")

def check_single_port(s:str, group:list, is_single=False):
    if re.match('^!',s):
        s = re.split('^!',s,maxsplit=1)[0]
        if s == "any": raise "Invalid '!any' address"
     
    for i in group:
        if s == i:
            return s

    if ':' in s:
        p = s.split(':')
        try:
            p[0] = int(p[0])
            p[1] = int(p[1])
        except ValueError as e:
            raise RuleError("Invalid port number '{}'".format(s)) from e

        if not (int(p[0]) <= 65535 and int(p[0]) >=0):
            raise RuleError("Invalid port number '{}'".format(s))

        if not (int(p[0]) <= 65535 and int(p[0]) >=0):
            raise RuleError("Invalid port number '{}'".format(s))
        else:
            if p[0]>p[1]:
                raise RuleError("Invalid port number '{}'".format(s))
            else:
                return s
    else:
        try:
            if int(s) <= 65535 and int(s) >=0:
                return s
        except ValueError as e:
            raise RuleError("Invalid port number '{}'".format(s)) from e
        
def check_port(s:str, group:list):
    header = s.lstrip()
    is_negative = False

    if not re.match('^!?\[',header):
        buf = header.split(' ',1)
        return check_single_port(buf[0], group), buf[1]
    else:
        port_list = []

        if re.match('^!',header): is_negative = True

        header = re.sub('^!?\[','',header)
        header = re.split('\]',header,maxsplit=1)   

        if len(header) == 2:
            h = header[0]

            if ',' not in h:
                return check_single_port(h,group), header[1]
            else:
                tmp = h.split(',')
                for i in tmp:
                    if re.fullmatch(' *',i.strip()): continue
                    port_list.append(check_single_port(i.strip(),group))
                return list_to_string(port_list, is_negative), header[1]
        else:
            raise RuleError("Invalid port list")

def check_sid(sid:int):
  try:
    s = int(sid)
    if s < 0:
      return False
    else:
      return True
  except Exception:
    return False
  
def check_gid(gid:int):
  try:
    g = int(gid)
    if g < 0:
      return False
    else:
      return True
  except Exception:
    return False

