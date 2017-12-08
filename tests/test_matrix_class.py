#!/usr/bin/env python3

import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from forSky import matrix


class TestMatrixClass(unittest.TestCase):
    def test_get_height(self):
        m = matrix.Matrix(4, 5, None)
        self.assertEqual(4, len(m.m))

    def test_get_width(self):
        m = matrix.Matrix(1, 2, None)
        self.assertEqual(2, len(m.m[0]))

    def test_check_rank_matrix(self):
        m = matrix.Matrix(None, None, [[1, 2, 3], [0, 0, 0]])
        self.assertEqual(2, m.height)
        self.assertEqual(3, m.width)

    def test_mul(self):
        m = matrix.Matrix(None, None, [[1, 2, 3], [1, 1, 1]])
        n = matrix.Matrix(None, None, [[1, 1], [4, 4], [-1, 3]])
        s = m * n
        result = [[6, 18], [4, 8]]
        for x in range(2):
            for y in range(2):
                self.assertEqual(result[x][y], s.m[x][y])


if __name__ == "__main__":
    unittest.main()
