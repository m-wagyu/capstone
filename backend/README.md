# Suricata Controller

### How to run

	sudo chmod u+x ./main.py
	sudo ./main.py

The program will show the web interface address (default 127.0.0.1:5000).
You can open the address from web browser to access the page.

To check if the Suricata is running, use:

	ps ax | grep suricata

List of api link:
 - /api/server\_status/
 - /api/server\_action/
 - /api/run\_log/
 - /api/alerts/
 - /api/clear\_log/
 - /api/stats/
 - /api/rules/
 - /api/add\_rule/

URL query parameter to access alerts:
![/api/alerts/](docs/images/alert.png)

Form to access add\_rule:
![/api/add\_rule/](docs/images/add_rule.png)

All URL returns json data.

# Frontend Webpack Compile

1. Install npm on your machine.
2. ```npm install``` at the folder
3. ```npm run start``` to watch frontend file change. 
4. ```npm run dev``` build for development.
5. ```npm run build``` build for production.
5. Run Suricata Server ```sudo ./backend/main.py```


# REST API

* GET /api/server_status - return JSON
* GET /api/alerts {page: number, count: number} - return JSON
* GET /api/clear_log - return JSON
* GET /api/stats - return JSON
* GET /api/rules - return JSON

* POST /api/server_action ```form-data {
	function: proc_stop|proc_reload|proc_start
}```
* POST /api/add_rule ```form-data {
	enable: "True"|"False"
	action: pass|reject|drop|alert
	proto: udp|tcp|icmp|ip
	src_address: IP_ADDRESS 
	src_port: any
	dst_addr: $HOME_NET
	dst_port: any
	direction: ->|<>
	msg: hello world
	sid: 100
	gid: 1
}```


