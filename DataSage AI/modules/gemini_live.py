"""
Gemini Live AI Assistant Module for DataSage AI

This module provides real-time conversational AI capabilities similar to Gemini Live:
- Streaming response generation
- Real-time voice interaction
- Contextual conversation memory
- Advanced natural language understanding
- Live data analysis capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time
import asyncio
from typing import Dict, List, Any, Optional, Generator
from google import genai
from google.genai import types
import threading
from datetime import datetime

class GeminiLiveAssistant:
    """Gemini Live-style AI Assistant with real-time capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini Live Assistant"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model = "gemini-2.5-flash"
        self.df = None
        self.conversation_context = []
        self.data_summary = {}
        self.is_streaming = False
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self._initialize_live_context()
            except Exception as e:
                st.error(f"Failed to initialize Gemini Live client: {str(e)}")
                self.client = None
        else:
            st.warning("⚠️ Gemini API key not found. Live AI features unavailable.")
    
    def _initialize_live_context(self):
        """Initialize the live conversation context"""
        self.conversation_context = [
            {
                "role": "system",
                "content": """You are DataSage AI Live, an advanced AI data analyst assistant similar to Gemini Live. 

Key characteristics:
- Conversational and natural like you're speaking with a colleague
- Provide real-time insights and analysis
- Ask clarifying questions when needed
- Maintain context throughout the conversation
- Be proactive in suggesting analysis directions
- Respond in a streaming, conversational manner
- Use everyday language, avoiding overly technical jargon
- Show enthusiasm for data discoveries

When analyzing data:
- Think out loud about patterns you notice
- Suggest next steps and follow-up questions
- Provide actionable insights
- Explain your reasoning process
- Connect findings to business implications"""
            }
        ]
    
    def is_available(self) -> bool:
        """Check if Live AI assistant is available"""
        return self.client is not None
    
    def set_dataset(self, df: pd.DataFrame) -> None:
        """Set the dataset for live analysis"""
        self.df = df
        self.data_summary = self._generate_live_data_summary()
        self._update_context_with_data()
    
    def _generate_live_data_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive data summary for live context"""
        if self.df is None:
            return {}
        
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
            
            summary = {
                'timestamp': datetime.now().isoformat(),
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'numeric_columns': list(numeric_cols),
                'categorical_columns': list(categorical_cols),
                'missing_values': self.df.isnull().sum().to_dict(),
                'data_types': self.df.dtypes.astype(str).to_dict(),
                'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                'duplicate_rows': int(self.df.duplicated().sum())
            }
            
            # Enhanced statistics for live analysis
            if len(numeric_cols) > 0:
                summary['statistics'] = {}
                for col in numeric_cols[:10]:  # Top 10 numeric columns
                    col_stats = self.df[col].describe()
                    summary['statistics'][col] = {
                        'mean': round(col_stats['mean'], 2),
                        'median': round(col_stats['50%'], 2),
                        'std': round(col_stats['std'], 2),
                        'min': col_stats['min'],
                        'max': col_stats['max'],
                        'range': round(col_stats['max'] - col_stats['min'], 2)
                    }
            
            # Categorical insights
            if len(categorical_cols) > 0:
                summary['categorical_insights'] = {}
                for col in categorical_cols[:5]:
                    unique_count = self.df[col].nunique()
                    most_common = self.df[col].mode().iloc[0] if len(self.df[col].mode()) > 0 else "N/A"
                    summary['categorical_insights'][col] = {
                        'unique_count': unique_count,
                        'most_common': str(most_common),
                        'diversity_ratio': round(unique_count / len(self.df), 3)
                    }
            
            return summary
            
        except Exception as e:
            st.error(f"Error generating live data summary: {str(e)}")
            return {}
    
    def _update_context_with_data(self):
        """Update conversation context with current dataset information"""
        if not self.data_summary:
            return
        
        data_context = {
            "role": "assistant", 
            "content": f"""I now have access to your dataset! Here's what I can see:

Dataset Overview:
- {self.data_summary['shape'][0]} rows and {self.data_summary['shape'][1]} columns
- {len(self.data_summary.get('numeric_columns', []))} numeric columns
- {len(self.data_summary.get('categorical_columns', []))} categorical columns
- {sum(self.data_summary.get('missing_values', {}).values())} total missing values
- {self.data_summary.get('duplicate_rows', 0)} duplicate rows

I'm ready to dive deep into your data! What would you like to explore first? I can help with:
- Finding interesting patterns and trends
- Identifying data quality issues
- Suggesting visualizations
- Uncovering business insights
- Recommending next steps for analysis

What catches your interest about this dataset?"""
        }
        
        self.conversation_context.append(data_context)
    
    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        """Generate streaming response like Gemini Live"""
        if not self.is_available():
            yield "I'm sorry, but I'm not able to connect to the AI service right now. Please check your API key."
            return
        
        if self.df is None:
            yield "I'd love to help, but I don't see any data loaded yet. Could you upload a dataset first?"
            return
        
        try:
            # Add user input to conversation context
            self.conversation_context.append({
                "role": "user",
                "content": user_input
            })
            
            # Prepare enhanced prompt with live context
            live_prompt = self._build_live_prompt(user_input)
            
            if self.client is None:
                yield "AI service unavailable"
                return
            
            # Generate streaming response
            response = self.client.models.generate_content(
                model=self.model,
                contents=live_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=2048,
                    candidate_count=1
                )
            )
            
            if response.text:
                # Simulate streaming by yielding chunks
                full_response = response.text
                words = full_response.split()
                
                current_chunk = ""
                for i, word in enumerate(words):
                    current_chunk += word + " "
                    
                    # Yield chunks of 3-5 words for natural streaming effect
                    if (i + 1) % 4 == 0 or i == len(words) - 1:
                        yield current_chunk.strip()
                        current_chunk = ""
                        time.sleep(0.1)  # Small delay for streaming effect
                
                # Add response to conversation context
                self.conversation_context.append({
                    "role": "assistant",
                    "content": full_response
                })
                
                # Trim context if it gets too long
                if len(self.conversation_context) > 20:
                    # Keep system prompt and recent 15 messages
                    self.conversation_context = self.conversation_context[:1] + self.conversation_context[-15:]
            else:
                yield "I'm having trouble generating a response right now. Could you try rephrasing your question?"
                
        except Exception as e:
            yield f"I encountered an error: {str(e)}. Let me try a different approach if you'd like to rephrase your question."
    
    def _build_live_prompt(self, user_input: str) -> str:
        """Build enhanced prompt for live conversation"""
        
        # Recent conversation context (last 5 exchanges)
        recent_context = ""
        if len(self.conversation_context) > 1:
            for msg in self.conversation_context[-10:]:
                if msg["role"] == "user":
                    recent_context += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    recent_context += f"Assistant: {msg['content']}\n"
        
        # Current data insights
        current_insights = self._get_current_data_insights()
        
        prompt = f"""You are DataSage AI Live, having a natural conversation about data analysis.

Current Dataset Context:
{json.dumps(self.data_summary, indent=2)}

Recent Conversation:
{recent_context}

Current Data Insights:
{current_insights}

User's Current Question: {user_input}

Respond naturally and conversationally, as if you're a knowledgeable data analyst colleague. Be:
- Enthusiastic about findings
- Clear in explanations
- Proactive in suggesting next steps
- Focused on actionable insights
- Natural in conversation flow

Provide specific insights about the data when relevant, and ask follow-up questions to guide the analysis forward."""
        
        return prompt
    
    def _get_current_data_insights(self) -> str:
        """Generate current insights about the dataset"""
        if not self.data_summary:
            return "No data insights available."
        
        insights = []
        
        # Data quality insights
        missing_values = sum(self.data_summary.get('missing_values', {}).values())
        if missing_values > 0:
            insights.append(f"Data has {missing_values} missing values that might need attention")
        
        # Duplicate insights
        duplicates = self.data_summary.get('duplicate_rows', 0)
        if duplicates > 0:
            insights.append(f"Found {duplicates} duplicate rows in the dataset")
        
        # Column distribution insights
        num_numeric = len(self.data_summary.get('numeric_columns', []))
        num_categorical = len(self.data_summary.get('categorical_columns', []))
        
        if num_numeric > num_categorical:
            insights.append("Dataset is primarily numeric - good for statistical analysis and modeling")
        elif num_categorical > num_numeric:
            insights.append("Dataset is primarily categorical - good for segmentation and classification")
        
        # Statistical insights
        if 'statistics' in self.data_summary:
            for col, stats in list(self.data_summary['statistics'].items())[:3]:
                if stats['std'] > stats['mean']:
                    insights.append(f"Column '{col}' shows high variability (std > mean)")
        
        return "; ".join(insights) if insights else "Dataset appears clean and ready for analysis"
    
    def get_quick_actions(self) -> List[Dict[str, str]]:
        """Get quick action suggestions for live interaction"""
        return [
            {"text": "What patterns do you see?", "action": "analyze_patterns"},
            {"text": "Find outliers in my data", "action": "find_outliers"}, 
            {"text": "Suggest visualizations", "action": "suggest_viz"},
            {"text": "Check data quality", "action": "quality_check"},
            {"text": "What insights can you find?", "action": "generate_insights"},
            {"text": "Help me clean this data", "action": "suggest_cleaning"}
        ]
    
    def get_proactive_suggestions(self) -> List[str]:
        """Get proactive suggestions based on current data"""
        if not self.data_summary:
            return []
        
        suggestions = []
        
        # Based on data characteristics
        if len(self.data_summary.get('numeric_columns', [])) >= 2:
            suggestions.append("I notice you have multiple numeric columns - shall we explore correlations?")
        
        if self.data_summary.get('duplicate_rows', 0) > 0:
            suggestions.append("I see some duplicate rows - would you like me to help clean them up?")
        
        missing_values = sum(self.data_summary.get('missing_values', {}).values())
        if missing_values > 0:
            suggestions.append("There are some missing values - let's discuss strategies to handle them.")
        
        if len(self.data_summary.get('categorical_columns', [])) > 0:
            suggestions.append("Your categorical data might reveal interesting segments - want to explore?")
        
        return suggestions[:2]  # Return top 2 suggestions
    
    def analyze_user_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze user intent for better responses"""
        intent_keywords = {
            'visualization': ['chart', 'plot', 'graph', 'visualize', 'show', 'display'],
            'statistics': ['mean', 'average', 'median', 'std', 'statistics', 'summary'],
            'patterns': ['pattern', 'trend', 'relationship', 'correlation', 'connection'],
            'quality': ['missing', 'null', 'duplicate', 'clean', 'quality', 'outlier'],
            'exploration': ['explore', 'understand', 'overview', 'insight', 'discover'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'between']
        }
        
        user_lower = user_input.lower()
        detected_intents = []
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return {
            'primary_intent': detected_intents[0] if detected_intents else 'general',
            'all_intents': detected_intents,
            'confidence': len(detected_intents) / len(intent_keywords)
        }

def create_gemini_live_assistant() -> Optional[GeminiLiveAssistant]:
    """Factory function to create Gemini Live assistant"""
    try:
        assistant = GeminiLiveAssistant()
        if assistant.is_available():
            return assistant
        else:
            st.warning("🤖 Gemini Live unavailable: Please set GEMINI_API_KEY environment variable")
            return None
    except Exception as e:
        st.error(f"Failed to create Gemini Live assistant: {str(e)}")
        return None