import unittest
from simplesi.dimensions import Dimensions


class TestDimensions(unittest.TestCase):

    def test_dimensions_creation(self):
        dim = Dimensions(kg=1.0, m=2.0, s=3.0, K=4.0, A=0.0, cd=0.0, mol=0.0)
        self.assertEqual(dim.kg, 1.0)
        self.assertEqual(dim.m, 2.0)
        self.assertEqual(dim.s, 3.0)
        self.assertEqual(dim.K, 4.0)
        self.assertEqual(dim.A, 0.0)
        self.assertEqual(dim.cd, 0.0)
        self.assertEqual(dim.mol, 0.0)

        dim = Dimensions(*[0 for x in range(7)])
        self.assertTrue(dim.dimensionsless)


if __name__ == '__main__':
    unittest.main()
