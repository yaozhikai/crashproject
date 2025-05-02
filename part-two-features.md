# Part Two Features


## 1. Validate user input: Crash Severity Report
### Implementation Approach
I implemented a reusable function read_valid_int() to handle user input validation for both crash year and speed limit.
The function uses the following logic:
    It first calls extract_valid_values() to dynamically collect unique valid values from the cleaned dataset, storing them in a tuple.
    It then prints the valid range to the user before input is requested, helping the user understand acceptable options.
    When receiving input, the function checks if the value is a digit using str.isdigit(). If not, it displays a warning and re-prompts the user.
    If the input is a digit, it is converted to an integer and compared against the tuple of valid values. If valid, the function returns the value. If not, a second warning is shown with the available values, and the user is prompted again.
This process is implemented using a while loop with recursive calls to re-ask the user until valid input is entered.
### Design Choice
In my initial version, I used fixed tuples to store valid years and speed limits, but through tutorial discussion, I later realised this approach lacked flexibility. 
Therefore, I changed to dynamically extracting valid values from the dataset to make the program more adaptive. I also added logic to display valid options before prompting the user, which can help the user to reduce the chance of invalid input.

## 2. Use temporary speed limit if defined instead of normal speed limit
### Implementation Approach
I created a dedicated function get_effective_speed() that determines the effective speed limit for each crash record. This function uses if statement to prioritise the temporary speed limit.
    Firstly, it checks whether the temporarySpeedLimit exists (is not NaN) and whether it is a valid multiple of 10 using the modulus operator (% 10 == 0).
    If the temporary speed is valid, it is returned as the effective speed.
    If not, the function checks whether the regular speedLimit is valid using the same condition.
    If both values are missing or invalid, the function returns None.
This function is used inside a loop in prepare_clean_data(), which processes the raw dataset record by record using a for loop. Only records with a valid effective speed limit are appended to the cleaned data list as a tuple: (crashYear, crashSeverity, effectiveSpeed).
This logic is also based on my assumption that both temporary and regular speed limits must be valid multiples of 10. I made this decision after exploring the raw dataset and observing that almost all speed values were standard figures like 30, 50, 70, and 100. Rare values such as 2, 5, 6, or 51 appeared only a few times and were likely due to data entry errors. Based on this observation, I excluded these outliers 
### Design Choice
Originally, I repeated speed validation logic in multiple parts of the program, which made the code too complex to maintain. 
I decided to move this logic into one central function and apply it during the data preparation stage. This helped simplify all later features and ensured consistent handling of speed values across the program.

## 3. Warn the user if no records are found  
### Implementation Approach
In the crash severity report for a specific year and speed limit, I implemented logic to check whether any records exist under the selected conditions.
I used a variable total_count as an accumulator to keep track of the number of crashes across all severity types. This was done using a for loop that iterates through each severity type and counts how many crashes match both the given year and speed.
If total_count remains zero after the loop, the program prints a warning message to inform the user that no records were found for that combination of year and speed limit.
This feature works together with Feature 1. If the input year or speed limit is not found in the dataset at all (e.g. the user enters 2025), the read_valid_int() function from Feature 1 detects this early and prevents further processing. It also displays the valid range to guide the user.
### Design Choice
Since feature 1 already handles input validation, any invalid year or speed limit (e.g. 2025 or 115) is caught before the report function is triggered. This avoids unnecessary computation and provides an early warning to the user.
Building on that, I designed this feature to handle the case where the input year and speed limit are valid, but the crash count is zero. Instead of printing empty results for each severity type, I used an accumulator (total_count) to detect whether any records exist. This approach allowed me to provide a single, clear warning message if no data is found, which simplifies the output for better user experience.

## 4. Add all years: Crash Severity Report
### Implementation Approach
To generate a summary report across all years, I reused the cleaned data and created a function called accumulate_year_severity() to count crashes by year and severity type.
This function uses two nested for loops:
    The outer loop iterates over each valid crash year.
    The inner loop iterates over each severity type.
    For each (year, severity) pair, it counts how many matching records exist in the cleaned data and stores the result as a tuple (year, severity, count).
The resulting list of tuples is then passed to transform_to_table(), which set up a table structure for display. It generates a list of rows, where each row contains a year followed by counts for each severity type. Each row is stored as a tuple: (year, count1, count2, ..., countN).
This table is printed as a formatted summary, showing crash counts by year and severity classification.
### Design Choice
My design is to re-use the existing data structures and applied a two-step transformation: first accumulating counts, then converting the results into a table ready for print.
I also think this logic can be re-used in later plotting feature.

## 5. Implement Crash Reports Over Time Graph
### Implementation Approach
To implement the "Crash Reports Over Time Graph" feature, I designed a process in which users are prompted to select a start year, an end year, and at least one crash severity type. The program then displays a line chart showing crash counts over the selected time range, grouped by severity type.
This feature is realised by several modular functions: 
    get_plot_year_range() prompts and validates the start and end years. 
    get_plot_severity_types() allows users to select severity types using (y/n) input and ensures that at least one type is selected before proceeding. 
    prepare_lists_for_plot() uses the accumulated data to prepare lists of yearly crash counts for each selected severity type. 
    Finally, plot_trends_over_time() visualises the data using matplotlib, generating a line chart with labelled axes, legend, and grid lines.
The plotting logic reuse data computed by accumulate_year_severity(), which generates a list of tuples in the form (year, severity, count). By reusing this preprocessed data, the design improves performance and avoids redundant computations.
### Design Choice
To ensure clarity and improve maintainability of the program, I tried to modularised my design into smaller reusable components. The process of collecting and validating user input is handled separately from the plotting logic. 
User input is validated consistently through reusable functions such as read_valid_int() and get_plot_severity_types(), which reduces code duplication comparing to my initial design. 
Although I also considered including speed limit as another category in begin, I realised such additional category will complex the program and is not feasible with my current coding knowledge, so I chose to meet the minimum requirement of including year and severity.
I also used 'while True' to require user input at least one severity category to aviod error that no severity type is passed to the plotting function.

## 6. Design Reflection
At the beginning of the project, my approach focused on reading data and performing calculations directly within each reporting function. This led to repeated logic, low flexibility, and increasing complexity. Through testing and tutorial discussions, I eventually changed my strategy to a more structured and dynamic process: first preparing and validating the data, then building reporting or visualisation features based on that clean foundation.
I later realised that the features in the program should be handled in a centralised and reusable way, as all of them rely on processing crash data by year and severity. This idea led me to rewrite the overall program structure.
As I made progress and continued learning, I began to see that the design could be further improved by using better data structures, such as dictionaries, or by applying pandas for more efficient data cleansing and transformation. Although I do not yet have the skills to fully rewrite the project using these ideas, I believe it is a possible direction for future improvement.