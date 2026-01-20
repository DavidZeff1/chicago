import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

hs_df = education_df[education_df['Elementary, Middle, or High School'] == 'HS'].copy()

def safe_numeric(series):
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# College Readiness Score (100 points total)
hs_df['graduation_norm'] = safe_numeric(hs_df['Graduation Rate %']) / 100 * 20
hs_df['college_elig_norm'] = safe_numeric(hs_df['College Eligibility %']) / 100 * 25
hs_df['college_enroll_norm'] = safe_numeric(hs_df['College Enrollment Rate %']) / 100 * 25
hs_df['act_norm'] = safe_numeric(hs_df['11th Grade Average ACT (2011) ']) / 36 * 20
hs_df['freshman_track_norm'] = safe_numeric(hs_df['Freshman on Track Rate %']) / 100 * 10

score_columns = ['graduation_norm', 'college_elig_norm', 'college_enroll_norm', 'act_norm', 'freshman_track_norm']
hs_df['college_readiness_score'] = hs_df[score_columns].sum(axis=1, skipna=True)

quality_by_community = hs_df.groupby('Community Area Name')['college_readiness_score'].mean().reset_index()
quality_by_community.columns = ['community', 'college_readiness_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='college_readiness_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='Viridis',
    title='High School College Readiness Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nCollege Readiness Score Breakdown (max 100 points):")
print("  Graduation Rate: 20 points")
print("  College Eligibility: 25 points")
print("  College Enrollment: 25 points")
print("  ACT Score: 20 points")
print("  Freshman on Track: 10 points")
