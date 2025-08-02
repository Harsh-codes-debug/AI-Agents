"""
DataSage AI Modules Package

This package contains all the core functionality modules for DataSage AI:
- eda: Exploratory Data Analysis
- chart_gen: Chart Generation
- query_parser: Natural Language Query Processing  
- ai_assistant_gemini: AI Assistant with Gemini Integration
- voice_handler: Voice Command Processing
- export: Data Export and Report Generation
"""

__version__ = "1.0.0"
__author__ = "DataSage AI Team"

# Import all modules for easy access
from . import eda
from . import chart_gen
from . import query_parser
from . import ai_assistant_gemini
from . import voice_handler
from . import export

__all__ = [
    'eda',
    'chart_gen', 
    'query_parser',
    'ai_assistant_gemini',
    'voice_handler',
    'export'
]
