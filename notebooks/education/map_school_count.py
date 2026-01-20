#%%
import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

school_counts = education_df.groupby('Community Area Name').size().reset_index(name='school_count')
school_counts.columns = ['community', 'school_count']
school_counts['community'] = school_counts['community'].str.upper()

fig = px.choropleth_mapbox(
    school_counts,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='school_count',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Blues',
    title='Number of Schools by Community'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

# %%
