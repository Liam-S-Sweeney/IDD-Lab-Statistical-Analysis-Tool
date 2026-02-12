import pandas as pd
import numpy as np

# Global Variables
RAW_DATA_PATH = r'data_files\VT Teen Study Waves 1,2,3,4 merged all youth variables.csv'
MISSING_CODES = [-99,-999,-9999]

RAW_DF = pd.read_csv(RAW_DATA_PATH)
NUMERIC_DF = raw_df.apply(pd.to_numeric, errors='coerce').replace(MISSING_CODES, np.nan)

HUE_COL = "CGender_4"
SIZE_COL = "CAge_4"
