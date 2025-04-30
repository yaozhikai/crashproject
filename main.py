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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
CONDITION = "fine"

def prepare_clean_data(raw_data):
    """
    New Solution:
    Prepare cleaned data with effective speed calculated.
    Input raw_data: list of (crashYear, speedLimit, crashSeverity, temporarySpeedLimit)
    Output clean_data: list of (crashYear, crashSeverity, effectiveSpeed)
    Only records with valid effective speed are included
    """
    clean_data = []
    for crash_year, speed_limit, crash_severity, temporary_speed in raw_data:
        effective_speed = get_effective_speed(speed_limit, temporary_speed)
        if effective_speed is not None: #to filter illegal speed limit values
            clean_data.append((crash_year, crash_severity, effective_speed))
    return clean_data

def extract_valid_values(clean_data, target_col_index):
    """a generic function to read valid unique values in dataset,
    use this dynamic function to replace pre-defined year and speed tuples
    """
    valid_values = unique_values(clean_data, target_col_index) #get unique value from clean_data
    valid_values.sort()
    return tuple(valid_values)




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

def prepare_lists_for_plot(accumulated_data, selected_types, start_year, end_year):
    """
    use accumulated (year, severity, count) data to build lists for plotting
    return:
    years (list range of start and end year +1)
    count_list: count_by_year for each selected seseverity
    """
    years = list(range(start_year, end_year+1))
    counts_list = []

    for severity in selected_types:
        counts = []
        for year in years:
            count =  0
            for y, sev,c in accumulated_data:
                if y == year and sev == severity:
                    count = c
                    break
            counts.append(count)
        counts_list.append(counts)
    return years, counts_list
                    

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


def unique_values(table: list, col_index: int) -> list:
    """Given a list of tuple returns a sorted list of unique values of a given row.
    Example:
    animals = [
        ("cat", "dog"),
        ("bird", "dog"),
        ("fish", "fish")
    ]

    print(unique_values(animals, 0))
    ['bird', 'cat', 'fish']

    print(unique_values(animals, 1))
    ['dog', 'fish']
    """
    out = []
    for row in table:
        if row[col_index] not in out:
            out.append(row[col_index])
    out.sort()
    return out


def print_crash_severity_report(year_of_interest: int, speed_of_interest: int, clean_data) -> None:
    """
    Prints a table outlining the number of crashes in a given year for a given speed limit
    based on clean_data: list of (crashYear, crashSeverity, effectiveSpeed)
    """    
    severity_types = unique_values(clean_data, 1)  # Index 1 is crashSeverity
    print("Crash Severity by Classification")
    print(f"Year: {year_of_interest}")
    print(f"Speed Limit: {speed_of_interest}")
    print()
    results = [] #accumulate total and store results in a list of tuple (type, count)
    total_count = 0 #use this to accumulate all kinds of accidents
    
    for severity_type in severity_types:
        # for loop to go through each severity_type
        count = 0
        for crashYear, crashSeverity, effectiveSpeed in clean_data:
            if (crashYear == year_of_interest) and (effectiveSpeed == speed_of_interest) and ( crashSeverity == severity_type):
                count += 1

        results.append((severity_type, count))
        total_count += count
        
    if total_count == 0: #example: year 2013/ speed 110
        print ('Warning: No records found in this category of year and speed limit.')
    else:
        for severity_type, count in results:
            print(f"{severity_type}: {count}")

def accumulate_year_severity(clean_data, crash_years, severity_types):
    """a generic accumulator to generate list of tuples contain
    (year, severity, count)
    """
    result = []

    for year in crash_years:
        for severity in severity_types:
            count = 0
            for record in clean_data:
                record_year, record_severity , effective_speed = record
                if record_year == year and record_severity == severity:
                    count += 1
            result.append((year, severity, count))

    return result

def transform_to_table(accumulated_data, crash_years, severity_types):
    """
    Transforms (year, severity, count) tuples into a list of rows:
    [(year, count1, count2, ...)] based on severity_types
      ['Fatal Crash', 'Minor Crash', 'Non-Injury Crash', 'Serious Crash'].
    """
    table = []

    for year in crash_years:
        row = [year]
        for severity in severity_types:
            count = 0
            for y, sev, c in accumulated_data:
                if y == year and sev == severity:
                    count = c
                    break
            row.append(count)
        table.append(tuple(row))

    return table

def print_report_all_year_severity(table_data, severity_types):
    """
    Print a report showing crash counts by year and severity type.
    """
    # print header
    header = ["Year"]
    for severity in severity_types:
        header.append(severity)
    header.append("Total")

    print(*header, sep="       ") 

    # print each data row
    for row in table_data:
        year = row[0]
        counts = row[1:]
        year_total = sum(counts)

        print(year, *counts, year_total, sep="              ")

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

    raw_data = read_csv_data(DATA_FILE, ["crashYear", "speedLimit", "crashSeverity", "temporarySpeedLimit"])
    clean_data = prepare_clean_data(raw_data) #clean_data: list of (crashYear, crashSeverity, effectiveSpeed)
    crash_years = extract_valid_values(clean_data, 0) 
    speed_limits = extract_valid_values(clean_data, 2) 
    severity_types = unique_values(clean_data, 1) #['Fatal Crash', 'Minor Crash', 'Non-Injury Crash', 'Serious Crash']


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
            print_crash_severity_report (year_of_interest, speed_of_interest, clean_data)

        elif option == 1:
            ###function to generate All Years Crash Severity Report
            accumulated_all_years = accumulate_year_severity(clean_data, crash_years, severity_types)
            table_data = transform_to_table(accumulated_all_years, crash_years, severity_types)
            print_report_all_year_severity(table_data, severity_types)


        elif option == 2:
            accumulated_all_years = accumulate_year_severity(clean_data, crash_years, severity_types)
            start_year, end_year, selected_types = get_plot_time_and_types(crash_years, severity_types)
            years, counts_lists = prepare_lists_for_plot(accumulated_all_years, selected_types, start_year, end_year)
            plot_trends_over_time (years, selected_types, counts_lists)

        elif option == 3:
            print("Bye")
            break

        print ("\n")

main ()