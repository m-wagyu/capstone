from socket import socket, AF_UNIX
from select import select
import json

'''
This is a strip down version of suricata control socket (suricatasc).
I have removed some unnecesary functions and if statement to fit
the program need.
'''


VERSION = '0.2'
INC_SIZE = 1024

class CmdReturnNOKException:
  pass

class ConSock:
  def __init__(self, consock_path, verbose=False):
    self.consock_path = consock_path
    self.socket = socket(AF_UNIX)
    self.verbose = verbose

  def __json_recv(self):
    ret = None
    data = ''
    while True:
      data += self.socket.recv(INC_SIZE).decode()
      if data.endswith('\n'):
        ret = json.loads(data)
        break
    return ret

  def send_cmd(self, command, arguments = None):
    cmd_msg = {}
    cmd_msg['command'] = command
    if command == 'iface-stat':
      if arguments:
        cmd_msg['arguments'] = {'iface':arguments}
      else:
        return None
        #raise MissingArgsException
    cmd_msg_str = json.dumps(cmd_msg)+'\n'
    if self.verbose: print('Send: ',cmd_msg_str)
    self.socket.send(cmd_msg_str.encode())
    ready = select([self.socket],[],[],600)
    if ready[0]:
      ret = self.__json_recv()
      if self.verbose: print('Send:',str(ret))
    else:
      ret = None
    if not ret:
      raise CmdReturnNOKException
    return ret

  def s_connect(self):
    try:
      if self.socket == None:
        self.socket = socket(AF_UNIX)
      self.socket.connect(self.consock_path)
    except Exception:
      pass
    self.socket.settimeout(10)
    self.socket.send(json.dumps({'version':VERSION}).encode())
    ready = select([self.socket],[],[],600)
    if ready[0]:
      cmdret = self.__json_recv()
    else:
      cmdret = None
    if cmdret['return'] == 'NOK':
      raise CmdReturnNOKException

  def s_close(self):
    self.socket.close()
    self.socket = None

  def s_reopen(self):
    self.s_close()
    self.socket = socket(AF_UNIX)
