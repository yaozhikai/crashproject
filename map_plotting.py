import folium
import geopandas as gpd
import pandas as pd
from clean_data import load_and_clean

MAP_FILE = "data/regional-council-2025.shp"
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def prepare_map_data(df, year):
    """Prepare the DataFrame for map function:
    - plan: include year for filter
    - group by region
    - DataFrame columns are region and 'crashCount'
    
    Parameter:
    cleaned crash data from clean_data.py
    int year for planned filter

    Return:
    DataFrame of crash count by region    
    """
    filtered_df = df[df['crashYear'] == year] #for later use as filter in streamlit? Choice: == one year or isin year list?
    grouped = filtered_df.groupby('region').size().reset_index(name = 'CrashCount') #use group to accumulate by region name and set column name
    return grouped

df = load_and_clean()

year = 2004

map_df = prepare_map_data(df, year)

print("Crash Count by Region in", year)
print(map_df)