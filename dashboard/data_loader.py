import pandas as pd
import geopandas as gpd
import requests
import streamlit as st
from .config import DATA_PATHS

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
