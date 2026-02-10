
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .utils import safe_numeric

def prepare_eda_data(data, metrics):
    """
    Merge all relevant data into a single DataFrame for analysis.
    """
    # 1. Start with Crime Metric components
    crime_metric = metrics['Safety (Low Crime)']
    df = crime_metric.copy()
    df = df.rename(columns={'value': 'Crime Rate (Per Capita)'})
    
    # 2. Add Education Metrics
    edu_overall = metrics['School Quality (Overall)'][['community', 'value']].rename(columns={'value': 'School Quality Score'})
    df = pd.merge(df, edu_overall, on='community', how='left')
    
    # 3. Add Socioeconomic Data
    socio = data['socioeconomic'].copy()
    
    # Normalize columns
    socio.columns = socio.columns.str.strip().str.upper()
    
    # Clean community names for merging - usually upper case
    socio['COMMUNITY AREA NAME'] = socio['COMMUNITY AREA NAME'].fillna('').astype(str).str.upper()
    
    # Selected columns to correlate (ensure these match the upper case versions)
    socio_cols = [
        'COMMUNITY AREA NAME',
        'HARDSHIP INDEX',
        'PER CAPITA INCOME',
        'PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA',
        'PERCENT HOUSEHOLDS BELOW POVERTY',
        'PERCENT AGED 16+ UNEMPLOYED'
    ]
    
    # Check if columns exist (avoid errors if csv triggers KeyError)
    available_cols = [c for c in socio_cols if c in socio.columns]
    socio = socio[available_cols].rename(columns={'COMMUNITY AREA NAME': 'community'})
    
    # Ensure numeric types
    for col in socio.columns:
        if col != 'community':
            socio[col] = pd.to_numeric(socio[col], errors='coerce')
    
    df = pd.merge(df, socio, on='community', how='left')
    
    return df

def render_correlation_heatmap(df):
    """Render a correlation heatmap of numeric columns."""
    st.subheader("Correlation Analysis")
    st.write("How do different factors relate to each other?")
    st.markdown("""
    This map shows how strongly different factors are connected. 
    * **Blue (1.0)** means they go up together (Positive Correlation). 
    * **Red (-1.0)** means when one goes up, the other goes down (Negative Correlation).
    """)
    
    # Select numeric columns only
    numeric_df = df.select_dtypes(include=['float64', 'int64']).drop(columns=['community', 'crime_count', 'Total Population', 'AREA_NUMBE'], errors='ignore')
    
    # Calculate correlation matrix
    corr = numeric_df.corr()
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r" # Red (negative) to Blue (positive)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    return corr

def render_scatter_plots(df):
    """Render interactive scatter plots."""
    st.subheader("Deep Dive: Relationships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Crime vs School Quality
        st.markdown("#### Crime vs. Education")
        st.markdown("""
        **What this shows:** This chart compares the crime rate in a neighborhood with its overall school quality score.
        
        **What to look for:** A *downward* trend suggests that neighborhoods with better schools tend to have less crime.
        """)
        fig1 = px.scatter(
            df,
            x='School Quality Score',
            y='Crime Rate (Per Capita)',
            hover_name='community',
            trendline='ols',
            title='Crime Rate vs. School Quality',
            color='HARDSHIP INDEX' # Add a 3rd dimension
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
         # Crime vs Hardship
        if 'HARDSHIP INDEX' in df.columns:
            st.markdown("#### Crime vs. Hardship")
            st.markdown("""
            **What this shows:** This compares crime rates with the "Hardship Index," a score from 1-100 measuring economic difficulty (income, housing, etc.).
            
            **What to look for:** An *upward* trend indicates that areas with more economic hardship often face higher crime rates.
            """)
            fig2 = px.scatter(
                df,
                x='HARDSHIP INDEX',
                y='Crime Rate (Per Capita)',
                hover_name='community',
                trendline='ols',
                title='Crime Rate vs. Hardship Index',
                color='School Quality Score'
            )
            st.plotly_chart(fig2, use_container_width=True)

def render_insights(corr):
    """Generate and display textual insights based on correlations."""
    st.subheader("Key Insights")
    
    # Extract correlations with Crime Rate
    if 'Crime Rate (Per Capita)' in corr.index:
        crime_corr = corr['Crime Rate (Per Capita)'].drop('Crime Rate (Per Capita)')
        
        # Sort by absolute value
        top_corr = crime_corr.abs().sort_values(ascending=False).head(3)
        
        for feature, correlation in top_corr.items():
            original_val = crime_corr[feature]
            relationship = "positive" if original_val > 0 else "negative"
            strength = "strong" if abs(original_val) > 0.7 else "moderate" if abs(original_val) > 0.4 else "weak"
            
            st.markdown(f"- **{feature}**: Shows a **{strength} {relationship}** correlation ({original_val:.2f}) with Crime Rate.")
            
            if feature == 'School Quality Score' and original_val < 0:
                 st.caption("👉 Higher school quality is associated with lower crime rates.")
            elif feature == 'HARDSHIP INDEX' and original_val > 0:
                 st.caption("👉 Areas with higher hardship indices tend to have higher crime rates.")
            elif feature == 'PER CAPITA INCOME ' and original_val < 0:
                 st.caption("👉 Higher income areas tend to have lower crime rates.")

def render_eda_section(data, metrics):
    """Main function to render the EDA section."""
    st.title("📊 Exploratory Data Analysis")
    st.markdown("Analyzing the relationships between Safety, Education, and Socioeconomic factors across Chicago's community areas.")
    
    # Prepare Data
    df = prepare_eda_data(data, metrics)
    
    # 1. Visualization
    render_scatter_plots(df)
    
    # 2. Correlation
    corr = render_correlation_heatmap(df)
    
    # 3. Insights
    render_insights(corr)
    
    # Show Raw Data (Optional)
    with st.expander("View Consolidated Data"):
        st.dataframe(df)
