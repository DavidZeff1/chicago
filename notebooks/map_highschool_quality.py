import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

# Filter to High Schools only
hs_df = education_df[education_df['Elementary, Middle, or High School'] == 'HS'].copy()

def safe_numeric(series):
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# School Environment (20 points)
hs_df['safety_norm'] = safe_numeric(hs_df['Safety Score']) / 100 * 8
hs_df['environment_norm'] = safe_numeric(hs_df['Environment Score']) / 100 * 6
hs_df['misconduct_norm'] = (100 - safe_numeric(hs_df['Rate of Misconducts (per 100 students) ']).clip(0, 100)) / 100 * 6

# Teaching Quality (20 points)
hs_df['instruction_norm'] = safe_numeric(hs_df['Instruction Score']) / 100 * 8
hs_df['teachers_norm'] = safe_numeric(hs_df['Teachers Score']) / 100 * 6
hs_df['leaders_norm'] = safe_numeric(hs_df['Leaders Score ']) / 100 * 6

# Family & Attendance (15 points)
hs_df['family_norm'] = safe_numeric(hs_df['Family Involvement Score']) / 100 * 5
hs_df['parent_eng_norm'] = safe_numeric(hs_df['Parent Engagement Score']) / 100 * 5
hs_df['student_attend_norm'] = safe_numeric(hs_df['Average Student Attendance'].str.rstrip('%')) / 100 * 5

# Academic & College Readiness (45 points) - HS specific
hs_df['graduation_norm'] = safe_numeric(hs_df['Graduation Rate %']) / 100 * 10
hs_df['college_elig_norm'] = safe_numeric(hs_df['College Eligibility %']) / 100 * 8
hs_df['college_enroll_norm'] = safe_numeric(hs_df['College Enrollment Rate %']) / 100 * 8
hs_df['act_norm'] = safe_numeric(hs_df['11th Grade Average ACT (2011) ']) / 36 * 8  # ACT max is 36
hs_df['algebra_norm'] = safe_numeric(hs_df['Students Passing  Algebra %']) / 100 * 6
hs_df['freshman_track_norm'] = safe_numeric(hs_df['Freshman on Track Rate %']) / 100 * 5

# Calculate total score
score_columns = [
    'safety_norm', 'environment_norm', 'misconduct_norm',
    'instruction_norm', 'teachers_norm', 'leaders_norm',
    'family_norm', 'parent_eng_norm', 'student_attend_norm',
    'graduation_norm', 'college_elig_norm', 'college_enroll_norm',
    'act_norm', 'algebra_norm', 'freshman_track_norm'
]

hs_df['quality_score'] = hs_df[score_columns].sum(axis=1, skipna=True)

# Aggregate by community
quality_by_community = hs_df.groupby('Community Area Name')['quality_score'].mean().reset_index()
quality_by_community.columns = ['community', 'highschool_quality_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

# Plot
fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='highschool_quality_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='RdYlGn',
    title='High School Quality Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

print("\nScore Breakdown (max 100 points):")
print("  Environment (20): Safety(8) + Environment(6) + Low Misconduct(6)")
print("  Teaching (20): Instruction(8) + Teachers(6) + Leaders(6)")
print("  Family/Attendance (15): Family(5) + Parent Engagement(5) + Attendance(5)")
print("  Academics/College (45): Graduation(10) + College Eligible(8) + College Enroll(8) + ACT(8) + Algebra(6) + Freshman Track(5)")
