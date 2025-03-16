# Part Two Features
Below are a list of features that are to be completed for the second part of the assignment. Refer to the Project section of the course page for more detail on each feature.

Please fill in the section for each feature, replace all text below each heading.

## 1. Validate user input: Crash Severity Report

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
Replace me with an outline of:

- how you implemented this feature
- choices you made and why

## 4. Add all years: Crash Severity Report
Replace me with an outline of:

- how you implemented this feature
- choices you made and why

## 5. Implement Crash Reports Over Time Graph
Replace me with an outline of:

- how you implemented this feature
- choices you made and why
