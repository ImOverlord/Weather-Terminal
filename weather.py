#! /usr/bin/env python3
import requests
import json
import sys
import os
from optparse import OptionParser
import time
from configparser import SafeConfigParser

with open('/home/ImOverlord/Documents/Proj/Weather/settings.json') as json_data_file:
    data = json.load(json_data_file)

API_key1 = "" #https://openweathermap.org/ API key
API_key2 = "" #https://www.wunderground.com API key
parser = OptionParser()
parser.add_option("-u", "--humidity", help="shows the humidity percentage", action="store_true")
parser.add_option("-c", "--cloud", action="store_true", dest="cloud", help="shows cloud percentage")
parser.add_option("-p", "--pressure", action="store_true", dest="pressure", help="shows the pressure")
parser.add_option("-r", "--sunrise", action="store_true", dest="sunrise", help="show the time the sun rises")
parser.add_option("-s", "--sunset", action="store_true", dest="sunset", help="show the time the sen sets")
parser.add_option("-v", "--version", action="store_true", dest="version", help="Shows the Version and the Author")
parser.add_option("-n", "--day", action="store", dest="day", help="gets the weather of nday", default="0", metavar="n")

(options, args) = parser.parse_args()
if options.day == "0" and options.version == None:
	url = ''.join(["http://api.openweathermap.org/data/2.5/weather?q=", data['city'], "&appid=", str(API_key1)])
	resp = requests.get(url=url)
	json = json.loads(resp.text)
	temp = json['main']['temp'] - 273.15
	desc = json['weather'][0]['main']
	cloudper = json['clouds']['all']
	humidityper = json['main']['humidity']
	pressureper = json['main']['pressure']
	sunriseT = json['sys']['sunrise']
	sunsetsT = json['sys']['sunset']
	print (''.join(["Hey the temp is ", str(temp), "C, the sky is ", str(desc)]))
elif (options.version == None):
	url2 = ''.join(["http://api.wunderground.com/api/",API_key2,"/forecast10day/q/", str(data['country_code']),"/", str(data['city']), ".json"])
	resp = requests.get(url=url2)
	json = json.loads(resp.text)
	day = int(options.day)
	temp_low = json['forecast']['simpleforecast']['forecastday'][day]['low']['celsius']
	temp_high = json['forecast']['simpleforecast']['forecastday'][day]['high']['celsius']
	desc = json['forecast']['simpleforecast']['forecastday'][day]['conditions']
	humidityper = json['forecast']['simpleforecast']['forecastday'][day]['avehumidity']
	date = json['forecast']['simpleforecast']['forecastday'][day]['date']['epoch']
	date = float(date)
	day = time.strftime("%a, %d %b", time.localtime(date))
	print (''.join(["Hey the temp for ", day, " will be ", str(temp_low), "C~", str(temp_high),"C, the sky will be ", str(desc)]))
if options.cloud == True and options.day == "0":
	print (''.join(["The clouds cover ", str(cloudper), "% of the sky"]))
if options.humidity == True:
	print (''.join(["The humidity level is ", str(humidityper), "%"]))
if options.pressure == True and options.day == "0":
	print (''.join(["The current pressure is ", str(pressureper), " hpa"]))
if options.sunrise == True and options.day == "0":
	sunriseT = time.strftime("%H:%M:%S (%a, %d %b)", time.localtime(sunriseT))
	print (''.join(["The sun rises at ", str(sunriseT)]))
if options.sunset == True and options.day == "0":
	sunsetsT = time.strftime("%H:%M:%S (%a, %d %b)", time.localtime(sunsetsT))
	print (''.join(["The sun sets at ", str(sunsetsT)]))
if options.version == True:
	print ("\033[92m Weather V1.0.0 created by ImOverlord (GamingAndChill) \x1B[0m")
