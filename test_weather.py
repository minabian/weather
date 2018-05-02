import time
from datetime import datetime
import requests
from sense_hat import SenseHat


# calLs API to get weather data and returns in json
def get_weather():
    weather = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?zip=94085,us&APPID=3cf4cd87d12e4025c0636ed5097aef1e&units=imperial')
    return weather.json()


# Creates file name using timestamp
def create_file_name():
    return "Result_" + str((time.strftime("%d-%m-%Y-%H-%M-%S"))) + ".txt"


class TestWeather():

    def __init__(self, filename):
        self.expected_tint1 = [216, 220, 200]
        self.expected_tint2 = [176, 180, 200]
        self.expected_tint3 = [96, 100, 200]
        self.expected_tint4 = [8, 8, 200]
        self.current_time = datetime.now()
        self.sense = SenseHat()
        self.morn_even_offset = 1
        self.filename = filename
        self.failed_expected_tint = {1: 0, 2: 0, 3: 0, 4: 0}
        self.passed_expected_tint = {1: 0, 2: 0, 3: 0, 4: 0}
        self.file = None
        self.weather = None
        self.cloud = None
        self.temp = None
        self.sunrise = None
        self.sunset = None
        self.visibility = None
        self.local_temp = None

    def write_result_in_file(self):
        self.file = open(self.filename, 'a')
        self.file.write("\n---------Final result for the day---------\n ")
        for key in self.passed_expected_tint:
            self.file.write("\n{0} times Passed for expected tint{1} \n".format(self.passed_expected_tint[key], key))
        for key in self.failed_expected_tint:
            self.file.write("\n{0} times Failed for expected tint{1} \n".format(self.failed_expected_tint[key], key))
        self.file.close()

    def check_tint_level(self):
        self.file = open(self.filename, 'a')
        self.weather = get_weather()
        self.cloud = self.weather['clouds']['all']
        self.temp = self.weather['main']['temp']
        self.sunrise = datetime.fromtimestamp(self.weather['sys']['sunrise'])
        self.sunset = datetime.fromtimestamp(self.weather['sys']['sunset'])
        self.visibility = self.weather['visibility']
        self.current_time = datetime.now()
        self.local_temp = self.sense.get_temperature() * 1.8 + 32
        current_tint = self.sense.get_pixel(1, 1)
        if (self.current_time.time().hour < (self.sunrise.hour - self.morn_even_offset)):

            if current_tint == self.expected_tint1:
                self.file.write("sunrise is {0} and current time time is {1}".format(self.sunrise, self.current_time))
                self.file.write(
                    " expected tint is tint1={0} which is equal to actual tint={1} ".format(self.expected_tint1,
                                                                                            current_tint))
                self.file.write("\n----------pas-------\n")
                self.passed_expected_tint[1] += 1
            else:
                self.file.write("sunrise is {0} and current time time is {1}".format(self.sunrise, self.current_time))
                self.file.write(
                    " expected tint is tint1={0} but actual tint is {1} ".format(self.expected_tint1, current_tint))
                self.file.write("\n----------Failed-------\n")
                self.failed_expected_tint[1] += 1
        elif (self.current_time.time().hour > (self.sunset.hour + self.morn_even_offset)):

            if current_tint == self.expected_tint1:
                self.file.write("sunset is {0} and current time time is {1}".format(self.sunset, self.current_time))
                self.file.write(
                    " expected tint is tint1={0} which is equal to actual tint={1} ".format(self.expected_tint1,
                                                                                            current_tint))
                self.file.write("\n----------pas-------\n")
                self.passed_expected_tint[1] += 1
            else:
                self.file.write("sunset is {0} and current time time is {1}".format(self.sunrise, self.current_time))
                self.file.write(
                    " expected tint is tint1={0} but actual tint is {1} ".format(self.expected_tint1, current_tint))
                self.file.write("\n----------Failed-------\n")
                self.failed_expected_tint[1] += 1
        elif (self.cloud >= 40 or self.visibility <= 3000):

            if (self.cloud >= 60):
                if current_tint == self.expected_tint1:
                    self.file.write(
                        " hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                            self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                    self.file.write(" cloud is {0} >= 60".format(self.cloud))
                    self.file.write(
                        " expected tint is tint1={0} which is equal to actual tint={1} ".format(self.expected_tint1,
                                                                                                current_tint))
                    self.file.write("\n----------pas-------\n")
                    self.passed_expected_tint[1] += 1
                else:
                    self.file.write(
                        " hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                            self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                    self.file.write(" cloud is {0}>=60".format(self.cloud))
                    self.file.write(
                        " expected tint is tint1={0} but actual tint is {1} ".format(self.expected_tint1, current_tint))
                    self.file.write("\n----------Failed-------\n")
                    self.failed_expected_tint[1] += 1
            else:
                if current_tint == self.expected_tint2:
                    self.file.write(
                        " hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                            self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                    self.file.write(" cloud is {0} < 60    and visibility is {1}".format(self.cloud, self.visibility))
                    self.file.write(
                        " expected tint is tint2={0} which is equal to actual tint={1} ".format(self.expected_tint2,
                                                                                                current_tint))
                    self.file.write("\n----------pas-------\n")
                    self.passed_expected_tint[2] += 1

                else:
                    self.file.write(
                        " hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                            self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                    self.file.write(" cloud is {0} < 60    and visibility is {1}".format(self.cloud, self.visibility))
                    self.file.write(
                        " expected tint is tint2={0} but actual tint is {1} ".format(self.expected_tint2, current_tint))
                    self.file.write("\n----------Failed-------\n")
                    self.failed_expected_tint[2] += 1

        elif (self.local_temp > 80):
            if current_tint == self.expected_tint4:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and ".format(self.cloud, self.visibility))
                self.file.write("environment temperature is {0} > 80".format(self.local_temp))
                self.file.write(
                    " expected tint is tint4={0} which is equal to actual tint={1} ".format(self.expected_tint4,
                                                                                            current_tint))
                self.file.write("\n----------pas-------\n")
                self.passed_expected_tint[4] += 1
            else:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and ".format(self.cloud, self.visibility))
                self.file.write("environment temperature is {0} > 80".format(self.local_temp))
                self.file.write(
                    " expected tint is tint4={0} but actual tint is {1} ".format(self.expected_tint4, current_tint))
                self.file.write("\n----------Failed-------\n")
                self.failed_expected_tint[4] += 1
        elif (self.local_temp > 65):

            if current_tint == self.expected_tint3:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and".format(self.cloud, self.visibility))
                self.file.write("65 < environment temperature is {0} <= 80".format(self.local_temp))
                self.file.write(
                    " expected tint is tint3={0} which is equal to actual tint={1} ".format(self.expected_tint3,
                                                                                            current_tint))
                self.file.write("\n----------pas-------\n")
                self.passed_expected_tint[3] += 1
            else:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and".format(self.cloud, self.visibility))
                self.file.write("65 < environment temperature is {0} <= 80".format(self.local_temp))
                self.file.write(
                    " expected tint is tint3={0} but actual tint is {1} ".format(self.expected_tint3, current_tint))
                self.file.write("\n----------Failed-------\n")
                self.failed_expected_tint[3] += 1

        else:
            if current_tint == self.expected_tint2:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and".format(self.cloud, self.visibility))
                self.file.write(" environment temperature is {0} <= 65".format(self.local_temp))
                self.file.write(
                    " expected tint is tint2={0} which is equal to actual tint={1} ".format(self.expected_tint2,
                                                                                            current_tint))
                self.file.write("\n----------pas-------\n")
                self.passed_expected_tint[2] += 1
            else:
                self.file.write(" hour of sunrise-1 {0} <=  hour of current time {1}  <= hour of sunset+1 {2}".format(
                    self.sunrise.hour - 1, self.current_time.time().hour, self.sunset.hour + 1))
                self.file.write(" cloud is {0} < 40    and visibility is {1}> 3000 and".format(self.cloud, self.visibility))
                self.file.write(" environment temperature is {0} <= 65".format(self.local_temp))
                self.file.write(
                    " expected tint is tint2={0} but actual tint is {1} ".format(self.expected_tint2, current_tint))
                self.file.write("\n----------Failed-------\n")
                self.failed_expected_tint[2] += 1
        self.file.close()


def main():
    filename = create_file_name()
    test_weather = TestWeather(filename)
    current_date = datetime.now()
    current_day = current_date.day
    while True:
        test_weather.check_tint_level()
        time.sleep(3)
        today = datetime.now().day
        if today != current_day:
            test_weather.write_result_in_file()
            filename = create_file_name()
            test_weather = TestWeather(filename)
            current_date = datetime.now()
            current_day = current_date.day


if __name__ == '__main__':
    main()
