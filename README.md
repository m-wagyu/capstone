# Suricata Controller

### How to run

	sudo chmod u+x ./main.py
	sudo ./main.py

The program will show the web interface address (default 127.0.0.1:5000).
You can open the address from web browser to access the page.

To check if the Suricata is running, use:

	ps ax | grep suricata

List of pages:
 - /home/
 - /home/run\_log
 - /alert/
 - /alert/alert\_log
 - /alert/clear\_log 

In case you accessing the /alert/clear\_log. Your eve.json and fast.log
file will be emptied. I have prepared sample page for eve.json and fast.log
in sample\_file folder.
