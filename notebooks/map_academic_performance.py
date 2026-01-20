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

# ISAT scores apply to most schools
df['isat_math_norm'] = safe_numeric(df['ISAT Exceeding Math %']) / 100 * 50
df['isat_read_norm'] = safe_numeric(df['ISAT Exceeding Reading % ']) / 100 * 50

df['academic_score'] = df[['isat_math_norm', 'isat_read_norm']].sum(axis=1, skipna=True)

quality_by_community = df.groupby('Community Area Name')['academic_score'].mean().reset_index()
quality_by_community.columns = ['community', 'academic_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='academic_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Blues',
    title='Academic Performance Score by Community (ISAT Exceeding %)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nAcademic Score Breakdown (max 100 points):")
print("  ISAT Exceeding Math %: 50 points")
print("  ISAT Exceeding Reading %: 50 points")
