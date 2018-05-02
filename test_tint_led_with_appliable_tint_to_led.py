import unittest
from sense_hat import SenseHat
import time

tint = [["tint1", [216, 220, 200]], ["tint2", [176, 180, 200]], ["tint3", [196, 100, 200]], ["tint4", [8, 8, 200]]]


class TestTint(unittest.TestCase):
    pass


def test_generator(tint):
    def test(self):
        sense = SenseHat()
        sense.clear()
        time.sleep(1)
        sense.clear(tint)
        time.sleep(2)
        led_tint = sense.get_pixel(1, 1)
        self.assertListEqual(tint, led_tint, "Expected tint is {0} but Led tinted to {1}".format(tint, led_tint))

    return test


if __name__ == '__main__':
    for t in tint:
        test_name = 'test_{}'.format(t[0])
        test = test_generator(t[1])
        setattr(TestTint, test_name, test)
    unittest.main()
