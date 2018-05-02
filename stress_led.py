from sense_hat import SenseHat
import time
import argparse


class StressLed():
    def __init__(self, cycle_count):
        self.sense = SenseHat()
        self.failed_to_tint = {1: 0, 2: 0, 3: 0, 4: 0}
        self.tint = {1: [216, 220, 200], 2: [176, 180, 200], 3: [96, 100, 200], 4: [8, 8, 200]}
        self.cycle_count = cycle_count

    def tint_led(self, tint):

        self.sense.clear()
        self.sense.clear(self.tint[tint])
        time.sleep(2)
        return self.sense.get_pixel(1, 1)

    def compare_expected_tint_with_actual_led_tint(self, expected_tint, actual_tint):
        if (self.tint[expected_tint] == actual_tint):
            print "Passed to tint to tint{0}".format(expected_tint)
            return True
        else:

            self.failed_to_tint[expected_tint] += 1
            print "failed to tint to tint{0} expected={1} but actual is{2} ".format(expected_tint,
                                                                                    self.tint[expected_tint],
                                                                                    actual_tint)
            return False

    def print_tint_result(self, tint, passed):
        if passed:
            print "{0} times tint to tint{1} passed".format(self.cycle_count, tint)
        else:
            print "{0} times tint to tint{1} failed out of {2} execution  ".format(self.failed_to_tint[tint], tint,
                                                                                   self.cycle_count, tint)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle_count", default=3,
                        help="Specify Number of Counts to operate tint to tint1,tint2,tint3 and tint4")
    args = parser.parse_args()
    cycle_count = int(args.cycle_count)
    stress = StressLed(cycle_count)
    cycle_count += 1
    for i in range(1, cycle_count):
        led_tint = stress.tint_led(1)
        stress.compare_expected_tint_with_actual_led_tint(1, led_tint)
        led_tint = stress.tint_led(2)
        stress.compare_expected_tint_with_actual_led_tint(2, led_tint)
        led_tint = stress.tint_led(3)
        stress.compare_expected_tint_with_actual_led_tint(3, led_tint)
        led_tint = stress.tint_led(4)
        stress.compare_expected_tint_with_actual_led_tint(4, led_tint)
        print "{0} cycles done out of {1}".format(i, stress.cycle_count)
    print "\n--------------------Final result------------------------------\n"
    if stress.failed_to_tint[1] == 0:
        stress.print_tint_result(1, True)
    else:
        stress.print_tint_result(1, False)

    if stress.failed_to_tint[2] == 0:
        stress.print_tint_result(2, True)
    else:
        stress.print_tint_result(2, False)
    if stress.failed_to_tint[3] == 0:
        stress.print_tint_result(3, True)
    else:
        stress.print_tint_result(3, False)
    if stress.failed_to_tint[4] == 0:
        stress.print_tint_result(4, True)
    else:
        stress.print_tint_result(4, False)


if __name__ == '__main__':
    main()
