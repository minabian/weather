from sense_hat import SenseHat
import time
import argparse


class TestTemperature():
    def __init__(self,delay):
        self.sense = SenseHat()
        self.temp_result = {}
        self.temperature_list = [-30, -20, -10, 0, 10, 20, 30, 40, 50, 60]
        self.delay=delay
        for temp in self.temperature_list:
            self.temp_result[temp] = None

    def read_temperature(self):
        return int(self.sense.get_temperature())

    def compare_expected_temp_with_sensor_temperature(self, expected_temp, actual_temp):
        if (expected_temp == actual_temp):
            print "temperature reading at {0} Passed".format(expected_temp)
            self.temp_result[expected_temp] = "Passed"
            return True
        else:

            print "temperature reading at {0} Failed because {1} reported by temperature sensor".format(expected_temp,
                                                                                                        actual_temp)
            self.temp_result[expected_temp] = actual_temp
            return False

    def print_test_result(self, temp):
        if self.temp_result[temp] == "Passed":
            print "temperature reading at {0} Passed because {1} reported by temperature sensor".format(temp, temp)
        else:
            print "temperature reading at {0} Failed because {1} reported by temperature sensor".format(temp,
                                                                                                        self.temp_result[
                                                                                                            temp])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", default=3600,
                        help="Specify Number of Counts to operate tint to tint1,tint2,tint3 and tint4")
    args = parser.parse_args()
    delay = int(args.delay)
    temperature = TestTemperature(delay)
    for temp in temperature.temperature_list:
        sensor_temperature = temperature.read_temperature()
        temperature.compare_expected_temp_with_sensor_temperature(temp, sensor_temperature)
        time.sleep(temperature.delay)

    print "\n--------------------Final result------------------------------\n"
    for temp in temperature.temperature_list:
        temperature.print_test_result(temp)


if __name__ == '__main__':
    main()
