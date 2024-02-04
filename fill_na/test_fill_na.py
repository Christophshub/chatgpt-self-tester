import pandas as pd 
import numpy as np 
import pytest

from fill_na import fill_na

# Create a fixture
@pytest.fixture
def input_data():
   return pd.DataFrame([[np.nan, 2, np.nan, 0],
                        [3, 4, np.nan, 1],
                        [np.nan, np.nan, np.nan, 5],
                        [np.nan, 3, np.nan, 4]],
                       columns=list('ABCD'))

# Using the fixture in test
def test_fill_na(input_data):
    result = fill_na(input_data)
    assert result.isnull().sum().sum() == 0
