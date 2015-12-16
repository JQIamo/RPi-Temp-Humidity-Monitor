#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Adafruit_DHT
from math import *
from influxdb import InfluxDBClient
from ConfigParser import SafeConfigParser
import datetime

# For Failure Recovery
import json
import os
import time
import errno

########### ##### ######################
## Channel : GPIO PIN, ordered from left to right when facing jacks

defaultPinmaps = {
	'v1.0':{1:23, 2:24, 3:25, 4:8, 5:7, 6:22, 7:17, 8:4},
	'v1.1':{1:4, 2:17, 3:22, 4:23, 5:24, 6:25, 7:8, 8:7},
	'custom':{}
}

## Load CONFIG stuff
parser = SafeConfigParser({'location':'/dev/shm/missedTempLogs'})
parser.read('/etc/templogger/templogger.conf')

PINMAPPING = defaultPinmaps[parser.get('board_options','version')]

sensors = {}
for channel in range(1,1+8):
	channelConf = "channel_%d" % channel
	if parser.has_section(channelConf):
		if (not parser.has_option(channelConf, 'use')) or  parser.getboolean(channelConf, 'use'):
			if parser.has_option(channelConf, 'pin'):
				sensors[channel] = {'pin':parser.getint(channelConf, 'pin')}
			else:
				sensors[channel] = {'pin':PINMAPPING[channel]}
			if parser.has_option(channelConf, 'name'):
				sensors[channel]['name'] = parser.get(channelConf,'name')
			else:
				sensors[channel]['name'] = channelConf

## Dew Point calculation
def dewPt(temp, humid):
	gamma = log(humid/100.0) + 17.67*temp/(243.5+temp)
	dp = 243.5*gamma/(17.67 - gamma)
	return dp

## We're using a DHT22
sensor = Adafruit_DHT.DHT22

data = []

for ch, info in sensors.items():
	try:
		# Pull the time for every sensor, prevents accidental overwriting
		current_time = str(datetime.datetime.utcnow())
		humidity, temperature = Adafruit_DHT.read_retry(sensor, info['pin'])
		print "On %d (%s) read %4.1f*C %3.1f%%H" % (ch, info['name'], temperature, humidity)
		if temperature and humidity:
			data += [{"measurement": "temperature", "time": current_time, "tags": {"channel": ch, "channel_name": info['name']}, "fields": { "value": temperature} }]
			data += [{"measurement": "humidity", "time": current_time, "tags": {"channel": ch, "channel_name": info['name']}, "fields": { "value": humidity} }]
			data += [{"measurement": "dewpoint", "time": current_time, "tags": {"channel": ch, "channel_name": info['name']}, "fields": { "value": dewPt(temperature, humidity)} }]
	except Exception, e:
		print "On channel %d, pin %d:" % (ch, (info['pin']))
		print e

## Now we have the data; try writing it. On failure, save it.
if data:
	try:
		influx_url = parser.get('influx', 'url')
		influx_port = parser.get('influx', 'port')
		influx_user = parser.get('influx', 'username')
		influx_pwd = parser.get('influx', 'password')
		influx_db = parser.get('influx', 'database')
		client = InfluxDBClient(influx_url, influx_port, influx_user, influx_pwd, influx_db)
		client.write_points(data)
	except Exception, e:
		print e
		missedDirectory = parser.get('missed','location')
		try:
			os.makedirs(missedDirectory)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
		saveFilename = "%d-missedTemps.json" % time.time()
		savePath = os.path.join(missedDirectory, saveFilename)
		print "Attempting to save reading to %s" % savePath
		with open(savePath,'w') as outfile:
			 json.dump(data, outfile)

