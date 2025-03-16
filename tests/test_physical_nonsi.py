# import unittest
# from simplesi.dimensions import Dimensions
# from simplesi import Physical, PRECISION
# import simplesi as si
# si.environment('imperial')
# si.environment('structural', replace=False)
#
#
# class TestPhysicalNonSI(unittest.TestCase):
#
#     def setUp(self):
#         self.physical = Physical(5, Dimensions(1, 0, 0, 0, 0, 0, 0))
#         self.nonsi_physical1 = Physical(2.5, Dimensions(1, 0, 0, 0, 0, 0, 0))
#         self.nonsi_physical2 = Physical(2.5, Dimensions(1, 0, 0, 0, 0, 0, 0))
#         self.nonsi_physical3 = Physical(0.5, Dimensions(1, 0, 0, 0, 0, 0, 0))
#         self.nonsi_physical4 = Physical(10.1, Dimensions(1, 0, 0, 0, 0, 0, 0))
#
#     def test_relation_between_nonsi(self):
#         self.assertTrue(self.nonsi_physical1 == self.nonsi_physical2)
#         self.assertTrue(self.nonsi_physical1 != self.nonsi_physical3)
#         self.assertTrue(self.nonsi_physical1 <= self.nonsi_physical2)
#         self.assertTrue(self.nonsi_physical1 >= self.nonsi_physical3)
#         self.assertTrue(self.nonsi_physical1 > self.nonsi_physical3)
#         self.assertTrue(self.nonsi_physical3 < self.nonsi_physical2)
#
#     def test_si_to_nonsi(self):
#         self.assertTrue(self.physical > self.nonsi_physical1)
#         self.assertTrue(self.physical < self.nonsi_physical4)
#
#         self.assertTrue(self.physical != self.nonsi_physical1)
#         self.assertTrue(self.physical == 2 * self.nonsi_physical3)
#
#     def test_to(self):
#         self.assertEqual((1 * si.inch).to('inch'), '1.0 inch')
#         self.assertEqual((1 * si.ft).to('inch'), '12.0 inch')
#         self.assertEqual((1 * si.m).to('m'), '1.0 m')
#         self.assertEqual((12 * si.inch).to('ft'), '1.0 ft')
#         self.assertEqual((1 * si.yard).to('ft'), '3.0 ft')
#
#         self.assertEqual((1 * si.m).to('inch'), '39.37 inch')
#         self.assertEqual((1 * si.m).to('ft'), '3.281 ft')
#
#         self.assertEqual((10 * si.inch).to('m'), '0.254 m')
#         self.assertEqual((1 * si.ft).to('cm'), '30.48 cm')
#         self.assertEqual((1 * si.ft).to('mm'), '304.8 mm')
#         self.assertEqual((2 * si.yard).to('mm'), '1828.8 mm')
#
#         self.assertEqual(12 * si.inch + 2 * si.ft, 1 * si.yard)
#         self.assertEqual(12 * si.cm + 2 * si.m, 2120 * si.mm)
#
#
# if __name__ == '__main__':
#     unittest.main()
