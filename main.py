#!/usr/bin/python3
from flask import Flask, request
from controller import Controller
import json


app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
@app.route('/home/',methods=['POST', 'GET'])
def home():
  out = None
  if request.method == "POST":
    out = s.proc_stop() if Controller.proc_is_run() else s.proc_start()
    out = json.loads(out)
    return """<h1>Suricata watcher</h1>
		<p>Suricata is {}running</p>
		<form action='#' method='post'>
		<input type='submit' value='Toggle'>
		</form>""".format('' if out['function'] == 'proc-start' else 'not ')
  else:
    return """<h1>Suricata watcher</h1>
		<p>Suricata is {}running</p>
		<form action='#' method='post'>
		<input type='submit' value='Toggle'>
		</form>""".format('' if Controller.proc_is_run() else 'not ')


s = Controller(queue_num=0,conf_file='/etc/suricata/suricata.yaml')
app.run(debug=True)
