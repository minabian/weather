import time
from sense_hat import SenseHat
import requests
import datetime


def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


tint4 = (8, 8, 200)
tint3 = (96, 100, 200)
tint2 = (176, 180, 200)
tint1 = (216, 220, 200)

tintMap = {1: tint1, 2: tint2, 3: tint3, 4: tint4}

morn_even_offset = 1
use_local_temp = True
sense = SenseHat()
sense.low_light = True
sense.clear(tint1)
time.sleep(5)


def get_weather():
    return requests.get(
        'http://api.openweathermap.org/data/2.5/weather?zip=94085,us&APPID=3cf4cd87d12e4025c0636ed5097aef1e&units=imperial').json()


def set_tint(r=get_weather()):
    response = r
    print response

    cloud = response['clouds']['all']
    temp = response['main']['temp']
    sunrise = datetime.datetime.fromtimestamp(response['sys']['sunrise'])
    sunset = datetime.datetime.fromtimestamp(response['sys']['sunset'])
    visibility = response['visibility']
    currentTime = datetime.datetime.now()
    if use_local_temp:
        temp = sense.get_temperature() * 1.8 + 32
    if (currentTime.time().hour < (sunrise.hour - morn_even_offset)):
        print "test"
        print "Clearing glass for morning"
        selectedTint = 1
    elif (currentTime.time().hour > (sunset.hour + morn_even_offset)):
        print "Clearing glass post sunset"
        selectedTint = 1
    elif (cloud >= 40 or visibility <= 3000):
        if (cloud >= 60):
            selectedTint = 1
        else:
            selectedTint = 2
    else:
        if (temp > 80):
            selectedTint = 4
        elif (temp > 65):
            print 'temp is 66'
            selectedTint = 3
        else:
            selectedTint = 2

    sense.clear(tintMap[selectedTint])

    print "Selected Tint : " + str(selectedTint)
    print "--------"
