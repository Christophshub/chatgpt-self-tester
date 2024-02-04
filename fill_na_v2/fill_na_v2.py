import pandas as pd
import numpy as np

def fill_na_v2(df):
    return df.replace(np.nan, 0)
