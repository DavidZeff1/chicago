import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

df = education_df.copy()

def safe_numeric(series):
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# Engagement focused score
df['family_norm'] = safe_numeric(df['Family Involvement Score']) / 100 * 35
df['parent_eng_norm'] = safe_numeric(df['Parent Engagement Score']) / 100 * 35
df['parent_env_norm'] = safe_numeric(df['Parent Environment Score']) / 100 * 30

df['engagement_score'] = df[['family_norm', 'parent_eng_norm', 'parent_env_norm']].sum(axis=1, skipna=True)

quality_by_community = df.groupby('Community Area Name')['engagement_score'].mean().reset_index()
quality_by_community.columns = ['community', 'engagement_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='engagement_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Purples',
    title='Parent & Community Engagement Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nEngagement Score Breakdown (max 100 points):")
print("  Family Involvement: 35 points")
print("  Parent Engagement: 35 points")
print("  Parent Environment: 30 points")
