import pandas as pd
import seaborn as sns
import requests
crimes_df = pd.read_csv('./data/raw/Crimes_-_One_year_prior_to_present.csv')
boundaries_df = pd.read_csv('./data/raw/Boundaries_-_Community_Areas.csv')
education_df = pd.read_csv('data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv')
parks_df = pd.read_csv('data/raw/CPD_Facilities.csv')
socioeconomic_df = pd.read_csv('data/raw/Census_Data_-_Selected_socioeconomic_indicators_in_Chicago,_2008_–_2012.csv')
