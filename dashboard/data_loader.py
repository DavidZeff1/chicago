import pandas as pd
import geopandas as gpd
import requests
import streamlit as st
from pathlib import Path

# Get the project root (parent of dashboard folder)
PROJECT_ROOT = Path(__file__).parent.parent

DATA_PATHS = {
    'crimes': PROJECT_ROOT / 'notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv',
    'education': PROJECT_ROOT / 'notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv',
    'socioeconomic': PROJECT_ROOT / 'notebooks/data/raw/Census_Data_-_Selected_socioeconomic_indicators_in_Chicago,_2008_–_2012.csv',
    'geojson': 'https://data.cityofchicago.org/resource/igwz-8jzy.geojson'
}

@st.cache_data
def load_crimes():
    return pd.read_csv(DATA_PATHS['crimes'])

@st.cache_data
def load_education():
    return pd.read_csv(DATA_PATHS['education'])

@st.cache_data
def load_socioeconomic():
    return pd.read_csv(DATA_PATHS['socioeconomic'])

@st.cache_data
def load_geojson():
    return requests.get(DATA_PATHS['geojson']).json()

@st.cache_data
def load_communities(_geojson):
    return gpd.GeoDataFrame.from_features(_geojson['features']).set_crs("EPSG:4326")

def load_all_data():
    """Load all datasets and return as dict."""
    geojson = load_geojson()
    return {
        'crimes': load_crimes(),
        'education': load_education(),
        'socioeconomic': load_socioeconomic(),
        'geojson': geojson,
        'communities': load_communities(geojson)
    }
