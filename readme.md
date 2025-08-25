Perfect — thanks for pasting the full README draft.
Here’s a **revised English version** of your README, keeping all the structure you already wrote but improving clarity, formatting, and adding a **Data section** explaining how to manually download and place the CSV file.

---

# Crash Data Analysis

## Overview

This project analyzes road crash data in New Zealand and provides both a command-line interface and a Streamlit dashboard for data exploration.
The dataset includes numeric variables (e.g., victim headcount, geographic coordinates) and categorical variables (e.g., location, road conditions, weather, severity).
Some attributes such as speed limit can be treated as either numeric or categorical, depending on the analysis.

---

## Data

The crash dataset is published by **Waka Kotahi NZ Transport Agency (NZTA)**:
[Crash Analysis System (CAS) – Open Data Portal](https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc_0/explore)

**Important:**
The dataset is large (>200 MB) and is **not included in this repository**.
To run the program, you must manually download the CSV file and place it inside a `data/` folder in the project directory.

Example structure:

```
crashproject/
│
├─ data/
│   └─ CAS.csv
│
├─ main.py
├─ clean_data.py
├─ dashboard_app.py
├─ map_plotting.py
...
```

If the data file is missing, the program will raise an error and instruct you to download it.

---

## Initial Program Behavior

Running the program presents a menu where the user can select a function by entering option numbers (`0`, `1`, or `2`).
The program validates input, and out-of-range entries will be rejected with a reminder message.

Available options:

* **Option 0** – Prompts the user to enter a year and a speed limit, then displays a crash severity report. If the chosen values are not in the dataset, the report shows zero counts.
* **Option 1** – Intended to generate a graph report (currently not implemented). It simply notifies the user that the function is unavailable.
* **Option 2** – Exits the program with a farewell message.

---

## Dependencies

* **Data**: Waka Kotahi NZTA CAS dataset (CC BY 4.0)
* **Shapefile**: `regional-council-2025.shp` (Stats NZ)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)
* [Streamlit](https://docs.streamlit.io/)
* [GeoPandas](https://geopandas.org/)
* [adjustText](https://pypi.org/project/adjustText/)

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## How to Run

To execute the CLI program:

```bash
python3 main.py
```

### Streamlit Dashboard (Part A3)

You can launch the dashboard in two ways:

1. Run directly:

   ```bash
   streamlit run dashboard_app.py
   ```
2. Run the main program (`python3 main.py`) and choose **Option 3** from the menu.

**Scripts related to Part A3:**

* `main.py` (entry point)
* `clean_data.py` (data preprocessing)
* `dashboard_app.py` (dashboard implementation)
* `map_plotting.py` (map rendering)

---

## Future Development

Planned improvements:

* Incorporating additional data (e.g., weather)
* Implementing visualizations to better illustrate accident trends and influencing factors

### Example Features

* **Weather vs. Crash Severity**: Analyze how different weather conditions affect crash severity by grouping records and generating comparative bar charts.
* **Accident Trends Over Time**: Plot time series of crash severity categories to detect long-term patterns.

### Student-Led Features (Part A3)

The Streamlit dashboard introduces a user-friendly web interface with two main tabs:

#### Tab 1 – Interactive Filtering and Visual Reports

* Filters: crash severity, speed limits, weather conditions
* Outputs: bar charts and summary tables that update in real time
* Warnings if no data matches the filters

#### Tab 2 – Annual Crash Mapping by Region

* Sidebar control for year selection (2000–2024)
* Displays a map of crash counts by region plus a summary table
* Helps identify regional crash patterns

---

## Citations

* Waka Kotahi. *Crash Analysis System (CAS) data*. Retrieved Jan 13, 2025, from [https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc\_0/explore](https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc_0/explore)
* Stats NZ. (2025). *Regional council 2025* \[Data set]. [https://datafinder.stats.govt.nz/layer/120946-regional-council-2025/](https://datafinder.stats.govt.nz/layer/120946-regional-council-2025/)
* GeeksforGeeks. *A beginner’s guide to Streamlit*. [https://www.geeksforgeeks.org/a-beginners-guide-to-streamlit/](https://www.geeksforgeeks.org/a-beginners-guide-to-streamlit/)
* GeoPandas developers. *Introduction to GeoPandas*. [https://geopandas.org/en/stable/getting\_started/introduction.html](https://geopandas.org/en/stable/getting_started/introduction.html)
* adjustText contributors. *adjustText documentation*. [https://adjusttext.readthedocs.io/en/latest/](https://adjusttext.readthedocs.io/en/latest/)