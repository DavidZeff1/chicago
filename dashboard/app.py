import streamlit as st
from dashboard import (
    load_all_data,
    calculate_all_metrics,
    render_metric_info,
    render_map,
    render_top_bottom,
    METRIC_INFO
)

# Page config
st.set_page_config(page_title="Chicago Neighborhood Explorer", layout="wide")
st.title("🏠 Chicago Neighborhood Explorer")
st.caption("Find the right neighborhood for you")

# Load data
data = load_all_data()

# Calculate metrics
metrics = calculate_all_metrics(
    data['crimes'],
    data['education'],
    data['communities']
)

# UI: Metric selector
metric_choice = st.selectbox("Select metric:", list(metrics.keys()))

# Get selected metric data and info
df = metrics[metric_choice].copy()
info = METRIC_INFO[metric_choice]

# Render components
render_metric_info(info, metric_choice)
render_map(df, data['geojson'])
render_top_bottom(df, info)
