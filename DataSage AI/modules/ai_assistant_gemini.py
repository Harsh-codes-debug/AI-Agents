"""
AI Assistant Module with Google Gemini Integration for DataSage AI

This module provides advanced AI-powered data analysis capabilities using Google's Gemini AI:
- Natural language query processing
- Automated insight generation
- Data cleaning suggestions
- Predictive analytics recommendations
- Comprehensive AI-powered reporting
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List, Any, Optional, Union
from google import genai
from google.genai import types

class GeminiAIAssistant:
    """AI Assistant powered by Google Gemini for data analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini AI Assistant
        
        Args:
            api_key (str, optional): Gemini API key. If None, will use environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.df = None
        self.data_summary = {}
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.model = "gemini-2.5-flash"
            except Exception as e:
                st.error(f"Failed to initialize Gemini client: {str(e)}")
                self.client = None
        else:
            st.warning("⚠️ Gemini API key not found. AI features will be limited.")
    
    def is_available(self) -> bool:
        """Check if AI assistant is available"""
        return self.client is not None
    
    def set_dataset(self, df: pd.DataFrame) -> None:
        """Set the dataset for analysis"""
        self.df = df
        self.data_summary = self._generate_data_summary()
    
    def _generate_data_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the dataset for AI processing"""
        if self.df is None:
            return {}
        
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
            
            summary = {
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'numeric_columns': list(numeric_cols),
                'categorical_columns': list(categorical_cols),
                'missing_values': self.df.isnull().sum().to_dict(),
                'data_types': self.df.dtypes.astype(str).to_dict(),
                'memory_usage_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
                'duplicate_rows': int(self.df.duplicated().sum())
            }
            
            # Add basic statistics for numeric columns
            if len(numeric_cols) > 0:
                summary['basic_stats'] = self.df[numeric_cols].describe().to_dict()
            
            # Add categorical summaries
            if len(categorical_cols) > 0:
                cat_summary = {}
                for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                    cat_summary[col] = {
                        'unique_count': int(self.df[col].nunique()),
                        'top_values': self.df[col].value_counts().head(5).to_dict()
                    }
                summary['categorical_summary'] = cat_summary
            
            return summary
            
        except Exception as e:
            st.error(f"Error generating data summary: {str(e)}")
            return {}
    
    def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language queries about the dataset using Gemini AI
        
        Args:
            query (str): Natural language query
            
        Returns:
            Dict[str, Any]: AI response with insights and recommendations
        """
        if not self.is_available():
            return {
                "error": "AI assistant not available. Please check your Gemini API key.",
                "fallback": "Try using the Query Data tab for basic data exploration."
            }
        
        if self.df is None:
            return {"error": "No dataset loaded. Please upload a CSV file first."}
        
        try:
            # Prepare context for AI
            context = self._prepare_context_for_ai()
            
            # Create comprehensive prompt
            prompt = f"""
            You are an expert data analyst assistant. A user has uploaded a dataset and asked: "{query}"

            Dataset Summary:
            {json.dumps(context, indent=2)}

            Please provide a comprehensive analysis addressing the user's query. Include:
            1. Direct answer to their question
            2. Key insights related to the query
            3. Actionable recommendations
            4. Any data quality concerns or opportunities

            Format your response as JSON with these fields:
            - "message": Your main response to the query
            - "insights": Array of key insights (max 5)
            - "recommendations": Array of actionable recommendations (max 5)
            - "data_quality_notes": Any important data quality observations
            """
            
            # Generate response using Gemini
            if self.client is None:
                return {"error": "AI client not initialized"}
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048
                )
            )
            
            # Parse response
            if response.text:
                try:
                    # Try to parse as JSON
                    ai_response = json.loads(response.text)
                    return ai_response
                except json.JSONDecodeError:
                    # If not valid JSON, return as simple message
                    return {
                        "message": response.text,
                        "insights": [],
                        "recommendations": []
                    }
            else:
                return {"error": "No response from AI assistant."}
                
        except Exception as e:
            return {
                "error": f"AI processing error: {str(e)}",
                "fallback": "Try rephrasing your question or use the Query Data tab for basic analysis."
            }
    
    def generate_automated_insights(self) -> Dict[str, Any]:
        """Generate automated insights about the dataset"""
        if not self.is_available():
            return {"error": "AI assistant not available."}
        
        if self.df is None:
            return {"error": "No dataset loaded."}
        
        try:
            context = self._prepare_context_for_ai()
            
            prompt = f"""
            As a senior data scientist, analyze this dataset and provide automated insights:

            Dataset Summary:
            {json.dumps(context, indent=2)}

            Generate comprehensive insights about:
            1. Data distribution patterns
            2. Correlation insights
            3. Data quality assessment
            4. Potential outliers or anomalies
            5. Business implications

            Format as JSON with:
            - "insights": Array of key insights (max 8)
            - "patterns": Array of interesting patterns found
            - "recommendations": Next steps for analysis
            """
            
            if self.client is None:
                return {"error": "AI client not initialized"}
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.8)
            )
            
            if response.text:
                try:
                    return json.loads(response.text)
                except json.JSONDecodeError:
                    return {"insights": [response.text]}
            else:
                return {"error": "No insights generated."}
                
        except Exception as e:
            return {"error": f"Error generating insights: {str(e)}"}
    
    def suggest_data_cleaning(self) -> Dict[str, Any]:
        """Suggest data cleaning operations based on dataset analysis"""
        if not self.is_available():
            return {"error": "AI assistant not available."}
        
        if self.df is None:
            return {"error": "No dataset loaded."}
        
        try:
            context = self._prepare_context_for_ai()
            
            prompt = f"""
            As a data preprocessing expert, analyze this dataset and suggest cleaning operations:

            Dataset Summary:
            {json.dumps(context, indent=2)}

            Provide specific recommendations for:
            1. Missing value treatment
            2. Outlier handling
            3. Data type conversions
            4. Duplicate row handling
            5. Data standardization/normalization
            6. Feature engineering opportunities

            Format as JSON with:
            - "cleaning_steps": Array of specific cleaning recommendations
            - "priority": High/Medium/Low priority items
            - "rationale": Explanation for each recommendation
            """
            
            if self.client is None:
                return {"error": "AI client not initialized"}
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.6)
            )
            
            if response.text:
                try:
                    return json.loads(response.text)
                except json.JSONDecodeError:
                    return {"cleaning_steps": [response.text]}
            else:
                return {"error": "No cleaning suggestions generated."}
                
        except Exception as e:
            return {"error": f"Error generating cleaning suggestions: {str(e)}"}
    
    def predict_trends(self) -> Dict[str, Any]:
        """Suggest predictive analytics approaches for the dataset"""
        if not self.is_available():
            return {"error": "AI assistant not available."}
        
        if self.df is None:
            return {"error": "No dataset loaded."}
        
        try:
            context = self._prepare_context_for_ai()
            
            prompt = f"""
            As a predictive analytics expert, analyze this dataset and suggest modeling approaches:

            Dataset Summary:
            {json.dumps(context, indent=2)}

            Suggest:
            1. Potential target variables for prediction
            2. Appropriate machine learning algorithms
            3. Feature engineering opportunities
            4. Time series analysis potential (if applicable)
            5. Classification vs regression opportunities
            6. Business value of predictions

            Format as JSON with:
            - "prediction_opportunities": Array of modeling suggestions
            - "recommended_algorithms": Suitable ML algorithms
            - "feature_engineering": Ideas for new features
            - "business_value": How predictions could add value
            """
            
            if self.client is None:
                return {"error": "AI client not initialized"}
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7)
            )
            
            if response.text:
                try:
                    return json.loads(response.text)
                except json.JSONDecodeError:
                    return {"prediction_opportunities": [response.text]}
            else:
                return {"error": "No trend predictions generated."}
                
        except Exception as e:
            return {"error": f"Error generating trend predictions: {str(e)}"}
    
    def generate_ai_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive AI-powered summary report"""
        if not self.is_available():
            return {"error": "AI assistant not available."}
        
        if self.df is None:
            return {"error": "No dataset loaded."}
        
        try:
            context = self._prepare_context_for_ai()
            
            prompt = f"""
            Create a comprehensive executive summary of this dataset as a senior data analyst:

            Dataset Summary:
            {json.dumps(context, indent=2)}

            Generate a professional report covering:
            1. Executive Summary
            2. Data Overview & Quality Assessment
            3. Key Findings & Insights
            4. Statistical Highlights
            5. Data Quality Issues & Recommendations
            6. Business Implications
            7. Next Steps for Analysis

            Write in a professional, clear style suitable for stakeholders.
            """
            
            if self.client is None:
                return {"error": "AI client not initialized"}
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    max_output_tokens=3000
                )
            )
            
            if response.text:
                return {"report": response.text}
            else:
                return {"error": "No summary report generated."}
                
        except Exception as e:
            return {"error": f"Error generating summary report: {str(e)}"}
    
    def _prepare_context_for_ai(self) -> Dict[str, Any]:
        """Prepare dataset context for AI processing"""
        if not self.data_summary:
            return {}
        
        # Create a focused context for AI
        context = {
            "dataset_shape": f"{self.data_summary['shape'][0]} rows, {self.data_summary['shape'][1]} columns",
            "column_types": {
                "numeric": len(self.data_summary.get('numeric_columns', [])),
                "categorical": len(self.data_summary.get('categorical_columns', []))
            },
            "data_quality": {
                "missing_values_total": sum(self.data_summary.get('missing_values', {}).values()),
                "duplicate_rows": self.data_summary.get('duplicate_rows', 0),
                "memory_usage_mb": round(self.data_summary.get('memory_usage_mb', 0), 2)
            }
        }
        
        # Add sample statistics for numeric columns
        if 'basic_stats' in self.data_summary:
            context["numeric_statistics"] = {
                col: {
                    "mean": round(stats.get('mean', 0), 2),
                    "std": round(stats.get('std', 0), 2),
                    "min": stats.get('min', 0),
                    "max": stats.get('max', 0)
                }
                for col, stats in list(self.data_summary['basic_stats'].items())[:5]
            }
        
        # Add categorical summaries
        if 'categorical_summary' in self.data_summary:
            context["categorical_info"] = self.data_summary['categorical_summary']
        
        # Add columns list (limited)
        context["columns"] = self.data_summary.get('columns', [])[:10]
        
        return context

def create_ai_assistant() -> Optional[GeminiAIAssistant]:
    """
    Factory function to create AI assistant instance
    
    Returns:
        GeminiAIAssistant: Initialized AI assistant or None if unavailable
    """
    try:
        assistant = GeminiAIAssistant()
        if assistant.is_available():
            return assistant
        else:
            st.warning("🤖 AI Assistant unavailable: Please set GEMINI_API_KEY environment variable")
            return None
    except Exception as e:
        st.error(f"Failed to create AI assistant: {str(e)}")
        return None

def get_ai_query_examples() -> List[str]:
    """Get example queries for AI assistant"""
    return [
        "What are the main patterns in this data?",
        "Identify any data quality issues",
        "What insights can you provide about this dataset?",
        "Suggest ways to improve this data",
        "What predictions could I make with this data?",
        "Summarize the key findings from this dataset",
        "What correlations should I investigate?",
        "Are there any outliers I should be concerned about?",
        "What business insights can you extract?",
        "How can I clean and improve this dataset?"
    ]
