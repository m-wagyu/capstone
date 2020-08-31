#!/usr/bin/python3
from flask import Flask, request, render_template, redirect, url_for, jsonify, abort
from controller import Controller
from time import sleep

# TODO:
# - add port argument
# - add config file argument

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def root():
  return redirect(url_for('home'))

@app.route('/home/',methods=['POST', 'GET'])
def home():
  if request.method == "GET":
    is_run = Controller.proc_is_run()
    f = 'proc_stop' if is_run else 'proc_start'
    l = s.log_get()
    return render_template('index.html',
  		status = 'Running' if is_run else 'Stopped',
  		function = f,
  		logs = l)

  if request.method == "POST":
    is_run = Controller.proc_is_run()
    f = request.form['function']
    if f == 'proc_stop':
      if is_run:
        out = s.proc_stop()
        if out['result'] == 'OK':
          status = 'Stopped'
          logs = s.log_get()
          return render_template('index.html',status=status,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to terminate Suricata due to '+out['error']
      else:
        status = 'Stopped'
        logs = s.log_get()
        return render_template('index.html',status=status,logs=logs)

    elif f == 'proc_start':
      if not is_run:
        out = s.proc_start()
        if out['result'] == 'OK':
          status = 'Running'
          logs = s.log_get()
          return render_template('index.html',status=status,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to start Suricata due to '+out['error']
      else:
        status = 'Running'
        logs = s.log_get()
        return render_template('index.html',status=status,logs=logs)

    elif f == 'proc_reload':
      if is_run:
        out = s.proc_reload()
        if out['result'] == 'OK':
          status = 'Running'
          logs = s.log_get()
          return render_template('index.html',status=status,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to reload Suricata due to '+out['error']
      else:
        abort(409)
        #error_message = 'Suricata is not running'

    else:
      abort(400)
      #error_message = 'Requesting unknown function'

@app.route('/api/run_log/',methods=['GET'])
def run_log():
  out = s.log_get()
  if out['result'] == 'OK':
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
  if out['result'] == 'OK':
    return jsonify(out)
  #else:
    #abort(500)
    #error_message = alert['error']

@app.route('/api/clear_log/',methods=['GET'])
def clear_log():
  out = s.alert_clear()
  if out['result'] == 'OK':
    return jsonify(out)
  #else:
    #abort(500)
    #error_message = out['error']

@app.route('/api/stats/',methods=['GET'])
def stats():
  out = s.stats_get()
  if out['result'] == 'OK':
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
  finally:
    if out['result'] == 'OK':
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
  if out['result'] == 'OK':
    return jsonify(out)


s = Controller(conf_file='/etc/suricata/suricata.yaml')
##### remove debug mode on final version !!! #####
app.run(debug=True)
