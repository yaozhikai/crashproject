# Part Two Features
Below are a list of features that are to be completed for the second part of the assignment. Refer to the Project section of the course page for more detail on each feature.

Please fill in the section for each feature, replace all text below each heading.

## 1. Validate user input: Crash Severity Report
### Assumptions of valid speed limit
For the purpose of further analysing the relationship between 'speed limit' and 'crash severity', only records with speed limits that are valid multiples of 10 between 10 and 110 km/h were retained.
Based on my observation of data, speed values such as 2, 5, 6, 15, 51, and 61 occurred extremely rarely and are likely due to data entry errors or irregular reporting. Meanwhile, records with missing speed limit values (0.12% of total data) were also limited in amount. Therefore, I assume these records are noise and should be exclude from the program, as speed limit is a critical independent variable for the analysis and the proportion of such abnormal data is negligible.
### Setting valid years and speed limits
I implemented valid year and speed limit values as tuples.
Tuples were chosen because they are immutable, preventing unintended modification during program execution. This design ensures consistency in validation checks and eliminates the risk of accidental updates to reference values.
### Validating user input
When the user enters a year or speed, the program checks whether the input exists in the predefined tuple. If the input is valid, the program confirms it; otherwise, it displays a message showing the acceptable range of years.
Additionally, displaying the valid options before the user inputs their response can help them understand the acceptable values in advance.
### Reasons for this approach and possible improvements
Tuples are immutable, which prevents unintended changes to the stored values.
Since valid years and speed limits are fixed reference values, using tuples helps maintain data integrity and ensures the program functions correctly.
Given that the number of years and speed limit values in this analysis is limited, using predefined tuples is more resource-efficient than dynamically reading and computing distinct values from the dataset at runtime.
If additional years need to be supported in the future, it can be easily accommodated by modifying the range() used to define the crash_year tuple.
### Input Validation Logic
Since both year and speed limit are integers, I tried to combine the functions into one read_valid_int() function. The prompts will remind the user about input instruction to aviod wrong input.
When users are prompted to enter a crash year or speed limit, the function verifies whether the input value exists within the predefined tuple of valid options.
If the user provides a valid input, the value is accepted and used in the report. If the input is invalid , the program displays an message and prompts the user again.

## 2. Use temporary speed limit if defined instead of normal seed limit
### Implementation Approach
I prioritize of temporary speed limits within the print function.
For each crash entry, the program checks whether a temporary speed limit is defined by testing if the value is not NaN (temporary_speed == temporary_speed). This leverages the fact that in Python, NaN is not equal to itself, making it a simple and efficient way to detect missing values (Python Software Foundation, 2025).
If a valid temporary speed limit is present, it is used as the effective speed for that crash. Otherwise, the function uses the normal speed limit. If both values are missing (i.e., both are NaN), the record is skipped to ensure data quality in the analysis.
### Reason for This Approach
Initially, I planned using dictionaries to manage and compare normal and temporary speed limits by mapping each crash record to its respective values. However, during further development and learning, I realised that detecting NaN values directly in the loop—using the expression x == x is a better and straightforward approach.
Since the temporary speed limits are only occasionally defined, I think this method is efficient and simplifies code complexity.



## 3. Warn the user if no records are found  
If the accident count for all severity categories is 0 given a valid year and speed limit, the program will now print a warning message that no records were found.
### Use accumulator and If loop
To implement this feature, I used an accumulator (total_count) to track the total number of accidents among all severity categories. At the same time, I created a results list to temporarily store each severity category and its count number.
If print the result witin the main body for loop, the function will iterates over each severity type. Therefore, I moved the output logic outside the for loop to ensure that the total count is only processed after all data has been finished. This method helped avioding repeated output during my earlier attempts.
The revised function allowed me to use a single if condition after the loop to check whether total_count is 0. If yes, the program prints a warning message. Otherwise, it iterates through the results list and prints each severity category and its count.
### Reason of this approach
Accumulator is suitable for counting the amounts when given condition is true. Meanwhile, I think this method requires only a few modification of existing function, which minimize the complexity and chance of error.

## 4. Add all years: Crash Severity Report
### Implementation Approach
To implement the “Add all years” feature, I used the reusable read_valid_int() function to accept an empty string as a valid response.
When the user follows the prompt and presses Enter without inputting a particular year, the function returns a list containing all valid years from 2000 to 2024. This approach allows the program to generate a full summary across all years without requiring any additional menu options or user confirmation.
The same logic is applied when prompting the user to input a valid speed limit. By supporting both full-range year and speed limit selections, the program enables users to retrieve the total number of crashes across all years and all valid speed limits, grouped by severity level.
### Design Choice
I chose to use a reusable input function for both year and speed limit to reduce code duplication and support optional reporting. Allowing empty input as a trigger for selecting the full range simplifies both the user experience and the program structure.
During the debugging process, I discovered that the crash severity report function expects input in the form of lists rather than single integers. To ensure compatibility, I updated the read_valid_int() function: when a user selects a single valid year or speed limit, the value is appended to an empty list. This guarantees that the function always returns a list, allowing the downstream processing logic to handle the input consistently.

## 5. Implement Crash Reports Over Time Graph
Replace me with an outline of:

- how you implemented this feature
- choices you made and why

### Reference
Python Software Foundation. (2025). math — Mathematical functions. In Python 3.13.3 documentation. Retrieved April 22, 2025, from https://docs.python.org/3/library/math.html