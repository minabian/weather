#!/usr/bin/python

import weather3
import time
from datetime import datetime, timedelta
import unittest
from sense_hat import SenseHat


# Convert date to Epoch
def convert_date_time_to_epoch(date):
    return int(time.mktime(date.timetuple()))


# Add hour and minute to entered date
def add_to_time(date=datetime.now, hour=0, minute=00):
    return date + timedelta(hours=hour, minutes=minute)


# create sunset or sunrise in date and epoch format
def create_sunset_sunrise(date=datetime.now, hour=0, minutes=0):
    sun = add_to_time(date, hour, minutes)
    sun_epoch = convert_date_time_to_epoch(sun)
    return sun, sun_epoch


# Change sunrise, sunset, cloud, visibility and temperature in weather data
def change_weather_data(weather_data, sunrise=None, sunset=None, cloud=None, visibility=None, temp=None):
    if sunset != None:
        weather_data['sys']['sunset'] = sunset
    if sunrise != None:
        weather_data['sys']['sunrise'] = sunrise
    if cloud != None:
        weather_data['clouds']['all'] = cloud
    if visibility != None:
        weather_data['visibility'] = visibility
    if temp != None:
        weather_data['main']['temp'] = temp
    return weather_data


class TestWeather(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_tint1 = [216, 220, 200]
        cls.expected_tint2 = [176, 180, 200]
        cls.expected_tint3 = [96, 100, 200]
        cls.expected_tint4 = [8, 8, 200]

    def setUp(self):
        self.currentTime = datetime.now()
        self.weather_data = {
            "base": "stations",
            "clouds": {
                "all": 75
            },
            "cod": 200,
            "coord": {
                "lat": 37.37,
                "lon": -122.04
            },
            "dt": 1524866340,
            "id": 420006359,
            "main": {
                "humidity": 48,
                "pressure": 1019,
                "temp": 65.79,
                "temp_max": 68,
                "temp_min": 62.6
            },
            "name": "Sunnyvale",
            "sys": {
                "country": "US",
                "id": 428,
                "message": 0.0056,
                "sunrise": 1524834996,
                "sunset": 1524884113,
                "type": 1
            },
            "visibility": 16093,
            "weather": [
                {
                    "description": "broken clouds",
                    "icon": "04d",
                    "id": 803,
                    "main": "Clouds"
                }
            ],
            "wind": {
                "deg": 360,
                "speed": 17.22
            }
        }

        print self.currentTime
        # print int(time.time())
        # print datetime.now() + timedelta(hours=2)
        # self.sunrise,self.sunrise_epoch,self.sunset,self.sunset_epoch= create_sunset_sunrise(self.currentTime,sunrise_hour=-10,sunset_hour=2)
        # print self.sunrise
        # print self.sunset
        self.sense = SenseHat()
        self.sense.clear()
        time.sleep(2)

    def test_clearing_glass_for_morning(self):
        expected = TestWeather.expected_tint1
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=2)
        print "sunrise is {0}".format(str(sunrise))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch)
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint1 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_clearing_glass_post_sunset(self):
        expected = TestWeather.expected_tint1
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=-2)
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunset=sunset_epoch)
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint1 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_40(self):
        expected = TestWeather.expected_tint2
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=40)
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint2 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_60(self):
        expected = TestWeather.expected_tint1
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=60)
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint1 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_39_visibility_3000(self):
        expected = TestWeather.expected_tint2
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=39,
                                                visibility=3000)
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint2 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_39_visibility_3001_temp_81(self):
        expected = TestWeather.expected_tint4
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=39,
                                                visibility=3001, temp=81)
        weather3.use_local_temp = False
        weather3.set_tint(self.weather_data)
        time.sleep(2)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint4 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_39_visibility_3001_temp_66(self):
        expected = TestWeather.expected_tint3
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=39,
                                                visibility=3001, temp=66)
        weather3.use_local_temp = False
        weather3.set_tint(self.weather_data)
        time.sleep(2)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint3 ({0}) but actual tint is {1}".format(expected, glass_tint))

    def test_current_time_between_sunsetPlusOne_and_sunriseSubOne_cloud_39_visibility_3001_temp_65(self):
        expected = TestWeather.expected_tint2
        sunset, sunset_epoch = create_sunset_sunrise(self.currentTime, hour=1)
        sunrise, sunrise_epoch = create_sunset_sunrise(self.currentTime, hour=-1)
        print "sunrise is {0}".format(str(sunrise))
        print "sunset is {0}".format(str(sunset))
        self.weather_data = change_weather_data(self.weather_data, sunrise=sunrise_epoch, sunset=sunset_epoch, cloud=39,
                                                visibility=3001, temp=65)
        weather3.use_local_temp = False
        weather3.set_tint(self.weather_data)
        glass_tint = self.sense.get_pixel(1, 1)
        self.assertListEqual(glass_tint, expected,
                             "Expected tint was tint2 ({0}) but actual tint is {1}".format(expected, glass_tint))

    # test_01()


if __name__ == '__main__':
    unittest.main()
