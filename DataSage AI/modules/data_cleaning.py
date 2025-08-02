"""
Advanced Data Cleaning Module for DataSage AI

This module provides comprehensive data cleaning capabilities for data analysts:
- Automated data quality assessment
- Missing value handling strategies
- Outlier detection and treatment
- Data type optimization
- Duplicate handling
- Text data cleaning
- Data validation and profiling
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Any, Tuple, Optional
from scipy import stats
import warnings

class DataCleaner:
    """Advanced data cleaning and preprocessing for analysts"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with dataset"""
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []
        self.data_profile = {}
        
    def generate_data_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive data quality assessment"""
        report = {
            'dataset_info': {
                'shape': self.df.shape,
                'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                'columns': list(self.df.columns)
            },
            'missing_data': self._analyze_missing_data(),
            'duplicates': self._analyze_duplicates(),
            'data_types': self._analyze_data_types(),
            'outliers': self._detect_outliers(),
            'text_quality': self._analyze_text_quality(),
            'numeric_ranges': self._analyze_numeric_ranges(),
            'categorical_distribution': self._analyze_categorical_distribution()
        }
        
        # Calculate overall quality score
        report['quality_score'] = self._calculate_quality_score(report)
        
        return report
    
    def _analyze_missing_data(self) -> Dict[str, Any]:
        """Analyze missing data patterns"""
        missing_counts = self.df.isnull().sum()
        missing_percentages = (missing_counts / len(self.df)) * 100
        
        missing_patterns = {}
        for col in self.df.columns:
            if missing_counts[col] > 0:
                missing_patterns[col] = {
                    'count': int(missing_counts[col]),
                    'percentage': round(missing_percentages[col], 2),
                    'pattern': 'scattered'
                }
        
        return {
            'total_missing': int(missing_counts.sum()),
            'columns_with_missing': len(missing_patterns),
            'patterns': missing_patterns,
            'severity': 'high' if missing_percentages.max() > 30 else 'moderate' if missing_percentages.max() > 5 else 'low'
        }
    
    def _analyze_duplicates(self) -> Dict[str, Any]:
        """Analyze duplicate records"""
        duplicate_count = self.df.duplicated().sum()
        duplicate_percentage = (duplicate_count / len(self.df)) * 100
        
        return {
            'total_duplicates': int(duplicate_count),
            'percentage': round(duplicate_percentage, 2),
            'severity': 'high' if duplicate_percentage > 10 else 'moderate' if duplicate_percentage > 1 else 'low'
        }
    
    def _analyze_data_types(self) -> Dict[str, Any]:
        """Analyze data types and optimization opportunities"""
        type_analysis = {}
        
        for col in self.df.columns:
            current_type = str(self.df[col].dtype)
            memory_usage = self.df[col].memory_usage(deep=True)
            
            # Simple optimization suggestions
            optimization_possible = False
            suggested_type = current_type
            
            if current_type == 'object':
                unique_ratio = self.df[col].nunique() / len(self.df)
                if unique_ratio < 0.5:
                    suggested_type = 'category'
                    optimization_possible = True
            
            type_analysis[col] = {
                'current_type': current_type,
                'suggested_type': suggested_type,
                'memory_usage_bytes': int(memory_usage),
                'optimization_possible': optimization_possible
            }
        
        return type_analysis
    
    def _detect_outliers(self) -> Dict[str, Any]:
        """Detect outliers in numeric columns"""
        outliers = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                iqr_outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                
                # Z-score outliers
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                z_score_outliers = (z_scores > 3).sum()
                
                outliers[col] = {
                    'iqr_outliers': int(iqr_outliers),
                    'z_score_outliers': int(z_score_outliers),
                    'iqr_bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)},
                    'severity': 'high' if iqr_outliers > len(self.df) * 0.1 else 'moderate' if iqr_outliers > len(self.df) * 0.05 else 'low'
                }
            except Exception:
                outliers[col] = {
                    'iqr_outliers': 0,
                    'z_score_outliers': 0,
                    'iqr_bounds': {'lower': 0, 'upper': 0},
                    'severity': 'low'
                }
        
        return outliers
    
    def _analyze_text_quality(self) -> Dict[str, Any]:
        """Analyze text column quality"""
        text_quality = {}
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            try:
                whitespace_issues = self.df[col].astype(str).str.startswith(' ').sum() + self.df[col].astype(str).str.endswith(' ').sum()
                empty_strings = (self.df[col] == '').sum()
                unique_count = self.df[col].nunique()
                
                text_quality[col] = {
                    'whitespace_issues': int(whitespace_issues),
                    'empty_strings': int(empty_strings),
                    'potential_categories': int(unique_count),
                    'avg_length': round(self.df[col].astype(str).str.len().mean(), 2)
                }
            except Exception:
                text_quality[col] = {
                    'whitespace_issues': 0,
                    'empty_strings': 0,
                    'potential_categories': 0,
                    'avg_length': 0
                }
        
        return text_quality
    
    def _analyze_numeric_ranges(self) -> Dict[str, Any]:
        """Analyze numeric column ranges and characteristics"""
        ranges = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                ranges[col] = {
                    'min': float(self.df[col].min()),
                    'max': float(self.df[col].max()),
                    'mean': round(float(self.df[col].mean()), 2),
                    'median': round(float(self.df[col].median()), 2),
                    'std': round(float(self.df[col].std()), 2),
                    'negative_values': int((self.df[col] < 0).sum()),
                    'zero_values': int((self.df[col] == 0).sum())
                }
            except Exception:
                ranges[col] = {
                    'min': 0, 'max': 0, 'mean': 0, 'median': 0, 'std': 0,
                    'negative_values': 0, 'zero_values': 0
                }
        
        return ranges
    
    def _analyze_categorical_distribution(self) -> Dict[str, Any]:
        """Analyze categorical column distributions"""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        distributions = {}
        
        for col in categorical_cols:
            try:
                value_counts = self.df[col].value_counts()
                distributions[col] = {
                    'unique_count': int(self.df[col].nunique()),
                    'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else 'None',
                    'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                    'cardinality_ratio': round(self.df[col].nunique() / len(self.df), 3),
                    'potential_high_cardinality': self.df[col].nunique() > len(self.df) * 0.8
                }
            except Exception:
                distributions[col] = {
                    'unique_count': 0, 'most_frequent': 'None', 'most_frequent_count': 0,
                    'cardinality_ratio': 0, 'potential_high_cardinality': False
                }
        
        return distributions
    
    def suggest_cleaning_strategies(self) -> Dict[str, List[str]]:
        """Suggest cleaning strategies based on data quality analysis"""
        quality_report = self.generate_data_quality_report()
        suggestions = {
            'missing_data': [],
            'duplicates': [],
            'outliers': [],
            'data_types': [],
            'text_cleaning': [],
            'general': []
        }
        
        # Missing data suggestions
        for col, info in quality_report['missing_data']['patterns'].items():
            if info['percentage'] < 5:
                suggestions['missing_data'].append(f"Remove rows with missing {col} (low impact)")
            elif info['percentage'] < 30:
                suggestions['missing_data'].append(f"Impute {col} with median/mode (moderate missing)")
            else:
                suggestions['missing_data'].append(f"Consider dropping {col} or advanced imputation (high missing)")
        
        # Duplicate suggestions
        if quality_report['duplicates']['total_duplicates'] > 0:
            suggestions['duplicates'].append("Remove exact duplicate rows")
        
        # Outlier suggestions
        for col, info in quality_report['outliers'].items():
            if info['iqr_outliers'] > 0:
                suggestions['outliers'].append(f"Review {col} outliers - consider capping or removal")
        
        # Data type suggestions
        for col, info in quality_report['data_types'].items():
            if info['optimization_possible']:
                suggestions['data_types'].append(f"Convert {col} to {info['suggested_type']} for memory efficiency")
        
        return suggestions
    
    def auto_clean_data(self, strategies: List[str]) -> pd.DataFrame:
        """Apply automated cleaning based on strategies"""
        cleaned_df = self.df.copy()
        self.cleaning_log = []
        
        for strategy in strategies:
            if strategy == 'remove_duplicates':
                before_count = len(cleaned_df)
                cleaned_df = cleaned_df.drop_duplicates()
                after_count = len(cleaned_df)
                self.cleaning_log.append(f"Removed {before_count - after_count} duplicate rows")
            
            elif strategy == 'fix_data_types':
                # Simple data type optimization
                for col in cleaned_df.columns:
                    if cleaned_df[col].dtype == 'object':
                        unique_ratio = cleaned_df[col].nunique() / len(cleaned_df)
                        if unique_ratio < 0.5:
                            try:
                                cleaned_df[col] = cleaned_df[col].astype('category')
                                self.cleaning_log.append(f"Converted {col} to category type")
                            except Exception:
                                pass
            
            elif strategy == 'handle_missing_basic':
                for col in cleaned_df.columns:
                    missing_count = cleaned_df[col].isnull().sum()
                    if missing_count > 0:
                        missing_pct = (missing_count / len(cleaned_df)) * 100
                        
                        if missing_pct < 5:  # Low missing - remove rows
                            cleaned_df = cleaned_df.dropna(subset=[col])
                            self.cleaning_log.append(f"Removed {missing_count} rows with missing {col}")
                        elif cleaned_df[col].dtype in ['int64', 'float64']:  # Numeric - fill with median
                            median_val = cleaned_df[col].median()
                            cleaned_df[col].fillna(median_val, inplace=True)
                            self.cleaning_log.append(f"Filled missing values in {col} with median")
                        else:  # Categorical - fill with mode
                            mode_val = cleaned_df[col].mode().iloc[0] if len(cleaned_df[col].mode()) > 0 else 'Unknown'
                            cleaned_df[col].fillna(mode_val, inplace=True)
                            self.cleaning_log.append(f"Filled missing values in {col} with mode")
            
            elif strategy == 'clean_text':
                text_cols = cleaned_df.select_dtypes(include=['object']).columns
                for col in text_cols:
                    # Basic text cleaning
                    cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                    cleaned_df[col] = cleaned_df[col].replace('', np.nan)
                    self.cleaning_log.append(f"Cleaned text formatting in {col}")
            
            elif strategy == 'remove_outliers':
                numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    try:
                        Q1 = cleaned_df[col].quantile(0.25)
                        Q3 = cleaned_df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        before_count = len(cleaned_df)
                        cleaned_df = cleaned_df[(cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)]
                        after_count = len(cleaned_df)
                        
                        if before_count != after_count:
                            self.cleaning_log.append(f"Removed {before_count - after_count} outliers from {col}")
                    except Exception:
                        pass
        
        # Update internal dataframe for summary
        self.df = cleaned_df
        return cleaned_df
    
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Get summary of cleaning operations performed"""
        return {
            'original_shape': self.original_df.shape,
            'current_shape': self.df.shape,
            'rows_changed': self.original_df.shape[0] - self.df.shape[0],
            'columns_changed': self.original_df.shape[1] - self.df.shape[1],
            'cleaning_log': self.cleaning_log,
            'memory_optimization': {
                'original_mb': round(self.original_df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                'current_mb': round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                'savings_mb': round((self.original_df.memory_usage(deep=True).sum() - self.df.memory_usage(deep=True).sum()) / (1024 * 1024), 2)
            }
        }
    
    def _calculate_quality_score(self, report: Dict[str, Any]) -> int:
        """Calculate overall data quality score (0-100)"""
        score = 100
        
        # Deduct for missing data
        missing_penalty = min(report['missing_data']['total_missing'] / len(self.df) * 50, 30)
        score -= missing_penalty
        
        # Deduct for duplicates
        duplicate_penalty = min(report['duplicates']['percentage'] * 2, 20)
        score -= duplicate_penalty
        
        # Deduct for outliers
        try:
            total_outliers = sum(info['iqr_outliers'] for info in report['outliers'].values())
            outlier_penalty = min(total_outliers / len(self.df) * 30, 25)
            score -= outlier_penalty
        except Exception:
            pass
        
        # Deduct for suboptimal data types
        type_issues = sum(1 for info in report['data_types'].values() if info['optimization_possible'])
        type_penalty = min(type_issues * 2, 15)
        score -= type_penalty
        
        return max(0, int(score))