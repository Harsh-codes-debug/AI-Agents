"""
Exploratory Data Analysis Module for DataSage AI

This module provides comprehensive EDA functionality including:
- Statistical summaries
- Data quality assessment
- Missing value analysis
- Correlation analysis
- Data type analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

def show_eda(df):
    """
    Generate and display comprehensive EDA report
    
    Args:
        df (pandas.DataFrame): The dataset to analyze
    """
    try:
        st.markdown("### 📋 Dataset Overview")
        
        # Basic info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        with col4:
            st.metric("Duplicate Rows", df.duplicated().sum())
        
        # Data types analysis
        st.markdown("### 🔍 Data Types Analysis")
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum(),
            'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(dtype_df, use_container_width=True)
        
        # Missing values visualization
        if df.isnull().sum().sum() > 0:
            st.markdown("### ❗ Missing Values Analysis")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
            
            if len(missing_data) > 0:
                missing_data.plot(kind='bar', ax=ax, color='coral')
                ax.set_title('Missing Values by Column')
                ax.set_xlabel('Columns')
                ax.set_ylabel('Number of Missing Values')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.success("✅ No missing values found in the dataset!")
        
        # Statistical summary for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.markdown("### 📊 Statistical Summary (Numeric Columns)")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            
            # Distribution plots for numeric columns
            st.markdown("### 📈 Distribution Analysis")
            
            if len(numeric_cols) <= 4:
                cols = st.columns(len(numeric_cols))
                for i, col in enumerate(numeric_cols):
                    with cols[i]:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        df[col].hist(bins=20, ax=ax, alpha=0.7, color='skyblue')
                        ax.set_title(f'Distribution of {col}')
                        ax.set_xlabel(col)
                        ax.set_ylabel('Frequency')
                        st.pyplot(fig)
            else:
                selected_cols = st.multiselect(
                    "Select columns to visualize distributions:", 
                    numeric_cols, 
                    default=list(numeric_cols[:3])
                )
                
                if selected_cols:
                    cols = st.columns(min(3, len(selected_cols)))
                    for i, col in enumerate(selected_cols):
                        with cols[i % 3]:
                            fig, ax = plt.subplots(figsize=(6, 4))
                            df[col].hist(bins=20, ax=ax, alpha=0.7, color='skyblue')
                            ax.set_title(f'Distribution of {col}')
                            ax.set_xlabel(col)
                            ax.set_ylabel('Frequency')
                            st.pyplot(fig)
        
        # Categorical columns analysis
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            st.markdown("### 🏷️ Categorical Variables Analysis")
            
            for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                st.markdown(f"**{col}**")
                unique_count = df[col].nunique()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Unique Values", unique_count)
                    if unique_count <= 20:
                        st.write("Value Counts:")
                        st.dataframe(df[col].value_counts().head(10))
                
                with col2:
                    if unique_count <= 10:
                        fig, ax = plt.subplots(figsize=(8, 6))
                        df[col].value_counts().plot(kind='bar', ax=ax, color='lightgreen')
                        ax.set_title(f'Distribution of {col}')
                        ax.set_xlabel(col)
                        ax.set_ylabel('Count')
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
        
        # Correlation analysis
        if len(numeric_cols) > 1:
            st.markdown("### 🔗 Correlation Analysis")
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Create correlation heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', 
                       center=0, square=True, ax=ax, cbar_kws={"shrink": .8})
            ax.set_title('Correlation Matrix')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Find strong correlations
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': round(corr_val, 3)
                        })
            
            if strong_corr:
                st.markdown("**Strong Correlations (|r| > 0.7):**")
                st.dataframe(pd.DataFrame(strong_corr))
            else:
                st.info("No strong correlations found (|r| > 0.7)")
        
        # Outlier detection
        if len(numeric_cols) > 0:
            st.markdown("### 🎯 Outlier Detection")
            
            outlier_summary = []
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(df)) * 100
                
                outlier_summary.append({
                    'Column': col,
                    'Outlier Count': outlier_count,
                    'Outlier Percentage': f"{outlier_percentage:.2f}%",
                    'Lower Bound': round(lower_bound, 2),
                    'Upper Bound': round(upper_bound, 2)
                })
            
            outlier_df = pd.DataFrame(outlier_summary)
            st.dataframe(outlier_df, use_container_width=True)
        
        # Data quality summary
        st.markdown("### ✅ Data Quality Summary")
        
        quality_metrics = {
            'Total Records': len(df),
            'Complete Records': len(df.dropna()),
            'Completeness': f"{(len(df.dropna()) / len(df) * 100):.1f}%",
            'Duplicate Records': df.duplicated().sum(),
            'Uniqueness': f"{((len(df) - df.duplicated().sum()) / len(df) * 100):.1f}%"
        }
        
        quality_df = pd.DataFrame.from_dict(quality_metrics, orient='index', columns=['Value'])
        st.dataframe(quality_df, use_container_width=True)
        
        st.success("✅ EDA Report generated successfully!")
        
    except Exception as e:
        st.error(f"Error generating EDA report: {str(e)}")
        st.info("Please ensure your data is in the correct format and try again.")

def get_data_summary(df):
    """
    Get a quick data summary for AI processing
    
    Args:
        df (pandas.DataFrame): The dataset to summarize
        
    Returns:
        dict: Summary statistics and information
    """
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'numeric_columns': list(numeric_cols),
            'categorical_columns': list(categorical_cols),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'basic_stats': df.describe().to_dict() if len(numeric_cols) > 0 else {}
        }
        
        return summary
    except Exception as e:
        return {'error': f"Failed to generate summary: {str(e)}"}
