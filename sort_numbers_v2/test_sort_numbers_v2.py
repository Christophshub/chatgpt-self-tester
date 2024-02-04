# test_sort_numbers_v2.py

import unittest
from sort_numbers_v2 import sort_numbers_v2

class TestSortNumbers_v2(unittest.TestCase):

    def test_sort_numbers_v2(self):
        self.assertEqual(sort_numbers_v2([5,2,3,1,4]), [1,2,3,4,5])
        self.assertEqual(sort_numbers_v2([0,0,0,0,0]), [0,0,0,0,0])
        self.assertEqual(sort_numbers_v2([-1,-2,-3,-4,-5]), [-5,-4,-3,-2,-1])
        self.assertEqual(sort_numbers_v2([1.1,2.2,3.3,4.4,5.5]), [1.1,2.2,3.3,4.4,5.5])

    def test_sort_numbers_v2_errors(self):
        self.assertRaises(ValueError, sort_numbers_v2, "string")
        self.assertRaises(ValueError, sort_numbers_v2, [1,2,3,"string",4,5])
        self.assertRaises(ValueError, sort_numbers_v2, 1)

if __name__ == '__main__':
    unittest.main()
