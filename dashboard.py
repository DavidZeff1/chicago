import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import requests
from shapely.geometry import Point

st.set_page_config(page_title="Chicago Neighborhood Explorer", layout="wide")
st.title("🏠 Chicago Neighborhood Explorer")
st.caption("Find the right neighborhood for you")

# Load data once
@st.cache_data
def load_data():
    crimes_df = pd.read_csv('./notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv')
    education_df = pd.read_csv('./notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
    socioeconomic_df = pd.read_csv('./notebooks/data/raw/Census_Data_-_Selected_socioeconomic_indicators_in_Chicago,_2008_–_2012.csv')
    geojson = requests.get("https://data.cityofchicago.org/resource/igwz-8jzy.geojson").json()
    return crimes_df, education_df, socioeconomic_df, geojson

crimes_df, education_df, socioeconomic_df, geojson = load_data()

# Metric descriptions
METRIC_INFO = {
    'Safety (Low Crime)': {
        'description': 'Measures neighborhood safety based on reported crime incidents over the past year. Higher scores indicate fewer crimes.',
        'score_explanation': 'Score is inverted crime count — higher means safer. A score of 25,000 means very few crimes; a score near 0 means high crime area.',
        'top_meaning': 'These are Chicago\'s safest neighborhoods. Residents here experience significantly fewer reported crimes including theft, assault, and property crime. Ideal for families and those prioritizing security.',
        'bottom_meaning': 'These neighborhoods have the highest crime rates in Chicago. Consider additional safety precautions, research specific blocks, and visit at different times of day before committing.'
    },
    'School Quality (Overall)': {
        'description': 'Comprehensive school quality score combining safety, instruction, environment, teacher quality, leadership, family involvement, and student attendance across all schools.',
        'score_explanation': 'Score out of 100 based on: Safety (15), Instruction (15), Environment (10), Low Misconduct (10), Teachers (10), Leaders (10), Family Involvement (10), Parent Engagement (10), Attendance (10).',
        'top_meaning': 'These neighborhoods have the strongest schools across all metrics. Expect quality instruction, safe environments, engaged parents, and strong leadership. Great for families with children of any age.',
        'bottom_meaning': 'Schools in these areas struggle across multiple dimensions — lower attendance, weaker instruction, and less parent engagement. Consider charter schools, magnet programs, or selective enrollment options if moving here.'
    },
    'Elementary Schools': {
        'description': 'Quality score for elementary schools (ES) only, focusing on early childhood metrics like PK-2 literacy/math and grades 3-5 performance.',
        'score_explanation': 'Score out of ~73 based on: Safety (10), Environment (8), Instruction (10), Teachers (8), Family Involvement (7), PK-2 Literacy (8), PK-2 Math (8), Gr3-5 Math (7), Gr3-5 Reading (7).',
        'top_meaning': 'Best neighborhoods for children ages 5-11. Strong early literacy and math foundations, safe classrooms, and involved parent communities. Kids here start their academic journey on solid footing.',
        'bottom_meaning': 'Elementary schools here show weaker early reading and math outcomes. Early intervention and supplemental tutoring may be needed. Research individual schools — some may outperform the neighborhood average.'
    },
    'High Schools': {
        'description': 'Quality score for high schools (HS) only, emphasizing college readiness metrics like graduation rates, college eligibility, and ACT scores.',
        'score_explanation': 'Score out of ~50 based on: Safety (8), Instruction (8), Graduation Rate (10), College Eligibility (8), College Enrollment (8), ACT Score (8).',
        'top_meaning': 'Teenagers here have the best shot at college success. High graduation rates, competitive ACT scores, and strong college enrollment. These schools open doors to universities and careers.',
        'bottom_meaning': 'High schools in these areas have lower graduation rates and college readiness. Many students don\'t finish or aren\'t prepared for higher education. Look into selective enrollment high schools or alternative pathways.'
    },
    'College Readiness': {
        'description': 'Focused purely on college preparation outcomes — how well do high schools prepare students for higher education?',
        'score_explanation': 'Score out of 100 based on: Graduation Rate (20), College Eligibility (25), College Enrollment (25), ACT Score (20), Freshman on Track (10).',
        'top_meaning': 'Students from these neighborhoods actually go to college. High ACT scores, strong graduation rates, and proven college enrollment. If higher education is your priority, these are your neighborhoods.',
        'bottom_meaning': 'Very few students from these high schools enroll in college. Lower ACT scores and graduation rates create barriers to higher education. Consider this carefully if college is a priority for your family.'
    }
}
# Helper function
def safe_numeric(series):
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')

# Calculate all metrics
@st.cache_data
def calculate_metrics(_crimes_df, _education_df, _socioeconomic_df, _geojson):
    metrics = {}
    
    # --- CRIME ---
    gdf_communities = gpd.GeoDataFrame.from_features(_geojson['features']).set_crs("EPSG:4326")
    crimes_clean = _crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
    geometry = [Point(lon, lat) for lon, lat in zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
    gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry, crs="EPSG:4326")
    gdf_crimes = gpd.sjoin(gdf_crimes, gdf_communities[['community', 'geometry']], how='left', predicate='within')
    crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')
    # Invert so higher = safer
    crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']
    metrics['Safety (Low Crime)'] = crime_counts
    
    # --- EDUCATION METRICS ---
    edu = _education_df.copy()
    
    # Overall School Quality
    edu['score'] = (
        safe_numeric(edu['Safety Score']) / 100 * 15 +
        safe_numeric(edu['Instruction Score']) / 100 * 15 +
        safe_numeric(edu['Environment Score']) / 100 * 10 +
        (100 - safe_numeric(edu['Rate of Misconducts (per 100 students) ']).clip(0, 100)) / 100 * 10 +
        safe_numeric(edu['Teachers Score']) / 100 * 10 +
        safe_numeric(edu['Leaders Score ']) / 100 * 10 +
        safe_numeric(edu['Family Involvement Score']) / 100 * 10 +
        safe_numeric(edu['Parent Engagement Score']) / 100 * 10 +
        safe_numeric(edu['Average Student Attendance'].str.rstrip('%')) / 100 * 10
    )
    overall = edu.groupby('Community Area Name')['score'].mean().reset_index()
    overall.columns = ['community', 'value']
    overall['community'] = overall['community'].str.upper()
    metrics['School Quality (Overall)'] = overall
    
    # Elementary Quality
    elem = edu[edu['Elementary, Middle, or High School'] == 'ES'].copy()
    elem['score'] = (
        safe_numeric(elem['Safety Score']) / 100 * 10 +
        safe_numeric(elem['Environment Score']) / 100 * 8 +
        safe_numeric(elem['Instruction Score']) / 100 * 10 +
        safe_numeric(elem['Teachers Score']) / 100 * 8 +
        safe_numeric(elem['Family Involvement Score']) / 100 * 7 +
        safe_numeric(elem['Pk-2 Literacy %']) / 100 * 8 +
        safe_numeric(elem['Pk-2 Math %']) / 100 * 8 +
        safe_numeric(elem['Gr3-5 Grade Level Math %']) / 100 * 7 +
        safe_numeric(elem['Gr3-5 Grade Level Read % ']) / 100 * 7
    )
    elem_agg = elem.groupby('Community Area Name')['score'].mean().reset_index()
    elem_agg.columns = ['community', 'value']
    elem_agg['community'] = elem_agg['community'].str.upper()
    metrics['Elementary Schools'] = elem_agg
    
    # High School Quality
    hs = edu[edu['Elementary, Middle, or High School'] == 'HS'].copy()
    hs['score'] = (
        safe_numeric(hs['Safety Score']) / 100 * 8 +
        safe_numeric(hs['Instruction Score']) / 100 * 8 +
        safe_numeric(hs['Graduation Rate %']) / 100 * 10 +
        safe_numeric(hs['College Eligibility %']) / 100 * 8 +
        safe_numeric(hs['College Enrollment Rate %']) / 100 * 8 +
        safe_numeric(hs['11th Grade Average ACT (2011) ']) / 36 * 8
    )
    hs_agg = hs.groupby('Community Area Name')['score'].mean().reset_index()
    hs_agg.columns = ['community', 'value']
    hs_agg['community'] = hs_agg['community'].str.upper()
    metrics['High Schools'] = hs_agg
    
    # College Readiness
    hs['college_score'] = (
        safe_numeric(hs['Graduation Rate %']) / 100 * 20 +
        safe_numeric(hs['College Eligibility %']) / 100 * 25 +
        safe_numeric(hs['College Enrollment Rate %']) / 100 * 25 +
        safe_numeric(hs['11th Grade Average ACT (2011) ']) / 36 * 20 +
        safe_numeric(hs['Freshman on Track Rate %']) / 100 * 10
    )
    college_agg = hs.groupby('Community Area Name')['college_score'].mean().reset_index()
    college_agg.columns = ['community', 'value']
    college_agg['community'] = college_agg['community'].str.upper()
    metrics['College Readiness'] = college_agg
    
    return metrics

metrics = calculate_metrics(crimes_df, education_df, socioeconomic_df, geojson)

# UI
metric_choice = st.selectbox("Select metric:", list(metrics.keys()))

# Show description for selected metric
info = METRIC_INFO[metric_choice]
st.info(f"**{metric_choice}**: {info['description']}")
st.caption(f"📊 *{info['score_explanation']}*")

# Get data for selected metric
df = metrics[metric_choice].copy()

# Color scale
color_scale = 'RdYlGn'  # Red=bad, Green=good

# Map
fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations='community',
    featureidkey='properties.community',
    color='value',
    mapbox_style='open-street-map',
    center={'lat': 41.8781, 'lon': -87.6298},
    zoom=9,
    color_continuous_scale=color_scale
)
fig.update_layout(
    height=600,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>Score: %{z:.1f}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# Top/Bottom neighborhoods
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏆 Top 5")
    st.caption(info['top_meaning'])
    top5 = df.nlargest(5, 'value')[['community', 'value']].reset_index(drop=True)
    top5.index = top5.index + 1
    top5.columns = ['Community', 'Score']
    st.dataframe(top5, use_container_width=True)

with col2:
    st.subheader("⚠️ Bottom 5")
    st.caption(info['bottom_meaning'])
    bottom5 = df.nsmallest(5, 'value')[['community', 'value']].reset_index(drop=True)
    bottom5.index = bottom5.index + 1
    bottom5.columns = ['Community', 'Score']
    st.dataframe(bottom5, use_container_width=True)
