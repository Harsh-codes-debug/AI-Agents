# DataSage AI

## Overview

DataSage AI is a comprehensive Streamlit-based web application that provides AI-powered data analysis capabilities for CSV datasets. The application features a revolutionary Gemini Live-style AI assistant that offers real-time conversational data analysis, streaming responses, and natural voice-like interactions. It combines automated exploratory data analysis, interactive visualizations, natural language querying, and AI-driven insights to make data analysis accessible to users without extensive technical expertise. The application features a modular architecture with Google Gemini AI integration, enhanced live conversation capabilities, and professional report generation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework providing a responsive single-page interface
- **Layout**: Wide page layout with expandable sidebar for file operations and main content area for analysis results
- **Styling**: Custom CSS dark mode theme with gradient backgrounds and modern typography using Inter font family
- **Navigation**: Sidebar-based navigation for data upload, configuration, and demo dataset access
- **Interactive Elements**: Drag-and-drop file upload, sortable data tables, and one-click analysis buttons

### Backend Architecture
- **Modular Design**: Core functionality separated into six specialized modules for maintainability and scalability
- **Data Processing Pipeline**: Pandas-based data manipulation with automatic validation and type detection
- **Session Management**: Streamlit session state for maintaining application state and user data across interactions
- **Error Handling**: Comprehensive error handling with graceful fallbacks for missing dependencies

### Core Modules
- **EDA Module**: Comprehensive exploratory data analysis including statistical summaries, data quality assessment, missing value analysis, correlation analysis, and data type profiling
- **Chart Generation Module**: Automated visualization creation with intelligent chart selection based on data characteristics, supporting histograms, scatter plots, line charts, bar charts, box plots, and correlation heatmaps
- **Query Parser Module**: Natural language interface for data queries using regex pattern matching to handle statistical operations, data exploration, and quality assessment queries
- **AI Assistant Module**: Google Gemini AI integration (gemini-2.5-flash model) for advanced natural language processing, automated insights generation, data cleaning suggestions, and predictive analytics recommendations
- **Gemini Live Module**: Revolutionary real-time conversational AI assistant with streaming responses, contextual memory, intent analysis, proactive suggestions, and natural voice-like interaction patterns similar to Gemini Live
- **Data Cleaning Module**: Professional-grade data cleaning and quality assessment tools for data analysts, including automated data quality scoring, outlier detection, missing value analysis, and comprehensive cleaning strategies
- **Voice Handler Module**: Speech recognition and text-to-speech capabilities with graceful fallbacks for cloud deployments where voice libraries may not be available
- **Export Module**: Comprehensive export functionality supporting CSV, Excel, and PDF report generation with professional formatting and charts

### Data Processing Architecture
- **File Upload System**: CSV file processing through Streamlit's file uploader with validation and detailed file information display
- **Demo Data Integration**: Built-in sample dataset functionality for testing and demonstration purposes
- **Data Validation Pipeline**: Automatic data type detection, missing value analysis, duplicate detection, and memory usage assessment
- **Statistical Analysis Engine**: Comprehensive statistical profiling using SciPy for advanced statistical functions and NumPy for numerical computations

### Visualization Architecture
- **Chart Generation Engine**: Matplotlib and Seaborn integration for publication-quality visualizations
- **Auto-Selection Logic**: Intelligent chart recommendation system based on data characteristics and column types
- **Styling System**: Consistent visual theme with custom color palettes and responsive design
- **Interactive Features**: Hover tooltips, zoom capabilities, and export-ready chart formatting

## External Dependencies

### Core Data Science Stack
- **Pandas**: Primary data manipulation and analysis library
- **NumPy**: Numerical computing and array operations
- **SciPy**: Advanced statistical functions and scientific computing
- **Matplotlib**: Static plotting and chart generation
- **Seaborn**: Statistical data visualization with enhanced aesthetics

### Web Framework
- **Streamlit**: Complete web application framework for the user interface and deployment

### AI and Machine Learning
- **Google Gemini AI**: Gemini-2.5-flash model integration for AI-powered analysis (requires GEMINI_API_KEY environment variable)
- **Google GenAI Client**: Official Google Generative AI client library for API interactions

### Voice and Audio (Optional)
- **SpeechRecognition**: Speech-to-text functionality with graceful fallback if unavailable
- **pyttsx3**: Text-to-speech engine with fallback for cloud deployments

### Export and Reporting (Optional)
- **ReportLab**: PDF generation for professional reports with tables and charts
- **WeasyPrint**: Alternative PDF generation engine with HTML/CSS rendering support

### Development and Utilities
- **OS**: File system operations and environment variable management
- **JSON**: Data serialization for API communications and configuration
- **Warnings**: Error suppression for cleaner user experience
- **IO**: BytesIO for in-memory file operations during export processes