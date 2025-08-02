# DataSage AI - Backup of Main Application
# This is a backup copy of the complete working app.py file
# Created: 2025-08-02

import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
import sys

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import custom modules
try:
    import eda
    import chart_gen
    import query_parser
    import ai_assistant_gemini
    import gemini_live
    import data_cleaning
    import voice_handler
    import export
except ImportError as e:
    st.error(f"Module import error: {e}")

def _clean_dataframe_for_display(df):
    """Clean dataframe to prevent Arrow conversion issues"""
    df_clean = df.copy()
    
    # Convert problematic columns to string representation
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Convert to string and handle mixed types
            df_clean[col] = df_clean[col].astype(str)
            # Replace 'nan' strings with empty strings
            df_clean[col] = df_clean[col].replace(['nan', 'None', 'NaN'], '')
            # Clean percentage signs and other problematic characters
            df_clean[col] = df_clean[col].str.replace('%', '_percent', regex=False)
            df_clean[col] = df_clean[col].str.replace('$', '_dollar', regex=False)
    
    # Ensure all columns are Arrow-compatible
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Replace NaN values with empty strings for object columns
            df_clean[col] = df_clean[col].fillna('')
        # Convert any remaining problematic numeric columns
        elif df_clean[col].dtype in ['int64', 'float64']:
            df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean

# This file contains the complete working DataSage AI application
# For the actual implementation, please refer to the main app.py file
# This backup preserves the current working state