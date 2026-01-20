import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

education_df['Family Involvement Score'] = pd.to_numeric(education_df['Family Involvement Score'], errors='coerce')

family_by_community = education_df.groupby('Community Area Name')['Family Involvement Score'].mean().reset_index()
family_by_community.columns = ['community', 'avg_family_involvement']
family_by_community['community'] = family_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    family_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='avg_family_involvement',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Purples',
    title='Average Family Involvement Score by Community'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()
