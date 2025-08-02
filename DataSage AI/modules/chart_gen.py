"""
Chart Generation Module for DataSage AI

This module provides automated chart generation based on data characteristics:
- Histograms for numeric distributions
- Scatter plots for relationships
- Bar charts for categorical data
- Box plots for outlier analysis
- Correlation heatmaps
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import warnings

warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

def generate_chart(df, chart_type="Auto (based on data)"):
    """
    Generate charts based on data characteristics and user selection
    
    Args:
        df (pandas.DataFrame): The dataset to visualize
        chart_type (str): Type of chart to generate
        
    Returns:
        matplotlib.figure.Figure: The generated chart figure
    """
    try:
        if chart_type == "Auto (based on data)":
            return _auto_generate_chart(df)
        elif chart_type == "Histogram":
            return _generate_histogram(df)
        elif chart_type == "Scatter Plot":
            return _generate_scatter_plot(df)
        elif chart_type == "Line Chart":
            return _generate_line_chart(df)
        elif chart_type == "Bar Chart":
            return _generate_bar_chart(df)
        elif chart_type == "Box Plot":
            return _generate_box_plot(df)
        elif chart_type == "Correlation Heatmap":
            return _generate_correlation_heatmap(df)
        else:
            st.warning(f"Unknown chart type: {chart_type}")
            return None
            
    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")
        return None

def _auto_generate_chart(df):
    """
    Automatically select and generate appropriate chart based on data characteristics
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Decision logic for automatic chart selection
    if len(numeric_cols) >= 2:
        # Generate correlation heatmap if multiple numeric columns
        return _generate_correlation_heatmap(df)
    elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
        # Generate box plot showing numeric by categorical
        return _generate_box_plot(df)
    elif len(numeric_cols) == 1:
        # Generate histogram for single numeric column
        return _generate_histogram(df)
    elif len(categorical_cols) >= 1:
        # Generate bar chart for categorical data
        return _generate_bar_chart(df)
    else:
        st.warning("No suitable columns found for visualization")
        return None

def _generate_histogram(df):
    """Generate histogram for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found for histogram")
        return None
    
    fig, axes = plt.subplots(
        nrows=(len(numeric_cols) + 2) // 3, 
        ncols=min(3, len(numeric_cols)), 
        figsize=(15, 5 * ((len(numeric_cols) + 2) // 3))
    )
    
    if len(numeric_cols) == 1:
        axes = [axes]
    elif len(numeric_cols) <= 3:
        axes = axes if hasattr(axes, '__iter__') else [axes]
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        if i < len(axes):
            axes[i].hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            axes[i].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
            axes[i].grid(True, alpha=0.3)
    
    # Hide empty subplots
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    return fig

def _generate_scatter_plot(df):
    """Generate scatter plot for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for scatter plot")
        return None
    
    # Select first two numeric columns or let user choose
    x_col = numeric_cols[0]
    y_col = numeric_cols[1]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create scatter plot
    scatter = ax.scatter(df[x_col], df[y_col], alpha=0.6, c='coral', s=50)
    
    # Add trend line
    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
    p = np.poly1d(z)
    ax.plot(df[x_col], p(df[x_col]), "r--", alpha=0.8, linewidth=2)
    
    ax.set_xlabel(x_col, fontweight='bold')
    ax.set_ylabel(y_col, fontweight='bold')
    ax.set_title(f'Scatter Plot: {x_col} vs {y_col}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add correlation coefficient
    corr = df[x_col].corr(df[y_col])
    ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    return fig

def _generate_line_chart(df):
    """Generate line chart for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found for line chart")
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot up to 5 numeric columns
    cols_to_plot = numeric_cols[:5]
    
    for col in cols_to_plot:
        ax.plot(df.index, df[col], marker='o', linewidth=2, label=col, alpha=0.8)
    
    ax.set_xlabel('Index', fontweight='bold')
    ax.set_ylabel('Values', fontweight='bold')
    ax.set_title('Line Chart of Numeric Columns', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def _generate_bar_chart(df):
    """Generate bar chart for categorical columns"""
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(categorical_cols) == 0:
        st.warning("No categorical columns found for bar chart")
        return None
    
    # Use first categorical column with reasonable number of unique values
    col = None
    for cat_col in categorical_cols:
        if df[cat_col].nunique() <= 20:
            col = cat_col
            break
    
    if col is None:
        st.warning("No suitable categorical column found (too many unique values)")
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    value_counts = df[col].value_counts()
    
    bars = ax.bar(range(len(value_counts)), value_counts.values, 
                  color='lightgreen', alpha=0.8, edgecolor='black')
    
    ax.set_xlabel(col, fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(value_counts)))
    ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def _generate_box_plot(df):
    """Generate box plot for numeric columns grouped by categorical"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(numeric_cols) == 0:
        st.warning("No numeric columns found for box plot")
        return None
    
    if len(categorical_cols) == 0:
        # Just box plots of numeric columns
        fig, ax = plt.subplots(figsize=(12, 6))
        
        box_data = [df[col].dropna() for col in numeric_cols[:5]]
        box_labels = list(numeric_cols[:5])
        
        bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)
        
        # Color the boxes
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        ax.set_title('Box Plot of Numeric Columns', fontsize=14, fontweight='bold')
        ax.set_ylabel('Values', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
    else:
        # Box plot of numeric by categorical
        numeric_col = numeric_cols[0]
        categorical_col = None
        
        # Find suitable categorical column
        for cat_col in categorical_cols:
            if df[cat_col].nunique() <= 10:
                categorical_col = cat_col
                break
        
        if categorical_col is None:
            categorical_col = categorical_cols[0]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create box plot
        unique_categories = df[categorical_col].unique()[:10]  # Limit to 10 categories
        box_data = [df[df[categorical_col] == cat][numeric_col].dropna() 
                   for cat in unique_categories]
        
        bp = ax.boxplot(box_data, labels=unique_categories, patch_artist=True)
        
        # Color the boxes
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_categories)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        ax.set_title(f'Box Plot: {numeric_col} by {categorical_col}', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel(categorical_col, fontweight='bold')
        ax.set_ylabel(numeric_col, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def _generate_correlation_heatmap(df):
    """Generate correlation heatmap for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for correlation heatmap")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    heatmap = sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm',
                         center=0, square=True, ax=ax, cbar_kws={"shrink": .8},
                         fmt='.2f', linewidths=0.5)
    
    ax.set_title('Correlation Matrix Heatmap', fontsize=16, fontweight='bold', pad=20)
    
    # Improve readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    return fig

def get_chart_recommendations(df):
    """
    Get chart recommendations based on data characteristics
    
    Args:
        df (pandas.DataFrame): The dataset to analyze
        
    Returns:
        list: List of recommended chart types with explanations
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    recommendations = []
    
    if len(numeric_cols) >= 2:
        recommendations.append({
            'chart_type': 'Correlation Heatmap',
            'reason': f'You have {len(numeric_cols)} numeric columns. A correlation heatmap will show relationships between variables.'
        })
        
        recommendations.append({
            'chart_type': 'Scatter Plot', 
            'reason': 'Scatter plots are great for exploring relationships between pairs of numeric variables.'
        })
    
    if len(numeric_cols) >= 1:
        recommendations.append({
            'chart_type': 'Histogram',
            'reason': 'Histograms show the distribution shape of your numeric variables.'
        })
        
        recommendations.append({
            'chart_type': 'Box Plot',
            'reason': 'Box plots help identify outliers and understand data spread.'
        })
    
    if len(categorical_cols) >= 1:
        suitable_cats = [col for col in categorical_cols if df[col].nunique() <= 20]
        if suitable_cats:
            recommendations.append({
                'chart_type': 'Bar Chart',
                'reason': f'Bar charts work well for categorical variables like {suitable_cats[0]}.'
            })
    
    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        recommendations.append({
            'chart_type': 'Box Plot',
            'reason': 'Box plots can show how numeric variables vary across categorical groups.'
        })
    
    return recommendations
