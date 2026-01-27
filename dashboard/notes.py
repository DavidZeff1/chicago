#%%
import pandas as pd
import geopandas as gpd
import streamlit as st
from shapely.geometry import Point
from config import DATA_PATHS
import requests
# %%
_geojson = requests.get(DATA_PATHS['geojson']).json()
crimes_df = pd.read_csv(DATA_PATHS['crimes'])
communities_gdf = gpd.GeoDataFrame.from_features(_geojson['features']).set_crs("EPSG:4326")
crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
geometry = [Point(lon, lat) for lon, lat in zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry, crs="EPSG:4326")
gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf[['community', 'geometry']], how='left', predicate='within')

crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')
crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']
# %%
