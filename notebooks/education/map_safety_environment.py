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

# Safety & Environment focused score
df['safety_norm'] = safe_numeric(df['Safety Score']) / 100 * 35
df['environment_norm'] = safe_numeric(df['Environment Score']) / 100 * 35
df['misconduct_norm'] = (100 - safe_numeric(df['Rate of Misconducts (per 100 students) ']).clip(0, 100)) / 100 * 30

df['safety_env_score'] = df[['safety_norm', 'environment_norm', 'misconduct_norm']].sum(axis=1, skipna=True)

quality_by_community = df.groupby('Community Area Name')['safety_env_score'].mean().reset_index()
quality_by_community.columns = ['community', 'safety_env_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='safety_env_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='OrRd',
    title='School Safety & Environment Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nSafety & Environment Score Breakdown (max 100 points):")
print("  Safety Score: 35 points")
print("  Environment Score: 35 points")
print("  Low Misconduct Rate: 30 points")
