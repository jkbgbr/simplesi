import unittest
from simplesi.dimensions import Dimensions
from simplesi import Physical, PRECISION


class TestPhysical(unittest.TestCase):

    def setUp(self):
        self.physical = Physical(5.2, Dimensions(1, 0, 0, 0, 0, 0, 0))

    # def test_int(self):
    #     self.assertEqual(int(self.physical), 5)

    def test_incorrect_init(self):
        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(0, 0, 0, 0, 0, 0, 0))
        with self.assertRaises(ValueError):
            Physical('5.0', Dimensions(1, 0, 0, 0, 0, 0, 0))
        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0), precision=1.2)
        # with self.assertRaises(ValueError):
        #     Physical(5.0, Dimensions(0.1, 0, 0, 0))

    def test_neg(self):
        neg_physical = -self.physical
        self.assertEqual(neg_physical.value, -5.2)
        self.assertEqual(neg_physical.dimensions, self.physical.dimensions)

    def test_abs(self):
        abs_physical = abs(self.physical)
        self.assertEqual(abs_physical.value, 5.2)
        self.assertEqual(abs_physical.dimensions, self.physical.dimensions)
        self.assertEqual(abs_physical, self.physical)

        neg_physical = -self.physical
        abs_neg_physical = abs(neg_physical)
        self.assertEqual(abs_neg_physical.value, 5.2)
        self.assertEqual(abs_neg_physical.dimensions, self.physical.dimensions)
        self.assertEqual(abs_neg_physical, self.physical)
        self.assertEqual(abs_neg_physical, abs_physical)

    def test_bool(self):
        self.assertTrue(bool(self.physical))

    def test_hash(self):
        self.assertEqual(hash(self.physical), hash((5.2, Dimensions(1, 0, 0, 0, 0, 0, 0), PRECISION, False)))

    def test_round(self):

        physical = Physical(5.25, Dimensions(1, 0, 0, 0, 0, 0, 0))
        rounded_physical = round(physical, 1)
        self.assertEqual(rounded_physical.value, 5.2)
        self.assertEqual(rounded_physical.dimensions, physical.dimensions)
        self.assertEqual(rounded_physical.precision, 1)

        physical = Physical(-5.25, Dimensions(1, 0, 0, 0, 0, 0, 0))
        rounded_physical = round(physical, 1)
        self.assertEqual(rounded_physical.value, -5.2)
        self.assertEqual(rounded_physical.dimensions, physical.dimensions)
        self.assertEqual(rounded_physical.precision, 1)

        physical = Physical(5.26, Dimensions(1, 0, 0, 0, 0, 0, 0))
        rounded_physical = round(physical, 0)
        self.assertEqual(rounded_physical.value, 5.0)
        self.assertEqual(rounded_physical.dimensions, physical.dimensions)
        self.assertEqual(rounded_physical.precision, 0)

    def test_contains(self):
        self.assertFalse(self.physical.__contains__(None))


class TestEquality(unittest.TestCase):

    def test_eq(self):

        self.assertTrue(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) == 0.0)

        self.assertTrue(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) == Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)))

        # comparing two Physical objects of different Dimensions raises a ValueError
        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0)) == Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))

        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0)) == 'string'

    def test_ne(self):

        # self.assertTrue(Physical(5.0, Dimensions(1, 0, 0, 0)) != "string")

        # these are equal
        self.assertFalse(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) != 0.0)
        self.assertFalse(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) != Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)))

        # these are not equal
        self.assertTrue(Physical(1.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) != 0.0)
        self.assertTrue(Physical(1.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) != Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)))

        # comparing two Physical objects of different Dimensions raises a ValueError
        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0)) != Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))

        with self.assertRaises(ValueError):
            Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0)) != 'string'


class TestRelations(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(-3.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical3 = Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0))

    def test_gt(self):

        # comparison with zero
        self.assertTrue(self.physical1 > 0)
        self.assertFalse(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) > 0)

        # comparison with another Physical object of the same dimensions
        self.assertTrue(self.physical1 > self.physical2)
        self.assertFalse(self.physical2 > self.physical1)

        # comparison with another Physical object of different dimensions raises ValueError
        with self.assertRaises(ValueError):
            self.physical1 > self.physical3

        with self.assertRaises(ValueError):
            self.physical1 > 'string'

    def test_ge(self):

        # comparison with zero
        self.assertTrue(self.physical1 >= 0)
        self.assertTrue(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) >= 0)

        # comparison with another Physical object of the same dimensions
        self.assertTrue(self.physical1 >= self.physical2)
        self.assertTrue(self.physical1 >= self.physical1)
        self.assertFalse(self.physical2 >= self.physical1)

        # comparison with another Physical object of different dimensions raises ValueError
        with self.assertRaises(ValueError):
            self.physical1 >= self.physical3

        with self.assertRaises(ValueError):
            self.assertFalse(self.physical1 >= "string")

    def test_lt(self):

        # comparison with zero
        self.assertFalse(self.physical1 < 0)
        self.assertFalse(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) < 0)

        # comparison with another Physical object of the same dimensions
        self.assertFalse(self.physical1 < self.physical2)
        self.assertTrue(self.physical2 < self.physical1)

        # comparison with another Physical object of different dimensions raises ValueError
        with self.assertRaises(ValueError):
            self.physical1 < self.physical3

        with self.assertRaises(ValueError):
            self.assertFalse(self.physical1 < "string")

    def test_le(self):

        # comparison with zero
        self.assertFalse(self.physical1 <= 0)
        self.assertTrue(Physical(0.0, Dimensions(1, 0, 0, 0, 0, 0, 0)) <= 0)

        # comparison with another Physical object of the same dimensions
        self.assertFalse(self.physical1 <= self.physical2)
        self.assertTrue(self.physical1 <= self.physical1)
        self.assertTrue(self.physical2 <= self.physical1)

        # comparison with another Physical object of different dimensions raises ValueError
        with self.assertRaises(ValueError):
            self.physical1 <= self.physical3

        with self.assertRaises(ValueError):
            self.assertFalse(self.physical1 <= "string")


class TestAddition(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(3.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical3 = Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0))

    def test_add_same_dimensions(self):
        result = self.physical1 + self.physical2
        self.assertEqual(result.value, 8.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

    def test_add_different_precision(self):
        self.physical1.precision = 1
        self.physical2.precision = 2
        result = self.physical1 + self.physical2
        self.assertEqual(result.value, 8.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, 1)

    def test_add_zero(self):
        result = self.physical1 + 0
        self.assertEqual(result.value, 5)
        self.assertEqual(result.dimensions, self.physical1.dimensions)

    def test_add_nonzero(self):
        with self.assertRaises(ValueError):
            5 + self.physical1

    def test_add_different_dimensions(self):
        with self.assertRaises(ValueError):
            self.physical1 + self.physical3

    def test_add_non_physical(self):
        with self.assertRaises(ValueError):
            self.physical1 + "string"

    def test_radd(self):
        result = 0.0 + self.physical1
        self.assertEqual(result.value, self.physical1.value)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        with self.assertRaises(ValueError):
            5 + self.physical1

    def test_iadd(self):
        with self.assertRaises(ValueError):
            self.physical1 += self.physical2


class TestSubtraction(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(3.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical3 = Physical(5.0, Dimensions(0, 1, 0, 0, 0, 0, 0))

    def test_sub_same_dimensions(self):
        result = self.physical1 - self.physical2
        self.assertEqual(result.value, 2.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

    def test_sub_different_precision(self):
        self.physical1.precision = 1
        self.physical2.precision = 2
        result = self.physical1 - self.physical2
        self.assertEqual(result.value, 2.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, 1)

    def test_sub_zero(self):
        result = self.physical1 - 0
        self.assertEqual(result.value, 5.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)

    def test_sub_different_dimensions(self):
        with self.assertRaises(ValueError):
            self.physical1 - self.physical3

    def test_sub_non_physical(self):
        with self.assertRaises(ValueError):
            self.physical1 - "string"

    def test_rsub(self):

        # two Physical objects of the same dimensions
        result = self.physical2 - self.physical1
        self.assertEqual(result.value, -2.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

        # zero and a Physical object
        result = 0 - self.physical1
        self.assertEqual(result.value, -5.0)
        self.assertEqual(result.dimensions, Dimensions(1, 0, 0, 0, 0, 0, 0))

        # non-zero and a Physical object
        with self.assertRaises(ValueError):
            5 - self.physical1

        # Physical object and a string
        with self.assertRaises(ValueError):
            'mi' - self.physical1

    def test_isub(self):
        with self.assertRaises(ValueError):
            self.physical1 -= self.physical2


class TestMultiplication(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(5.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(3.0, Dimensions(0, 1, 0, 0, 0, 0, 0))
        self.physical3 = Physical(2.0, Dimensions(1, 0, 0, 0, 0, 0, 0))

    def test_mul_same_dimensions(self):
        result = self.physical1 * self.physical3
        self.assertEqual(result.value, 10.0)
        self.assertEqual(result.dimensions, Dimensions(2, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_mul_different_dimensions(self):
        result = self.physical1 * self.physical2
        self.assertEqual(result.value, 15.0)
        self.assertEqual(result.dimensions, Dimensions(1, 1, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_result_is_dimensionsless(self):
        pyhsical1 = Physical(5.0, Dimensions(1, 2, 0, 0, 0, 0, 0))
        physical2 = Physical(3.0, Dimensions(-1, -2, 0, 0, 0, 0, 0))
        self.assertEqual(pyhsical1 * physical2, 15.0)

    def test_mul_by_scalar(self):
        result = self.physical1 * 2
        self.assertEqual(result.value, 10.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

        result = self.physical1 * -2
        self.assertEqual(result.value, -10.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

    def test_mul_non_physical(self):
        with self.assertRaises(ValueError):
            self.physical1 * "string"

    def test_rmul(self):
        result = 2 * self.physical1
        self.assertEqual(result.value, 10.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

    def test_imul(self):
        with self.assertRaises(ValueError):
            self.physical1 *= self.physical2


class TestDivision(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(6.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(3.0, Dimensions(0, 1, 0, 0, 0, 0, 0))
        self.physical3 = Physical(2.0, Dimensions(1, 0, 0, 0, 0, 0, 0))

    def test_truedivision_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.physical1 / 0

        with self.assertRaises(ZeroDivisionError):
            self.physical1 / Physical(0, Dimensions(1, 0, 0, 0, 0, 0, 0))

    def test_truediv_same_dimensions(self):  # same as dimensionsless
        result = self.physical1 / self.physical3
        self.assertEqual(result, 3.0)

    def test_truediv_different_dimensions(self):
        result = self.physical1 / self.physical2
        self.assertEqual(result.value, 2.0)
        self.assertEqual(result.dimensions, Dimensions(1, -1, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_result_is_dimensionsless(self):
        physical1 = Physical(6.0, Dimensions(1, 1, 0, 0, 0, 0, 0))
        physical2 = Physical(3.0, Dimensions(1, 1, 0, 0, 0, 0, 0))
        self.assertEqual(physical1 / physical2, 2.0)

    def test_truediv_by_scalar(self):
        result = self.physical1 / 2
        self.assertEqual(result.value, 3.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

        result = self.physical1 / -2
        self.assertEqual(result.value, -3.0)
        self.assertEqual(result.dimensions, self.physical1.dimensions)
        self.assertEqual(result.precision, self.physical1.precision)

    def test_truediv_non_physical(self):
        with self.assertRaises(ValueError):
            self.physical1 / "string"

    def test_rtruediv(self):
        result = 0 / self.physical1
        self.assertEqual(result.value, 0.0)
        self.assertEqual(result.dimensions, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

        with self.assertRaises(ValueError):
            5 / self.physical1

        result = self.physical1 / self.physical3
        self.assertEqual(result, 3.0)

    def test_idiv(self):
        with self.assertRaises(ValueError):
            self.physical1 /= self.physical2


class TestPower(unittest.TestCase):

    def setUp(self):
        self.physical1 = Physical(2.0, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.physical2 = Physical(3.0, Dimensions(0, 1, 0, 0, 0, 0, 0))

    def test_pow_integer(self):
        result = self.physical1 ** 3
        self.assertEqual(result.value, 8.0)
        self.assertEqual(result.dimensions, Dimensions(3, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_pow_fraction(self):
        result = self.physical1 ** 0.5
        self.assertEqual(result.value, 2.0 ** 0.5)
        self.assertEqual(result.dimensions, Dimensions(0.5, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_pow_zero(self):
        result = self.physical1 ** 0
        self.assertEqual(result, 1.0)

    def test_pow_negative(self):
        result = self.physical1 ** -1
        self.assertEqual(result.value, 0.5)
        self.assertEqual(result.dimensions, Dimensions(-1, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

        result = self.physical1 ** -2
        self.assertEqual(result.value, 0.25)
        self.assertEqual(result.dimensions, Dimensions(-2, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result.precision, self.physical1.precision)

    def test_pow_non_number(self):

        with self.assertRaises(ValueError):
            self.physical1 ** self.physical2

        with self.assertRaises(ValueError):
            2 ** self.physical2




if __name__ == '__main__':
    unittest.main()
