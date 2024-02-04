import pandas as pd
import numpy as np
import pytest
from fill_na import fill_na

@pytest.fixture
def sample_dataframe():
    df = pd.DataFrame({
        'A': [1, 2, np.nan],
        'B': [4, np.nan, 5],
        'C': [np.nan, 7, 8]
    })
    return df

def test_fill_na(sample_dataframe):
    filled_df = fill_na(sample_dataframe)
    assert not filled_df.isnull().values.any()
    assert filled_df.equals(pd.DataFrame({
        'A': [1, 2, 0],
        'B': [4, 0, 5],
        'C': [0, 7, 8],
    }))
