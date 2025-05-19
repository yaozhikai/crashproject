import streamlit as st
import matplotlib.pyplot as plt

from clean_data import load_and_clean
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def calculate_proportional_table(df, SEVERITY_ORDER):
    """
    Group by weather and severity, then calculate and generate percentage table with 'div' method.
    """
    grouped = df.groupby(['weatherA', 'crashSeverity'], observed=False).size().unstack(fill_value=0)
    grouped = grouped.reindex(columns=SEVERITY_ORDER, fill_value=0)
    proportion_df = grouped.div(grouped.sum(axis=1), axis=0)
    return proportion_df

def get_urban_filter(df):
    """a subfunction for select 'urban' for another dimension to study weather impact"""
    urbans = sorted(df['urban'].dropna().unique())
    selected = st.sidebar.multiselect("Select urban status", urbans, default=urbans)
    return selected

def run_dashboard():
    """a function to generate dashboard for users.
    The dashboard shows the proportion of severity types under different weatherA conditons
    """
    df = load_and_clean()
    urban_types = get_urban_filter(df) #use sub-function for filter application
    df = df[df["urban"].isin(urban_types)] #slice

    proportion_table = calculate_proportional_table(df, SEVERITY_ORDER)
    proportion_table = proportion_table[proportion_table.index != "Null"] #remove weatherA = Null row

    st.title("Crash Severity Proportion Report")
    st.subheader("Porportion Table")
    st.dataframe(proportion_table.style.format("{:.1%}"))

    st.subheader("Stacked Bar Chart")
    fig, axes = plt.subplots(figsize = (10,6))
    proportion_table.plot (kind = 'bar', stacked = True, ax = axes)
    axes.set_xlabel("Weather Conditon")
    axes.set_ylabel("Proportion")
    axes.set_title('Crash Severity Proportion')
    axes.legend(title = 'Crash Severity')
    st.pyplot(fig)

if __name__ == "__main__":
    run_dashboard()

#streamlit run dashboard_app.py