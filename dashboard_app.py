from clean_data import load_and_clean
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def calculate_proportional_table(df):
    """
    Group by weather and severity, then calculate and generate percentage table with 'div' method.
    """
    grouped = df.groupby(['weatherA', 'crashSeverity'], observed=False).size().unstack(fill_value=0)
    grouped = grouped.reindex(columns=SEVERITY_ORDER, fill_value=0)
    proportion_df = grouped.div(grouped.sum(axis=1), axis=0) #sum by roww and divide by row total value
    return proportion_df

df = load_and_clean()

# test calculation
proportion_table = calculate_proportional_table(df)

print(proportion_table)