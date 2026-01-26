import pandas as pd
import geopandas as gpd
import streamlit as st
from shapely.geometry import Point
from .utils import safe_numeric

def calculate_crime_metric(crimes_df, communities_gdf):
    """Calculate safety score (inverted crime count)."""
    crimes_clean = crimes_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
    geometry = [Point(lon, lat) for lon, lat in zip(crimes_clean['LONGITUDE'], crimes_clean['LATITUDE'])]
    gdf_crimes = gpd.GeoDataFrame(crimes_clean, geometry=geometry, crs="EPSG:4326")
    gdf_crimes = gpd.sjoin(gdf_crimes, communities_gdf[['community', 'geometry']], how='left', predicate='within')
    
    crime_counts = gdf_crimes.groupby('community').size().reset_index(name='value')
    crime_counts['value'] = crime_counts['value'].max() - crime_counts['value']
    return crime_counts

def calculate_overall_school_quality(edu_df):
    """Calculate overall school quality score."""
    edu = edu_df.copy()
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
    result = edu.groupby('Community Area Name')['score'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result

def calculate_elementary_quality(edu_df):
    """Calculate elementary school quality score."""
    elem = edu_df[edu_df['Elementary, Middle, or High School'] == 'ES'].copy()
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
    result = elem.groupby('Community Area Name')['score'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result

def calculate_highschool_quality(edu_df):
    """Calculate high school quality score."""
    hs = edu_df[edu_df['Elementary, Middle, or High School'] == 'HS'].copy()
    hs['score'] = (
        safe_numeric(hs['Safety Score']) / 100 * 8 +
        safe_numeric(hs['Instruction Score']) / 100 * 8 +
        safe_numeric(hs['Graduation Rate %']) / 100 * 10 +
        safe_numeric(hs['College Eligibility %']) / 100 * 8 +
        safe_numeric(hs['College Enrollment Rate %']) / 100 * 8 +
        safe_numeric(hs['11th Grade Average ACT (2011) ']) / 36 * 8
    )
    result = hs.groupby('Community Area Name')['score'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result

def calculate_college_readiness(edu_df):
    """Calculate college readiness score."""
    hs = edu_df[edu_df['Elementary, Middle, or High School'] == 'HS'].copy()
    hs['score'] = (
        safe_numeric(hs['Graduation Rate %']) / 100 * 20 +
        safe_numeric(hs['College Eligibility %']) / 100 * 25 +
        safe_numeric(hs['College Enrollment Rate %']) / 100 * 25 +
        safe_numeric(hs['11th Grade Average ACT (2011) ']) / 36 * 20 +
        safe_numeric(hs['Freshman on Track Rate %']) / 100 * 10
    )
    result = hs.groupby('Community Area Name')['score'].mean().reset_index()
    result.columns = ['community', 'value']
    result['community'] = result['community'].str.upper()
    return result

@st.cache_data
def calculate_all_metrics(_crimes_df, _education_df, _communities_gdf):
    """Calculate all metrics and return as dict."""
    return {
        'Safety (Low Crime)': calculate_crime_metric(_crimes_df, _communities_gdf),
        'School Quality (Overall)': calculate_overall_school_quality(_education_df),
        'Elementary Schools': calculate_elementary_quality(_education_df),
        'High Schools': calculate_highschool_quality(_education_df),
        'College Readiness': calculate_college_readiness(_education_df)
    }
