import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

# Filter to Middle Schools only
middle_df = education_df[education_df['Elementary, Middle, or High School'] == 'MS'].copy()

def safe_numeric(series):
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# School Environment (25 points)
middle_df['safety_norm'] = safe_numeric(middle_df['Safety Score']) / 100 * 10
middle_df['environment_norm'] = safe_numeric(middle_df['Environment Score']) / 100 * 8
middle_df['misconduct_norm'] = (100 - safe_numeric(middle_df['Rate of Misconducts (per 100 students) ']).clip(0, 100)) / 100 * 7

# Teaching Quality (25 points)
middle_df['instruction_norm'] = safe_numeric(middle_df['Instruction Score']) / 100 * 10
middle_df['teachers_norm'] = safe_numeric(middle_df['Teachers Score']) / 100 * 8
middle_df['leaders_norm'] = safe_numeric(middle_df['Leaders Score ']) / 100 * 7

# Family & Attendance (20 points)
middle_df['family_norm'] = safe_numeric(middle_df['Family Involvement Score']) / 100 * 7
middle_df['parent_eng_norm'] = safe_numeric(middle_df['Parent Engagement Score']) / 100 * 6
middle_df['student_attend_norm'] = safe_numeric(middle_df['Average Student Attendance'].str.rstrip('%')) / 100 * 7

# Academic Performance - Middle School Specific (30 points)
middle_df['gr68_math_norm'] = safe_numeric(middle_df['Gr6-8 Grade Level Math %']) / 100 * 8
middle_df['gr68_read_norm'] = safe_numeric(middle_df['Gr6-8 Grade Level Read %']) / 100 * 8
middle_df['explore_math_norm'] = safe_numeric(middle_df['Gr-8 Explore Math %']) / 100 * 7
middle_df['explore_read_norm'] = safe_numeric(middle_df['Gr-8 Explore Read %']) / 100 * 7

# Calculate total score
score_columns = [
    'safety_norm', 'environment_norm', 'misconduct_norm',
    'instruction_norm', 'teachers_norm', 'leaders_norm',
    'family_norm', 'parent_eng_norm', 'student_attend_norm',
    'gr68_math_norm', 'gr68_read_norm', 'explore_math_norm', 'explore_read_norm'
]

middle_df['quality_score'] = middle_df[score_columns].sum(axis=1, skipna=True)

# Aggregate by community
quality_by_community = middle_df.groupby('Community Area Name')['quality_score'].mean().reset_index()
quality_by_community.columns = ['community', 'middle_quality_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

# Plot
fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='middle_quality_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='RdYlGn',
    title='Middle School Quality Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nScore Breakdown (max 100 points):")
print("  Environment (25): Safety(10) + Environment(8) + Low Misconduct(7)")
print("  Teaching (25): Instruction(10) + Teachers(8) + Leaders(7)")
print("  Family/Attendance (20): Family(7) + Parent Engagement(6) + Attendance(7)")
print("  Academics (30): Gr6-8 Math(8) + Gr6-8 Read(8) + Explore Math(7) + Explore Read(7)")
