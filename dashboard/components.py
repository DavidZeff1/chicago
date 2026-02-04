import streamlit as st
import plotly.express as px
import geopandas as gpd
import pandas as pd


MAP_CENTER = {'lat': 41.8781, 'lon': -87.6298}
MAP_ZOOM = 9
MAP_STYLE = 'open-street-map'
COLOR_SCALE = 'RdYlGn_r'

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
        color_continuous_scale=COLOR_SCALE,
        opacity=0.6
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

def render_neighborhood_map(communities, crimes):
    st.title('Explore Specific Neighborhood')
    st.subheader('Select neighborhood to get more specific insights')
    
    neighborhood = st.selectbox("Select neighborhood:", list(communities.community))
    crime = st.selectbox("Select type of crime:", list(crimes[' PRIMARY DESCRIPTION'].unique()))

    commun = communities[communities.community == neighborhood]
    community_number = int(commun.iloc[0, 3])

    # Create area_code columns for merging
    communities['area_code'] = communities['area_num_1'].astype('Int64')
    crimes['area_code'] = crimes['WARD'].astype('Int64')
    merged = pd.merge(communities, crimes, on='area_code')

    # === SECTION 1: Selected Neighborhood & Crime Type ===
    st.header(f"📍 {neighborhood} - {crime}")
    
    filtered_crimes = crimes[(crimes[' PRIMARY DESCRIPTION'] == crime) & 
                            (crimes['WARD'] == community_number)]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Incidents", len(filtered_crimes))
    with col2:
        # Compare to city average
        city_avg = len(crimes[crimes[' PRIMARY DESCRIPTION'] == crime]) / crimes['WARD'].nunique()
        st.metric("City Average per Ward", f"{city_avg:.0f}")
    

    # === SECTION 2: Crime Distribution in Selected Neighborhood ===
    st.header(f"🔍 All Crime Types in {neighborhood}")
    
    neighborhood_crimes = merged[merged['community'] == neighborhood]
    crime_counts = neighborhood_crimes.groupby(' PRIMARY DESCRIPTION').size().sort_values(ascending=False)
    
    # Bar chart: Crime types in this neighborhood
    fig1 = px.bar(
        x=crime_counts.head(10).values,
        y=crime_counts.head(10).index,
        orientation='h',
        title=f"Top 10 Crime Types in {neighborhood}",
        labels={'x': 'Number of Incidents', 'y': 'Crime Type'},
        color=crime_counts.head(10).values,
        color_continuous_scale='Reds'
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

    # === SECTION 3: Selected Crime Across All Neighborhoods ===
    st.header(f"🏙️ {crime} Across Chicago")
    
    crime_by_community = merged[merged[' PRIMARY DESCRIPTION'] == crime].groupby('community').size().sort_values(ascending=False)
    
    fig2 = px.bar(
        x=crime_by_community.head(15).values,
        y=crime_by_community.head(15).index,
        orientation='h',
        title=f"{crime} by Neighborhood (Top 15)",
        labels={'x': 'Number of Incidents', 'y': 'Neighborhood'},
        color=crime_by_community.head(15).index,
        color_discrete_map={neighborhood: 'red'}
    )
    fig2.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig2, use_container_width=True)

    # === SECTION 4: Comparison - Selected vs City ===
    st.header("📊 Comparison: Selected Neighborhood vs City")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart: Crime distribution in selected neighborhood
        neighborhood_top5 = crime_counts.head(5)
        fig3 = px.pie(
            values=neighborhood_top5.values,
            names=neighborhood_top5.index,
            title=f"Crime Mix in {neighborhood}"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Pie chart: Crime distribution citywide
        city_crimes = merged.groupby(' PRIMARY DESCRIPTION').size().sort_values(ascending=False).head(5)
        fig4 = px.pie(
            values=city_crimes.values,
            names=city_crimes.index,
            title="Crime Mix Citywide"
        )
        st.plotly_chart(fig4, use_container_width=True)


    # === SECTION 6: Time-based analysis (if you have date column) ===
    if 'DATE  OF OCCURRENCE' in crimes.columns:
        st.header("📅 Trend Over Time")
        
        # Convert to datetime
        crimes['date'] = pd.to_datetime(crimes['DATE  OF OCCURRENCE'], errors='coerce')
        
        # Monthly trend for selected crime in selected neighborhood
        neighborhood_time = crimes[
            (crimes['WARD'] == community_number) & 
            (crimes[' PRIMARY DESCRIPTION'] == crime)
        ].copy()
        
        if len(neighborhood_time) > 0:
            neighborhood_time['month'] = neighborhood_time['date'].dt.to_period('M')
            monthly_counts = neighborhood_time.groupby('month').size()
            
            fig5 = px.line(
                x=monthly_counts.index.astype(str),
                y=monthly_counts.values,
                title=f"{crime} Trend in {neighborhood}",
                labels={'x': 'Month', 'y': 'Incidents'}
            )
            st.plotly_chart(fig5, use_container_width=True)


def render_show_data(communities, crimes, education):
    st.title('Data Used In This Project')

    st.subheader('communities (converted from geojson)')
    st.dataframe(communities)

    st.subheader('crimes')
    st.dataframe(crimes)

    st.subheader('education')
    st.dataframe(education)

