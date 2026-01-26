import pandas as pd

def safe_numeric(series):
    """Convert series to numeric, handling percentages and errors."""
    if series.dtype == 'object':
        series = series.str.rstrip('%').astype(float, errors='ignore')
    return pd.to_numeric(series, errors='coerce')
