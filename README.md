# yutaki
Connect Hitachi Yutaki Heatpump to Influxdb, Grafana and Domoticz

The main purpose of this project is to enable extensive data-logging and visualization of the Hitachi Yutaki Heatpump system.

Hardware used:
1. Hitachi Yutaki RASM-4VNE Monobloc heatpump
2. Hitachi Modbus Gateway ATW-MBS-02
3. Raspberry Pi 3b

Hardware Connections:
* Connect the Monobloc heatpump (1) via two-wires with the Modbus Gateway (2), by linking positions 1 and 2 on the terminals of the heatpump with 1 and 2 on the Modbus Gateway

* Connect the Modbus Gateway (2) via an ethernet cable to the Raspberry Pi 3b (3)

Software Installation:
On the Raspberry Pi 3b install:

a) Influx database
b) Grafana
c) pymodbus
In the terminal type the following commands:
  sudo apt-get update
  sudo apt-get install python-dev
  sudo apt-get install python-pip
  pip install pymodbus
d) Domoticz

Create a database in influx to which we'll write the data for now we use database "test"
In the terminal:
  influx
  create database test

Download and put the file "datalogger.py" under the home directory of the pi (/home/pi)
Modify the file "datalogger.py" with the variables as per your installation

Make the file "datalogger.py" executable:
  chmod +x datalogger.py

Edit the crontab to run the file datalogger.py every minute
In the terminal:
  sudo crontab -e
  
In the crontab file append this with:
PYTHONPATH=/home/pi/.local/lib/python2.7/site-packages/
* * * * * python /home/pi/datalogger.py > /tmp/listerner.log 2>&1

Now every minute the file "datalogger.py" is run





  
