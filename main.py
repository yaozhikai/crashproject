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

def get_valid_values(filename, columns, target_col_index):
    """a generic function to read valid unique values in dataset,
    use this dynamic function to replace pre-defined year and speed tuples
    """
    data = read_csv_data(filename, columns) #read column in dataset
    valid_values = unique_values(data, target_col_index) #get unique value from the column
    valid_values.sort()
    return tuple(valid_values)

def filter_valid_speed(DATA_FILE):
    """assume valid speed limits are multiples of 10,
    filter unique speed values to return a tuple of leagal speed"""
    raw_speed_limits = get_valid_values(DATA_FILE, ["speedLimit"], 0) #get speed from csv file
    valid_speeds = []
    for value in raw_speed_limits:
        if value % 10 == 0: #filter legal values- assume it's multiple of 10
            valid_speeds.append(int(value))
    valid_speeds.sort()
    return tuple(valid_speeds)

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
            print (f'{value} must be between {min(valid_data)} and {max(valid_data)}') 
            return read_valid_int(prompt, valid_data, value)   
    else:
        print ('Input must be one integer.')
        return read_valid_int(prompt, valid_data, value)

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


def print_crash_severity_report(year_of_interest: int, speed_of_interest: int) -> None:
    """Prints a table outlining the number of crashes in a given year for a given speed limit"""
    data = read_csv_data(
        DATA_FILE, ["crashYear", "speedLimit", "crashSeverity" ,"temporarySpeedLimit"])
    severity_types = unique_values(data, 2)
    print("Crash Severity by Classification")
    print(f"Speed: {speed_of_interest}")
    print(f"Year: {year_of_interest}")
    print()
    results = [] #accumulate total and store results in a list of tuple (type, count)
    total_count = 0 #use this to accumulate all kinds of accidents
    
    for severity_type in severity_types:
        # for loop to go through each severity_type
        count = 0
        for year, speed_limit, crash_type, temporary_speed in data:
            effective_speed = get_effective_speed(speed_limit, temporary_speed)
            if effective_speed is None:
                continue  # skip invalid data

            if (year == year_of_interest) and (effective_speed == speed_of_interest) and (crash_type == severity_type):
                count += 1

        results.append((severity_type, count))
        total_count += count
        
    if total_count == 0: #example: year 2013/ speed 110
        print ('Warning: No records found in this category of year and speed limit.')
    else:
        for severity_type, count in results:
            print(f"{severity_type}: {count}")

def plot_crash_over_time(): 
    """plot a bar chart showing total crash amout for each year"""
    data = read_csv_data(DATA_FILE, ["crashYear"]) #read crashyear column

    ys = get_crash_each_year(data) #give crash each year to Y axes

    xs = crash_years

    axes = plt.axes()
    axes.bar(xs, ys)
    axes.grid(True)
    axes.set_xlabel("Year")
    axes.set_ylabel("Amount of Accidents")
    axes.set_title("Crash Over Time Graph", size = 15)
    plt.show()

def get_crash_each_year(data):
    """decomposition function to accumulate yearly crash data"""
    crash_each_year = []
    for crash_year in crash_years:
        count = 0
        for year in data:
            if year[0] == crash_year:
                count +=1
        crash_each_year.append(count)
    return crash_each_year
            
def main():
    """Small application that presents tables and graphs based on crash data"""

    global crash_years, speed_limits ### set crash year as global in the program
    crash_years = get_valid_values(DATA_FILE, ["crashYear"], 0)
    speed_limits = filter_valid_speed(DATA_FILE)

    menu_options = [
        "Crash Severity Report",
        "Crash Reports Over Time Graph",
        "Exit"
    ]
    option = menu_select(menu_options)
    if option == 0:
        """this is to read user input year"""
        year_of_interest = read_valid_int("Please enter crash year.", crash_years, "Year")
        #year_of_interest    = read_year()
        """this is to read user input speed limit"""
        speed_of_interest = read_valid_int("Please enter speed limit. Value should be multiple of 10", speed_limits, "Speed Limit")
        #speed_of_interest = read_speed_limit()
        """this calls the print function"""
        print_crash_severity_report (year_of_interest, speed_of_interest)
    elif option == 1:
        plot_crash_over_time()
    elif option == 2:
        print("Bye")

main ()