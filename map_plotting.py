"""
For A3:

Purpose:
Generates map showing crash data distributions across 
New Zealand regions (based on shp) for specific year.

Key Functions:

get_region_crash_counts_for_join: Counts crashes by region for a specific year.
* corrected Auckland name

merge_shp_with_map_data: Merges shapefile geographic data with crash data, 
ensuring all regions are represented. Exclude outside region.

generate_region_crash_map_by_year: Plots the crash count map with matplotlib.

draw_nz_map: testing function to check map layout (shp geo data).

Input & Output:
Input: Cleaned crash data and shp path.
Output: Figure object of the map, ready for display or saving.
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from clean_data import load_and_clean

MAP_FILE = "data/regional-council-2025.shp"
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

Auckland_name_mapping = {'Auckland Region': 'Auckland'} #solve the Auckland name anomaly

def get_region_crash_counts_for_join(df, year):
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
    filtered_df = df.loc[df['crashYear'] == year]  
    grouped = filtered_df.groupby('region', observed= False).size().reset_index(name = 'CrashCount') 
    grouped['region'] = grouped['region'].astype(str).replace(Auckland_name_mapping)
    #use group to accumulate by region name using size() and set column name as 'CrashCount'
    return grouped 

#note: defalut arguments can be automatically passed to main function
#note: crash_map_data is not good naming, caused confusion when revisiting the sub-function
def merge_shp_with_map_data (region_crash_counts, shp_path=MAP_FILE, region_key_shp="REGC2025_1", region_key_data="region", count_col="CrashCount"):
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
    gpd_df = gpd_df[gpd_df['REGC2025_1'] != 'Area Outside Region'] #remind from Edward, this region can be excluded
    merged = gpd_df.merge(region_crash_counts, left_on=region_key_shp, right_on=region_key_data, how="left")
    #why left: maintain integrity of shp data, if data for certain region of a year is 0, nan will be given for the region
    #right join: if one region is 0, shp will not be introduced and cause error
    #inner: if one region is 0, shp will not be joined and lose part of region.
    merged[count_col] = merged[count_col].fillna(0).astype(int) 
    #fill nan with 0, transfer to int as nan is float
    return merged

def generate_region_crash_map_by_year(cleaned_df, year, cmap="OrRd"):
    """
    generate a crash count in NZ map for a given year, scalable for streamlit based on scroll bar usage.
    
    Parameters:
        df (pd.DataFrame): cleaned crash data
        year (int): year to filter
        cmap (str): color map #OrRd - color from orange to red to show data difference

    To do: need to include data as legend. Will it be able to show the legend dataframe (region & counts) in streamlit dashboard?
    """
    region_crash_counts = get_region_crash_counts_for_join(cleaned_df, year)
    merged_gdf = merge_shp_with_map_data(region_crash_counts)

    fig, axes = plt.subplots(figsize=(10, 8)) #setup canvas and axes in canvas
    merged_gdf.plot(
        column="CrashCount",
        cmap=cmap,
        linewidth=0.5,
        edgecolor="black",
        legend=True,
        ax=axes
    )
    axes.set_title(f"Annual Crash Count by Region of {year}")
    axes.axis("off")
    plt.tight_layout() #auto adjusts the plot layout
    
    #use adjusttext to adjust the text locations
    texts = [] #prepare list for text (region)
    for idx, row in merged_gdf.iterrows(): #iterate over gdf for each row/region with geo data
        centroid = row['geometry'].centroid #calculate center of region
        text = axes.text(centroid.x, centroid.y, row['REGC2025_1'], 
                         ha='center', fontsize=6, color='black') 
        #parameter: row name for region, horizontally align in center, font size and color
        texts.append(text)

    adjust_text(texts, ax=axes, expand_text=(1.5, 1.5), expand_objects=(6, 6))
    #parameters: object: texts list, axes, max distance to center, space between

    return fig

cleaned_df = load_and_clean()