import unittest
from simplesi.dimensions import Dimensions
from simplesi import Physical, PRECISION


class TestPhysicalNonSI(unittest.TestCase):

    def setUp(self):
        self.physical = Physical(5, Dimensions(1, 0, 0, 0, 0, 0, 0))
        self.nonsi_physical1 = Physical(5, Dimensions(1, 0, 0, 0, 0, 0, 0), conv_factor=0.5)
        self.nonsi_physical2 = Physical(5, Dimensions(1, 0, 0, 0, 0, 0, 0), conv_factor=0.5)
        self.nonsi_physical3 = Physical(2.5, Dimensions(1, 0, 0, 0, 0, 0, 0), conv_factor=0.5)
        self.nonsi_physical4 = Physical(10.1, Dimensions(1, 0, 0, 0, 0, 0, 0), conv_factor=0.5)

    def test_relation_between_nonsi(self):
        self.assertTrue(self.nonsi_physical1 == self.nonsi_physical2)
        self.assertTrue(self.nonsi_physical1 != self.nonsi_physical3)
        self.assertTrue(self.nonsi_physical1 <= self.nonsi_physical2)
        self.assertTrue(self.nonsi_physical1 >= self.nonsi_physical3)
        self.assertTrue(self.nonsi_physical1 > self.nonsi_physical3)
        self.assertTrue(self.nonsi_physical3 < self.nonsi_physical2)

    def test_si_to_nonsi(self):
        self.assertTrue(self.physical > self.nonsi_physical1)
        self.assertTrue(self.physical < self.nonsi_physical4)
        self.assertTrue(self.physical == 2 * self.nonsi_physical3)
        self.assertTrue(self.physical != self.nonsi_physical1)




if __name__ == '__main__':
    unittest.main()
