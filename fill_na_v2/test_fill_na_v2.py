import pandas as pd
import numpy as np
from fill_na_v2 import fill_na_v2
import unittest

class TestFillNaV2(unittest.TestCase):
    def test_fill_na_v2(self):
        df = pd.DataFrame({
            "A": [1, np.nan, 3],
            "B": [4, np.nan, 6],
            "C": [7, 8, np.nan]
        })
        expected_output = pd.DataFrame({
            "A": [1.0, 0.0, 3.0],
            "B": [4.0, 0.0, 6.0],
            "C": [7.0, 8.0, 0.0]
        })
        pd.testing.assert_frame_equal(fill_na_v2(df), expected_output)

if __name__ == "__main__":
    unittest.main()
