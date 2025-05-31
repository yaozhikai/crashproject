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
- regional-council-2025.shp (Stat NZ)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Streamlit](https://docs.streamlit.io/)
- [GeoPandas](https://geopandas.org/)
- [adjustText](https://pypi.org/project/adjustText/)

## How to Run
To execute this program run following command from a terminal:

`python3 main.py`

### Part A3
For Part A3 (Streamlit dashboard), alternative execution methods are:
1. Directly launch it by running the following command in the terminal:
 `streamlit run dashboard_app.py`
2. Or, after executing `python3 main.py`, select Option 3 from the menu. 

### Python scripts related to part A3 are:
main.py (to run the main program)
clean_data.py
dashboard_app.py
map_plotting.py

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
The A3 project introduces an interactive dashboard based on streamlit, which is designed to enhance the exploration and visualization of crash data. The dashboard is user-friendly, providing clear insights into crash trends and regional distributions.

#### Feature Overview
The dashboard is implemented in dashboard_app.py, leveraging the Streamlit framework for web-based interactivity. It is structured into two key tabs.
Before rendering, the dashboard relies on a clean and preprocessed dataset prepared in clean_data.py via the load_and_clean() function. This ensures that all data used in the dashboard (including crash counts, weather conditions, and severity categories) is valid, consistently formatted, and free from errors. The cleaned dataset serves as the foundation for generating accurate crash reports and visualizations across both tabs.

##### Tab 1: Interactive Filtering and Visual Reports
Purpose: 
Enables users to dynamically filter crash data by selecting crash severity categories (e.g., Fatal, Serious, Minor, Non-injury), applicable speed limits (multiples of 10 km/h), and weather conditions.

Functionality:
- Sidebar filter controls allow multiple selections for severity, speed limit and weather.
- Real-time generation of visual reports (bar charts) and Crash count table summaries based on selected filters.
- Designed to reveal crash patterns under specific conditions and facilitate comparative analysis.

Code Reference:
Core logic is handled in dashboard_app.py, where:
  - get_weather_filter() and get_dashboard_filter() handle filter inputs.
  - calculate_count_table() generates the count table by speed and severity.
  - run_dashboard() combines filters, plots a stacked bar chart, and renders the report in Tab 1.

##### Tab 1 Example:
- Remove 'Non-injury Crash' from the Crash Severity Types filter in side bar
- View the generated bar chart and summary table reflecting the selected data filters.
- If no data matches the selected filters, a warning will notify the user.

##### Tab 2: Annual Crash Accident Mapping by Region
Purpose: 
Provides an intuitive, spatial visualization of crash incidents across regions for a selected year.

Functionality:
- Single year selection via a sidebar scroll bar (covers 2000–2024).
- Dynamic map showing crash counts for the selected year, and a crash count table summarising crash counts by region.
- Interactive maps aid in identifying regional accident patterns.

Code Reference:
- Map generation utilizes geopandas and matplotlib in map_plotting.py, implemented in dashboard through dashboard_app.py.

##### Tab 2 Example:
- Set year selection to 2023 through scroll bar above the map
- Observe the crash distribution map highlighting crash counts by region for that year.

## Citations

- Waka Kotahi. _Crash Analysis System (CAS) data_ [Review of  Crash Analysis System (CAS) data]. Retrieved January 13, 2025, from https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc_0/explore
- Stats NZ. (2025). Regional council 2025 [Data set]. https://datafinder.stats.govt.nz/layer/120946-regional-council-2025/
- GeeksforGeeks. (n.d.). A beginner’s guide to Streamlit. https://www.geeksforgeeks.org/a-beginners-guide-to-streamlit/
- GeoPandas developers. (n.d.). Introduction to GeoPandas. https://geopandas.org/en/stable/getting_started/introduction.html
- adjustText contributors. (n.d.). adjustText documentation. https://adjusttext.readthedocs.io/en/latest/