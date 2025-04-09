"""
Traffic Accident Analysis Tool

This program provides an interactive menu to generate text and visual reports 
for traffic accident statistics (by severity level, year, and speed limit) 
based on historical data from 2000 to 2025.

Features:
- Generate text reports summarizing accident counts by severity
- Plot graphical trends of accidents by year and speed limit
"""

import pandas as pd

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
CONDITION = "fine"

#glboal variable
crash_year = tuple(range(2000,2025))
speed_limit = tuple(range(10,110+1,10))




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

# verify if input is int, and if it is in the tuple
# cannot return all data if empty now.
def read_valid_int (prompt, valid_data, value='value'):
    """This is a generic function to read user input of integer value
    - If user press enter, return a list of all valid value for full summary
    - If user input a valid integer within tuple, return the integer
    - If input is invalid, prompt again."""
    print(prompt)
    print(f"{value} Valid range: {min(valid_data)} to {max(valid_data)}")
    print(f"Or press Enter to select all {value.lower()}s.")

    user_value = input(f'{value}: ')
    result = []

    if len(user_value) == 0: #default value, select all
        return list(valid_data)
    elif user_value.isdigit():
        user_int = int(user_value)
        if user_int in valid_data:
            result.append(user_int)
            return result
        else:
            print (f'{value} must be between {min(valid_data)} and {max(valid_data)}') 
            return read_valid_int(prompt, valid_data, value)   
    else:
        print ('Input must be an integer.')
        return read_valid_int(prompt, valid_data, value)

#validate the year input
def read_year():
    """verify if input is integer, and if it is in the range of year tuple"""
    print (f'Please input an integer between {min(crash_year)} and {max(crash_year)}')
    print (f'Or please left empty if a full summary of year is prefered')
    year = input("Year: ")
    if year == "":  # default value
        return list(crash_year)
    elif year.isdigit():
        year = int(year)
        if year in crash_year:
            return year
        else:
            print ("Year must be between 2000 and 2024")
            return read_year()
    else:
        print ("Year must be a integer")
        return read_year()
    pass

#validate the speed limit input
## next phase: can combine with read_year() function--- solved
## problem: not output of accident report--- solved
def read_speed_limit():
    """verify if input is integer, and if it is in the range of speed tuple"""
    print (f'Please input an integer between {min(speed_limit)} and {max(speed_limit)}')
    print (f'Or please left empty if a full summary of speed limit is prefered')
    speed = input("Speed Limit: ")
    if speed == "":  # default value
        return list(speed_limit)
    elif speed.isdigit():
        speed = int(speed)
        if speed in speed_limit:
            return speed
        else:    
            print("Speed limit must be between 0 and 110 step by 10")
            return read_speed_limit()
    else:
        print ("Speed limit must be a integer")
        return read_speed_limit()
    pass

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
    total_count = 0 #use this to accumulate all kinds of acc
    
    for severity_type in severity_types:
        count = 0

        for year, speed_limit, crash_type, temporary_speed in data:
            
            # Check if there's a temporary speed limit.
            # In Python, float('nan') != float('nan'), use this to detect NaN (missing values).
            # If temporary_speed is valid (not NaN), use it. Otherwise, fall back to speed_limit.
            # If both are NaN, skip the record based on my assumption.

            if temporary_speed == temporary_speed : #solution- nan cannot equal to nan, to ignore null cells
                effective_speed = int(temporary_speed)
            elif speed_limit == speed_limit:
                effective_speed = int(speed_limit)
            else:
                continue

            if (year in year_of_interest) and (effective_speed in speed_of_interest) and crash_type == severity_type:
                count += 1
        results.append((severity_type, count))
        total_count += count
        
    if total_count == 0:
        print ('Warning: No records found in this category of year and speed limit.')
    else:
        for severity_type, count in results:
            print(f"{severity_type}: {count}")
    
            
def main():
    """Small application that presents tables and graphs based on crash data"""
    menu_options = [
        "Crash Severity Report",
        "Crash Reports Over Time Graph",
        "Exit"
    ]
    option = menu_select(menu_options)
    if option == 0:
        """this is to read user input year"""
        year_of_interest = read_valid_int("Please enter crash year.", crash_year, "Year")
        #year_of_interest    = read_year()
        """this is to read user input speed limit"""
        speed_of_interest = read_valid_int("Please enter speed limit. Value should be multiple of 10", speed_limit, "Speed Limit")
        #speed_of_interest = read_speed_limit()
        """this calls the print function"""
        print_crash_severity_report (year_of_interest, speed_of_interest)
    elif option == 1:
        print("Not Implemented Yet")
    elif option == 2:
        print("Bye")


main()