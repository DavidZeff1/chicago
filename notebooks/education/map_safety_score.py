#%%
import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('.././data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

safety_by_community = education_df.groupby('Community Area Name')['Safety Score'].mean().reset_index()
safety_by_community.columns = ['community', 'avg_safety_score']
safety_by_community['community'] = safety_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    safety_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='avg_safety_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='RdYlGn',
    title='Average School Safety Score by Community'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

# %%
