import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
from modules import eda, chart_gen, query_parser, export, voice_handler
from modules import ai_assistant_gemini as ai_assistant
from modules import gemini_live, data_cleaning

# Suppress warnings for cleaner UI
warnings.filterwarnings('ignore')

def _clean_dataframe_for_display(df):
    """Clean dataframe to prevent Arrow conversion issues"""
    df_clean = df.copy()
    
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Convert to string first to handle all mixed types
            df_clean[col] = df_clean[col].astype(str)
            # Replace 'nan' strings with empty strings
            df_clean[col] = df_clean[col].replace(['nan', 'None', 'NaN'], '')
            # Clean problematic characters that cause Arrow conversion issues
            df_clean[col] = df_clean[col].str.replace('%', '_percent', regex=False)
            df_clean[col] = df_clean[col].str.replace('$', '_dollar', regex=False)
            df_clean[col] = df_clean[col].str.replace(':', '_colon', regex=False)
    
    # Ensure all columns are Arrow-compatible
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Replace NaN values with empty strings for object columns
            df_clean[col] = df_clean[col].fillna('')
        # Handle numeric columns
        elif df_clean[col].dtype in ['int64', 'float64']:
            df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean

# Configure page
st.set_page_config(
    page_title="DataSage AI", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS for dark mode
if os.path.exists("assets/dark_mode.css"):
    with open("assets/dark_mode.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🤖 DataSage AI – Your Free Data Analyst Assistant")
st.markdown("Upload your CSV or Excel data and get instant insights with AI-powered analysis")

# Check API key status and show helpful message
if not os.getenv("GEMINI_API_KEY"):
    st.warning("⚠️ **API Key Required for AI Features** - Get your free key in 2 minutes:")
    with st.expander("🔑 How to Get Your Free API Key", expanded=True):
        st.markdown("""
        **Quick Setup (2 minutes):**
        1. Visit: [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with any Google account
        3. Click "Create API Key" 
        4. Copy the key and add to Replit Secrets as `GEMINI_API_KEY`
        
        **Why you need your own key:**
        - API keys are personal and completely free
        - No credit card required
        - Generous usage limits for data analysis
        - Keeps your usage secure and separate
        
        **Without an API key:** You can still use data upload, visualization, and basic analysis features.
        """)
    st.info("💡 **Tip:** Each person who uses this app needs their own free API key for security reasons.")

# Sidebar for configuration
with st.sidebar:
    st.header("📁 Data Upload")
    uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx", "xls"])
    
    # Demo data buttons
    st.markdown("**Try with sample data:**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Clean Data", type="secondary"):
            try:
                demo_df = pd.read_csv("demo_data.csv")
                st.session_state.demo_data = demo_df
                st.success("Clean CSV dataset loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading demo data: {str(e)}")
    
    with col2:
        if st.button("🧹 Dirty Data", type="primary"):
            try:
                dirty_df = pd.read_csv("demo_dirty_data.csv")
                st.session_state.demo_data = dirty_df
                st.success("Dirty dataset loaded!")
                st.info("Perfect for practicing data cleaning!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading dirty data: {str(e)}")
    
    # Create demo Excel file if it doesn't exist
    if not os.path.exists("demo_data.xlsx"):
        try:
            demo_df = pd.read_csv("demo_data.csv")
            demo_df.to_excel("demo_data.xlsx", index=False, sheet_name="Employee_Data")
        except:
            pass  # Fail silently if can't create Excel file
    
    st.markdown("**Supported formats:** CSV, Excel (.xlsx, .xls)")
    st.info("💡 For Excel files with multiple sheets, you can select which sheet to analyze")
    
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        
        # File info
        file_extension = uploaded_file.name.split('.')[-1].upper()
        file_details = {
            "Filename": uploaded_file.name,
            "File type": file_extension,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)

# Handle demo data or uploaded file
data_source = None
df = None

if uploaded_file is not None:
    try:
        # Determine file type and load accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            # For Excel files, try to read the first sheet
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0)
                
                # If Excel has multiple sheets, let user choose
                excel_file = pd.ExcelFile(uploaded_file)
                if len(excel_file.sheet_names) > 1:
                    st.info(f"Excel file has {len(excel_file.sheet_names)} sheets. Using first sheet: '{excel_file.sheet_names[0]}'")
                    
                    # Option to select different sheet
                    with st.sidebar:
                        selected_sheet = st.selectbox(
                            "Select Excel sheet:",
                            excel_file.sheet_names,
                            key="sheet_selector"
                        )
                        
                        if selected_sheet != excel_file.sheet_names[0]:
                            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                            st.success(f"Switched to sheet: '{selected_sheet}'")
                            
            except Exception as excel_error:
                st.error(f"Error reading Excel file: {str(excel_error)}")
                st.info("Try saving your Excel file as CSV format")
                df = None
        else:
            st.error("Unsupported file format")
            df = None
        
        if df is not None:
            data_source = "uploaded"
            # Clean data to prevent Arrow conversion issues
            df = _clean_dataframe_for_display(df)
            st.success(f"File loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
        
    except Exception as e:
        st.error(f"Error loading uploaded file: {str(e)}")
        st.info("Please ensure your file is in CSV or Excel format and properly formatted")

elif 'demo_data' in st.session_state:
    # Use demo data if available
    df = st.session_state.demo_data.copy()
    data_source = "demo"
    
    # Clean data to prevent Arrow conversion issues
    df = _clean_dataframe_for_display(df)
    st.success("Using demo dataset for analysis")

if df is not None:
    try:
        # Use cleaned data if available
        current_df = st.session_state.get('cleaned_data', df)
        is_cleaned = 'cleaned_data' in st.session_state
        
        # Data overview
        st.subheader("📊 Data Overview")
        if is_cleaned:
            st.success("🧹 Using cleaned data")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows", len(current_df))
        with col2:
            st.metric("Columns", len(current_df.columns))
        with col3:
            st.metric("Missing Values", current_df.isnull().sum().sum())
        with col4:
            st.metric("Memory Usage", f"{current_df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(current_df.head(10), use_container_width=True)
        
        # Create tabs for different functionalities
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🧪 EDA Report", "💬 Query Data", "📊 Visualizations", "🧹 Data Cleaning", "🤖 AI Assistant", "📤 Export"])
        
        with tab1:
            st.subheader("Exploratory Data Analysis")
            if st.button("🚀 Generate EDA Report", type="primary"):
                with st.spinner("Generating comprehensive EDA report..."):
                    eda.show_eda(current_df)
        
        with tab2:
            st.subheader("Natural Language Querying")
            st.info("💡 Ask questions about your data in plain English")
            
            # Query examples
            with st.expander("📝 Example queries"):
                st.markdown("""
                - "Show me null values"
                - "What are the data types?"
                - "Give me basic statistics"
                - "Show correlation between columns"
                - "What are the unique values in column X?"
                """)
            
            query = st.text_input(
                "💬 Ask about your data:",
                placeholder="e.g., 'Show null values' or 'What are the data types?'"
            )
            
            if query:
                with st.spinner("Processing your query..."):
                    try:
                        response = query_parser.handle_query(df, query)
                        st.success("🔍 Query Result:")
                        
                        if isinstance(response, pd.DataFrame):
                            st.dataframe(response, use_container_width=True)
                        else:
                            st.write(response)
                    except Exception as e:
                        st.error(f"❌ Error processing query: {str(e)}")
        
        with tab3:
            st.subheader("Data Visualizations")
            
            # Chart type selection
            chart_type = st.selectbox(
                "Select chart type:",
                ["Auto (based on data)", "Histogram", "Scatter Plot", "Line Chart", "Bar Chart", "Box Plot", "Correlation Heatmap"]
            )
            
            if st.button("📊 Generate Visualization", type="primary"):
                with st.spinner("Creating visualization..."):
                    try:
                        fig = chart_gen.generate_chart(df, chart_type)
                        if fig:
                            st.pyplot(fig, use_container_width=True)
                        else:
                            st.warning("⚠️ Could not generate chart for this data")
                    except Exception as e:
                        st.error(f"❌ Error generating chart: {str(e)}")
        
        with tab4:
            st.subheader("🧹 Professional Data Cleaning")
            
            # Data cleaning walkthrough for new users
            if df.isnull().sum().sum() > 0 or len(df[df.duplicated()]) > 0:
                st.warning("⚠️ Data quality issues detected! Let's clean your data step by step.")
                
                with st.expander("📚 How to Clean Your Data (Step-by-Step Guide)", expanded=True):
                    st.markdown("""
                    ### 🎯 Quick Start Guide for Data Cleaning
                    
                    **Step 1:** Click "🔍 Analyze Data Quality" to see what needs fixing
                    **Step 2:** Review the quality score and detailed analysis  
                    **Step 3:** Click "💡 Get Cleaning Suggestions" for recommendations
                    **Step 4:** Select cleaning operations and click "🧹 Auto-Clean Data"
                    **Step 5:** Click "✅ Use Cleaned Data" to apply changes
                    
                    Your original data is always preserved - you can reset anytime!
                    """)
            
            # Initialize data cleaner
            cleaner = data_cleaning.DataCleaner(current_df if 'current_df' in locals() else df)
            
            # Data Quality Dashboard
            st.markdown("### 📊 Data Quality Assessment")
            
            if st.button("🔍 Analyze Data Quality", type="primary"):
                with st.spinner("Analyzing data quality..."):
                    quality_report = cleaner.generate_data_quality_report()
                
                # Display quality score prominently
                score = quality_report['quality_score']
                score_color = "green" if score >= 80 else "orange" if score >= 60 else "red"
                st.markdown(f"### Overall Quality Score: <span style='color: {score_color}'>{score}/100</span>", unsafe_allow_html=True)
                
                # Quality metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Missing Values", 
                        quality_report['missing_data']['total_missing'],
                        delta=f"{quality_report['missing_data']['columns_with_missing']} columns affected"
                    )
                
                with col2:
                    st.metric(
                        "Duplicate Rows", 
                        quality_report['duplicates']['total_duplicates'],
                        delta=f"{quality_report['duplicates']['percentage']}%"
                    )
                
                with col3:
                    outlier_count = sum(info['iqr_outliers'] for info in quality_report['outliers'].values())
                    st.metric("Outliers Detected", outlier_count)
                
                with col4:
                    memory_mb = quality_report['dataset_info']['memory_usage_mb']
                    st.metric("Memory Usage", f"{memory_mb} MB")
                
                # Detailed quality analysis
                st.markdown("### 📋 Detailed Quality Analysis")
                
                # Missing data analysis
                if quality_report['missing_data']['total_missing'] > 0:
                    with st.expander("🔍 Missing Data Analysis", expanded=True):
                        missing_df = pd.DataFrame([
                            {
                                'Column': col, 
                                'Missing Count': info['count'],
                                'Missing %': info['percentage'],
                                'Pattern': info['pattern'],
                                'Severity': quality_report['missing_data']['severity']
                            }
                            for col, info in quality_report['missing_data']['patterns'].items()
                        ])
                        st.dataframe(missing_df, use_container_width=True)
                
                # Outlier analysis
                if quality_report['outliers']:
                    with st.expander("📈 Outlier Analysis"):
                        outlier_df = pd.DataFrame([
                            {
                                'Column': col,
                                'IQR Outliers': info['iqr_outliers'],
                                'Z-Score Outliers': info['z_score_outliers'],
                                'Lower Bound': info['iqr_bounds']['lower'],
                                'Upper Bound': info['iqr_bounds']['upper'],
                                'Severity': info['severity']
                            }
                            for col, info in quality_report['outliers'].items()
                        ])
                        st.dataframe(outlier_df, use_container_width=True)
                
                # Data type recommendations
                with st.expander("🔧 Data Type Optimization"):
                    type_df = pd.DataFrame([
                        {
                            'Column': col,
                            'Current Type': info['current_type'],
                            'Suggested Type': info['suggested_type'],
                            'Memory (bytes)': info['memory_usage_bytes'],
                            'Needs Optimization': info['optimization_possible']
                        }
                        for col, info in quality_report['data_types'].items()
                    ])
                    st.dataframe(type_df, use_container_width=True)
            
            # Cleaning Strategies
            st.markdown("### 🛠️ Cleaning Strategies")
            
            if st.button("💡 Get Cleaning Suggestions", type="secondary"):
                with st.spinner("Generating cleaning recommendations..."):
                    suggestions = cleaner.suggest_cleaning_strategies()
                
                for category, suggestion_list in suggestions.items():
                    if suggestion_list:
                        st.markdown(f"**{category.replace('_', ' ').title()}:**")
                        for suggestion in suggestion_list:
                            st.write(f"• {suggestion}")
                        st.write("")
            
            # Auto-Cleaning Options
            st.markdown("### 🤖 Automated Cleaning")
            
            cleaning_options = st.multiselect(
                "Select cleaning operations:",
                options=[
                    "remove_duplicates",
                    "fix_data_types", 
                    "handle_missing_basic",
                    "clean_text",
                    "remove_outliers"
                ],
                default=["remove_duplicates", "fix_data_types", "handle_missing_basic"],
                help="Choose which automated cleaning operations to apply"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🧹 Auto-Clean Data", type="primary"):
                    if cleaning_options:
                        with st.spinner("Applying cleaning operations..."):
                            try:
                                cleaned_df = cleaner.auto_clean_data(cleaning_options)
                                cleaning_summary = cleaner.get_cleaning_summary()
                                
                                # Store cleaned data and summary in session state
                                st.session_state['temp_cleaned_data'] = cleaned_df
                                st.session_state['cleaning_summary'] = cleaning_summary
                                st.session_state['show_cleaning_results'] = True
                                
                            except Exception as e:
                                st.error(f"Error during cleaning: {str(e)}")
                                st.session_state['show_cleaning_results'] = False
                    else:
                        st.warning("Please select at least one cleaning operation")
            
            # Show cleaning results if available
            if st.session_state.get('show_cleaning_results', False) and 'temp_cleaned_data' in st.session_state:
                st.success("Data cleaning completed!")
                
                cleaning_summary = st.session_state['cleaning_summary']
                
                # Show cleaning summary
                st.markdown("#### 📊 Cleaning Summary")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("Original Rows", cleaning_summary['original_shape'][0])
                    st.metric("Cleaned Rows", cleaning_summary['current_shape'][0])
                
                with col_b:
                    st.metric("Rows Removed", cleaning_summary['rows_changed'])
                    memory_savings = cleaning_summary['memory_optimization']
                    st.metric("Memory Saved", f"{memory_savings['savings_mb']} MB")
                
                # Show cleaning operations performed
                with st.expander("🔍 Operations Performed"):
                    for operation in cleaning_summary['cleaning_log']:
                        st.write(f"• {operation}")
                
                # Buttons for applying or discarding cleaned data
                col_apply, col_reset = st.columns(2)
                
                with col_apply:
                    if st.button("✅ Use Cleaned Data", type="primary"):
                        st.session_state['cleaned_data'] = st.session_state['temp_cleaned_data']
                        st.session_state['show_cleaning_results'] = False
                        # Clean up temporary data
                        if 'temp_cleaned_data' in st.session_state:
                            del st.session_state['temp_cleaned_data']
                        if 'cleaning_summary' in st.session_state:
                            del st.session_state['cleaning_summary']
                        st.success("Cleaned data is now being used for analysis!")
                        st.rerun()
                
                with col_reset:
                    if st.button("🔄 Reset to Original", type="secondary"):
                        # Remove cleaned data and show original
                        if 'cleaned_data' in st.session_state:
                            del st.session_state['cleaned_data']
                        st.session_state['show_cleaning_results'] = False
                        # Clean up temporary data
                        if 'temp_cleaned_data' in st.session_state:
                            del st.session_state['temp_cleaned_data']
                        if 'cleaning_summary' in st.session_state:
                            del st.session_state['cleaning_summary']
                        st.success("Reset to original data!")
                        st.rerun()
                    else:
                        st.warning("Please select at least one cleaning operation")
            
            with col2:
                if st.button("🔄 Reset to Original Data"):
                    if 'cleaned_data' in st.session_state:
                        del st.session_state['cleaned_data']
                        st.success("Reset to original data")
                        st.rerun()
            
            # Advanced Cleaning Options
            with st.expander("🔬 Advanced Cleaning Options"):
                st.markdown("#### Custom Missing Value Handling")
                
                missing_strategy = st.selectbox(
                    "Missing value strategy:",
                    ["Drop rows", "Fill with mean/median", "Fill with mode", "Forward fill", "Backward fill", "Custom value"]
                )
                
                if missing_strategy == "Custom value":
                    custom_fill = st.text_input("Custom fill value:", "Unknown")
                
                st.markdown("#### Outlier Treatment")
                outlier_method = st.selectbox(
                    "Outlier handling:",
                    ["Remove outliers", "Cap outliers", "Log transformation", "Keep outliers"]
                )
                
                if outlier_method == "Cap outliers":
                    percentile = st.slider("Cap at percentile:", 90, 99, 95)
                
                st.markdown("#### Text Cleaning Options")
                text_options = st.multiselect(
                    "Text cleaning operations:",
                    ["Remove special characters", "Convert to lowercase", "Remove extra spaces", "Remove leading/trailing spaces"]
                )
            
            # Data Validation
            st.markdown("### ✅ Data Validation")
            
            if st.button("🔍 Validate Data Quality"):
                # Use cleaned data if available, otherwise original
                validation_df = st.session_state.get('cleaned_data', df)
                validator = data_cleaning.DataCleaner(validation_df)
                validation_report = validator.generate_data_quality_report()
                
                st.markdown("#### Validation Results")
                
                # Show improvements if cleaned data exists
                if 'cleaned_data' in st.session_state:
                    original_cleaner = data_cleaning.DataCleaner(df)
                    original_report = original_cleaner.generate_data_quality_report()
                    
                    improvement_col1, improvement_col2 = st.columns(2)
                    
                    with improvement_col1:
                        st.metric("Original Quality Score", f"{original_report['quality_score']}/100")
                        st.metric("Original Missing Values", original_report['missing_data']['total_missing'])
                    
                    with improvement_col2:
                        st.metric(
                            "Current Quality Score", 
                            f"{validation_report['quality_score']}/100",
                            delta=f"{validation_report['quality_score'] - original_report['quality_score']:.1f}"
                        )
                        st.metric(
                            "Current Missing Values", 
                            validation_report['missing_data']['total_missing'],
                            delta=validation_report['missing_data']['total_missing'] - original_report['missing_data']['total_missing']
                        )
                
                # Quality checklist
                checks = []
                if validation_report['missing_data']['total_missing'] == 0:
                    checks.append("✅ No missing values")
                else:
                    checks.append(f"⚠️ {validation_report['missing_data']['total_missing']} missing values remain")
                
                if validation_report['duplicates']['total_duplicates'] == 0:
                    checks.append("✅ No duplicate rows")
                else:
                    checks.append(f"⚠️ {validation_report['duplicates']['total_duplicates']} duplicate rows remain")
                
                outlier_count = sum(info['iqr_outliers'] for info in validation_report['outliers'].values())
                if outlier_count == 0:
                    checks.append("✅ No outliers detected")
                else:
                    checks.append(f"⚠️ {outlier_count} outliers detected")
                
                for check in checks:
                    st.write(check)

        with tab5:
            st.subheader("🤖 Gemini Live AI Assistant")
            
            # Initialize Gemini Live Assistant
            live_assistant = gemini_live.create_gemini_live_assistant()
            if live_assistant:
                live_assistant.set_dataset(df)
                
                # Gemini Live Interface
                st.markdown("### 💬 Live Conversation with AI")
                st.info("Chat naturally with your AI data analyst - just like Gemini Live!")
                
                # Initialize chat history for live assistant
                if 'live_chat_history' not in st.session_state:
                    st.session_state.live_chat_history = []
                
                # Display live chat history
                chat_container = st.container()
                with chat_container:
                    for chat in st.session_state.live_chat_history:
                        with st.chat_message("user"):
                            st.write(chat["user"])
                        with st.chat_message("assistant"):
                            st.write(chat["assistant"])
                
                # Quick action buttons
                st.markdown("### 🚀 Quick Actions")
                quick_actions = live_assistant.get_quick_actions()
                
                cols = st.columns(3)
                for i, action in enumerate(quick_actions[:6]):
                    with cols[i % 3]:
                        if st.button(action["text"], key=f"quick_{i}", type="secondary"):
                            # Process quick action
                            with st.spinner("Processing..."):
                                response_chunks = []
                                placeholder = st.empty()
                                
                                for chunk in live_assistant.stream_response(action["text"]):
                                    response_chunks.append(chunk)
                                    placeholder.write(" ".join(response_chunks))
                                
                                full_response = " ".join(response_chunks)
                                placeholder.empty()
                            
                            # Add to chat history
                            st.session_state.live_chat_history.append({
                                "user": action["text"],
                                "assistant": full_response
                            })
                            st.rerun()
                
                # Proactive suggestions
                suggestions = live_assistant.get_proactive_suggestions()
                if suggestions:
                    st.markdown("### 💡 AI Suggestions")
                    for suggestion in suggestions:
                        st.info(suggestion)
                
                # Live chat input with streaming response
                user_input = st.chat_input("Ask me anything about your data...")
                
                if user_input:
                    # Analyze user intent
                    intent = live_assistant.analyze_user_intent(user_input)
                    
                    # Add user message to chat
                    with st.chat_message("user"):
                        st.write(user_input)
                    
                    # Generate streaming response
                    with st.chat_message("assistant"):
                        response_placeholder = st.empty()
                        response_chunks = []
                        
                        with st.spinner("Thinking..."):
                            for chunk in live_assistant.stream_response(user_input):
                                response_chunks.append(chunk)
                                # Update placeholder with accumulated response
                                response_placeholder.write(" ".join(response_chunks))
                        
                        full_response = " ".join(response_chunks)
                    
                    # Add to chat history
                    st.session_state.live_chat_history.append({
                        "user": user_input,
                        "assistant": full_response
                    })
                    st.rerun()
                
                # Additional AI Controls
                st.markdown("### 🎯 AI Control Center")
                
                control_cols = st.columns(4)
                with control_cols[0]:
                    if st.button("🔍 Deep Analysis", type="secondary"):
                        response_chunks = []
                        placeholder = st.empty()
                        
                        for chunk in live_assistant.stream_response("Perform a comprehensive deep analysis of this dataset, including statistical insights, patterns, and business implications"):
                            response_chunks.append(chunk)
                            placeholder.write(" ".join(response_chunks))
                        
                        full_response = " ".join(response_chunks)
                        placeholder.empty()
                        
                        st.session_state.live_chat_history.append({
                            "user": "🔍 Deep Analysis",
                            "assistant": full_response
                        })
                        st.rerun()
                
                with control_cols[1]:
                    if st.button("🎙️ Voice Mode", type="primary"):
                        st.info("Voice mode activated! Chat naturally below.")
                        
                with control_cols[2]:
                    if st.button("📊 Data Story", type="secondary"):
                        response_chunks = []
                        placeholder = st.empty()
                        
                        for chunk in live_assistant.stream_response("Tell me the story of this data - what narrative does it reveal? What are the key characters (variables) and plot points (insights)?"):
                            response_chunks.append(chunk)
                            placeholder.write(" ".join(response_chunks))
                        
                        full_response = " ".join(response_chunks)
                        placeholder.empty()
                        
                        st.session_state.live_chat_history.append({
                            "user": "📊 Tell me the data story",
                            "assistant": full_response
                        })
                        st.rerun()
                
                with control_cols[3]:
                    if st.button("🗑️ Clear Chat", type="secondary"):
                        st.session_state.live_chat_history = []
                        st.rerun()
                
                # Create two columns for additional AI features
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🎯 Live Session Status")
                    
                    # Live session metrics
                    if st.session_state.live_chat_history:
                        st.success(f"Live session active with {len(st.session_state.live_chat_history)} interactions")
                        
                        # Show last interaction
                        if st.session_state.live_chat_history:
                            last_chat = st.session_state.live_chat_history[-1]
                            st.markdown("**Last exchange:**")
                            st.text(f"You: {last_chat['user'][:50]}...")
                            st.text(f"AI: {str(last_chat['assistant'])[:50]}...")
                    else:
                        st.info("Start a conversation to begin your live AI session")
                    
                    # Conversation analytics
                    st.markdown("### 📊 Session Analytics")
                    if st.session_state.live_chat_history:
                        total_words = sum(len(str(chat['assistant']).split()) for chat in st.session_state.live_chat_history)
                        avg_response_length = total_words // len(st.session_state.live_chat_history)
                        
                        metrics_cols = st.columns(2)
                        with metrics_cols[0]:
                            st.metric("Total Exchanges", len(st.session_state.live_chat_history))
                        with metrics_cols[1]:
                            st.metric("Avg Response Length", f"{avg_response_length} words")
                
                with col2:
                    st.markdown("### 🎙️ Voice-Style Interaction")
                    st.info("Experience natural conversation like Gemini Live")
                    
                    # Voice-style quick prompts
                    st.markdown("**Natural conversation starters:**")
                    voice_prompts = [
                        "Hey, what's interesting about this data?",
                        "Can you walk me through the key findings?", 
                        "I'm looking for business insights here",
                        "Help me understand what stands out",
                        "What story does this data tell?"
                    ]
                    
                    for prompt in voice_prompts:
                        if st.button(f"💬 \"{prompt}\"", key=f"voice_{hash(prompt)}", type="secondary"):
                            # Process as live conversation
                            response_chunks = []
                            placeholder = st.empty()
                            
                            for chunk in live_assistant.stream_response(prompt):
                                response_chunks.append(chunk)
                                placeholder.write(" ".join(response_chunks))
                            
                            full_response = " ".join(response_chunks)
                            placeholder.empty()
                            
                            st.session_state.live_chat_history.append({
                                "user": prompt,
                                "assistant": full_response
                            })
                            st.rerun()
                    
                    # Session controls
                    st.markdown("**Session Controls:**")
                    session_cols = st.columns(2)
                    with session_cols[0]:
                        if st.button("🔄 Reset AI Context"):
                            live_assistant._initialize_live_context()
                            st.success("AI context reset")
                    
                    with session_cols[1]:
                        if st.button("📱 Mobile View"):
                            st.info("Optimized for conversational use")
            else:
                st.error("❌ AI Assistant could not be initialized. Please check your Gemini API key.")
                st.info("Add your GEMINI_API_KEY in the Secrets tab to enable AI features.")
        
        with tab6:
            st.subheader("📤 Export Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Data Export")
                
                # Export current data (cleaned if available)
                export_df = st.session_state.get('cleaned_data', current_df)
                
                if st.button("📄 Export as CSV", type="secondary"):
                    exporter = export.DataExporter(export_df)
                    csv_data = exporter.export_csv()
                    if csv_data:
                        filename = "cleaned_data_export.csv" if 'cleaned_data' in st.session_state else "data_export.csv"
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_data,
                            file_name=filename,
                            mime="text/csv"
                        )
                
                if st.button("📊 Export as Excel", type="secondary"):
                    exporter = export.DataExporter(export_df)
                    excel_data = exporter.export_excel()
                    if excel_data:
                        filename = "cleaned_data_export.xlsx" if 'cleaned_data' in st.session_state else "data_export.xlsx"
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            with col2:
                st.markdown("### 📋 Report Export")
                
                if st.button("📑 Generate PDF Report", type="primary"):
                    with st.spinner("Generating PDF report..."):
                        try:
                            exporter = export.DataExporter(df)
                            pdf_data = exporter.generate_pdf_report()
                            if pdf_data:
                                st.success("✅ PDF report generated successfully!")
                                st.download_button(
                                    label="⬇️ Download PDF Report",
                                    data=pdf_data,
                                    file_name="data_analysis_report.pdf",
                                    mime="application/pdf"
                                )
                            else:
                                st.error("❌ Failed to generate PDF report")
                        except Exception as e:
                            st.error(f"❌ Error generating PDF: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ An error occurred while processing your data: {str(e)}")
        st.info("Please check your data format and try again")

else:
    # Welcome screen
    st.info("👆 Upload a CSV file or click 'Load Demo Dataset' in the sidebar to get started")
    
    st.markdown("""
    ## 🚀 Welcome to DataSage AI
    
    Your powerful AI-driven data analysis assistant! Here's what you can do:
    
    ### ✨ Key Features
    - **🧪 Automated EDA**: Get comprehensive exploratory data analysis
    - **💬 Natural Language Queries**: Ask questions about your data in plain English  
    - **📊 Smart Visualizations**: Auto-generated charts and graphs
    - **🤖 AI Assistant**: ChatGPT-powered insights and recommendations
    - **🎙️ Voice Commands**: Speak to your data (text-based fallback available)
    - **📤 Export Options**: Download reports as PDF, CSV, or Excel
    
    ### 🎯 Getting Started
    1. **Upload your CSV file** using the sidebar
    2. **Or try our demo dataset** to explore all features
    3. **Navigate through tabs** to explore different analysis options
    4. **Chat with the AI Assistant** for personalized insights
    
    ### 💡 Example Use Cases
    - **Business Analytics**: Sales data, customer metrics, KPIs
    - **Research Data**: Survey results, experimental data, statistics
    - **Financial Analysis**: Investment data, budget tracking, performance
    - **HR Analytics**: Employee data, recruitment metrics, performance
    """)
