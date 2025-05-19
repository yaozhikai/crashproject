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
    return pd.read_csv(filename, usecols=columns, dtype=dtypes, index_col="OBJECTID")

def filter_effective_speed_series(df):
    """
    Filter and return a series of effective speed limits by prioritising temporary limits.

    Returns:
    - pd.Series of valid speeds (multiples of 10), with original index preserved.
    """
    processed = df['temporarySpeedLimit'].combine_first(df['speedLimit'])
    effective_speed = processed[(processed.notna()) & (processed % 10 == 0)]
    return effective_speed.astype('Int64') #float in raw data, due to Nan

def prepare_clean_df(df):
    """
    Prepare cleaned DataFrame from raw data:
    - Generates effectiveSpeed
    - Returns relevant columns for following features

    Returns:
    - Cleaned DataFrame with crashYear, crashSeverity, effectiveSpeed, weatherA, region
    """
    effective_speed = filter_effective_speed_series(df)
    cleaned_df = df.loc[effective_speed.index].copy() #generate new df, avioding only generates a view on original df
    cleaned_df["effectiveSpeed"] = effective_speed #add new column and relate data
    return cleaned_df[["crashYear", "crashSeverity", "effectiveSpeed", "weatherA", "region", "urban"]]

def load_and_clean():
    """
    prepare for future use in main() features
    """
    raw_df = load_raw_dataframe()
    return prepare_clean_df(raw_df)