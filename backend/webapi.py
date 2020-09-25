#!/usr/bin/python3
from flask import Flask, request, redirect, url_for, jsonify, abort, render_template
from flask_cors import CORS, cross_origin
from time import sleep

from . import sccontroller
from . import config_reader as cr

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
r'/api/server_action/*' : {
	'origins': 'http://localhost:5000'
	}
})


@app.route('/',methods=['GET'])
def root():
  return render_template('index.html')

@app.route('/api/server_action/',methods=['POST'])
def server_action():
  if request.method == "POST":
    is_run = s.proc_is_run()
    f = request.form['function']
    if f == 'proc_stop':
      if is_run['result'] == 'success':
        return jsonify(s.proc_stop())
      else:
        return jsonify({'result':'not-success','error':'Suricata is not running'})

    elif f == 'proc_start':
      if is_run['result'] == 'not-success':
        return jsonify(s.proc_start())
      else:
        return jsonify({'result':'not-success','error':'Suricata is already running'})

    elif f == 'proc_reload':
      if is_run['result'] == 'success':
        return jsonify(s.proc_reload())
      else:
        return jsonify({'result':'not-success','error':'Suricata is not running'})

    else:
      return jsonify({'result':'not-success','error':'Invalid function'})


@app.route('/api/server_status/',methods=['GET'])
def server_status():
  return jsonify(s.proc_is_run())


@app.route('/api/run_log/',methods=['GET'])
def run_log():
  out = s.log_get()
  if out['result'] == 'success':
    return jsonify(out)
  else:
    abort(500)
    #error_message = out['error']


# For alert()
# By default showing 30 alerts max.
# To increase the limit, use the argument page & count:
# For example: localhost:5000/alerts?page=0&count=50

@app.route('/api/alerts/',methods=['GET'])
def alert():
  out = None
  page_num = request.args.get('page')
  count_per_page = request.args.get('count')
  if not page_num:
    out = s.alert_get(0,30)
    return jsonify(out)
  else:
    page_num = int(page_num)
  if count_per_page:
    count_per_page = int(count_per_page)
  else:
    count_per_page = 30
  out = s.alert_get(page_num,count_per_page)
  if out['result'] == 'success':
    return jsonify(out)
  #else:
    #abort(500)
    #error_message = alert['error']

@app.route('/api/clear_log/',methods=['GET'])
def clear_log():
  out = s.alert_clear()
  if out['result'] == 'success':
    return jsonify(out)
  #else:
    #abort(500)
    #error_message = out['error']

@app.route('/api/stats/',methods=['GET'])
def stats():
  out = s.stats_get()
  if out['result'] == 'success':
    return jsonify(out)
  #else:
    #abort(500)
    #error_message = out['error']

@app.route('/api/rules/',methods=['GET'])
def rules():
  try:
    page = int(request.args.get('page'))
    count = int(request.args.get('count'))
    out = s.rule_get(page,count)
  except (ValueError, TypeError):
    page = 0
    count = 30
    out = s.rule_get(page,count)
  if out['result'] == 'success':
    return jsonify(out)
  else:
    abort(500)

@app.route('/api/add_rule/',methods=['POST'])
def rule_add():
  rule = {}
  rule['enabled'] = request.form['enabled'] # value="True" or ""
  rule['action'] = request.form['action'] # value=("drop"|"alert"|"pass"|"reject")
  rule['proto'] = request.form['proto'] # value=('icmp'|'tcp'|'udp'|'ip')
  rule['direction'] = request.form['direction'] # value=('->'|'<>') --> shown as "unidirectional"/"bi-directional"
  rule['src_addr'] = request.form['src_addr'] # value=<a string>
  rule['dst_addr'] = request.form['dst_addr'] # value=<a string>
  rule['src_port'] = request.form['src_port'] # value=<a string>
  rule['dst_port'] = request.form['dst_port'] # value=<a string>
  rule['msg'] = request.form['msg'] # value=<a string>
  rule['sid'] = request.form['sid'] # value=<an integer>
  rule['gid'] = request.form['gid'] # value=<an integer>

  out = s.rule_add(rule)
  if out['result'] == 'success':
    return jsonify(out)


s = sccontroller.Controller()
##### remove debug mode on final version !!! #####
sock_addr = cr.get_socket_addr()
app.run(debug=True,
        host=sock_addr[0],
        port=sock_addr[1])
