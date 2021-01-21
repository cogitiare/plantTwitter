#imports for interfacing with soil sensor
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw

#import for twitter API
from twython import Twython

import random

#declaring credentials from auth file
from auth import (
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)
twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)

#def function for random line selection
def random_line(fileName):
    lines = open(fileName).read().splitlines()
    return random.choice(lines)
	
#Setting up i2c compatibility for sensor
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)


#read moisture level
moistureLevel = ss.moisture_read()
#read temp
temp = ss.get_temp()
#converting temperature to F
temp *= 1.8
temp += 32

if temp < 66:
	#select lowTemp textLine
	message = random_line('./text/temp/lowTemp.txt')
elif temp >76:
	#select hightTemp textLine
	message = random_line('./text/temp/highTemp.txt')
else:
	if moistureLevel > 1250:
		message = random_line('./text/moisture/flooded.txt')
	elif moistureLevel >= 1100 and moistureLevel <=1250:
		message = random_line('./text/moisture/prettyWet.txt')
	elif moistureLevel >= 900 and moistureLevel <1100:
		message = random_line('./text/moisture/great.txt')
	elif moistureLevel >= 700 and moistureLevel <900:
		message = random_line('./text/moisture/good.txt')
	elif moistureLevel >= 600 and moistureLevel <700:
		message = random_line('./text/moisture/dry.txt')
	elif moistureLevel >= 500 and moistureLevel <600:
		message = random_line('./text/moisture/veryDry.txt')
	elif moistureLevel >= 400 and moistureLevel <500:
		message = random_line('./text/moisture/extremelyDry.txt')
	else:
		message = random_line('./text/moisture/dead.txt')

#message = str(moistureLevel) + " brrr " + str(temp)
# twitter.update_status(status=message)

print("Done! I tweeted: " +  message + " temp is " + str(temp) + "F. Moisture is " + str(moistureLevel))
#to print, use str(temp/moistureLevel)
#to tweet, use "twitter.update_status(status=message)" where message is predeclared
