#%%
import pandas as pd
import geopandas as gpd
import streamlit as st
from shapely.geometry import Point
from config import DATA_PATHS
import requests
# %%
_geojson = requests.get('https://data.cityofchicago.org/resource/igwz-8jzy.geojson').json()
crimes_df = pd.read_csv('../notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv')
communities_gdf = gpd.GeoDataFrame.from_features(_geojson['features']).set_crs("EPSG:4326")
crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
geometry = [Point(lon, lat) for lon, lat in zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry, crs="EPSG:4326")
gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf[['community', 'geometry']], how='left', predicate='within')

crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')
# %%
