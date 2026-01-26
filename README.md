````markdown
# 🏠 Chicago Neighborhood Explorer

An interactive dashboard to help people moving to Chicago find the right neighborhood based on crime rates, school quality, and other metrics.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![License](https://img.shields.io/badge/License-MIT-green)```markdown

# 🏠 Chicago Neighborhood Explorer

An interactive dashboard to help people moving to Chicago find the right neighborhood based on crime rates, school quality, and other metrics.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Data Flow](#data-flow)
  - [File-by-File Breakdown](#file-by-file-breakdown)
- [Metrics Explained](#metrics-explained)
- [Data Sources](#data-sources)
- [Adding New Metrics](#adding-new-metrics)
- [Contributing](#contributing)

---

## Overview

Choosing a neighborhood is one of the most important decisions when moving to a new city. This dashboard helps prospective Chicago residents make data-driven decisions by visualizing key metrics across Chicago's 77 community areas.

The dashboard answers questions like:

- Which neighborhoods are safest?
- Where are the best schools for my kids?
- Which areas have the highest college readiness rates?

---

## Features

- 🗺️ **Interactive Map**: Choropleth map of Chicago colored by selected metric
- 📊 **Multiple Metrics**: Safety, school quality, elementary schools, high schools, college readiness
- 🏆 **Rankings**: Top 5 and Bottom 5 neighborhoods for each metric
- 📝 **Explanations**: Detailed descriptions of what each metric means and how it's calculated
- ⚡ **Fast Loading**: Data is cached so the app loads quickly after first run

---

## Demo
````

┌─────────────────────────────────────────────────────────────────┐
│ 🏠 Chicago Neighborhood Explorer │
│ Find the right neighborhood for you │
├─────────────────────────────────────────────────────────────────┤
│ Select metric: [Elementary Schools ▼] │
├─────────────────────────────────────────────────────────────────┤
│ ℹ️ Elementary Schools: Quality score for elementary schools │
│ focusing on early childhood metrics like PK-2 literacy... │
│ │
│ 📊 Score out of ~73 based on: Safety (10), Environment (8)... │
├─────────────────────────────────────────────────────────────────┤
│ │
│ [ CHICAGO MAP ] │
│ (colored by metric) │
│ │
├─────────────────────────────────────────────────────────────────┤
│ 🏆 Top 5 │ ⚠️ Bottom 5 │
│ Best for ages 5-11... │ Weaker outcomes... │
│ ┌────────────────────────┐ │ ┌────────────────────────┐ │
│ │ 1. LINCOLN PARK 52.3 │ │ │ 1. WEST ENGLEWOOD 18.2 │ │
│ │ 2. NEAR NORTH 48.7 │ │ │ 2. AUSTIN 21.4 │ │
│ │ ... │ │ │ ... │ │
│ └────────────────────────┘ │ └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

````

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chicago-neighborhood-explorer.git
   cd chicago-neighborhood-explorer
````

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**

   ```bash
   streamlit run run_dashboard.py
   ```

5. **Open in browser**

   The app will automatically open at `http://localhost:8501`

---

## Usage

1. **Select a metric** from the dropdown menu
2. **Hover over neighborhoods** on the map to see their scores
3. **Review Top 5 and Bottom 5** rankings below the map
4. **Read the explanations** to understand what the scores mean

---

## Project Structure

```
chicago/
│
├── run_dashboard.py          # Entry point - run this file
│
├── dashboard/                # Main application package
│   ├── __init__.py          # Package exports
│   ├── config.py            # Settings, descriptions, file paths
│   ├── utils.py             # Helper functions
│   ├── data_loader.py       # Data loading functions
│   ├── metrics.py           # Metric calculations
│   └── components.py        # UI rendering functions
│
├── notebooks/               # Jupyter notebooks and data
│   ├── data/
│   │   └── raw/            # Raw CSV data files
│   ├── crime/              # Crime analysis notebooks
│   └── education/          # Education analysis notebooks
│
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Why This Structure?

| Benefit                    | Description                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Separation of Concerns** | Each file has one job: config stores settings, metrics does math, components renders UI      |
| **Easy to Navigate**       | Need to change a file path? Go to `config.py`. Need to fix a calculation? Go to `metrics.py` |
| **Reusable Code**          | Functions can be imported and used elsewhere                                                 |
| **Easier Testing**         | Each function can be tested independently                                                    |
| **Scalable**               | Adding new metrics only requires changes to 2 files                                          |

---

## How It Works

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: LOAD DATA
─────────────────
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Crimes.csv  │     │Education.csv│     │  GeoJSON    │
    │ (258k rows) │     │ (566 rows)  │     │(77 polygons)│
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │  load_all_data()│
                      │                 │
                      │ Returns dict:   │
                      │ - crimes: DF    │
                      │ - education: DF │
                      │ - geojson: dict │
                      │ - communities:  │
                      │   GeoDataFrame  │
                      └────────┬────────┘
                               │
                               ▼
Step 2: CALCULATE METRICS
─────────────────────────
                      ┌──────────────────────┐
                      │calculate_all_metrics()│
                      └──────────┬───────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │   Crime     │      │   School    │      │  College    │
    │   Metric    │      │   Quality   │      │  Readiness  │
    │             │      │             │      │             │
    │ Spatial join│      │ Weighted    │      │ Weighted    │
    │ + count     │      │ average     │      │ average     │
    │ + invert    │      │             │      │             │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Returns dict:         │
                    │                       │
                    │ 'Safety': DataFrame   │
                    │ 'School Quality': DF  │
                    │ 'Elementary': DF      │
                    │ 'High Schools': DF    │
                    │ 'College Ready': DF   │
                    │                       │
                    │ Each DF has columns:  │
                    │ [community, value]    │
                    └───────────┬───────────┘
                                │
                                ▼
Step 3: USER INTERACTION
────────────────────────
                    ┌───────────────────────┐
                    │  st.selectbox()       │
                    │                       │
                    │  User picks:          │
                    │  "Elementary Schools" │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Get data for that    │
                    │  metric:              │
                    │                       │
                    │  df = metrics[choice] │
                    │  info = METRIC_INFO[  │
                    │         choice]       │
                    └───────────┬───────────┘
                                │
                                ▼
Step 4: RENDER UI
─────────────────
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │render_metric│      │ render_map()│      │render_top_  │
    │   _info()   │      │             │      │  bottom()   │
    │             │      │             │      │             │
    │ Blue info   │      │ Choropleth  │      │ Top 5 and   │
    │ box with    │      │ map colored │      │ Bottom 5    │
    │ description │      │ by value    │      │ tables      │
    └─────────────┘      └─────────────┘      └─────────────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │   RENDERED WEBPAGE    │
                    │                       │
                    └───────────────────────┘
```

### File-by-File Breakdown

#### 1. `config.py` — Configuration & Text

**Purpose:** Store all settings and text in one place. No logic, just data.

```python
# Metric descriptions shown to users
METRIC_INFO = {
    'Safety (Low Crime)': {
        'description': '...',        # What this metric measures
        'score_explanation': '...',  # How the score is calculated
        'top_meaning': '...',        # What being in the top 5 means
        'bottom_meaning': '...'      # What being in the bottom 5 means
    },
    # ... more metrics
}

# Map display settings
MAP_CENTER = {'lat': 41.8781, 'lon': -87.6298}  # Chicago coordinates
MAP_ZOOM = 9
MAP_STYLE = 'open-street-map'
COLOR_SCALE = 'RdYlGn'  # Red (bad) → Yellow → Green (good)

# File paths
DATA_PATHS = {
    'crimes': './notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv',
    'education': './notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv',
    'geojson': 'https://data.cityofchicago.org/resource/igwz-8jzy.geojson'
}
```

**Why separate?**

- Change a file path? Edit one line in `config.py`
- Update a description? Edit one line in `config.py`
- No hunting through code to find settings

---

#### 2. `utils.py` — Helper Functions

**Purpose:** Small utility functions used across the codebase.

```python
def safe_numeric(series):
    """Convert a pandas series to numeric, handling percentages and errors."""
    # Input:  ['95%', '80%', 'N/A', '75%']
    # Output: [95.0, 80.0, NaN, 75.0]

    if series.dtype == 'object':
        # Remove '%' sign: '95%' → '95'
        series = series.str.rstrip('%').astype(float, errors='ignore')

    # Convert to numbers, invalid values become NaN
    return pd.to_numeric(series, errors='coerce')
```

**Example usage:**

```python
>>> safe_numeric(pd.Series(['95%', '80%', 'N/A']))
0    95.0
1    80.0
2     NaN
dtype: float64
```

---

#### 3. `data_loader.py` — Load Data

**Purpose:** Functions that read data from files and APIs.

```python
@st.cache_data  # ← This decorator caches the result
def load_crimes():
    """Load crime data from CSV."""
    return pd.read_csv(DATA_PATHS['crimes'])

@st.cache_data
def load_geojson():
    """Fetch Chicago community boundaries from API."""
    return requests.get(DATA_PATHS['geojson']).json()

def load_all_data():
    """Load all datasets and return as a dictionary."""
    geojson = load_geojson()
    return {
        'crimes': load_crimes(),
        'education': load_education(),
        'geojson': geojson,
        'communities': load_communities(geojson)
    }
```

**What does `@st.cache_data` do?**

```
First time load_crimes() is called:
├── Reads CSV file (takes ~2 seconds)
├── Stores result in cache
└── Returns DataFrame

Second time load_crimes() is called:
├── Finds result in cache
└── Returns cached DataFrame instantly
```

This makes the app much faster after the first load.

---

#### 4. `metrics.py` — Calculate Scores

**Purpose:** All the math happens here. Each function calculates one metric.

**Crime Metric Example:**

```python
def calculate_crime_metric(crimes_df, communities_gdf):
    """
    Calculate safety score for each community.

    Process:
    1. Take all crime locations (lat/lon points)
    2. Figure out which community each crime falls in
    3. Count crimes per community
    4. Invert so higher score = safer
    """

    # Step 1: Remove rows with missing coordinates
    crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Step 2: Convert lat/lon to geographic points
    geometry = [Point(lon, lat) for lon, lat in
                zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
    gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry)

    # Step 3: Spatial join - "which polygon contains this point?"
    #
    #         LINCOLN PARK polygon
    #        ┌─────────────────────┐
    #        │    • crime 1        │
    #        │         • crime 2   │  ← These 3 crimes are
    #        │  • crime 3          │    assigned to LINCOLN PARK
    #        └─────────────────────┘
    #
    gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf, predicate='within')

    # Step 4: Count crimes per community
    crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')

    # Result so far:
    # community        value
    # AUSTIN           5000   (high crime)
    # LINCOLN PARK      800   (low crime)

    # Step 5: Invert so higher = better (safer)
    crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']

    # Final result:
    # community        value
    # AUSTIN              0   (low score = unsafe)
    # LINCOLN PARK     4200   (high score = safe)

    return crime_counts
```

**School Quality Example:**

```python
def calculate_overall_school_quality(edu_df):
    """
    Calculate weighted school quality score.

    Formula (100 points max):
    - Safety Score:        15 points
    - Instruction Score:   15 points
    - Environment Score:   10 points
    - Low Misconduct:      10 points
    - Teachers Score:      10 points
    - Leaders Score:       10 points
    - Family Involvement:  10 points
    - Parent Engagement:   10 points
    - Attendance:          10 points
    """

    edu = edu_df.copy()

    # Calculate weighted score for each school
    edu['score'] = (
        safe_numeric(edu['Safety Score']) / 100 * 15 +
        safe_numeric(edu['Instruction Score']) / 100 * 15 +
        safe_numeric(edu['Environment Score']) / 100 * 10 +
        # ... more components
    )

    # Average all schools in each community
    result = edu.groupby('Community Area Name')['score'].mean().reset_index()

    # Example result:
    # community        value
    # LINCOLN PARK     78.5
    # AUSTIN           42.3

    return result
```

---

#### 5. `components.py` — UI Rendering

**Purpose:** Functions that create visual elements on the page.

```python
def render_metric_info(info, metric_name):
    """Display the metric description box."""
    st.info(f"**{metric_name}**: {info['description']}")
    st.caption(f"📊 *{info['score_explanation']}*")

    # Renders:
    # ┌─────────────────────────────────────────────────────┐
    # │ ℹ️ Elementary Schools: Quality score for elementary │
    # │    schools focusing on early childhood metrics...   │
    # ├─────────────────────────────────────────────────────┤
    # │ 📊 Score out of ~73 based on: Safety (10)...        │
    # └─────────────────────────────────────────────────────┘

def render_map(df, geojson):
    """Render the choropleth map."""
    fig = px.choropleth_mapbox(
        df,                                    # Data with community + value
        geojson=geojson,                       # Polygon shapes
        locations='community',                 # Column to match on
        featureidkey='properties.community',   # GeoJSON field to match
        color='value',                         # Column that determines color
        color_continuous_scale='RdYlGn'        # Red → Yellow → Green
    )
    st.plotly_chart(fig)

def render_top_bottom(df, info):
    """Render the Top 5 and Bottom 5 tables side by side."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 5")
        st.caption(info['top_meaning'])
        top5 = df.nlargest(5, 'value')
        st.dataframe(top5)

    with col2:
        st.subheader("⚠️ Bottom 5")
        st.caption(info['bottom_meaning'])
        bottom5 = df.nsmallest(5, 'value')
        st.dataframe(bottom5)
```

---

#### 6. `__init__.py` — Package Exports

**Purpose:** Makes `dashboard/` a Python package and defines what can be imported.

```python
from .data_loader import load_all_data
from .metrics import calculate_all_metrics
from .components import render_metric_info, render_map, render_top_bottom
from .config import METRIC_INFO
```

**Effect:**

```python
# Without __init__.py:
from dashboard.data_loader import load_all_data
from dashboard.metrics import calculate_all_metrics

# With __init__.py:
from dashboard import load_all_data, calculate_all_metrics
```

---

#### 7. `run_dashboard.py` — Entry Point

**Purpose:** The main file that Streamlit runs. Ties everything together.

```python
import streamlit as st
from dashboard import (
    load_all_data,
    calculate_all_metrics,
    render_metric_info,
    render_map,
    render_top_bottom,
    METRIC_INFO
)

# Configure the page
st.set_page_config(page_title="Chicago Neighborhood Explorer", layout="wide")
st.title("🏠 Chicago Neighborhood Explorer")

# Step 1: Load all data
data = load_all_data()

# Step 2: Calculate all metrics
metrics = calculate_all_metrics(
    data['crimes'],
    data['education'],
    data['communities']
)

# Step 3: User selects a metric
metric_choice = st.selectbox("Select metric:", list(metrics.keys()))

# Step 4: Get data for selected metric
df = metrics[metric_choice]
info = METRIC_INFO[metric_choice]

# Step 5: Render the UI
render_metric_info(info, metric_choice)
render_map(df, data['geojson'])
render_top_bottom(df, info)
```

---

## Metrics Explained

### Safety (Low Crime)

| Aspect               | Details                                                               |
| -------------------- | --------------------------------------------------------------------- |
| **What it measures** | Neighborhood safety based on reported crimes                          |
| **Data source**      | Chicago Police Department - Crimes from past year                     |
| **Calculation**      | Count crimes per community, then invert (fewer crimes = higher score) |
| **Score range**      | 0 to ~25,000 (higher = safer)                                         |

### School Quality (Overall)

| Aspect               | Details                                              |
| -------------------- | ---------------------------------------------------- |
| **What it measures** | Comprehensive school quality across all school types |
| **Data source**      | CPS Progress Report Cards (2011-2012)                |
| **Calculation**      | Weighted average of 9 factors (see below)            |
| **Score range**      | 0 to 100                                             |

**Score Components:**
| Factor | Weight |
|--------|--------|
| Safety Score | 15 |
| Instruction Score | 15 |
| Environment Score | 10 |
| Low Misconduct Rate | 10 |
| Teachers Score | 10 |
| Leaders Score | 10 |
| Family Involvement | 10 |
| Parent Engagement | 10 |
| Student Attendance | 10 |

### Elementary Schools

| Aspect               | Details                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| **What it measures** | Quality of elementary schools (grades K-5)                                                       |
| **Calculation**      | Safety + Environment + Instruction + Teachers + Family + PK-2 Literacy/Math + Gr3-5 Reading/Math |
| **Score range**      | 0 to ~73                                                                                         |

### High Schools

| Aspect               | Details                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------- |
| **What it measures** | Quality of high schools with college readiness focus                                          |
| **Calculation**      | Safety + Instruction + Graduation Rate + College Eligibility + College Enrollment + ACT Score |
| **Score range**      | 0 to ~50                                                                                      |

### College Readiness

| Aspect               | Details                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| **What it measures** | How well high schools prepare students for college                                                       |
| **Calculation**      | Graduation (20) + College Eligibility (25) + College Enrollment (25) + ACT (20) + Freshman on Track (10) |
| **Score range**      | 0 to 100                                                                                                 |

---

## Data Sources

| Dataset | Source               | Records  | Description                            |
| ------- | -------------------- | -------- | -------------------------------------- |
| Crimes  | Chicago Data Portal  | ~258,000 | All reported crimes from past year     |
| Schools | CPS Progress Reports | 566      | School performance metrics (2011-2012) |
| GeoJSON | Chicago Data Portal  | 77       | Community area boundaries              |

**Links:**

- [Chicago Data Portal](https://data.cityofchicago.org/)
- [CPS School Data](https://www.cps.edu/about/district-data/)

---

## Adding New Metrics

To add a new metric, you only need to edit 2 files:

### Step 1: Add calculation to `metrics.py`

```python
def calculate_my_new_metric(some_df):
    """Calculate my new metric."""
    # Your calculation here
    result = some_df.groupby('Community Area Name')['some_column'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result
```

Add it to `calculate_all_metrics()`:

```python
def calculate_all_metrics(...):
    return {
        'Safety (Low Crime)': calculate_crime_metric(...),
        # ... existing metrics
        'My New Metric': calculate_my_new_metric(...)  # ← Add here
    }
```

### Step 2: Add description to `config.py`

```python
METRIC_INFO = {
    # ... existing metrics
    'My New Metric': {
        'description': 'What this metric measures...',
        'score_explanation': 'How the score is calculated...',
        'top_meaning': 'What being in the top 5 means...',
        'bottom_meaning': 'What being in the bottom 5 means...'
    }
}
```

That's it! The new metric will automatically appear in the dropdown.

---

## Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add more metrics (housing prices, transit access, parks)
- [ ] Add time-based filtering (crime by year/month)
- [ ] Add neighborhood comparison feature```markdown

# 🏠 Chicago Neighborhood Explorer

An interactive dashboard to help people moving to Chicago find the right neighborhood based on crime rates, school quality, and other metrics.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Data Flow](#data-flow)
  - [File-by-File Breakdown](#file-by-file-breakdown)
- [Metrics Explained](#metrics-explained)
- [Data Sources](#data-sources)
- [Adding New Metrics](#adding-new-metrics)
- [Contributing](#contributing)

---

## Overview

Choosing a neighborhood is one of the most important decisions when moving to a new city. This dashboard helps prospective Chicago residents make data-driven decisions by visualizing key metrics across Chicago's 77 community areas.

The dashboard answers questions like:

- Which neighborhoods are safest?
- Where are the best schools for my kids?
- Which areas have the highest college readiness rates?

---

## Features

- 🗺️ **Interactive Map**: Choropleth map of Chicago colored by selected metric
- 📊 **Multiple Metrics**: Safety, school quality, elementary schools, high schools, college readiness
- 🏆 **Rankings**: Top 5 and Bottom 5 neighborhoods for each metric
- 📝 **Explanations**: Detailed descriptions of what each metric means and how it's calculated
- ⚡ **Fast Loading**: Data is cached so the app loads quickly after first run

---

## Demo

```
┌─────────────────────────────────────────────────────────────────┐
│  🏠 Chicago Neighborhood Explorer                               │
│  Find the right neighborhood for you                            │
├─────────────────────────────────────────────────────────────────┤
│  Select metric: [Elementary Schools ▼]                          │
├─────────────────────────────────────────────────────────────────┤
│  ℹ️ Elementary Schools: Quality score for elementary schools    │
│     focusing on early childhood metrics like PK-2 literacy...   │
│                                                                 │
│  📊 Score out of ~73 based on: Safety (10), Environment (8)...  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    [ CHICAGO MAP ]                              │
│                    (colored by metric)                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  🏆 Top 5                    │  ⚠️ Bottom 5                     │
│  Best for ages 5-11...       │  Weaker outcomes...              │
│  ┌────────────────────────┐  │  ┌────────────────────────┐      │
│  │ 1. LINCOLN PARK   52.3 │  │  │ 1. WEST ENGLEWOOD 18.2 │      │
│  │ 2. NEAR NORTH     48.7 │  │  │ 2. AUSTIN         21.4 │      │
│  │ ...                    │  │  │ ...                    │      │
│  └────────────────────────┘  │  └────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/chicago-neighborhood-explorer.git
   cd chicago-neighborhood-explorer
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**

   ```bash
   streamlit run run_dashboard.py
   ```

5. **Open in browser**

   The app will automatically open at `http://localhost:8501`

---

## Usage

1. **Select a metric** from the dropdown menu
2. **Hover over neighborhoods** on the map to see their scores
3. **Review Top 5 and Bottom 5** rankings below the map
4. **Read the explanations** to understand what the scores mean

---

## Project Structure

```
chicago/
│
├── run_dashboard.py          # Entry point - run this file
│
├── dashboard/                # Main application package
│   ├── __init__.py          # Package exports
│   ├── config.py            # Settings, descriptions, file paths
│   ├── utils.py             # Helper functions
│   ├── data_loader.py       # Data loading functions
│   ├── metrics.py           # Metric calculations
│   └── components.py        # UI rendering functions
│
├── notebooks/               # Jupyter notebooks and data
│   ├── data/
│   │   └── raw/            # Raw CSV data files
│   ├── crime/              # Crime analysis notebooks
│   └── education/          # Education analysis notebooks
│
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Why This Structure?

| Benefit                    | Description                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Separation of Concerns** | Each file has one job: config stores settings, metrics does math, components renders UI      |
| **Easy to Navigate**       | Need to change a file path? Go to `config.py`. Need to fix a calculation? Go to `metrics.py` |
| **Reusable Code**          | Functions can be imported and used elsewhere                                                 |
| **Easier Testing**         | Each function can be tested independently                                                    |
| **Scalable**               | Adding new metrics only requires changes to 2 files                                          |

---

## How It Works

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: LOAD DATA
─────────────────
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Crimes.csv  │     │Education.csv│     │  GeoJSON    │
    │ (258k rows) │     │ (566 rows)  │     │(77 polygons)│
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │  load_all_data()│
                      │                 │
                      │ Returns dict:   │
                      │ - crimes: DF    │
                      │ - education: DF │
                      │ - geojson: dict │
                      │ - communities:  │
                      │   GeoDataFrame  │
                      └────────┬────────┘
                               │
                               ▼
Step 2: CALCULATE METRICS
─────────────────────────
                      ┌──────────────────────┐
                      │calculate_all_metrics()│
                      └──────────┬───────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │   Crime     │      │   School    │      │  College    │
    │   Metric    │      │   Quality   │      │  Readiness  │
    │             │      │             │      │             │
    │ Spatial join│      │ Weighted    │      │ Weighted    │
    │ + count     │      │ average     │      │ average     │
    │ + invert    │      │             │      │             │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Returns dict:         │
                    │                       │
                    │ 'Safety': DataFrame   │
                    │ 'School Quality': DF  │
                    │ 'Elementary': DF      │
                    │ 'High Schools': DF    │
                    │ 'College Ready': DF   │
                    │                       │
                    │ Each DF has columns:  │
                    │ [community, value]    │
                    └───────────┬───────────┘
                                │
                                ▼
Step 3: USER INTERACTION
────────────────────────
                    ┌───────────────────────┐
                    │  st.selectbox()       │
                    │                       │
                    │  User picks:          │
                    │  "Elementary Schools" │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Get data for that    │
                    │  metric:              │
                    │                       │
                    │  df = metrics[choice] │
                    │  info = METRIC_INFO[  │
                    │         choice]       │
                    └───────────┬───────────┘
                                │
                                ▼
Step 4: RENDER UI
─────────────────
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │render_metric│      │ render_map()│      │render_top_  │
    │   _info()   │      │             │      │  bottom()   │
    │             │      │             │      │             │
    │ Blue info   │      │ Choropleth  │      │ Top 5 and   │
    │ box with    │      │ map colored │      │ Bottom 5    │
    │ description │      │ by value    │      │ tables      │
    └─────────────┘      └─────────────┘      └─────────────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │   RENDERED WEBPAGE    │
                    │                       │
                    └───────────────────────┘
```

### File-by-File Breakdown

#### 1. `config.py` — Configuration & Text

**Purpose:** Store all settings and text in one place. No logic, just data.

```python
# Metric descriptions shown to users
METRIC_INFO = {
    'Safety (Low Crime)': {
        'description': '...',        # What this metric measures
        'score_explanation': '...',  # How the score is calculated
        'top_meaning': '...',        # What being in the top 5 means
        'bottom_meaning': '...'      # What being in the bottom 5 means
    },
    # ... more metrics
}

# Map display settings
MAP_CENTER = {'lat': 41.8781, 'lon': -87.6298}  # Chicago coordinates
MAP_ZOOM = 9
MAP_STYLE = 'open-street-map'
COLOR_SCALE = 'RdYlGn'  # Red (bad) → Yellow → Green (good)

# File paths
DATA_PATHS = {
    'crimes': './notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv',
    'education': './notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv',
    'geojson': 'https://data.cityofchicago.org/resource/igwz-8jzy.geojson'
}
```

**Why separate?**

- Change a file path? Edit one line in `config.py`
- Update a description? Edit one line in `config.py`
- No hunting through code to find settings

---

#### 2. `utils.py` — Helper Functions

**Purpose:** Small utility functions used across the codebase.

```python
def safe_numeric(series):
    """Convert a pandas series to numeric, handling percentages and errors."""
    # Input:  ['95%', '80%', 'N/A', '75%']
    # Output: [95.0, 80.0, NaN, 75.0]

    if series.dtype == 'object':
        # Remove '%' sign: '95%' → '95'
        series = series.str.rstrip('%').astype(float, errors='ignore')

    # Convert to numbers, invalid values become NaN
    return pd.to_numeric(series, errors='coerce')
```

**Example usage:**

```python
>>> safe_numeric(pd.Series(['95%', '80%', 'N/A']))
0    95.0
1    80.0
2     NaN
dtype: float64
```

---

#### 3. `data_loader.py` — Load Data

**Purpose:** Functions that read data from files and APIs.

```python
@st.cache_data  # ← This decorator caches the result
def load_crimes():
    """Load crime data from CSV."""
    return pd.read_csv(DATA_PATHS['crimes'])

@st.cache_data
def load_geojson():
    """Fetch Chicago community boundaries from API."""
    return requests.get(DATA_PATHS['geojson']).json()

def load_all_data():
    """Load all datasets and return as a dictionary."""
    geojson = load_geojson()
    return {
        'crimes': load_crimes(),
        'education': load_education(),
        'geojson': geojson,
        'communities': load_communities(geojson)
    }
```

**What does `@st.cache_data` do?**

```
First time load_crimes() is called:
├── Reads CSV file (takes ~2 seconds)
├── Stores result in cache
└── Returns DataFrame

Second time load_crimes() is called:
├── Finds result in cache
└── Returns cached DataFrame instantly
```

This makes the app much faster after the first load.

---

#### 4. `metrics.py` — Calculate Scores

**Purpose:** All the math happens here. Each function calculates one metric.

**Crime Metric Example:**

```python
def calculate_crime_metric(crimes_df, communities_gdf):
    """
    Calculate safety score for each community.

    Process:
    1. Take all crime locations (lat/lon points)
    2. Figure out which community each crime falls in
    3. Count crimes per community
    4. Invert so higher score = safer
    """

    # Step 1: Remove rows with missing coordinates
    crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Step 2: Convert lat/lon to geographic points
    geometry = [Point(lon, lat) for lon, lat in
                zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
    gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry)

    # Step 3: Spatial join - "which polygon contains this point?"
    #
    #         LINCOLN PARK polygon
    #        ┌─────────────────────┐
    #        │    • crime 1        │
    #        │         • crime 2   │  ← These 3 crimes are
    #        │  • crime 3          │    assigned to LINCOLN PARK
    #        └─────────────────────┘
    #
    gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf, predicate='within')

    # Step 4: Count crimes per community
    crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')

    # Result so far:
    # community        value
    # AUSTIN           5000   (high crime)
    # LINCOLN PARK      800   (low crime)

    # Step 5: Invert so higher = better (safer)
    crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']

    # Final result:
    # community        value
    # AUSTIN              0   (low score = unsafe)
    # LINCOLN PARK     4200   (high score = safe)

    return crime_counts
```

**School Quality Example:**

```python
def calculate_overall_school_quality(edu_df):
    """
    Calculate weighted school quality score.

    Formula (100 points max):
    - Safety Score:        15 points
    - Instruction Score:   15 points
    - Environment Score:   10 points
    - Low Misconduct:      10 points
    - Teachers Score:      10 points
    - Leaders Score:       10 points
    - Family Involvement:  10 points
    - Parent Engagement:   10 points
    - Attendance:          10 points
    """

    edu = edu_df.copy()

    # Calculate weighted score for each school
    edu['score'] = (
        safe_numeric(edu['Safety Score']) / 100 * 15 +
        safe_numeric(edu['Instruction Score']) / 100 * 15 +
        safe_numeric(edu['Environment Score']) / 100 * 10 +
        # ... more components
    )

    # Average all schools in each community
    result = edu.groupby('Community Area Name')['score'].mean().reset_index()

    # Example result:
    # community        value
    # LINCOLN PARK     78.5
    # AUSTIN           42.3

    return result
```

---

#### 5. `components.py` — UI Rendering

**Purpose:** Functions that create visual elements on the page.

```python
def render_metric_info(info, metric_name):
    """Display the metric description box."""
    st.info(f"**{metric_name}**: {info['description']}")
    st.caption(f"📊 *{info['score_explanation']}*")

    # Renders:
    # ┌─────────────────────────────────────────────────────┐
    # │ ℹ️ Elementary Schools: Quality score for elementary │
    # │    schools focusing on early childhood metrics...   │
    # ├─────────────────────────────────────────────────────┤
    # │ 📊 Score out of ~73 based on: Safety (10)...        │
    # └─────────────────────────────────────────────────────┘

def render_map(df, geojson):
    """Render the choropleth map."""
    fig = px.choropleth_mapbox(
        df,                                    # Data with community + value
        geojson=geojson,                       # Polygon shapes
        locations='community',                 # Column to match on
        featureidkey='properties.community',   # GeoJSON field to match
        color='value',                         # Column that determines color
        color_continuous_scale='RdYlGn'        # Red → Yellow → Green
    )
    st.plotly_chart(fig)

def render_top_bottom(df, info):
    """Render the Top 5 and Bottom 5 tables side by side."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 5")
        st.caption(info['top_meaning'])
        top5 = df.nlargest(5, 'value')
        st.dataframe(top5)

    with col2:
        st.subheader("⚠️ Bottom 5")
        st.caption(info['bottom_meaning'])
        bottom5 = df.nsmallest(5, 'value')
        st.dataframe(bottom5)
```

---

#### 6. `__init__.py` — Package Exports

**Purpose:** Makes `dashboard/` a Python package and defines what can be imported.

```python
from .data_loader import load_all_data
from .metrics import calculate_all_metrics
from .components import render_metric_info, render_map, render_top_bottom
from .config import METRIC_INFO
```

**Effect:**

```python
# Without __init__.py:
from dashboard.data_loader import load_all_data
from dashboard.metrics import calculate_all_metrics

# With __init__.py:
from dashboard import load_all_data, calculate_all_metrics
```

---

#### 7. `run_dashboard.py` — Entry Point

**Purpose:** The main file that Streamlit runs. Ties everything together.

```python
import streamlit as st
from dashboard import (
    load_all_data,
    calculate_all_metrics,
    render_metric_info,
    render_map,
    render_top_bottom,
    METRIC_INFO
)

# Configure the page
st.set_page_config(page_title="Chicago Neighborhood Explorer", layout="wide")
st.title("🏠 Chicago Neighborhood Explorer")

# Step 1: Load all data
data = load_all_data()

# Step 2: Calculate all metrics
metrics = calculate_all_metrics(
    data['crimes'],
    data['education'],
    data['communities']
)

# Step 3: User selects a metric
metric_choice = st.selectbox("Select metric:", list(metrics.keys()))

# Step 4: Get data for selected metric
df = metrics[metric_choice]
info = METRIC_INFO[metric_choice]

# Step 5: Render the UI
render_metric_info(info, metric_choice)
render_map(df, data['geojson'])
render_top_bottom(df, info)
```

---

## Metrics Explained

### Safety (Low Crime)

| Aspect               | Details                                                               |
| -------------------- | --------------------------------------------------------------------- |
| **What it measures** | Neighborhood safety based on reported crimes                          |
| **Data source**      | Chicago Police Department - Crimes from past year                     |
| **Calculation**      | Count crimes per community, then invert (fewer crimes = higher score) |
| **Score range**      | 0 to ~25,000 (higher = safer)                                         |

### School Quality (Overall)

| Aspect               | Details                                              |
| -------------------- | ---------------------------------------------------- |
| **What it measures** | Comprehensive school quality across all school types |
| **Data source**      | CPS Progress Report Cards (2011-2012)                |
| **Calculation**      | Weighted average of 9 factors (see below)            |
| **Score range**      | 0 to 100                                             |

**Score Components:**
| Factor | Weight |
|--------|--------|
| Safety Score | 15 |
| Instruction Score | 15 |
| Environment Score | 10 |
| Low Misconduct Rate | 10 |
| Teachers Score | 10 |
| Leaders Score | 10 |
| Family Involvement | 10 |
| Parent Engagement | 10 |
| Student Attendance | 10 |

### Elementary Schools

| Aspect               | Details                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| **What it measures** | Quality of elementary schools (grades K-5)                                                       |
| **Calculation**      | Safety + Environment + Instruction + Teachers + Family + PK-2 Literacy/Math + Gr3-5 Reading/Math |
| **Score range**      | 0 to ~73                                                                                         |

### High Schools

| Aspect               | Details                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------- |
| **What it measures** | Quality of high schools with college readiness focus                                          |
| **Calculation**      | Safety + Instruction + Graduation Rate + College Eligibility + College Enrollment + ACT Score |
| **Score range**      | 0 to ~50                                                                                      |

### College Readiness

| Aspect               | Details                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| **What it measures** | How well high schools prepare students for college                                                       |
| **Calculation**      | Graduation (20) + College Eligibility (25) + College Enrollment (25) + ACT (20) + Freshman on Track (10) |
| **Score range**      | 0 to 100                                                                                                 |

---

## Data Sources

| Dataset | Source               | Records  | Description                            |
| ------- | -------------------- | -------- | -------------------------------------- |
| Crimes  | Chicago Data Portal  | ~258,000 | All reported crimes from past year     |
| Schools | CPS Progress Reports | 566      | School performance metrics (2011-2012) |
| GeoJSON | Chicago Data Portal  | 77       | Community area boundaries              |

**Links:**

- [Chicago Data Portal](https://data.cityofchicago.org/)
- [CPS School Data](https://www.cps.edu/about/district-data/)

---

## Adding New Metrics

To add a new metric, you only need to edit 2 files:

### Step 1: Add calculation to `metrics.py`

```python
def calculate_my_new_metric(some_df):
    """Calculate my new metric."""
    # Your calculation here
    result = some_df.groupby('Community Area Name')['some_column'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result
```

Add it to `calculate_all_metrics()`:

```python
def calculate_all_metrics(...):
    return {
        'Safety (Low Crime)': calculate_crime_metric(...),
        # ... existing metrics
        'My New Metric': calculate_my_new_metric(...)  # ← Add here
    }
```

### Step 2: Add description to `config.py`

```python
METRIC_INFO = {
    # ... existing metrics
    'My New Metric': {
        'description': 'What this metric measures...',
        'score_explanation': 'How the score is calculated...',
        'top_meaning': 'What being in the top 5 means...',
        'bottom_meaning': 'What being in the bottom 5 means...'
    }
}
```

That's it! The new metric will automatically appear in the dropdown.

---

## Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add more metrics (housing prices, transit access, parks)
- [ ] Add time-based filtering (crime by year/month)
- [ ] Add neighborhood comparison feature
- [ ] Improve mobile responsiveness
- [ ] Add data export functionality

---

## License

MIT License - feel free to use this project for any purpose.

---

## Acknowledgments

- Data provided by the [City of Chicago Data Portal](https://data.cityofchicago.org/)
- Built with [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/), and [GeoPandas](https://geopandas.org/)

```
- [ ] Improve mobile responsiveness
- [ ] Add data export functionality

---

## License

MIT License - feel free to use this project for any purpose.

---

## Acknowledgments

- Data provided by the [City of Chicago Data Portal](https://data.cityofchicago.org/)
- Built with [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/), and [GeoPandas](https://geopandas.org/)

```

---

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Data Flow](#data-flow)
  - [File-by-File Breakdown](#file-by-file-breakdown)
- [Metrics Explained](#metrics-explained)
- [Data Sources](#data-sources)
- [Adding New Metrics](#adding-new-metrics)
- [Contributing](#contributing)

---

## Overview

Choosing a neighborhood is one of the most important decisions when moving to a new city. This dashboard helps prospective Chicago residents make data-driven decisions by visualizing key metrics across Chicago's 77 community areas.

The dashboard answers questions like:

- Which neighborhoods are safest?
- Where are the best schools for my kids?
- Which areas have the highest college readiness rates?

---

## Features

- 🗺️ **Interactive Map**: Choropleth map of Chicago colored by selected metric
- 📊 **Multiple Metrics**: Safety, school quality, elementary schools, high schools, college readiness
- 🏆 **Rankings**: Top 5 and Bottom 5 neighborhoods for each metric
- 📝 **Explanations**: Detailed descriptions of what each metric means and how it's calculated
- ⚡ **Fast Loading**: Data is cached so the app loads quickly after first run

---

## Demo

```

┌─────────────────────────────────────────────────────────────────┐
│ 🏠 Chicago Neighborhood Explorer │
│ Find the right neighborhood for you │
├─────────────────────────────────────────────────────────────────┤
│ Select metric: [Elementary Schools ▼] │
├─────────────────────────────────────────────────────────────────┤
│ ℹ️ Elementary Schools: Quality score for elementary schools │
│ focusing on early childhood metrics like PK-2 literacy... │
│ │
│ 📊 Score out of ~73 based on: Safety (10), Environment (8)... │
├─────────────────────────────────────────────────────────────────┤
│ │
│ [ CHICAGO MAP ] │
│ (colored by metric) │
│ │
├─────────────────────────────────────────────────────────────────┤
│ 🏆 Top 5 │ ⚠️ Bottom 5 │
│ Best for ages 5-11... │ Weaker outcomes... │
│ ┌────────────────────────┐ │ ┌────────────────────────┐ │
│ │ 1. LINCOLN PARK 52.3 │ │ │ 1. WEST ENGLEWOOD 18.2 │ │
│ │ 2. NEAR NORTH 48.7 │ │ │ 2. AUSTIN 21.4 │ │
│ │ ... │ │ │ ... │ │
│ └────────────────────────┘ │ └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chicago-neighborhood-explorer.git
   cd chicago-neighborhood-explorer
   ```

````

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**

   ```bash
   streamlit run run_dashboard.py
   ```

5. **Open in browser**

   The app will automatically open at `http://localhost:8501`

---

## Usage

1. **Select a metric** from the dropdown menu
2. **Hover over neighborhoods** on the map to see their scores
3. **Review Top 5 and Bottom 5** rankings below the map
4. **Read the explanations** to understand what the scores mean

---

## Project Structure

```
chicago/
│
├── run_dashboard.py          # Entry point - run this file
│
├── dashboard/                # Main application package
│   ├── __init__.py          # Package exports
│   ├── config.py            # Settings, descriptions, file paths
│   ├── utils.py             # Helper functions
│   ├── data_loader.py       # Data loading functions
│   ├── metrics.py           # Metric calculations
│   └── components.py        # UI rendering functions
│
├── notebooks/               # Jupyter notebooks and data
│   ├── data/
│   │   └── raw/            # Raw CSV data files
│   ├── crime/              # Crime analysis notebooks
│   └── education/          # Education analysis notebooks
│
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Why This Structure?

| Benefit                    | Description                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Separation of Concerns** | Each file has one job: config stores settings, metrics does math, components renders UI      |
| **Easy to Navigate**       | Need to change a file path? Go to `config.py`. Need to fix a calculation? Go to `metrics.py` |
| **Reusable Code**          | Functions can be imported and used elsewhere                                                 |
| **Easier Testing**         | Each function can be tested independently                                                    |
| **Scalable**               | Adding new metrics only requires changes to 2 files                                          |

---

## How It Works

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: LOAD DATA
─────────────────
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ Crimes.csv  │     │Education.csv│     │  GeoJSON    │
    │ (258k rows) │     │ (566 rows)  │     │(77 polygons)│
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │  load_all_data()│
                      │                 │
                      │ Returns dict:   │
                      │ - crimes: DF    │
                      │ - education: DF │
                      │ - geojson: dict │
                      │ - communities:  │
                      │   GeoDataFrame  │
                      └────────┬────────┘
                               │
                               ▼
Step 2: CALCULATE METRICS
─────────────────────────
                      ┌──────────────────────┐
                      │calculate_all_metrics()│
                      └──────────┬───────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │   Crime     │      │   School    │      │  College    │
    │   Metric    │      │   Quality   │      │  Readiness  │
    │             │      │             │      │             │
    │ Spatial join│      │ Weighted    │      │ Weighted    │
    │ + count     │      │ average     │      │ average     │
    │ + invert    │      │             │      │             │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Returns dict:         │
                    │                       │
                    │ 'Safety': DataFrame   │
                    │ 'School Quality': DF  │
                    │ 'Elementary': DF      │
                    │ 'High Schools': DF    │
                    │ 'College Ready': DF   │
                    │                       │
                    │ Each DF has columns:  │
                    │ [community, value]    │
                    └───────────┬───────────┘
                                │
                                ▼
Step 3: USER INTERACTION
────────────────────────
                    ┌───────────────────────┐
                    │  st.selectbox()       │
                    │                       │
                    │  User picks:          │
                    │  "Elementary Schools" │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Get data for that    │
                    │  metric:              │
                    │                       │
                    │  df = metrics[choice] │
                    │  info = METRIC_INFO[  │
                    │         choice]       │
                    └───────────┬───────────┘
                                │
                                ▼
Step 4: RENDER UI
─────────────────
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │render_metric│      │ render_map()│      │render_top_  │
    │   _info()   │      │             │      │  bottom()   │
    │             │      │             │      │             │
    │ Blue info   │      │ Choropleth  │      │ Top 5 and   │
    │ box with    │      │ map colored │      │ Bottom 5    │
    │ description │      │ by value    │      │ tables      │
    └─────────────┘      └─────────────┘      └─────────────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │   RENDERED WEBPAGE    │
                    │                       │
                    └───────────────────────┘
```

### File-by-File Breakdown

#### 1. `config.py` — Configuration & Text

**Purpose:** Store all settings and text in one place. No logic, just data.

```python
# Metric descriptions shown to users
METRIC_INFO = {
    'Safety (Low Crime)': {
        'description': '...',        # What this metric measures
        'score_explanation': '...',  # How the score is calculated
        'top_meaning': '...',        # What being in the top 5 means
        'bottom_meaning': '...'      # What being in the bottom 5 means
    },
    # ... more metrics
}

# Map display settings
MAP_CENTER = {'lat': 41.8781, 'lon': -87.6298}  # Chicago coordinates
MAP_ZOOM = 9
MAP_STYLE = 'open-street-map'
COLOR_SCALE = 'RdYlGn'  # Red (bad) → Yellow → Green (good)

# File paths
DATA_PATHS = {
    'crimes': './notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv',
    'education': './notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv',
    'geojson': 'https://data.cityofchicago.org/resource/igwz-8jzy.geojson'
}
```

**Why separate?**

- Change a file path? Edit one line in `config.py`
- Update a description? Edit one line in `config.py`
- No hunting through code to find settings

---

#### 2. `utils.py` — Helper Functions

**Purpose:** Small utility functions used across the codebase.

```python
def safe_numeric(series):
    """Convert a pandas series to numeric, handling percentages and errors."""
    # Input:  ['95%', '80%', 'N/A', '75%']
    # Output: [95.0, 80.0, NaN, 75.0]

    if series.dtype == 'object':
        # Remove '%' sign: '95%' → '95'
        series = series.str.rstrip('%').astype(float, errors='ignore')

    # Convert to numbers, invalid values become NaN
    return pd.to_numeric(series, errors='coerce')
```

**Example usage:**

```python
>>> safe_numeric(pd.Series(['95%', '80%', 'N/A']))
0    95.0
1    80.0
2     NaN
dtype: float64
```

---

#### 3. `data_loader.py` — Load Data

**Purpose:** Functions that read data from files and APIs.

```python
@st.cache_data  # ← This decorator caches the result
def load_crimes():
    """Load crime data from CSV."""
    return pd.read_csv(DATA_PATHS['crimes'])

@st.cache_data
def load_geojson():
    """Fetch Chicago community boundaries from API."""
    return requests.get(DATA_PATHS['geojson']).json()

def load_all_data():
    """Load all datasets and return as a dictionary."""
    geojson = load_geojson()
    return {
        'crimes': load_crimes(),
        'education': load_education(),
        'geojson': geojson,
        'communities': load_communities(geojson)
    }
```

**What does `@st.cache_data` do?**

```
First time load_crimes() is called:
├── Reads CSV file (takes ~2 seconds)
├── Stores result in cache
└── Returns DataFrame

Second time load_crimes() is called:
├── Finds result in cache
└── Returns cached DataFrame instantly
```

This makes the app much faster after the first load.

---

#### 4. `metrics.py` — Calculate Scores

**Purpose:** All the math happens here. Each function calculates one metric.

**Crime Metric Example:**

```python
def calculate_crime_metric(crimes_df, communities_gdf):
    """
    Calculate safety score for each community.

    Process:
    1. Take all crime locations (lat/lon points)
    2. Figure out which community each crime falls in
    3. Count crimes per community
    4. Invert so higher score = safer
    """

    # Step 1: Remove rows with missing coordinates
    crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Step 2: Convert lat/lon to geographic points
    geometry = [Point(lon, lat) for lon, lat in
                zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
    gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry)

    # Step 3: Spatial join - "which polygon contains this point?"
    #
    #         LINCOLN PARK polygon
    #        ┌─────────────────────┐
    #        │    • crime 1        │
    #        │         • crime 2   │  ← These 3 crimes are
    #        │  • crime 3          │    assigned to LINCOLN PARK
    #        └─────────────────────┘
    #
    gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf, predicate='within')

    # Step 4: Count crimes per community
    crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')

    # Result so far:
    # community        value
    # AUSTIN           5000   (high crime)
    # LINCOLN PARK      800   (low crime)

    # Step 5: Invert so higher = better (safer)
    crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']

    # Final result:
    # community        value
    # AUSTIN              0   (low score = unsafe)
    # LINCOLN PARK     4200   (high score = safe)

    return crime_counts
```

**School Quality Example:**

```python
def calculate_overall_school_quality(edu_df):
    """
    Calculate weighted school quality score.

    Formula (100 points max):
    - Safety Score:        15 points
    - Instruction Score:   15 points
    - Environment Score:   10 points
    - Low Misconduct:      10 points
    - Teachers Score:      10 points
    - Leaders Score:       10 points
    - Family Involvement:  10 points
    - Parent Engagement:   10 points
    - Attendance:          10 points
    """

    edu = edu_df.copy()

    # Calculate weighted score for each school
    edu['score'] = (
        safe_numeric(edu['Safety Score']) / 100 * 15 +
        safe_numeric(edu['Instruction Score']) / 100 * 15 +
        safe_numeric(edu['Environment Score']) / 100 * 10 +
        # ... more components
    )

    # Average all schools in each community
    result = edu.groupby('Community Area Name')['score'].mean().reset_index()

    # Example result:
    # community        value
    # LINCOLN PARK     78.5
    # AUSTIN           42.3

    return result
```

---

#### 5. `components.py` — UI Rendering

**Purpose:** Functions that create visual elements on the page.

```python
def render_metric_info(info, metric_name):
    """Display the metric description box."""
    st.info(f"**{metric_name}**: {info['description']}")
    st.caption(f"📊 *{info['score_explanation']}*")

    # Renders:
    # ┌─────────────────────────────────────────────────────┐
    # │ ℹ️ Elementary Schools: Quality score for elementary │
    # │    schools focusing on early childhood metrics...   │
    # ├─────────────────────────────────────────────────────┤
    # │ 📊 Score out of ~73 based on: Safety (10)...        │
    # └─────────────────────────────────────────────────────┘

def render_map(df, geojson):
    """Render the choropleth map."""
    fig = px.choropleth_mapbox(
        df,                                    # Data with community + value
        geojson=geojson,                       # Polygon shapes
        locations='community',                 # Column to match on
        featureidkey='properties.community',   # GeoJSON field to match
        color='value',                         # Column that determines color
        color_continuous_scale='RdYlGn'        # Red → Yellow → Green
    )
    st.plotly_chart(fig)

def render_top_bottom(df, info):
    """Render the Top 5 and Bottom 5 tables side by side."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 5")
        st.caption(info['top_meaning'])
        top5 = df.nlargest(5, 'value')
        st.dataframe(top5)

    with col2:
        st.subheader("⚠️ Bottom 5")
        st.caption(info['bottom_meaning'])
        bottom5 = df.nsmallest(5, 'value')
        st.dataframe(bottom5)
```

---

#### 6. `__init__.py` — Package Exports

**Purpose:** Makes `dashboard/` a Python package and defines what can be imported.

```python
from .data_loader import load_all_data
from .metrics import calculate_all_metrics
from .components import render_metric_info, render_map, render_top_bottom
from .config import METRIC_INFO
```

**Effect:**

```python
# Without __init__.py:
from dashboard.data_loader import load_all_data
from dashboard.metrics import calculate_all_metrics

# With __init__.py:
from dashboard import load_all_data, calculate_all_metrics
```

---

#### 7. `run_dashboard.py` — Entry Point

**Purpose:** The main file that Streamlit runs. Ties everything together.

```python
import streamlit as st
from dashboard import (
    load_all_data,
    calculate_all_metrics,
    render_metric_info,
    render_map,
    render_top_bottom,
    METRIC_INFO
)

# Configure the page
st.set_page_config(page_title="Chicago Neighborhood Explorer", layout="wide")
st.title("🏠 Chicago Neighborhood Explorer")

# Step 1: Load all data
data = load_all_data()

# Step 2: Calculate all metrics
metrics = calculate_all_metrics(
    data['crimes'],
    data['education'],
    data['communities']
)

# Step 3: User selects a metric
metric_choice = st.selectbox("Select metric:", list(metrics.keys()))

# Step 4: Get data for selected metric
df = metrics[metric_choice]
info = METRIC_INFO[metric_choice]

# Step 5: Render the UI
render_metric_info(info, metric_choice)
render_map(df, data['geojson'])
render_top_bottom(df, info)
```

---

## Metrics Explained

### Safety (Low Crime)

| Aspect               | Details                                                               |
| -------------------- | --------------------------------------------------------------------- |
| **What it measures** | Neighborhood safety based on reported crimes                          |
| **Data source**      | Chicago Police Department - Crimes from past year                     |
| **Calculation**      | Count crimes per community, then invert (fewer crimes = higher score) |
| **Score range**      | 0 to ~25,000 (higher = safer)                                         |

### School Quality (Overall)

| Aspect               | Details                                              |
| -------------------- | ---------------------------------------------------- |
| **What it measures** | Comprehensive school quality across all school types |
| **Data source**      | CPS Progress Report Cards (2011-2012)                |
| **Calculation**      | Weighted average of 9 factors (see below)            |
| **Score range**      | 0 to 100                                             |

**Score Components:**
| Factor | Weight |
|--------|--------|
| Safety Score | 15 |
| Instruction Score | 15 |
| Environment Score | 10 |
| Low Misconduct Rate | 10 |
| Teachers Score | 10 |
| Leaders Score | 10 |
| Family Involvement | 10 |
| Parent Engagement | 10 |
| Student Attendance | 10 |

### Elementary Schools

| Aspect               | Details                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| **What it measures** | Quality of elementary schools (grades K-5)                                                       |
| **Calculation**      | Safety + Environment + Instruction + Teachers + Family + PK-2 Literacy/Math + Gr3-5 Reading/Math |
| **Score range**      | 0 to ~73                                                                                         |

### High Schools

| Aspect               | Details                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------- |
| **What it measures** | Quality of high schools with college readiness focus                                          |
| **Calculation**      | Safety + Instruction + Graduation Rate + College Eligibility + College Enrollment + ACT Score |
| **Score range**      | 0 to ~50                                                                                      |

### College Readiness

| Aspect               | Details                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| **What it measures** | How well high schools prepare students for college                                                       |
| **Calculation**      | Graduation (20) + College Eligibility (25) + College Enrollment (25) + ACT (20) + Freshman on Track (10) |
| **Score range**      | 0 to 100                                                                                                 |

---

## Data Sources

| Dataset | Source               | Records  | Description                            |
| ------- | -------------------- | -------- | -------------------------------------- |
| Crimes  | Chicago Data Portal  | ~258,000 | All reported crimes from past year     |
| Schools | CPS Progress Reports | 566      | School performance metrics (2011-2012) |
| GeoJSON | Chicago Data Portal  | 77       | Community area boundaries              |

**Links:**

- [Chicago Data Portal](https://data.cityofchicago.org/)
- [CPS School Data](https://www.cps.edu/about/district-data/)

---

## Adding New Metrics

To add a new metric, you only need to edit 2 files:

### Step 1: Add calculation to `metrics.py`

```python
def calculate_my_new_metric(some_df):
    """Calculate my new metric."""
    # Your calculation here
    result = some_df.groupby('Community Area Name')['some_column'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result
```

Add it to `calculate_all_metrics()`:

```python
def calculate_all_metrics(...):
    return {
        'Safety (Low Crime)': calculate_crime_metric(...),
        # ... existing metrics
        'My New Metric': calculate_my_new_metric(...)  # ← Add here
    }
```

### Step 2: Add description to `config.py`

```python
METRIC_INFO = {
    # ... existing metrics
    'My New Metric': {
        'description': 'What this metric measures...',
        'score_explanation': 'How the score is calculated...',
        'top_meaning': 'What being in the top 5 means...',
        'bottom_meaning': 'What being in the bottom 5 means...'
    }
}
```

That's it! The new metric will automatically appear in the dropdown.

---

## Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add more metrics (housing prices, transit access, parks)
- [ ] Add time-based filtering (crime by year/month)
- [ ] Add neighborhood comparison feature
- [ ] Improve mobile responsiveness
- [ ] Add data export functionality

---

## License

MIT License - feel free to use this project for any purpose.

---

## Acknowledgments

- Data provided by the [City of Chicago Data Portal](https://data.cityofchicago.org/)
- Built with [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/), and [GeoPandas](https://geopandas.org/)

```




## 1. Elementary School Quality Score (`map_elementary_quality.py`)

**What it shows:** A comprehensive quality rating for elementary schools (ES) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (25 pts)**       | Safety Score                   | 10         |
|                                | Environment Score              | 8          |
|                                | Low Misconduct Rate (inverted) | 7          |
| **Teaching (25 pts)**          | Instruction Score              | 10         |
|                                | Teachers Score                 | 8          |
|                                | Leaders Score                  | 7          |
| **Family/Attendance (20 pts)** | Family Involvement             | 7          |
|                                | Parent Engagement              | 6          |
|                                | Student Attendance             | 7          |
| **Academics (30 pts)**         | PK-2 Literacy %                | 8          |
|                                | PK-2 Math %                    | 8          |
|                                | Gr3-5 Math %                   | 7          |
|                                | Gr3-5 Reading %                | 7          |

**Why it's useful:** Parents choosing elementary schools can see which neighborhoods have the best overall elementary education. The score balances safety, teaching quality, family engagement, and age-appropriate academic outcomes (PK-5 metrics).

---

## 2. Middle School Quality Score (`map_middle_quality.py`)

**What it shows:** A comprehensive quality rating for middle schools (MS) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (25 pts)**       | Safety Score                   | 10         |
|                                | Environment Score              | 8          |
|                                | Low Misconduct Rate (inverted) | 7          |
| **Teaching (25 pts)**          | Instruction Score              | 10         |
|                                | Teachers Score                 | 8          |
|                                | Leaders Score                  | 7          |
| **Family/Attendance (20 pts)** | Family Involvement             | 7          |
|                                | Parent Engagement              | 6          |
|                                | Student Attendance             | 7          |
| **Academics (30 pts)**         | Gr6-8 Math %                   | 8          |
|                                | Gr6-8 Reading %                | 8          |
|                                | Gr8 Explore Math %             | 7          |
|                                | Gr8 Explore Reading %          | 7          |

**Why it's useful:** Middle school is a critical transition period. This map uses grade 6-8 specific metrics and the 8th grade EXPLORE test (a pre-ACT assessment) to show which communities have strong middle schools preparing students for high school.

---

## 3. High School Quality Score (`map_highschool_quality.py`)

**What it shows:** A comprehensive quality rating for high schools (HS) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (20 pts)**       | Safety Score                   | 8          |
|                                | Environment Score              | 6          |
|                                | Low Misconduct Rate (inverted) | 6          |
| **Teaching (20 pts)**          | Instruction Score              | 8          |
|                                | Teachers Score                 | 6          |
|                                | Leaders Score                  | 6          |
| **Family/Attendance (15 pts)** | Family Involvement             | 5          |
|                                | Parent Engagement              | 5          |
|                                | Student Attendance             | 5          |
| **Academics/College (45 pts)** | Graduation Rate                | 10         |
|                                | College Eligibility %          | 8          |
|                                | College Enrollment Rate %      | 8          |
|                                | ACT Score (normalized to 36)   | 8          |
|                                | Algebra Pass Rate              | 6          |
|                                | Freshman on Track Rate         | 5          |

**Why it's useful:** High school quality heavily determines college and career outcomes. This score weights academics and college readiness at 45% — the highest of any category — because that's what matters most at this level. It answers: "Which neighborhoods prepare students best for life after high school?"

---

## 4. College Readiness Score (`map_college_readiness.py`)

**What it shows:** A focused score measuring only how well high schools prepare students for college, scored 0-100.

**How it's calculated:**

| Component                    | Max Points | Why this weight                          |
| ---------------------------- | ---------- | ---------------------------------------- |
| College Eligibility %        | 25         | Meeting college admission requirements   |
| College Enrollment Rate %    | 25         | Actually going to college                |
| Graduation Rate %            | 20         | Can't go to college without graduating   |
| ACT Score (normalized to 36) | 20         | Standardized measure of readiness        |
| Freshman on Track Rate %     | 10         | Early indicator of graduation likelihood |

**Why it's useful:** Unlike the full high school quality score, this strips away everything except college outcomes. It's the purest measure of "if my kid goes to high school here, will they end up in college?" Useful for families where college is the primary goal.

---

## 5. Overall School Quality Score (`map_overall_quality.py`)

**What it shows:** A universal quality score applied to ALL schools (elementary, middle, and high) using only metrics that exist across all school types, scored 0-100.

**How it's calculated:**

| Component                      | Max Points |
| ------------------------------ | ---------- |
| Safety Score                   | 15         |
| Instruction Score              | 15         |
| Environment Score              | 10         |
| Low Misconduct Rate (inverted) | 10         |
| Teachers Score                 | 10         |
| Leaders Score                  | 10         |
| Family Involvement             | 10         |
| Parent Engagement              | 10         |
| Student Attendance             | 10         |

**Why it's useful:** This gives a single "overall education quality" view of each neighborhood by averaging all schools together. It answers: "Generally speaking, how good are the schools in this area?" Good for getting a quick snapshot without diving into elementary vs. middle vs. high school separately.

---

## 6. Academic Performance Score (`map_academic_performance.py`)

**What it shows:** Pure academic achievement based on standardized test scores, scored 0-100.

**How it's calculated:**

| Component                | Max Points |
| ------------------------ | ---------- |
| ISAT Exceeding Math %    | 50         |
| ISAT Exceeding Reading % | 50         |

**Why it's useful:** This is the most objective measure — standardized test performance only. No subjective scores, no surveys. It shows which neighborhoods have students performing at the highest levels academically. Useful for comparing raw academic output across communities.

---

## 7. Safety & Environment Score (`map_safety_environment.py`)

**What it shows:** How safe and conducive to learning each community's schools are, scored 0-100.

**How it's calculated:**

| Component                      | Max Points | What it measures                   |
| ------------------------------ | ---------- | ---------------------------------- |
| Safety Score                   | 35         | Physical safety, security          |
| Environment Score              | 35         | Learning environment quality       |
| Low Misconduct Rate (inverted) | 30         | Behavioral issues (fewer = better) |

**Why it's useful:** Some parents prioritize safety above academics. This map isolates just the safety and environment factors. It answers: "Where will my child be physically safe and in a good learning environment?" — especially relevant for families moving from areas with school safety concerns.

---

## 8. Parent & Community Engagement Score (`map_engagement.py`)

**What it shows:** How involved families and the community are in schools, scored 0-100.

**How it's calculated:**

| Component                | Max Points | What it measures                        |
| ------------------------ | ---------- | --------------------------------------- |
| Family Involvement Score | 35         | How much families participate in school |
| Parent Engagement Score  | 35         | How engaged parents are with education  |
| Parent Environment Score | 30         | How welcoming schools are to parents    |

**Why it's useful:** Research shows parent involvement is one of the strongest predictors of student success. This map shows which communities have strong school-family connections. High engagement often indicates: active PTAs, good communication, parents who show up to events, and schools that welcome family participation.

---

## Summary Table

| Map                  | Focus                          | Best for answering                      |
| -------------------- | ------------------------------ | --------------------------------------- |
| Elementary Quality   | ES schools, full picture       | "Best neighborhoods for young kids?"    |
| Middle Quality       | MS schools, full picture       | "Best neighborhoods for pre-teens?"     |
| High School Quality  | HS schools, full picture       | "Best neighborhoods for teenagers?"     |
| College Readiness    | HS only, college outcomes      | "Where do kids actually go to college?" |
| Overall Quality      | All schools, universal metrics | "Generally good schools here?"          |
| Academic Performance | Test scores only               | "Where are kids scoring highest?"       |
| Safety & Environment | Safety metrics only            | "Where are schools safest?"             |
| Engagement           | Parent involvement only        | "Where are families most involved?"     |
```
````
