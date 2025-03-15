import unittest
from simplesi.dimensions import Dimensions, DimensionError


class TestDimensions(unittest.TestCase):

    def test_dimensions_creation(self):
        dim = Dimensions(kg=1.0, m=2.0, s=3.0, K=4.0)
        self.assertEqual(dim.kg, 1.0)
        self.assertEqual(dim.m, 2.0)
        self.assertEqual(dim.s, 3.0)
        self.assertEqual(dim.K, 4.0)

    def test_dimension_error(self):
        with self.assertRaises(DimensionError):
            raise DimensionError("This is a dimension error")


if __name__ == '__main__':
    unittest.main()
