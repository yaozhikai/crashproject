"""
Traffic Accident Analysis Tool

This program provides an interactive menu to generate text and visual reports 
for traffic accident statistics (by severity level, year, and speed limit) 
based on historical data from 2000 to 2025.

Features:
- Based on user input year and speed limit,
  generate text reports summarizing accident counts by severity.
- Plot graphical report of accident amounts by year.
"""

"""
NOTES FOR FUTURE REFACTORING FOR A3:

To enhance maintainability and advanced data analysis (e.g. correlation with weather), 
the following parts of the current code will be considered for refactoring using pandas:

1. Data Cleaning (prepare_clean_data):
   - Replace tuple iteration with DataFrame filtering and a processed 'effectiveSpeed' column.
   - Done!

2. Accumulation (accumulate_year_severity, transform_to_table):
   - Use DataFrame operations such as groupby and unstack to simplify aggregation.
   - Done!

3. Printing Reports:
   - Replace nested loops with formatted DataFrame output 
     (to be verified: is the DataFrame already structured, ready for print?).
    - Done!

4. Single-Year Report (print_crash_severity_report):
   - Apply filters directly on the DataFrame for cleaner logic.
   - Done!

5. Plot Preparation:
   - Similar to (3) and (4), use filtered DataFrame slices to generate x and y values for plotting.
   - Done!

Other improvements to be considered:
- Inital plan to incooperate a long weekend dataset to study impact of long weekend, however original data has no excat date
after review
- CAS dataset includes region data, which can be incooperate with NZ Stat council region map data. Consider to use this based
on new lib (folium? plotly?) study still pending
- Add new options? for weather and region? add these filters on map/dashboard?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
CONDITION = "fine"
# Define fixed severity order for consistent report form
SEVERITY_ORDER = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]

def prepare_clean_df (df):
    """
    Prepare a cleaned DataFrame by using filters:
    - effective speed limits , insert a new column 'effectiveSpeed'.

    steps:
    1. Call filter function
    2. Filter by index for the rows which are valid in filter
    3. Inserts a new column 'effectiveSpeed' into the cleaned DataFrame.
    4. Create a new cleaned df

    Parameters:
        df (raw df)
        -other filteres will be extended

    Returns:
        new cleaned with effectiveSpeed, index is OBJECTID
        """
    effective_speed = filter_effective_speed_series(df)
    cleaned_df = df.loc[effective_speed.index].copy() #create a new copy, include all rows which index matches with effectiveSpeed 
    cleaned_df["effectiveSpeed"] = effective_speed #insert new column for effective speed
    return cleaned_df.drop(columns=["speedLimit", "temporarySpeedLimit"])

def filter_effective_speed_series(df):
    """Filter and return a series of effective speed limits by prioritising temporary limits.

    - Prioritises 'temporarySpeedLimit' over 'speedLimit',
    - Filters out missing values and those not divisible by 10,
    - Returns a Series of valid effective speeds with integer type ('Int64').

    Parameters:
        df : Input raw dataframe which has 'temporarySpeedLimit' and 'speedLimit' columns.
    Returns:
        pd.Series: A Series containing valid effective speeds, indexed as in the input DataFrame."""
    processed = df['temporarySpeedLimit'].combine_first(df['speedLimit'])
    effective_speed = processed[(processed.notna()) &
                            (processed % 10 == 0)]
    return effective_speed.astype('Int64') #float in raw data, due to Nan

def extract_valid_values(df, column_name):
    """
    A generic function to extract sorted unique values from df and 
    required column.

    Parameters: df (cleaed df), column name

    Returns: list of sorted unique values    
    """
    unique_values = df[column_name].dropna().unique()
    cleaned_values = []
    for value in unique_values:
        cleaned_values.append(int(value))
    cleaned_values.sort()
    return cleaned_values

def get_effective_speed(speed_limit, temporary_speed):
    """get effective speed limit by prioritising temporarySpeedLimit if available and valid."""
    # check if temporary speed exists and is valid as multiples of 10
    if temporary_speed == temporary_speed and temporary_speed % 10 == 0:
        return int(temporary_speed)
    # check if normal speed limit exists and is valid
    elif speed_limit == speed_limit and speed_limit % 10 == 0:
        return int(speed_limit)
    else:
        return None  # Both are missing or invalid
pass

def read_csv_data(filename: str, columns: list[str]) -> list[tuple]:
    """
    IMPORTANT NOTE:
      When completing Part one and Part Two of the project you do NOT need to understand how this function works.
    Reads in data from a list of csv files.
    Returns columns of data requested, in the order given in
    """
    df = pd.read_csv(filename)
    desired_columns = df[columns]
    return list(desired_columns.itertuples(index=False, name=None))
pass

def load_raw_dataframe(filename, columns, dtypes, index_col = None):
    """This function will replace original read_csv function
    It will load raw crash data from csv file with given columns and data types.
    Parameters:
    - filename
    - required columns (list of cols)
    - dtypes (tbc, still researching, flexible for future inclusion of date and coordinates?
    speed use float as they contains NaN
    - index (use OBJECTID as unique id for downstream processing)
    )
    Returns:
    DF contains all selected colms with specified data type.
    """
    return pd.read_csv(filename, usecols=columns, dtype=dtypes, index_col=index_col)

def read_valid_int (prompt, valid_data, value='value'):
    """This is a combined function to read user input of integer value for year and speed
    - If user input a valid integer within tuple, return the integer
    - If input is invalid, prompt again."""
    print(prompt)
    print(f"{value} Valid range: {min(valid_data)} to {max(valid_data)}")

    user_input_str = input(f'{value}: ')

    if user_input_str.isdigit():  #verify if input is digit
        user_int = int(user_input_str)
        if user_int in valid_data: #verify if input is in tuple (valid)
            return user_int
        else:
            print (f"Warning: {value} {user_int} does not exist in the dataset.")
            print (f"Available {value.lower()}s are: {sorted(valid_data)}.") 
            return read_valid_int(prompt, valid_data, value)   
    else:
        print ('Input must be one integer.')
        return read_valid_int(prompt, valid_data, value)
    
def get_plot_year_range(crash_years):   #For part 2 feature 5: 
    """
    Prompt user to enter a start and end year within available crash years
    Validate input is legal
    Returns a tuple containing start and end year selected by user.
    """
    print(f"Available years: {min(crash_years)} to {max(crash_years)}")
    
    start_year = read_valid_int("Please enter start year.", crash_years, "Start Year")
    end_year = read_valid_int("Please enter end year later than start year.", crash_years, "End Year")
    
    while end_year < start_year:
        print("Warning: End year must not be earlier than start year. Please try again.")
        end_year = read_valid_int("Please enter end year later than start year.", crash_years, "End Year")

    return start_year, end_year

def get_plot_severity_types(severity_types):
    """
    Prompt user to select desired crash severity types using (y/n) prompts.
    If none selected, warn and restart the selection process.
    Returns a list of selected types.
    """
    while True: #restart the loop if user select n for all types
        selected = []
        print("Please select desired crash severity types.")
        
        for severity in severity_types:
            while True:
                response = input(f"  {severity} (y/n): ").lower()
                if response == 'y':
                    selected.append(severity)
                    break
                elif response == 'n':
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        if len(selected) > 0:
            return selected
        else:
            print("At least one severity type must be selected.")
            print("Please try again.")

def get_plot_time_and_types(crash_years, severity_types):
    """Prompt user to select time range and crash severity types for plotting."""
    start_year, end_year = get_plot_year_range(crash_years)
    selected_types = get_plot_severity_types(severity_types)
    return start_year, end_year, selected_types

def prepare_lists_from_df(df, selected_types, start_year, end_year):
    """
    Extract years and count lists for plotting from crash summary table.
    Parameters:
        df (pd.DataFrame): Output from generate_crash_table_by_year()
        selected_types (list): List of selected severity types
        start_year (int): Start year for range
        end_year (int): End year for range

    Returns:
        tuple: (years, list of counts for each severity type)
    """
    df_range = df.loc[start_year:end_year, selected_types] #slice the df with given parameters
    years = df_range.index.tolist() #Extract the list of years (for x-axis values)
    counts_lists = []
    # For each selected severity type, extract a list of crash counts (for y-axis series)
    for severity in selected_types:
        counts = df_range[severity].tolist()
        counts_lists.append(counts)
    return years, counts_lists


def menu_select(options: list[str]) -> int:
    """
    - Prints a list of enumerated options and collects the users
    - The user is prompted until they enter a valid menu index
    - returns valid user selection
    """
    prompt = f"0-{len(options) - 1}: "
    i = 0
    while i < len(options):
        print(f'[{i}] {options[i]}')
        i += 1

    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid option\nTry again')
        selection = int(input(prompt))
    return selection

def print_crash_severity_report(year_of_interest: int, speed_of_interest: int, df) :
    """
    Prints a table outlining the number of crashes in a given year for a given speed limit
    based on DataFrame
    """    
    filtered = df[(df['crashYear'] == year_of_interest) & (df['effectiveSpeed'] == speed_of_interest)]
    if filtered.empty:
        print(f"Warning: No records found for year {year_of_interest} and speed {speed_of_interest}.")
        return
    print("Crash Severity by Classification")
    print(f"Year: {year_of_interest}")
    print(f"Speed Limit: {speed_of_interest}\n")
    summary = filtered['crashSeverity'].value_counts().reindex(SEVERITY_ORDER, fill_value=0)
    for severity, count in summary.items():
        print(f"{severity}: {count}")

def generate_crash_table_by_year(df):
    """Gerenate a crash count table by year and severity type.
    Replace original design through accumulator and list of tuples.

    Parameter: cleaned df

    Return: DataFrame contains Year and Severity
    """
    crash_summary = df.groupby(['crashYear', 'crashSeverity'],observed=False).size().unstack(fill_value=0) 
    #fill 0 for a cell which has no accident record, add speed limit as another filter in displaying?
    crash_summary = crash_summary.reindex(columns = SEVERITY_ORDER, fill_value = 0)
    crash_summary['Total'] = crash_summary.sum(axis = 1)
    return crash_summary

def plot_trends_over_time (years, selected_types, counts_lists):
    """
    plot trend line over user's time range by selected severity type
    """
    axes = plt.axes()

    for i in range(len(selected_types)):
        xs = years
        ys = counts_lists[i]
        axes.plot(xs, ys, label = selected_types[i], marker = 'o')

    axes.set_xlabel("Year")
    axes.set_xticks(years) #set years as x ticks, aviod float
    axes.set_ylabel("Crash Count")
    axes.set_title("Crash Over Time by Severity Type")
    axes.legend()
    axes.grid(True)
    plt.show()




def main():
    """Small application that presents tables and graphs based on crash data
    Process steps:
    1. Read raw data as a list of tuples containing (crashYear, speedLimit, crashSeverity, temporarySpeedLimit).
    2. Generate a cleaned list of tuples containing (crashYear, crashSeverity, effectiveSpeedLimit).
    3. Extract legal year and speed limit from clean_data
    4. Perform reporting and visualization functions based on the cleaned data.
    """

    #raw_data = read_csv_data(DATA_FILE, ["crashYear", "speedLimit", "crashSeverity", "temporarySpeedLimit"])
    raw_data_df = load_raw_dataframe(
    DATA_FILE,
    columns=["OBJECTID", "crashYear", "speedLimit", "crashSeverity", "temporarySpeedLimit", "weatherA", "region"],
    dtypes={
        "crashYear": "int16",
        "speedLimit": "float32",
        "temporarySpeedLimit": "float32",
        "crashSeverity": "category",
        "weatherA": "category",
        "region": "category"
    },
    index_col="OBJECTID"
    ) #also include objected ID as unique identifier if pd.join is needed in future
      
    cleaned_df = prepare_clean_df(raw_data_df)
    crash_years = extract_valid_values(cleaned_df, column_name='crashYear') 
    speed_limits = extract_valid_values(cleaned_df, column_name='effectiveSpeed') 

    menu_options = [
        "Crash Severity Report (single year and single speed limit)",
        "Crash Severity Report (All years)",
        "Crash Reports Over Time Graph",
        "Exit"
    ]

    while True:
        option = menu_select(menu_options)

        if option == 0:
            #this is to read user input year
            year_of_interest = read_valid_int("Please enter crash year.", crash_years, "Year")
            #this is to read user input speed limit
            speed_of_interest = read_valid_int("Please enter speed limit. Value should be multiple of 10", speed_limits, "Speed Limit")
            #this calls the print function
            print_crash_severity_report (year_of_interest, speed_of_interest, cleaned_df)

        elif option == 1:
            ###function to generate All Years Crash Severity Report
            table_df = generate_crash_table_by_year(cleaned_df)
            print(table_df)

        elif option == 2:
            table_df = generate_crash_table_by_year(cleaned_df)
            start_year, end_year, selected_types = get_plot_time_and_types(crash_years, SEVERITY_ORDER)
            years, counts_lists = prepare_lists_from_df(table_df, selected_types, start_year, end_year)
            plot_trends_over_time (years, selected_types, counts_lists)

        elif option == 3:
            print("Bye")
            break

        print ("\n")

main ()