#clean_data.py
#move load and clean functions for re-use in new features

import pandas as pd

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"

def load_raw_dataframe(filename=DATA_FILE):
    """
    Load raw crash data from csv file with given columns and data types.

    Parameters:
    - filename: CSV file path 

    Returns:
    - Raw DataFrame with specified columns and types, indexed by OBJECTID.
    """
    columns = ["OBJECTID", "crashYear", "speedLimit", "crashSeverity", "temporarySpeedLimit", "weatherA", "region","urban"]
    dtypes = {
        "crashYear": "int16",
        "speedLimit": "float32",
        "temporarySpeedLimit": "float32",
        "crashSeverity": "category",
        "weatherA": "category",
        "region": "category",
        "urban": "category"
    }
    #review note: select columns from oringal data and set types
    return pd.read_csv(filename, usecols=columns, dtype=dtypes, index_col="OBJECTID")

def filter_effective_speed_series(df):
    """Filter and return a series of effective speed limits by prioritising temporary limits.

    - Prioritises 'temporarySpeedLimit' over 'speedLimit',
    - Filters out missing values and those not divisible by 10,
    - Returns a Series of valid effective speeds with integer type ('Int64').

    Parameters:
        df : Input raw dataframe which has 'temporarySpeedLimit' and 'speedLimit' columns.
    Returns:
        pd.Series of valid speeds (multiples of 10), with original index preserved.
    """
    processed = df['temporarySpeedLimit'].combine_first(df['speedLimit']) 
    #first, prioritize temporary speed limit
    effective_speed = processed[(processed.notna()) & (processed % 10 == 0)] 
    #then, remove invalid speeds (nan, illegal value like 5,11)
    return effective_speed.astype('Int64') #float in raw data, due to Nan

def prepare_clean_df(raw_df):
    """
    Prepare a cleaned DataFrame by using filters:
    - effective speed limits , insert a new column 'effectiveSpeed'.

    steps:
    1. Call filter function
    2. Filter by index for the rows which are valid in filter
    3. Inserts a new column 'effectiveSpeed' into the cleaned DataFrame.
    4. Create a new cleaned df (adding weatherA and region for new features)

    Parameters:
        df (raw df)
        -other filteres will be extended

    Returns:
        new cleaned with effectiveSpeed, index is OBJECTID
    """
    effective_speed = filter_effective_speed_series(raw_df)
    cleaned_df = raw_df.loc[effective_speed.index].copy() 
    #generate new df, avioding only generates a view on original df, align row with index which is ObjectID
    #review note: slice of df didn't change index value, slice all rows with effective speed.
    cleaned_df["effectiveSpeed"] = effective_speed #add new column and relate data
    return cleaned_df[["crashYear", "crashSeverity", "effectiveSpeed", "weatherA", "region", "urban"]]

def load_and_clean():
    """
    prepare for future use in main() features
    return a cleaned df ready for use later
    """
    raw_df = load_raw_dataframe()
    return prepare_clean_df(raw_df)