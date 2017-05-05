#!/usr/bin/env python
# 
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#  
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
#
import socket
import argparse
import json
import time
import datetime

version = 0.1

# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip

# get month and year for dailyConsumption
date = datetime.datetime.now()
month = date.month
year = date.year
dailyconsumptionCommand = str('{"emeter":{"get_daystat":{"month":') + str(month) + str(',"year":') +str(year) +str("}}}")

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {'info'                 : '{"system":{"get_sysinfo":{}}}',
			'on'                   : '{"system":{"set_relay_state":{"state":1}}}',
			'off'                  : '{"system":{"set_relay_state":{"state":0}}}',
			'cloudinfo'            : '{"cnCloud":{"get_info":{}}}',
			'wlanscan'             : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'                 : '{"time":{"get_time":{}}}',
			'schedule'             : '{"schedule":{"get_rules":{}}}',
			'countdown'            : '{"count_down":{"get_rules":{}}}',
			'antitheft'            : '{"anti_theft":{"get_rules":{}}}',
			'reboot'               : '{"system":{"reboot":{"delay":1}}}',
			'reset'                : '{"system":{"reset":{"delay":1}}}',
            'relay_state'          : '{"system":{"get_sysinfo":{}}}',
            'nightmodeon'          : '{"system":{"set_led_off":{"off":1}}}',
            'nightmodeoff'         : '{"system":{"set_led_off":{"off":0}}}',
            'realtimeVoltage'      : '{"emeter":{"get_realtime":{}}}',
            'EMeterVGain'          : '{"emeter":{"get_vgain_igain":{}}}',
            'currentRunTime'       : '{"system":{"get_sysinfo":{}}}',
            'currentPower'         : '{"emeter":{"get_realtime":{}}}',
            'voltage'              : '{"emeter":{"get_realtime":{}}}',
            'dailyConsumption'     : dailyconsumptionCommand,
            'gettime'              : '{"emeter":{"get_daystat":{"month":4,"year":2017}}}',
            'currentRunTimeHour'   : '{"system":{"get_sysinfo":{}}}',
            'resetcounter'         : '{"emeter":{"erase_emeter_stat":null}}'
}


# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = "\0\0\0\0"
	for i in string: 
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171 
	result = ""
	for i in string: 
		a = key ^ ord(i)
		key = ord(i) 
		result += chr(a)
	return result
	

#01/04/2017 parse relay state
def parsecurrentRunTime(string):
	result = ""
	jsonObj = json.loads(string)
	print json.loads(string)['system']['get_sysinfo']['on_time']
	return jsonObj['system']['get_sysinfo']['on_time']
	
def decoupe(seconde):
    day=seconde / 86400
    seconde %=86400
    heure=seconde /3600
    seconde %= 3600
    minute = seconde/60
    seconde%=60
    if( day<10) :
		day = "0"+ str(day)
    if(heure <10) :
		heure = "0"+ str(heure)
    if(minute <10) :
		minute = "0"+ str(minute)
    if(seconde <10) :
        seconde = "0"+ str(seconde)
    return (day,heure,minute,seconde)


# get daily consumption from get_daystat command
def dailyConsumption(string):
	result = ""
	jsonObj = json.loads(string)
	for x in jsonObj['emeter']['get_daystat']['day_list']:
		result = x['energy']
	return result

#return json.loads(string)['emeter']['get_daystat']['day_list']



# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<ip>", required=True, help="Target IP Address", type=validIP)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands) 
group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")
args = parser.parse_args()

# Set target IP, port and command to send
ip = args.target
port = 9999
if args.command is None:
	cmd = args.json
else:
	cmd = commands[args.command]



# Send command and receive reply 
try:
	sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_tcp.connect((ip, port))
	sock_tcp.send(encrypt(cmd))
	data = sock_tcp.recv(2048)
	sock_tcp.close()

	if args.command  == "relay_state":
		print json.loads(decrypt(data[4:]))['system']['get_sysinfo']['relay_state']
	elif args.command  == "currentRunTime":
		print json.loads(decrypt(data[4:]))['system']['get_sysinfo']['on_time']
	elif args.command  == "currentRunTimeHour":
		print "%s:%s:%s:%s" % decoupe(json.loads(decrypt(data[4:]))['system']['get_sysinfo']['on_time'])
	elif args.command  == "currentPower":
		print json.loads(decrypt(data[4:]))['emeter']['get_realtime']['power']
	elif args.command  == "voltage":
		print json.loads(decrypt(data[4:]))['emeter']['get_realtime']['voltage']
	elif args.command  == "dailyConsumption":
		print dailyConsumption(decrypt(data[4:]))
	elif args.command  == "gettime":
		print "Sent:     ", cmd
		print "Received: ", decrypt(data[4:])
		print dailyConsumption(decrypt(data[4:]))
	else :
		print "Sent:     ", cmd
		print "Received: ", decrypt(data[4:])

#01/04/2017 add parse result info for get relay stat directly 0 off 1 on

	
except socket.error:
	quit("Cound not connect to host " + ip + ":" + str(port))
