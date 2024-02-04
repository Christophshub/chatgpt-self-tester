import pandas as pd
import numpy as np

def fill_na(df):
    return df.replace(np.NaN, 0)
