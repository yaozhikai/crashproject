import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from clean_data import load_and_clean

MAP_FILE = "data/regional-council-2025.shp"
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

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
    #for later use as filter in streamlit? Choice: == one year or isin year list?
    grouped = filtered_df.groupby('region', observed= False).size().reset_index(name = 'CrashCount') 
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
    merged = gpd_df.merge(region_crash_counts, left_on=region_key_shp, right_on=region_key_data, how="left")
    #why left: maintain integrity of shp data, if data for certain region of a year is 0, nan will be given for the region
    #right join: if one region is 0, shp will not be introduced and cause error
    #inner: if one region is 0, shp will not be joined and lose part of region.
    merged[count_col] = merged[count_col].fillna(0).astype(int) 
    #fill nan with 0, transfer to int as nan is float
    return merged

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
    return fig

cleaned_df = load_and_clean()

test_year = 2023
fig = generate_region_crash_map_by_year(cleaned_df, test_year, cmap="OrRd")
plt.show()