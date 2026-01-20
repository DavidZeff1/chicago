import pandas as pd
import plotly.express as px
import requests

education_df = pd.read_csv('../data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()

# Filter to Elementary Schools only
elem_df = education_df[education_df['Elementary, Middle, or High School'] == 'ES'].copy()

# Define columns and weights for Elementary Quality Score
# Normalize each to 0-100 scale, then weight them

def safe_numeric(series):
    """Convert to numeric, replacing errors with NaN"""
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# School Environment (25 points)
elem_df['safety_norm'] = safe_numeric(elem_df['Safety Score']) / 100 * 10          # max 10
elem_df['environment_norm'] = safe_numeric(elem_df['Environment Score']) / 100 * 8  # max 8
elem_df['misconduct_norm'] = (100 - safe_numeric(elem_df['Rate of Misconducts (per 100 students) ']).clip(0, 100)) / 100 * 7  # max 7 (inverted)

# Teaching Quality (25 points)
elem_df['instruction_norm'] = safe_numeric(elem_df['Instruction Score']) / 100 * 10  # max 10
elem_df['teachers_norm'] = safe_numeric(elem_df['Teachers Score']) / 100 * 8         # max 8
elem_df['leaders_norm'] = safe_numeric(elem_df['Leaders Score ']) / 100 * 7          # max 7

# Family & Attendance (20 points)
elem_df['family_norm'] = safe_numeric(elem_df['Family Involvement Score']) / 100 * 7        # max 7
elem_df['parent_eng_norm'] = safe_numeric(elem_df['Parent Engagement Score']) / 100 * 6     # max 6
elem_df['student_attend_norm'] = safe_numeric(elem_df['Average Student Attendance'].str.rstrip('%')) / 100 * 7  # max 7

# Academic Performance (30 points)
elem_df['pk2_literacy_norm'] = safe_numeric(elem_df['Pk-2 Literacy %']) / 100 * 8     # max 8
elem_df['pk2_math_norm'] = safe_numeric(elem_df['Pk-2 Math %']) / 100 * 8             # max 8
elem_df['gr35_math_norm'] = safe_numeric(elem_df['Gr3-5 Grade Level Math %']) / 100 * 7  # max 7
elem_df['gr35_read_norm'] = safe_numeric(elem_df['Gr3-5 Grade Level Read % ']) / 100 * 7  # max 7

# Calculate total score (max 100)
score_columns = [
    'safety_norm', 'environment_norm', 'misconduct_norm',
    'instruction_norm', 'teachers_norm', 'leaders_norm',
    'family_norm', 'parent_eng_norm', 'student_attend_norm',
    'pk2_literacy_norm', 'pk2_math_norm', 'gr35_math_norm', 'gr35_read_norm'
]

elem_df['quality_score'] = elem_df[score_columns].sum(axis=1, skipna=True)

# Aggregate by community
quality_by_community = elem_df.groupby('Community Area Name')['quality_score'].mean().reset_index()
quality_by_community.columns = ['community', 'elementary_quality_score']
quality_by_community['community'] = quality_by_community['community'].str.upper()

# Plot
fig = px.choropleth_mapbox(
    quality_by_community,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='elementary_quality_score',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale='RdYlGn',
    title='Elementary School Quality Score by Community (0-100)'
)
fig.update_layout(width=1000, height=800, margin={"r":0,"t":50,"l":0,"b":0})
fig.show()

# Print breakdown
print("\nScore Breakdown (max 100 points):")
print("  Environment (25): Safety(10) + Environment(8) + Low Misconduct(7)")
print("  Teaching (25): Instruction(10) + Teachers(8) + Leaders(7)")
print("  Family/Attendance (20): Family(7) + Parent Engagement(6) + Attendance(7)")
print("  Academics (30): PK-2 Literacy(8) + PK-2 Math(8) + Gr3-5 Math(7) + Gr3-5 Read(7)")
