import unittest

from galeneinstance import GaleneInstance, InvalidInstanceSizeException


class Testing(unittest.TestCase):
    def test_valid_instance_mappings(self):
        self.assertEqual(GaleneInstance.map_instance_type(2), "n2-highcpu-2")
        self.assertEqual(GaleneInstance.map_instance_type(29), "n2-highcpu-2")
        self.assertEqual(GaleneInstance.map_instance_type(30), "n2-highcpu-4")
        self.assertEqual(GaleneInstance.map_instance_type(40), "n2-highcpu-4")
        self.assertEqual(GaleneInstance.map_instance_type(41), "n2-highcpu-16")
        self.assertEqual(GaleneInstance.map_instance_type(80), "n2-highcpu-16")
        self.assertEqual(GaleneInstance.map_instance_type(81), "n2-highcpu-32")
        self.assertEqual(GaleneInstance.map_instance_type(100), "n2-highcpu-32")

    def test_max_user_out_of_range(self):
        self.assertRaises(InvalidInstanceSizeException, GaleneInstance.map_instance_type, 0)
        self.assertRaises(InvalidInstanceSizeException, GaleneInstance.map_instance_type, 1)
        self.assertRaises(InvalidInstanceSizeException, GaleneInstance.map_instance_type, 101)


if __name__ == '__main__':
    unittest.main()
