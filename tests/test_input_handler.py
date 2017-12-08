#!/usr/bin/env python3

import unittest
import datetime
import math
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from forSky import input_handler, stars_data


class TestInputHandlerClass(unittest.TestCase):
    def test_get_center_x_from_time_sec(self):
        dates = []
        for x in range(24):
            dates.append(datetime.datetime(2000, 1, 1, x, 0, 0))
        results = []
        for date in dates:
            results.append(
                input_handler.get_center_x_from_time_sec(date) / 3600)
        for i in range(len(dates) - 1):
            self.assertTrue(math.fabs(results[i] - results[i+1] - 15) < 10**-5)

    def test_change_constellation_from_year(self):
        stars_data.DATA_BASE = './tests/for tests/test_input_handler/'
        constellations = stars_data.get_constellations()
        new_date = datetime.datetime(3000, 3, 6, 12, 45, 0)
        constellations = input_handler.change_constellation_from_year(
            new_date, constellations)
        self.assertEqual(constellations[0].stars[0].x_sec, 53990)
        self.assertEqual(constellations[0].stars[0].y_sec, 2998)

        self.assertEqual(constellations[0].stars[1].x_sec, 54400)
        self.assertEqual(constellations[0].stars[1].y_sec, -200)

        self.assertEqual(constellations[0].stars[2].x_sec, 108500)
        self.assertEqual(constellations[0].stars[2].y_sec, 70)


if __name__ == "__main__":
    unittest.main()
