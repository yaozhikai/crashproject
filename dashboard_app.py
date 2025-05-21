import streamlit as st
import matplotlib.pyplot as plt
from map_plotting import generate_region_crash_map_by_year
from clean_data import load_and_clean
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def calculate_proportional_table(df, SEVERITY_ORDER):
    """
    Group by weather and severity, then calculate and generate percentage table with 'div' method.
    """
    grouped = df.groupby(['urban', 'crashSeverity'], observed=False).size().unstack(fill_value=0)
    grouped = grouped.reindex(columns=SEVERITY_ORDER, fill_value=0)
    proportion_df = grouped.div(grouped.sum(axis=1), axis=0)
    return proportion_df

def get_weather_filter(df):
    """a subfunction for select 'urban' for another dimension to study weather impact"""
    weathers = sorted(df[df['weatherA'].notna() & (df['weatherA'] != 'Null')]['weatherA'].unique())
    selected = st.sidebar.multiselect("Select weather status", weathers, default=weathers)
    return selected

def run_dashboard():
    """a function to generate dashboard for users.
    The dashboard shows the proportion of severity types under different weatherA conditons
    """
    df = load_and_clean()
    tab1, tab2 = st.tabs(["Impact of Weather on Crash Severity by Area Type", "Annual Crash Amounts by Region"])

    with tab1:
        urban_types = get_weather_filter(df) #use sub-function for filter application
        df = df[df["weatherA"].isin(urban_types)] #slice

        proportion_table = calculate_proportional_table(df, SEVERITY_ORDER)
        proportion_table = proportion_table[proportion_table.index != "Null"] #remove weatherA = Null row

        st.title("Impact of Weather on Crash Severity by Area Type")
        st.subheader("Porportion Table")
        st.dataframe(proportion_table.style.format("{:.1%}")) #print the proportion table

        st.subheader("Stacked Bar Chart")
        fig, axes = plt.subplots(figsize = (10,6)) #plot a sub graph under propoertion table
        proportion_table.plot (kind = 'bar', stacked = True, ax = axes)
        axes.set_xlabel("Urban Status")
        axes.set_ylabel("Proportion")
        axes.set_title('Crash Severity Proportion')
        axes.legend(title = 'Crash Severity')
        st.pyplot(fig)

    with tab2:
        st.title("Annual Crash Amounts by Region")
        selected_year = st.slider("Select year for crash map", min_value=2000, max_value=2024, value=2000)
        st.caption(f"Displaying crash counts for year {selected_year}")
        fig = generate_region_crash_map_by_year(df, selected_year, cmap="OrRd")
        st.pyplot(fig)

if __name__ == "__main__":
    run_dashboard()

#streamlit run dashboard_app.py