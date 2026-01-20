import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

education_df['healthy_numeric'] = (education_df['Healthy Schools Certified?'] == 'Yes').astype(int)

healthy_by_community = education_df.groupby('Community Area Name')['healthy_numeric'].mean().reset_index()
healthy_by_community.columns = ['community', 'pct_healthy_certified']
healthy_by_community['community'] = healthy_by_community['community'].str.upper()
healthy_by_community['pct_healthy_certified'] *= 100

fig = px.choropleth_mapbox(
    healthy_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='pct_healthy_certified',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Greens',
    title='% of Healthy Schools Certified by Community'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()
