# Part Two Features
Below are a list of features that are to be completed for the second part of the assignment. Refer to the Project section of the course page for more detail on each feature.

Please fill in the section for each feature, replace all text below each heading.

## 1. Validate user input: Crash Severity Report
### Assumptions of valid speed limit
For the purpose of further analysing the relationship between 'speed limit' and 'crash severity', only records with speed limits that are valid multiples of 10 between 10 and 110 km/h were retained.
Based on my observation of data, speed values such as 2, 5, 6, 15, 51, and 61 occurred extremely rarely and are likely due to data entry errors or irregular reporting. Meanwhile, records with missing speed limit values (0.12% of total data) were also limited in amount. Therefore, I assume these records are noise and should be exclude from the program, as speed limit is a critical independent variable for the analysis and the proportion of such abnormal data is negligible.

### Setting valid years and speed limits
I plan to store valid years and speed limits as tuples.
A tuple is an immutable data structure, which means its values cannot be changed once defined. This helps prevent accidental modifications that could affect the program's functionality.
By using tuples, I can ensure that the valid values for years and speed limits remain fixed and consistent.
### Validating user input
When the user enters a year or speed, the program checks whether the input exists in the predefined tuple. If the input is valid, the program confirms it; otherwise, it displays a message showing the acceptable range of years.
Additionally, displaying the valid options before the user inputs their response can help them understand the acceptable values in advance.
### Reasons for this approach and possible improvements
Tuples are immutable, which prevents unintended changes to the stored values.
Since valid years and speed limits are fixed reference values, using tuples helps maintain data integrity and ensures the program functions correctly.
A more efficient approach would be to automatically extract distinct values from the dataset and sort them, to ensure the efficiency and accuracy of the program to handle future changes of dataset.
### Possible change in the future
This part might be changed after introduce Pandas

## 2. Use temporary speed limit if defined instead of normal seed limit
### Use of dictionaries
I plan to establish two dictionaries:
One dictionary stores the standard road speed limits, with the accident ID or serial number as the key and the normal speed limit as the value.
Another dictionary stores temporary speed limits, also using the same key while set temporary limit as the value.
The program will then use a loop (for i in the temporary speed limit dictionary) to check whether an accident ID exists in the temporary speed limit dictionary.
If a temporary speed limit is defined, the program will use the temporary speed limit.
Otherwise, it will use the standard road speed limit.

### Reason for this appraoch
Using two separate dictionaries allows the system to be adaptable.
If a temporary speed limit is added, it does not overwrite the original data, preserving the integrity of the normal speed limits.
If a temporary speed limit is unavailable, the program automatically defaults to the standard speed limit, ensuring there is always a valid value to use.

## 3. Warn the user if no records are found  
If the accident count for all severity categories is 0 given a valid year and speed limit, the program will now print a warning message that no records were found.
### Use accumulator and If loop
To implement this feature, I used an accumulator (total_count) to track the total number of accidents among all severity categories. At the same time, I created a results list to temporarily store each severity category and its count number.

If print the result witin the main body for loop, the function will iterates over each severity type. Therefore, I moved the output logic outside the for loop to ensure that the total count is only processed after all data has been finished. This method helped avioding repeated output during my earlier attempts.
The revised function allowed me to use a single if condition after the loop to check whether total_count is 0. If yes, the program prints a warning message. Otherwise, it iterates through the results list and prints each severity category and its count.
### Reason of this approach
Accumulator is suitable for counting the amounts when given condition is true. Meanwhile, I think this method requires only a few modification of existing function, which minimize the complexity and chance of error.

## 4. Add all years: Crash Severity Report
Replace me with an outline of:

- how you implemented this feature
- choices you made and why

## 5. Implement Crash Reports Over Time Graph
Replace me with an outline of:

- how you implemented this feature
- choices you made and why
