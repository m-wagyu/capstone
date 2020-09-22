import re
import os

pkg_dir = os.getcwd()
conf_path = pkg_dir+'/backend/config.cfg'

class InvalidOptionError(Exception):
    pass


def get_socket_addr():
    ip = '127.0.0.1'
    port = '5000'

    with open(conf_path) as f:
        for line in f:
            if re.match('^ *ip_address',line):
                ip = re.split(' *= *',line.strip())[1]
            if re.match('^ *port_number',line):
                port = re.split(' *= *',line.strip())[1]
        return (ip,port)


def get_sc_config():
    sc_conf_path = '/etc/suricata/suricata.yaml'
    with open(conf_path) as f:
        for line in f:
            if re.match('^ *config_file',line):
                sc_conf_path = re.split(' *= *',line.strip())[1]
        return sc_conf_path


def get_sc_param():
    with open(conf_path) as f:
        args = ''
        for line in f:
            if re.match('^ *options',line):
                cleaned = re.sub('(\'|\"|\n)','',line)
                args = re.split(' *= *',cleaned)[1]
            if re.match('(\n|\||&|;)',args):
                raise InvalidOptionError('Invalid character detected')

        # using RE -ve lookbehind to split spaces.
        unescaped = re.split(r'(?<!\\) ',args)
        escaped = []

        # elements of unescaped are still having '\'.
        for val in unescaped:
            escaped.append(re.sub(r'\\','',val))

        return escaped
