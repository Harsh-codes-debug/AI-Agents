"""
Natural Language Query Parser Module for DataSage AI

This module processes natural language queries about datasets and returns appropriate responses:
- Statistical queries (mean, median, count, etc.)
- Data exploration queries (columns, types, missing values)
- Filtering and aggregation queries
- Data quality assessment queries
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
from typing import Union, Any

def handle_query(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str, dict]:
    """
    Process natural language queries about the dataset
    
    Args:
        df (pandas.DataFrame): The dataset to query
        query (str): Natural language query
        
    Returns:
        Union[pd.DataFrame, str, dict]: Query result
    """
    try:
        query = query.lower().strip()
        
        # Null/missing value queries
        if any(keyword in query for keyword in ['null', 'missing', 'na', 'empty', 'blank']):
            return _handle_null_queries(df, query)
        
        # Data type queries
        elif any(keyword in query for keyword in ['type', 'dtype', 'data type']):
            return _handle_type_queries(df, query)
        
        # Statistical queries
        elif any(keyword in query for keyword in ['stat', 'mean', 'median', 'average', 'sum', 'count', 'max', 'min', 'std']):
            return _handle_statistical_queries(df, query)
        
        # Shape/size queries
        elif any(keyword in query for keyword in ['shape', 'size', 'dimension', 'rows', 'columns']):
            return _handle_shape_queries(df, query)
        
        # Column queries
        elif any(keyword in query for keyword in ['column', 'field', 'variable']):
            return _handle_column_queries(df, query)
        
        # Unique value queries
        elif any(keyword in query for keyword in ['unique', 'distinct', 'different']):
            return _handle_unique_queries(df, query)
        
        # Correlation queries
        elif any(keyword in query for keyword in ['corr', 'correlation', 'relationship', 'relate']):
            return _handle_correlation_queries(df, query)
        
        # Memory/info queries
        elif any(keyword in query for keyword in ['memory', 'info', 'information']):
            return _handle_info_queries(df, query)
        
        # Outlier queries
        elif any(keyword in query for keyword in ['outlier', 'anomal', 'extreme']):
            return _handle_outlier_queries(df, query)
        
        # Sample/head/tail queries
        elif any(keyword in query for keyword in ['sample', 'head', 'tail', 'first', 'last', 'random']):
            return _handle_sample_queries(df, query)
        
        # Duplicate queries
        elif any(keyword in query for keyword in ['duplicate', 'duplicated', 'repeat']):
            return _handle_duplicate_queries(df, query)
        
        else:
            return _handle_general_queries(df, query)
            
    except Exception as e:
        return f"❌ Error processing query: {str(e)}"

def _handle_null_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle queries about null/missing values"""
    if 'show' in query or 'display' in query:
        null_summary = pd.DataFrame({
            'Column': df.columns,
            'Null Count': df.isnull().sum(),
            'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2),
            'Data Type': df.dtypes.astype(str)
        })
        return null_summary
    
    elif 'count' in query:
        total_nulls = df.isnull().sum().sum()
        return f"Total missing values in dataset: {total_nulls:,}"
    
    elif 'percentage' in query or 'percent' in query:
        total_cells = df.shape[0] * df.shape[1]
        null_percentage = (df.isnull().sum().sum() / total_cells) * 100
        return f"Missing data percentage: {null_percentage:.2f}%"
    
    else:
        null_summary = pd.DataFrame({
            'Column': df.columns,
            'Null Count': df.isnull().sum(),
            'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        return null_summary

def _handle_type_queries(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Handle queries about data types"""
    type_summary = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count(),
        'Memory Usage (bytes)': df.memory_usage(deep=True).values[1:]  # Exclude index
    })
    return type_summary

def _handle_statistical_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle statistical queries"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return "No numeric columns found for statistical analysis."
    
    if 'basic' in query or 'summary' in query:
        return df[numeric_cols].describe()
    
    elif 'mean' in query or 'average' in query:
        means = df[numeric_cols].mean()
        return pd.DataFrame({'Column': means.index, 'Mean': means.values})
    
    elif 'median' in query:
        medians = df[numeric_cols].median()
        return pd.DataFrame({'Column': medians.index, 'Median': medians.values})
    
    elif 'std' in query or 'standard deviation' in query:
        stds = df[numeric_cols].std()
        return pd.DataFrame({'Column': stds.index, 'Standard Deviation': stds.values})
    
    elif 'max' in query or 'maximum' in query:
        maxs = df[numeric_cols].max()
        return pd.DataFrame({'Column': maxs.index, 'Maximum': maxs.values})
    
    elif 'min' in query or 'minimum' in query:
        mins = df[numeric_cols].min()
        return pd.DataFrame({'Column': mins.index, 'Minimum': mins.values})
    
    else:
        return df[numeric_cols].describe()

def _handle_shape_queries(df: pd.DataFrame, query: str) -> str:
    """Handle queries about dataset shape and size"""
    rows, cols = df.shape
    
    if 'rows' in query:
        return f"Number of rows: {rows:,}"
    elif 'columns' in query or 'cols' in query:
        return f"Number of columns: {cols}"
    else:
        return f"Dataset shape: {rows:,} rows × {cols} columns"

def _handle_column_queries(df: pd.DataFrame, query: str) -> Union[list, str]:
    """Handle queries about columns"""
    if 'list' in query or 'show' in query or 'name' in query:
        return f"Column names: {list(df.columns)}"
    elif 'count' in query:
        return f"Number of columns: {len(df.columns)}"
    else:
        return list(df.columns)

def _handle_unique_queries(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Handle queries about unique values"""
    # Extract column name if specified
    column_mentioned = None
    for col in df.columns:
        if col.lower() in query:
            column_mentioned = col
            break
    
    if column_mentioned:
        unique_count = df[column_mentioned].nunique()
        unique_vals = df[column_mentioned].unique()[:20]  # Show first 20 unique values
        return f"Column '{column_mentioned}' has {unique_count} unique values. First 20: {list(unique_vals)}"
    else:
        unique_summary = pd.DataFrame({
            'Column': df.columns,
            'Unique Count': [df[col].nunique() for col in df.columns],
            'Unique Percentage': [(df[col].nunique() / len(df) * 100) for col in df.columns]
        })
        unique_summary['Unique Percentage'] = unique_summary['Unique Percentage'].round(2)
        return unique_summary

def _handle_correlation_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle correlation queries"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return "Need at least 2 numeric columns for correlation analysis."
    
    corr_matrix = df[numeric_cols].corr()
    
    if 'strong' in query or 'high' in query:
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
            return pd.DataFrame(strong_corr)
        else:
            return "No strong correlations found (|r| > 0.7)"
    
    else:
        return corr_matrix

def _handle_info_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle general info queries"""
    memory_usage = df.memory_usage(deep=True).sum()
    
    info_summary = {
        'Dataset Shape': f"{df.shape[0]:,} rows × {df.shape[1]} columns",
        'Memory Usage': f"{memory_usage / 1024:.2f} KB",
        'Total Cells': f"{df.shape[0] * df.shape[1]:,}",
        'Missing Values': f"{df.isnull().sum().sum():,}",
        'Duplicate Rows': f"{df.duplicated().sum():,}",
        'Numeric Columns': len(df.select_dtypes(include=[np.number]).columns),
        'Categorical Columns': len(df.select_dtypes(include=['object', 'category']).columns)
    }
    
    return pd.DataFrame.from_dict(info_summary, orient='index', columns=['Value'])

def _handle_outlier_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle outlier detection queries"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return "No numeric columns found for outlier detection."
    
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
    
    return pd.DataFrame(outlier_summary)

def _handle_sample_queries(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Handle sample/head/tail queries"""
    # Extract number if specified
    numbers = re.findall(r'\d+', query)
    n = int(numbers[0]) if numbers else 5
    n = min(n, len(df))  # Don't exceed dataset size
    
    if 'tail' in query or 'last' in query:
        return df.tail(n)
    elif 'random' in query or 'sample' in query:
        return df.sample(n) if len(df) >= n else df
    else:  # head/first
        return df.head(n)

def _handle_duplicate_queries(df: pd.DataFrame, query: str) -> Union[pd.DataFrame, str]:
    """Handle duplicate-related queries"""
    duplicated_rows = df.duplicated()
    duplicate_count = duplicated_rows.sum()
    
    if 'count' in query:
        return f"Number of duplicate rows: {duplicate_count:,}"
    elif 'show' in query or 'display' in query:
        if duplicate_count > 0:
            return df[duplicated_rows]
        else:
            return "No duplicate rows found."
    else:
        return f"Duplicate analysis: {duplicate_count:,} duplicate rows found ({duplicate_count/len(df)*100:.2f}% of dataset)"

def _handle_general_queries(df: pd.DataFrame, query: str) -> str:
    """Handle general/unrecognized queries with helpful suggestions"""
    suggestions = [
        "Try these query examples:",
        "• 'Show null values' - Display missing data analysis",
        "• 'What are the data types?' - Show column data types", 
        "• 'Give me basic statistics' - Statistical summary of numeric columns",
        "• 'Show correlation between columns' - Correlation analysis",
        "• 'What are unique values in [column]?' - Unique value analysis",
        "• 'Show first 10 rows' - Display sample data",
        "• 'Find outliers' - Outlier detection",
        "• 'Show duplicates' - Duplicate row analysis"
    ]
    
    return "\n".join(suggestions)

def get_query_suggestions(df: pd.DataFrame) -> list:
    """
    Generate query suggestions based on dataset characteristics
    
    Args:
        df (pandas.DataFrame): The dataset to analyze
        
    Returns:
        list: List of suggested queries
    """
    suggestions = []
    
    # Basic data exploration
    suggestions.extend([
        "Show null values",
        "What are the data types?",
        "Give me basic statistics",
        "Show dataset shape"
    ])
    
    # Column-specific suggestions
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        suggestions.extend([
            "Find outliers",
            "Show correlation between columns"
        ])
    
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        first_cat_col = categorical_cols[0]
        suggestions.append(f"What are unique values in {first_cat_col}?")
    
    # Data quality suggestions
    if df.isnull().sum().sum() > 0:
        suggestions.append("Count missing values")
    
    if df.duplicated().sum() > 0:
        suggestions.append("Show duplicate rows")
    
    # Sample data suggestions
    suggestions.extend([
        "Show first 5 rows",
        "Show random sample"
    ])
    
    return suggestions[:10]  # Return top 10 suggestions
