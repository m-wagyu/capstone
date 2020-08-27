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
          function = 'proc_start'
          logs = s.log_get()
          return render_template('index.html',status=status,function=function,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to terminate Suricata due to '+out['error']
      else:
        status = 'Stopped'
        function = 'proc_start'
        logs = s.log_get()
        return render_template('index.html',status=status,function=function,logs=logs)

    elif f == 'proc_start':
      if not is_run:
        out = s.proc_start()
        if out['result'] == 'OK':
          status = 'Running'
          function = 'proc_stop'
          logs = s.log_get()
          return render_template('index.html',status=status,function=function,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to start Suricata due to '+out['error']
      else:
        status = 'Running'
        function = 'proc_stop'
        logs = s.log_get()
        return render_template('index.html',status=status,function=function,logs=logs)

    elif f == 'proc_reload':
      if is_run:
        out = s.proc_reload()
        if out['result'] == 'OK':
          status = 'Running'
          function = 'proc_stop'
          logs = s.log_get()
          return render_template('index.html',status=status,function=function,logs=logs)
        else:
          abort(500)
          #error_message = 'Failed to reload Suricata due to '+out['error']
      else:
        abort(409)
        #error_message = 'Suricata is not running'

    else:
      abort(400)
      #error_message = 'Requesting unknown function'

@app.route('/run_log/',methods=['GET'])
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
# For example: localhost:5000/alert?page=0&count=50

@app.route('/alerts/',methods=['GET'])
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
  alerts = s.alert_get(page_num,count_per_page)
  if out['result'] == 'OK':
    return jsonify(out)
  else:
    abort(500)
    #error_message = alert['error']

@app.route('/clear_log/',methods=['GET'])
def clear_log():
  out = s.alert_clear()
  if out['result'] == 'OK':
    return jsonify(out)
  else:
    abort(500)
    #error_message = out['error']

@app.route('/stats/',methods=['GET'])
def stats():
  out = s.stats_get()
  if out['result'] == 'OK':
    return jsonify(out)
  else:
    abort(500)
    #error_message = out['error']

'''
@app.route('/rules/',methods=['GET'])
def rules():
  out = s.rule_get()
  if out['result'] == 'OK':
    return jsonify(out)
  else:
    abort(500)

@app.route('/rules/',methods=['POST'])
def rule_add():
  out = s.rule_add(<args>)
  if out['result'] == 'OK':
    return jsonify(out)
  else:
    abort(500)
'''

s = Controller(conf_file='/etc/suricata/suricata.yaml')
##### remove debug mode on final version !!! #####
app.run(debug=True)
