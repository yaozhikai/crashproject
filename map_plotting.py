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

def merge_shp_with_map_data (crash_map_data, shp_path=MAP_FILE, region_key_shp="REGC2025_1", region_key_data="region", count_col="CrashCount"):
    """Merge map shp data with prepared data for map
    Parameters:
    -introduce shp file
    -prepared crash_map_data
    -join key from shp file
    -join key from crash map data
    -column name of crash count data

    Returns:
    gpd dataframe merged with crash count, need to filled 0 if no data for the region record.
    """
    gpd_df = gpd.read_file(shp_path)
    merged = gpd_df.merge(crash_map_data, left_on=region_key_shp, right_on=region_key_data, how="left")
    merged[count_col] = merged[count_col].fillna(0).astype(int)
    return merged

pass

import geopandas as gpd
import matplotlib.pyplot as plt

import geopandas as gpd
import matplotlib.pyplot as plt

def draw_nz_map(shapefile_path=MAP_FILE):
    """
    Draw a clean static outline map of New Zealand regions using shapefile.
    No labels or index are shown—just geometry for visual inspection or base map use.

    Parameters:
        shapefile_path (str): Path to the shapefile (.shp)
    """
    gdf = gpd.read_file(shapefile_path)
    gdf.plot(color='white', edgecolor='black')
    plt.axis("off")
    plt.tight_layout()
    plt.show()


draw_nz_map(shapefile_path=MAP_FILE)
