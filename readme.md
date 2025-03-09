# Crash Data Analysis
## Tasks
- [ ] Download the initial project files from the LMS
- [ ] Write your first commit adding these files in your repository
- [ ] Inspect the code in `main.py`
- Fill in missing sections of `readme.md`
  - [ ] Fill in *Initial Program Behaviour* section
  - [ ] Fill in the *Future Development* sections
- [ ] Commit the changes to `readme.md` and push the changes to your eng-git repository

## Initial Program Behavior
The CSV file contains records of car crash accidents. The data consists of numerical data, 
such as victim headcount and geographic coordinates, and categorical data, including location, 
road conditions, weather, severity, and other details of accidents. 
Some data like speed limit can be treated as either numerical or categorical, depending on the purpose of the data analysis.

By running the program, the user can select a function by entering the number 0,1 or 2 shown in the menu.
After the user inputs the option number, the program will validate the input. 
If the input is out of the pre-set range, the program will remind the user that it is an invalid input and prompt them to try again.The program can generating reports, creating graphical reports (not implemented yet), and exiting.

The functions are:
Option 0: If the user input 0, they need to follow the menu prompts to enter year and speed limit. 
The program will then display a crash severity report, showing the number of crashes categorized by severity that match the conditions.
If the input is outside the range of the data, the report will show zero for all crash severity categories.

Option 1: Name of the function suggests when user input 1, it will generate a graph report.
However, this function is not implemented yet and will return a message to notify the user.

Option 2: User input 0 to exit the program and print a message "bye".

## Dependencies
Fill in this section, list any libraries that this program requires to run.
- Data (Waka Kotahi) CC BY 4.0
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

## How to Run
To execute this program run following command from a terminal:

`python3 main.py`

## Future Development
In addition to the required features, I plan to add extra data (e.g., weatherA) from the given dataset and include visualizations to improve the project.
These developments will help users better understand accident trends and possible factors affecting accident severity.

### Basic Analysis Feature
#### Relationship Between Weather Conditions and Accident Severity
This analysis will check how different weather conditions affect the severity of car crashes.
The hypothesis is bad weather may cause more serious accidents due to reduced visibility and poor road conditions.
The method is to group accident records by weather condition and severity level and use Matplotlib to generate a bar chart to show how accident severity changes in different weather conditions.
#### Accident Trends Over Time
Matplotlib can be used to create a line graph to show trends in different accident severity over the years.
The graph can help users review and compare if there are any patterns in an intuitive approach.

### Student Lead Features


## Citations

- Waka Kotahi. _Crash Analysis System (CAS) data_ [Review of  Crash Analysis System (CAS) data]. Retrieved January 13, 2025, from https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc_0/explore