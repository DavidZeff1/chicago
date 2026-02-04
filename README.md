````markdown
# Chicago Neighborhood Explorer 🏠

A comprehensive data-driven tool for people considering moving to Chicago. Explore neighborhood safety, school quality, and crime statistics across all Chicago communities.

## 🎯 Project Overview

This interactive dashboard provides statistical breakdowns of key factors that matter when choosing where to live:

- **Crime Rate**: Number of reported crimes per neighborhood
- **Education Quality**: Unified score composed of multiple weighted features including:
  - School safety and environment
  - Instruction quality and teacher ratings
  - College readiness and graduation rates
  - Parent involvement and student attendance

All data is sourced from the official [Chicago Data Portal](https://data.cityofchicago.org/), maintained by the City of Chicago.

## 🚀 How to Use

### Running Locally

streamlit run dashboard.py

### Live Demo

Access the deployed application: [Chicago Neighborhood Explorer](https://davidzeff1-chicago-dashboard-wxkmlm.streamlit.app/)

### Using the Dashboard

1. **Select a metric** (Safety, School Quality, Elementary Schools, High Schools, College Readiness)
2. **Explore the map** to see neighborhood comparisons
3. **View rankings** of top and bottom performing neighborhoods
4. **Drill down** by selecting specific neighborhoods and crime types for detailed insights

## 📁 Project Structure

```
chicago/
│
├── dashboard.py              # Entry point - run this file
│
└── dashboard/                # Main package folder
    ├── __init__.py          # Makes dashboard a Python package
    ├── components.py        # Streamlit UI components (maps, charts, graphs)
    ├── data_loader.py       # Data import and loading logic
    └── metrics.py           # Data processing and metric calculations
```

### File Descriptions

**`dashboard.py`**  
Application entry point. Orchestrates the UI and connects all components.

**`dashboard/components.py`**  
Defines all Streamlit visual components including interactive maps, bar charts, comparison graphs, and data tables. Handles data manipulation with pandas and plotly for visualization.

**`dashboard/data_loader.py`**  
Loads all necessary datasets:

- Crime data from CSV (`notebooks/data/raw/`)
- Education data from CSV (`notebooks/data/raw/`)
- Community boundaries via GeoJSON API (converted to dataframe)

**`dashboard/metrics.py`**  
Performs data aggregation, calculates composite scores, and prepares dataframes for UI rendering.

## 📊 Data Sources

- **Chicago Data Portal**: Crime statistics and community area boundaries
- **Chicago Public Schools**: School performance metrics
- All data is publicly available and regularly updated by the City of Chicago

## 🛠️ Technologies Used

- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations and maps
- **GeoPandas**: Geographic data processing

```

```
````
