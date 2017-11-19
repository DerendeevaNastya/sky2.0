#!/usr/bin/env python3

import stars_data
import math
import unittest


class TestStarsData(unittest.TestCase):
    def test_star_dublicate_star(self):
        new_star = stars_data.Star('first', 0, '00:00:00', '+00:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        dublicate_star = new_star.dublicate_star()
        dublicate_star.constellation_name = 'second'
        self.assertEqual('first', new_star.constellation_name)
        self.assertEqual('second', dublicate_star.constellation_name)

    def test_star_get_location_x_zero(self):
        new_star = stars_data.Star('', 0, '00:00:00', '+00:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(0, new_star.x_sec)

    def test_star_get_location_x(self):
        new_star = stars_data.Star('', 0, '01:0:00', '+00:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(3600 * 15, new_star.x_sec)
        second_star = stars_data.Star('', 0, '04:30:04', '+00:00:00',
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(16204 * 15, second_star.x_sec)

    def test_star_get_location_y_zero(self):
        new_star = stars_data.Star('', 0, '00:00:00', '+00:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(0, new_star.y_sec)

    def test_star_get_location_y(self):
        new_star = stars_data.Star('', 0, '00:0:00', '+01:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(3600, new_star.y_sec)
        second_star = stars_data.Star('', 0, '00:00:00', '-10:03:04',
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(-36184, second_star.y_sec)

    def test_star_get_three_coordinates(self):
        new_star = stars_data.Star('', 0, '00:0:00', '+01:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        new_star.x_sec = 0
        new_star.y_sec = 90 * 3600
        new_star.set_three_coordinates(500)
        self.assertEqual([0, 0, 500], new_star.three_coordinates)

        new2_star = stars_data.Star('', 0, '00:0:00', '+01:00:00',
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        new2_star.x_sec = 45 * 3600
        new2_star.y_sec = 45 * 3600
        new2_star.set_three_coordinates(100)
        result = [100 / 2, 100 / 2, 100 / 2 ** 0.5]
        for i in range(0, len(result)):
            self.assertTrue(
                math.fabs(result[i]-new2_star.three_coordinates[i]) < 10**(-6)
            )

    def test_star_get_information(self):
        new_star = stars_data.Star('test', 0, '00:0:00', '+00:00:00',
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        inf = new_star.get_information()
        result = 'constellation: test\nlocation: 00:0:00 +00:00:00\n'
        result += 'apparent magnitude: 0.0\nspectral class: 0'
        self.assertEqual(result, inf)

    def test_get_constellations(self):
        stars_data.DATA_BASE = './for tests/'
        constellations = stars_data.get_constellations()
        names = [x.name for x in constellations]
        result = ['first', 'second']
        for i in range(len(names)):
            self.assertEqual(result[i], names[i])
        first_star_coordinates = ['23:39:8.3', '+50:28:18']
        second_star_coordinates = ['2:13:36.3', '+51:3:57']
        for cons in constellations:
            self.assertEqual(1, len(cons.stars))
        self.assertEqual(first_star_coordinates[0],
                         constellations[0].stars[0].x_str)
        self.assertEqual(first_star_coordinates[1],
                         constellations[0].stars[0].y_str)
        self.assertEqual(second_star_coordinates[0],
                         constellations[1].stars[0].x_str)
        self.assertEqual(second_star_coordinates[1],
                         constellations[1].stars[0].y_str)


if __name__ == "__main__":
    unittest.main()
