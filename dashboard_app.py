""" 
For A3:

Purpose:
Uses Streamlit to create an interactive web dashboard, 
allowing users to apply filters (speed, severity, weather) 
to visualize crash data as stacked bar charts and geographic maps.

Key Functions:

calculate_count_table: Generates a crash count table by speed and severity.

get_weather_filter, get_dashboard_filter: Provides filter options for weather, speed, and severity categories.

run_dashboard: Combines the dashboard logic into two tabs:

Tab 1: Displays the crash count table and stacked bar chart.

Tab 2: Displays crash map for selected years and a summary crash count table by region.
"""


import streamlit as st
import matplotlib.pyplot as plt
from map_plotting import generate_region_crash_map_by_year
from map_plotting import get_region_crash_counts_for_join #generic function, use to slice df by region and year
from clean_data import load_and_clean
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def calculate_count_table(df, SEVERITY_ORDER):
    """
    refacor from proportion calculate function. now similar to main calculation function.
    retain for better adjustment and documentation.
    original design was    
    Group by weather and severity, then calculate and generate percentage table with 'div' method.
    """
    grouped = df.groupby(['effectiveSpeed','crashSeverity'], observed=False).size().unstack(fill_value=0)
    #grouped = df.groupby(['urban', 'crashSeverity'], observed=False).size().unstack(fill_value=0)
    grouped = grouped.reindex(columns=SEVERITY_ORDER, fill_value=0)
    #proportion_df = grouped.div(grouped.sum(axis=1), axis=0)
    return grouped #proportion_df

def get_weather_filter(df):
    """a subfunction for select 'weatherA' for another dimension to study weather impact"""
    filtered_weatherA = df.loc[
    df['weatherA'].notna() & (df['weatherA'] != 'Null'),
    'weatherA']
    weathers = sorted(filtered_weatherA.unique())
    selected = st.sidebar.multiselect("Select weather status", weathers, default=weathers) #as tested, side bar is tab-wised, cannot delete from other tabs.
    # the filter still works in new tab!!!
    return selected

def get_dashboard_filter(df, column_name, label):
    """
    General filter function for any categorical column. combine speed and severity filter
    """
    unique_values = sorted(df[column_name].dropna().unique())
    selected = st.sidebar.multiselect(label, unique_values, default=unique_values)
    return selected


def get_speed_for_speed(df): #legacy, combined to one filter
    """a subfunction for select speed limit, didn't reuse weather filter as for weather orther filter logic is needed and tested"""
    speeds = sorted(df['effectiveSpeed'].unique())
    selected = st.sidebar.multiselect("Select speed limit", speeds, default=speeds)
    return selected
pass
                    
def get_severity_filter(df): #legacy, combined to one filter
    """Filter for selecting crash severity types"""
    severity_types = sorted(df['crashSeverity'].unique())
    selected = st.sidebar.multiselect("Select Crash Severity Types", severity_types, default=severity_types)
    return selected
pass

def run_dashboard():
    """a function to generate dashboard for users.
    The dashboard shows the proportion of severity types under different weatherA conditons
    """
    df = load_and_clean()
    tab1, tab2 = st.tabs(["Crash Count Visual Report", "Annual Crash Amounts by Region"])

    with tab1:
        weather_types = get_weather_filter(df) #use sub-function for filter application
        df = df[df["weatherA"].isin(weather_types)] #slice
        #speed_types = get_speed_for_speed(df)
        #df = df[df["effectiveSpeed"].isin(speed_types)]
        #selected_severities = get_severity_filter(df)
        #df = df[df['crashSeverity'].isin(selected_severities)] 
        speed_types = get_dashboard_filter(df, 'effectiveSpeed', "Select speed limit")
        df = df[df["effectiveSpeed"].isin(speed_types)]
        selected_severities = get_dashboard_filter(df, 'crashSeverity', "Select Crash Severity Types")
        df = df[df['crashSeverity'].isin(selected_severities)]

        if df.empty: #use boolean
            #for plotting, error appears if no data selected
            #add warning to remind user, aviod error output
            st.warning("No data available for the selected filters. Please select at least one criteria.")
        else:
            crash_count_table = calculate_count_table(df, SEVERITY_ORDER)

            st.title("Crash Count Visual Report")
            st.subheader("Crash Count Table")
            st.dataframe(crash_count_table) #print the crash count table

            st.subheader("Stacked Bar Chart")
            fig, axes = plt.subplots(figsize = (10,6)) #plot a sub graph under crash count table
            crash_count_table.plot (kind = 'bar', stacked = True, ax = axes)
            axes.set_xlabel("Speed Limit")
            axes.set_ylabel("Crash Counts")
            axes.set_title('Crash Count Table')
            axes.legend(title = 'Crash Severity')
            st.pyplot(fig)

    with tab2:
        st.title("Annual Crash Amounts by Region")
        selected_year = st.slider("Select year for crash map", min_value=2000, max_value=2024, value=2000) #defalut step is 1
        st.caption(f"Displaying crash counts for year {selected_year}")
        fig = generate_region_crash_map_by_year(df, selected_year, cmap="OrRd") 
        #pass selected year to plotting function, color from orange to red
        st.pyplot(fig)

        # generate and display crash table sorted by region, use as legend
        region_df = get_region_crash_counts_for_join(df, selected_year)
        region_df_sorted = region_df.sort_values(by="region")  # sort region name alphabetically in the 'legend'
        st.subheader("Crash Count by Region")
        st.dataframe(region_df_sorted.rename(columns={"region": "Region", "CrashCount": "Crash Count"}))



if __name__ == "__main__":
    run_dashboard()

#streamlit run dashboard_app.py