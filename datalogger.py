#!/usr/bin/env python
from pymodbus.client.sync import ModbusTcpClient
from influxdb import InfluxDBClient
from influxdb import SeriesHelper

host='127.0.0.1'
port=8086
user = 'root'
password = 'root'
dbname = 'test'

blup = 65534
largenum = 65536

client = InfluxDBClient(host, port, user, password, dbname)


c = ModbusTcpClient(host="192.168.0.4")
c.connect()
result = c.read_input_registers(0x442,4)
#print result.registers
result3 = c.read_input_registers(0x425,20)
#print result3.registers
circuit1_room_temp =  result3.registers[0]/10
dhw_temp =  result3.registers[19]

blup = result.registers[1]

if blup > 100:
	outdoor_ambient_temperature = blup - largenum
#	print outdoor_ambient_temperature
else:
	outdoor_ambient_temperature = blup

operation_state = result.registers[0]
#outdoor_ambient_temperature = result.registers[1]
water_inlet_temperature = result.registers[2]
water_outlet_temperature = result.registers[3]
delta_temperature = water_outlet_temperature-water_inlet_temperature

#print "Out temp",outdoor_ambient_temperature




"""Instantiate a connection to the InfluxDB."""
json_body = [
        {
            "measurement": "Temperature",
"tags":{
"name":"Yutaki_Data"
},
            "fields": {
		"operation_state": operation_state,
                "outdoor_ambient_temperature": outdoor_ambient_temperature,
		"water_inlet_unit_temperature": water_inlet_temperature,
		"water_outlet_unit_temperature": water_outlet_temperature,
		"circuit1_room_temp": circuit1_room_temp,
		"dhw_temp": dhw_temp
 }
        }
    ]

#print("Write points: {0}".format(json_body))
client.write_points(json_body)

#Get Service Data

result2 = c.read_input_registers(0x4BC,10)
print result2.registers
invert_freq    = result2.registers[0]
comp_current   = result2.registers[2]
defrosting     = result2.registers[5]
water_temp_set = result2.registers[7]
water_flow_level = result2.registers[8]
water_pump_speed = result2.registers[9]

capacity = delta_temperature*4.2*water_flow_level/3.6
#print capacity


json_body2 = [
        {
            "measurement": "performance",
"tags":{
"name":"Yutaki_Data"
},
            "fields": {
		"invert_freq": invert_freq,
                "comp_current": comp_current,
		"defrosting": defrosting,
		"water_temp_set": water_temp_set,
		"water_flow_level": water_flow_level,
		"water_pump_speed": water_pump_speed,
		"capacity":capacity

            }
        }
    ]

#print("Write points: {0}".format(json_body))
client.write_points(json_body2)
