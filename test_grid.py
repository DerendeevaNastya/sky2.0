#!/usr/bin/env python3

import unittest
import grid

class TestGrid(unittest.TestCase):
    def test_create_earth_mark(self):
        pass

    def test_create_latitudes_and_longtitudes(self):
        sky_grid = grid.create_latitudes_and_longtitudes()
        for cons in sky_grid:
            self.assertTrue('latitude' in cons.name or 'longtitude' in cons.name)
        for cons in sky_grid:
            if 'latitude' in cons.name:
                self.assertEqual(73, len(cons.stars))
            else:
                self.assertEqual(37, len(cons.stars))


if __name__ == "__main__":
    unittest.main()