import streamlit as st
import plotly.express as px
from .config import MAP_CENTER, MAP_ZOOM, MAP_STYLE, COLOR_SCALE

def render_metric_info(info, metric_name):
    """Render the metric description and score explanation."""
    st.info(f"**{metric_name}**: {info['description']}")
    st.caption(f"📊 *{info['score_explanation']}*")

def render_map(df, geojson):
    """Render the choropleth map."""
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='community',
        featureidkey='properties.community',
        color='value',
        mapbox_style=MAP_STYLE,
        center=MAP_CENTER,
        zoom=MAP_ZOOM,
        color_continuous_scale=COLOR_SCALE
    )
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Score: %{z:.1f}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_top_bottom(df, info):
    """Render top 5 and bottom 5 neighborhoods."""
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
