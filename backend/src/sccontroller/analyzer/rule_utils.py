import re
import json
from .. import regex

class RuleError(Exception):
    pass


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

        header = re.sub('^!?\[','',header)            # header is still string
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

##############################################################################

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

