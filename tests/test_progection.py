#!/usr/bin/env python3
import copy
import unittest
import math
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from forSky import stars_data, progection


class FormParams:
    form_x = 200
    form_y = 200
    dx = 0
    dy = 0
    sky_radius = 100
    sky_center_x = 100
    sky_center_y = 100


class TestProgection(unittest.TestCase):
    def test_change_sky_bright_value(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        model.SkyProgection.current_bright = 5
        model.change_bright()
        self.assertEqual(1, len(model.current_visual_progection))

    def test_change_rotation(self):
        progection.SkyProgection.radius = 100
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        progection.SkyProgection.center_x = 0
        model = progection.Progection(FormParams, constellations)
        model.change_sky_progect_rotation_angle(90)
        model.change_rotation()
        for star in model.full_progection:
            if star.spectral_class == 'K4+III':
                self.assertEqual(100, star.y_visual_progect)
                self.assertEqual(100, star.x_visual_progect)
            if star.spectral_class == 'B9V':
                self.assertEqual(100, star.y_visual_progect)
                self.assertEqual(200, star.x_visual_progect)

    def test_change_sky_progect_rotation_angle(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        model.change_sky_progect_rotation_angle(390)
        self.assertEqual(30, model.SkyProgection.rotation_angle)
        model.change_sky_progect_rotation_angle(-30)
        self.assertEqual(0, model.SkyProgection.rotation_angle)

    def test_change_sky_progect_center_x(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        model.change_sky_progect_center_x(45)
        self.assertEqual(True, model.need_to_change_current_model)
        self.assertEqual(315, model.SkyProgection.center_x)

        model.change_sky_progect_center_x(-405)
        self.assertEqual(True, model.need_to_change_current_model)
        self.assertEqual(0, model.SkyProgection.center_x)

    def test_change_sky_progect_center_y(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        model.change_sky_progect_center_y(45)
        self.assertEqual(True, model.need_to_change_current_model)
        self.assertEqual(45, model.SkyProgection.center_y)

        model.change_sky_progect_center_y(-45)
        self.assertEqual(True, model.need_to_change_current_model)
        self.assertEqual(0, model.SkyProgection.center_y)

    def test_change_sky_progect_half_view_angle(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        progection.SkyProgection.radius = 100
        model.change_sky_progect_half_view_angle(60)
        self.assertEqual(30, model.SkyProgection.half_view_angle)
        self.assertTrue(
            math.fabs(50 - model.SkyProgection.radius) < 10**6)

        model.change_sky_progect_half_view_angle(-60)
        self.assertEqual(90, model.SkyProgection.half_view_angle)
        self.assertTrue(
            math.fabs(100 - model.SkyProgection.radius) < 10 ** 6)

    def test_change_earth_location(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        progection.SkyProgection.radius = 100
        model = progection.Progection(FormParams, constellations)
        model.change_sky_progect_center_x(90)
        model.change_earth_location()
        counter = 0
        for star in model.constellations[0].stars:
            if star.spectral_class == 'B9V':
                self.assertEqual([0, 0, 100], star.three_coordinates)
                counter += 1
            if star.spectral_class == 'G8III':
                result = [-100, 0, 0]
                for i in range(3):
                    self.assertTrue(
                        math.fabs(
                            result[i] - star.three_coordinates[i]
                        ) < 10**6)
                counter += 1
        self.assertEqual(2, counter)

    def test_change_size(self):
        stars_data.DATA_BASE = './tests/for tests/tests_progection/'
        constellations = stars_data.get_constellations()
        model = progection.Progection(FormParams, constellations)
        progection.SkyProgection.radius = 100
        model.change_sky_progect_half_view_angle(60)
        model.change_size()
        flag = False
        for star in model.current_progection:
            if star.spectral_class == 'K4+III':
                self.assertEqual(100, star.y_visual_progect)
                self.assertEqual(100, star.x_visual_progect)
                flag = True
        self.assertTrue(flag)
        model.change_sky_progect_half_view_angle(-60)
        self.assertEqual(90, model.SkyProgection.half_view_angle)

if __name__ == "__main__":
    unittest.main()