# *-* coding: utf-8 -*-
import re
import urllib2
import Adafruit_DHT

dht_sensor = Adafruit_DHT.DHT11
dht_pin = 4

with open("/home/pi/.maker_key", "r") as key_file:
    maker_key = key_file.read()

with open("/sys/bus/w1/devices/28-031663113dff/w1_slave", "r") as temp_file:
    for line in temp_file:
        line = re.findall(r't=.*', line)
        if line:
            line = line[0].split('=')[1]
            ds_temp0 = int(line)

ds_temp1 = ds_temp0 / 1000
ds_temp2 = ds_temp0 / 100
ds_tempM = ds_temp2 % ds_temp1
ds_temp = str(ds_temp1) + "." + str(ds_tempM)
print("DS Temperature: " + str(ds_temp + "°C"))


dht_humidity, dht_temp = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

if dht_humidity is not None and dht_temp is not None:
    print('DHT Temperature: {0:0.1f}°C DHT Humidity: {1:0.1f}%'.format(dht_temp, dht_humidity))
else:
    dht_temp = 0
    dht_humidity = 0
    print('Failed to get DHT reading. Try again!')


maker_url = "https://maker.ifttt.com/trigger/roomtemp/with/key/" + maker_key + "?value1=" + ds_temp + "&value2=" + str(dht_temp) + "&value3=" + str(dht_humidity)
content = urllib2.urlopen(maker_url).read()
print(content)