#%%
import pandas as pd
import geopandas as gpd
import plotly.express as px
import requests
from shapely.geometry import Point

# Load data
crimes_df = pd.read_csv('.././data/raw/Crimes_-_One_year_prior_to_present.csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

# 1. Convert to GeoDataFrames
gdf_communities = gpd.GeoDataFrame.from_features(geojson['features']).set_crs("EPSG:4326")

crimes_df = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
geometry = [Point(lon, lat) for lon, lat in zip(crimes_df['LONGITUDE'], crimes_df['LATITUDE'])]
gdf_crimes = gpd.GeoDataFrame(crimes_df, geometry=geometry, crs="EPSG:4326")

# 2. Spatial join — assign each crime to a community
gdf_crimes = gpd.sjoin(gdf_crimes, gdf_communities[['community', 'geometry']], how='left', predicate='within')

# 3. Count crimes per community
crime_counts = gdf_crimes.groupby('community').size().reset_index(name='crime_count')

# Add percentage column
total_crimes = crime_counts['crime_count'].sum()
crime_counts['pct_of_total'] = (crime_counts['crime_count'] / total_crimes * 100).round(2)

# 4. Plot with custom hover
fig = px.choropleth_mapbox(
    crime_counts,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='crime_count',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Reds',
    custom_data=['pct_of_total']
)

# Custom hover template
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>" +
                  "Crimes: %{z:,}<br>" +
                  "% of Total: %{customdata[0]:.2f}%<extra></extra>"
)

fig.update_layout(width=1000, height=800, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
# %%
