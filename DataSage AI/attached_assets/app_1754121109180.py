import streamlit as st
import pandas as pd
import os
from modules import eda, chart_gen, query_parser, export, voice_handler
from modules import ai_assistant_gemini as ai_assistant

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
st.markdown("Upload your CSV data and get instant insights with AI-powered analysis")

# Sidebar for configuration
with st.sidebar:
    st.header("📁 Data Upload")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    # Demo data button
    if st.button("🎯 Load Demo Dataset", type="secondary"):
        try:
            demo_df = pd.read_csv("demo_data.csv")
            st.session_state.demo_data = demo_df
            st.success("✅ Demo dataset loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading demo data: {str(e)}")
    
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        
        # File info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)

# Handle demo data or uploaded file
data_source = None
df = None

if uploaded_file is not None:
    try:
        # Load and display data from uploaded file
        df = pd.read_csv(uploaded_file)
        data_source = "uploaded"
        
    except Exception as e:
        st.error(f"Error loading uploaded file: {str(e)}")
        st.info("Please ensure your file is a valid CSV format")

elif 'demo_data' in st.session_state:
    # Use demo data if available
    df = st.session_state.demo_data
    data_source = "demo"
    st.success("Using demo dataset for analysis")

if df is not None:
    try:
        # Data overview
        st.subheader("📊 Data Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col4:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Create tabs for different functionalities
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧪 EDA Report", "💬 Query Data", "📊 Visualizations", "🤖 AI Assistant", "📤 Export"])
        
        with tab1:
            st.subheader("Exploratory Data Analysis")
            if st.button("🚀 Generate EDA Report", type="primary"):
                with st.spinner("Generating comprehensive EDA report..."):
                    eda.show_eda(df)
        
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
            st.subheader("🤖 AI Assistant & Voice Commands")
            
            # Initialize AI Assistant
            ai_assist = ai_assistant.create_ai_assistant()
            if ai_assist:
                ai_assist.set_dataset(df)
                
                # Create two columns for AI features
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💬 ChatGPT-like Interface")
                    
                    # Chat interface
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    # Display chat history
                    chat_container = st.container()
                    with chat_container:
                        for i, chat in enumerate(st.session_state.chat_history):
                            with st.chat_message("user"):
                                st.write(chat["user"])
                            with st.chat_message("assistant"):
                                if isinstance(chat["assistant"], dict):
                                    if "message" in chat["assistant"]:
                                        st.write(chat["assistant"]["message"])
                                    if "insights" in chat["assistant"]:
                                        st.write("**Key Insights:**")
                                        for insight in chat["assistant"]["insights"]:
                                            st.write(f"• {insight}")
                                    if "recommendations" in chat["assistant"]:
                                        st.write("**Recommendations:**")
                                        for rec in chat["assistant"]["recommendations"]:
                                            st.write(f"• {rec}")
                                    if "error" in chat["assistant"]:
                                        st.error(chat["assistant"]["error"])
                                else:
                                    st.write(chat["assistant"])
                    
                    # Chat input
                    user_input = st.chat_input("Ask me anything about your data...")
                    
                    if user_input:
                        # Process with AI
                        with st.spinner("🤖 AI is analyzing your request..."):
                            ai_response = ai_assist.process_natural_language_query(user_input)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "user": user_input,
                            "assistant": ai_response
                        })
                        st.rerun()
                    
                    # Quick action buttons
                    st.markdown("### 🚀 Quick AI Actions")
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("🔮 Generate Insights", type="secondary"):
                            with st.spinner("Generating automated insights..."):
                                insights = ai_assist.generate_automated_insights()
                            st.session_state.chat_history.append({
                                "user": "Generate automated insights",
                                "assistant": insights
                            })
                            st.rerun()
                    
                    with col_b:
                        if st.button("🧹 Suggest Cleaning", type="secondary"):
                            with st.spinner("Analyzing data quality..."):
                                cleaning = ai_assist.suggest_data_cleaning()
                            st.session_state.chat_history.append({
                                "user": "Suggest data cleaning operations",
                                "assistant": cleaning
                            })
                            st.rerun()
                    
                    col_c, col_d = st.columns(2)
                    
                    with col_c:
                        if st.button("📈 Predict Trends", type="secondary"):
                            with st.spinner("Analyzing predictive opportunities..."):
                                trends = ai_assist.predict_trends()
                            st.session_state.chat_history.append({
                                "user": "Suggest predictive analytics approaches",
                                "assistant": trends
                            })
                            st.rerun()
                    
                    with col_d:
                        if st.button("📋 AI Summary", type="secondary"):
                            with st.spinner("Creating AI-powered summary report..."):
                                summary = ai_assist.generate_ai_summary_report()
                            st.session_state.chat_history.append({
                                "user": "Generate comprehensive AI summary report",
                                "assistant": summary.get("report", "Report generation failed") if isinstance(summary, dict) else summary
                            })
                            st.rerun()
                
                with col2:
                    st.markdown("### 🎙️ Voice Commands")
                    
                    # Initialize voice handler with better error handling
                    st.markdown("### 🎙️ Text-to-Speech Voice Commands")
                    st.info("Voice features work best in local environments. In Replit, use the text interface for full AI functionality.")
                    
                    # Text input for voice-like commands
                    st.markdown("**Type a voice-style command:**")
                    voice_text_input = st.text_input(
                        "Enter a command as if speaking:",
                        placeholder="analyze my data",
                        key="voice_text_input"
                    )
                    
                    if st.button("🗣️ Process Voice Command", type="primary"):
                        if voice_text_input:
                            # Process voice command with AI
                            voice_processor = voice_handler.VoiceCommandProcessor(ai_assist)
                            with st.spinner("Processing voice command..."):
                                voice_response = voice_processor.process_voice_command(voice_text_input)
                            
                            # Add to chat history
                            st.session_state.chat_history.append({
                                "user": f"🎤 Voice Command: {voice_text_input}",
                                "assistant": voice_response
                            })
                            st.rerun()
                    
                    # Voice command examples
                    with st.expander("🗣️ Voice Command Examples"):
                        st.markdown("""
                        **Try these commands:**
                        - "analyze my data"
                        - "clean the missing values"  
                        - "show me some charts"
                        - "what insights can you find?"
                        - "create a summary report"
                        - "help me understand this data"
                        """)
            else:
                st.error("❌ AI Assistant could not be initialized. Please check your OpenAI API key.")
                st.info("Add your OpenAI API key in the Secrets tab to enable AI features.")
        
        with tab5:
            st.subheader("📤 Export Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Data Export")
                
                if st.button("📄 Export as CSV", type="secondary"):
                    csv_data = export.export_csv(df)
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_data,
                        file_name="data_export.csv",
                        mime="text/csv"
                    )
                
                if st.button("📊 Export as Excel", type="secondary"):
                    excel_data = export.export_excel(df)
                    if excel_data:
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_data,
                            file_name="data_export.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            with col2:
                st.markdown("### 📋 Report Export")
                
                if st.button("📑 Generate PDF Report", type="primary"):
                    with st.spinner("Generating PDF report..."):
                        try:
                            pdf_data = export.generate_pdf_report(df)
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
