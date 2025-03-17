import pathlib
import pprint
import sys
import math
import unittest
from simplesi.dimensions import Dimensions
from simplesi import Physical, PRECISION
import simplesi as si
si.environment('imperial')
si.environment('structural', replace=False)


class TestPhysicalWithUnits(unittest.TestCase):

    def test_relation(self):
        self.assertTrue(1 * si.m == 1000 * si.mm)
        self.assertTrue(1 * si.m != 1 * si.ft)
        self.assertTrue(0.5 * si.m <= 500 * si.mm)
        self.assertTrue(3 * si.cm >= 30 * si.mm)
        self.assertTrue(3 * si.cm > 1 * si.inch)
        self.assertTrue(1 * si.yard < 1258 * si.mm)

        self.assertFalse(1 * si.m != 1000 * si.mm)
        self.assertFalse(1 * si.m == 1 * si.ft)
        self.assertFalse(0.5 * si.m > 500 * si.mm)
        self.assertFalse(3 * si.cm > 30 * si.mm)
        self.assertFalse(3 * si.cm < 1 * si.inch)
        self.assertFalse(1 * si.yard > 1258 * si.mm)

    def test_to(self):
        self.assertEqual((1 * si.inch).to('inch'), '1.0 inch')
        self.assertEqual((1 * si.ft).to('inch'), '12.0 inch')
        self.assertEqual((1 * si.m).to('m'), '1.0 m')
        self.assertEqual((12 * si.inch).to('ft'), '1.0 ft')
        self.assertEqual((1 * si.yard).to('ft'), '3.0 ft')

        self.assertEqual((1 * si.m).to('inch'), '39.37 inch')
        self.assertEqual((1 * si.m).to('ft'), '3.281 ft')

        self.assertEqual((10 * si.inch).to('m'), '0.254 m')
        self.assertEqual((1 * si.ft).to('cm'), '30.48 cm')
        self.assertEqual((1 * si.ft).to('mm'), '304.8 mm')
        self.assertEqual((2 * si.yard).to('mm'), '1828.8 mm')

        self.assertEqual(12 * si.inch + 2 * si.ft, 1 * si.yard)
        self.assertEqual(12 * si.cm + 2 * si.m, 2120 * si.mm)

    def test_print(self):
        self.assertIsNone(si.km.to())
        self.assertIsNone(si.Hz.to())
        self.assertEqual(si.Hz.__str__(), '1.0 Hz')
        self.assertEqual(eval(si.km.__repr__()), si.km)

    def test_SI(self):
        self.assertTrue(si.m.is_SI)
        self.assertFalse(si.ft.is_SI)

    def test_addition(self):
        self.assertEqual(1 * si.m + 1 * si.mm, 1001 * si.mm)
        self.assertAlmostEqual(3 * si.ft + 1 * si.yard, 2 * si.yard, delta=0.01 * si.mm)
        self.assertAlmostEqual(3 * si.ft + 25.4 * si.mm, 0.9398 * si.m, delta=0.01 * si.mm)
        self.assertAlmostEqual(3 * si.ft + 25.4 * si.mm, 25.4 * si.mm + 3 * si.ft + 0, delta=0.01 * si.mm)  # radd

        with self.assertRaises(ValueError):
            3 * si.ft + 5
            3 * si.ft + 4 * si.kNm

        # summing
        vals = [x * 1 * si.mm for x in range(1, 11)]
        self.assertEqual(sum(vals), sum(range(1, 11)) * si.mm)

    def test_subtraction(self):
        self.assertEqual(1 * si.m - 1 * si.mm, 999 * si.mm)
        self.assertAlmostEqual(3 * si.ft - 1 * si.yard, 0 * si.yard, delta=0.01 * si.mm)
        self.assertAlmostEqual(3 * si.ft - 25.4 * si.mm, 939.8 * si.mm - 2 * 25.4 * si.mm, delta=0.01 * si.mm)
        self.assertAlmostEqual(3 * si.ft - 25.4 * si.mm, - 1 * 25.4 * si.mm + 3 * si.ft + 0, delta=0.01 * si.mm)  # rsub

        with self.assertRaises(ValueError):
            3 * si.ft - 5
            3 * si.ft - 4 * si.kNm

    def test_multiplication(self):
        self.assertAlmostEqual(1 * si.m * 1 * si.N, 1 * si.Nm, delta=1 * si.N * si.mm)
        self.assertEqual((1 * si.m) * 1, 1000 * si.mm)
        self.assertEqual(2 * (si.m * 1), 2000 * si.mm)

    def test_division(self):
        self.assertEqual((1 * si.m) / 2, 500 * si.mm)
        self.assertEqual((1 * si.kNm) / (2 * si.m), 0.5 * si.kN)
        self.assertEqual((1 * si.kN) / (2 * si.m ** 2), 0.5 * si.kN_m2)

        # only 0 and 1 can be divided with a unit
        self.assertEqual(1 / (1 * si.s), 1 * si.Hz)
        self.assertEqual(1 / (1 * si.m ** 2), 1 * (si.m ** -2))
        self.assertEqual(1 / (1 * si.m ** 2), 1 / si.m2)

        with self.assertRaises(ZeroDivisionError):
            1 * si.m / 0

        with self.assertRaises(ValueError):
            3 / (1 * si.s)

    def test_power(self):
        self.assertEqual((1 * si.m) ** 2, 1 * si.m2)
        self.assertEqual((1 * si.s) ** -1, 1 * si.Hz)
        self.assertEqual((4 * si.m2) ** 0.5, 2 * si.m)

        with self.assertRaises(TypeError):
            math.sqrt(4 * si.m2)

        with self.assertRaises(ValueError):
            si.m ** si.s




if __name__ == '__main__':
    unittest.main()
