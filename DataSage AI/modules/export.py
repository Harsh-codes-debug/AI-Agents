"""
Export Module for DataSage AI

This module provides data export functionality:
- CSV and Excel export
- PDF report generation
- Comprehensive analysis reports
- Custom formatting and styling
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO
from typing import Optional, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns

# Import PDF libraries with fallbacks
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

class DataExporter:
    """Handles data export functionality"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize data exporter
        
        Args:
            df (pandas.DataFrame): Dataset to export
        """
        self.df = df
        self.report_data = {}
    
    def export_csv(self) -> bytes:
        """
        Export dataset as CSV
        
        Returns:
            bytes: CSV data as bytes
        """
        try:
            return self.df.to_csv(index=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error exporting CSV: {str(e)}")
            return b""
    
    def export_excel(self) -> bytes:
        """
        Export dataset as Excel with multiple sheets
        
        Returns:
            bytes: Excel data as bytes
        """
        try:
            output = BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Main data sheet
                self.df.to_excel(writer, sheet_name='Data', index=False)
                
                # Summary statistics sheet
                numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    summary_stats = self.df[numeric_cols].describe()
                    summary_stats.to_excel(writer, sheet_name='Statistics')
                
                # Data info sheet
                info_data = {
                    'Column': self.df.columns,
                    'Data Type': self.df.dtypes.astype(str),
                    'Non-Null Count': self.df.count(),
                    'Null Count': self.df.isnull().sum(),
                    'Null Percentage': (self.df.isnull().sum() / len(self.df) * 100).round(2)
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='Data Info', index=False)
                
                # Missing values sheet if any exist
                if self.df.isnull().sum().sum() > 0:
                    missing_data = pd.DataFrame({
                        'Column': self.df.columns,
                        'Missing Count': self.df.isnull().sum(),
                        'Missing Percentage': (self.df.isnull().sum() / len(self.df) * 100).round(2)
                    })
                    missing_data = missing_data[missing_data['Missing Count'] > 0]
                    missing_data.to_excel(writer, sheet_name='Missing Values', index=False)
            
            return output.getvalue()
            
        except Exception as e:
            st.error(f"Error exporting Excel: {str(e)}")
            return b""
    
    def generate_pdf_report(self, include_charts: bool = True) -> Optional[bytes]:
        """
        Generate comprehensive PDF report
        
        Args:
            include_charts (bool): Whether to include visualizations
            
        Returns:
            bytes: PDF data or None if failed
        """
        if REPORTLAB_AVAILABLE:
            return self._generate_reportlab_pdf(include_charts)
        elif WEASYPRINT_AVAILABLE:
            return self._generate_weasyprint_pdf(include_charts)
        else:
            st.error("PDF generation requires either ReportLab or WeasyPrint. Please install one of them.")
            return None
    
    def _generate_reportlab_pdf(self, include_charts: bool = True) -> bytes:
        """Generate PDF using ReportLab"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("DataSage AI - Data Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Dataset Overview
            story.append(Paragraph("Dataset Overview", styles['Heading2']))
            
            overview_data = [
                ['Metric', 'Value'],
                ['Total Rows', f"{len(self.df):,}"],
                ['Total Columns', str(len(self.df.columns))],
                ['Memory Usage', f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB"],
                ['Missing Values', str(self.df.isnull().sum().sum())],
                ['Duplicate Rows', str(self.df.duplicated().sum())]
            ]
            
            overview_table = Table(overview_data)
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(overview_table)
            story.append(Spacer(1, 20))
            
            # Column Information
            story.append(Paragraph("Column Information", styles['Heading2']))
            
            col_data = [['Column Name', 'Data Type', 'Non-Null Count', 'Null Count', 'Null %']]
            for col in self.df.columns:
                null_count = self.df[col].isnull().sum()
                null_pct = (null_count / len(self.df) * 100)
                col_data.append([
                    col,
                    str(self.df[col].dtype),
                    str(self.df[col].count()),
                    str(null_count),
                    f"{null_pct:.1f}%"
                ])
            
            col_table = Table(col_data)
            col_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(col_table)
            story.append(Spacer(1, 20))
            
            # Statistical Summary
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                story.append(Paragraph("Statistical Summary", styles['Heading2']))
                
                stats_df = self.df[numeric_cols].describe()
                stats_data = [['Statistic'] + list(stats_df.columns)]
                
                for idx in stats_df.index:
                    row = [idx] + [f"{val:.2f}" if pd.notnull(val) else "N/A" 
                                  for val in stats_df.loc[idx]]
                    stats_data.append(row)
                
                stats_table = Table(stats_data)
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(stats_table)
                story.append(Spacer(1, 20))
            
            # Data Quality Assessment
            story.append(Paragraph("Data Quality Assessment", styles['Heading2']))
            
            total_cells = len(self.df) * len(self.df.columns)
            missing_cells = self.df.isnull().sum().sum()
            completeness = ((total_cells - missing_cells) / total_cells) * 100
            
            quality_text = f"""
            <b>Completeness:</b> {completeness:.1f}% ({total_cells - missing_cells:,} of {total_cells:,} cells)<br/>
            <b>Missing Data:</b> {missing_cells:,} cells ({(missing_cells/total_cells)*100:.1f}%)<br/>
            <b>Duplicate Rows:</b> {self.df.duplicated().sum():,} ({(self.df.duplicated().sum()/len(self.df))*100:.1f}%)<br/>
            <b>Unique Rows:</b> {len(self.df) - self.df.duplicated().sum():,} ({((len(self.df) - self.df.duplicated().sum())/len(self.df))*100:.1f}%)
            """
            
            story.append(Paragraph(quality_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Sample Data
            story.append(Paragraph("Sample Data (First 5 Rows)", styles['Heading2']))
            
            sample_data = [list(self.df.columns)]
            for idx in range(min(5, len(self.df))):
                row = []
                for col in self.df.columns:
                    val = str(self.df.iloc[idx][col])
                    # Truncate long values
                    if len(val) > 20:
                        val = val[:17] + "..."
                    row.append(val)
                sample_data.append(row)
            
            sample_table = Table(sample_data)
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(sample_table)
            
            # Build PDF
            doc.build(story)
            return buffer.getvalue()
            
        except Exception as e:
            st.error(f"Error generating PDF with ReportLab: {str(e)}")
            return b""
    
    def _generate_weasyprint_pdf(self, include_charts: bool = True) -> bytes:
        """Generate PDF using WeasyPrint (fallback)"""
        try:
            html_content = self._generate_html_report()
            pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
            return pdf_bytes
            
        except Exception as e:
            st.error(f"Error generating PDF with WeasyPrint: {str(e)}")
            return b""
    
    def _generate_html_report(self) -> str:
        """Generate HTML content for PDF conversion"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DataSage AI - Data Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2E86AB; text-align: center; }}
                h2 {{ color: #A23B72; border-bottom: 2px solid #A23B72; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; font-weight: bold; }}
                .metric {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>DataSage AI - Data Analysis Report</h1>
            
            <h2>Dataset Overview</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Rows</td><td>{len(self.df):,}</td></tr>
                <tr><td>Total Columns</td><td>{len(self.df.columns)}</td></tr>
                <tr><td>Memory Usage</td><td>{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB</td></tr>
                <tr><td>Missing Values</td><td>{self.df.isnull().sum().sum()}</td></tr>
                <tr><td>Duplicate Rows</td><td>{self.df.duplicated().sum()}</td></tr>
            </table>
            
            <h2>Column Information</h2>
            <table>
                <tr><th>Column Name</th><th>Data Type</th><th>Non-Null Count</th><th>Null Count</th><th>Null %</th></tr>
        """
        
        for col in self.df.columns:
            null_count = self.df[col].isnull().sum()
            null_pct = (null_count / len(self.df) * 100)
            html += f"""
                <tr>
                    <td>{col}</td>
                    <td>{self.df[col].dtype}</td>
                    <td>{self.df[col].count()}</td>
                    <td>{null_count}</td>
                    <td>{null_pct:.1f}%</td>
                </tr>
            """
        
        html += "</table>"
        
        if len(numeric_cols) > 0:
            html += "<h2>Statistical Summary</h2><table>"
            stats_df = self.df[numeric_cols].describe()
            
            html += "<tr><th>Statistic</th>"
            for col in stats_df.columns:
                html += f"<th>{col}</th>"
            html += "</tr>"
            
            for idx in stats_df.index:
                html += f"<tr><td>{idx}</td>"
                for col in stats_df.columns:
                    val = stats_df.loc[idx, col]
                    html += f"<td>{val:.2f}</td>"
                html += "</tr>"
            
            html += "</table>"
        
        html += "</body></html>"
        return html

def create_export_interface(df: pd.DataFrame) -> None:
    """
    Create Streamlit interface for data export
    
    Args:
        df (pandas.DataFrame): Dataset to export
    """
    st.subheader("📤 Export Data & Reports")
    
    exporter = DataExporter(df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 CSV Export")
        if st.button("💾 Download CSV", type="secondary"):
            csv_data = exporter.export_csv()
            if csv_data:
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv_data,
                    file_name="data_export.csv",
                    mime="text/csv"
                )
    
    with col2:
        st.markdown("### 📊 Excel Export")
        if st.button("💾 Download Excel", type="secondary"):
            excel_data = exporter.export_excel()
            if excel_data:
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_data,
                    file_name="data_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col3:
        st.markdown("### 📑 PDF Report")
        if st.button("💾 Generate PDF Report", type="secondary"):
            if REPORTLAB_AVAILABLE or WEASYPRINT_AVAILABLE:
                with st.spinner("Generating comprehensive PDF report..."):
                    pdf_data = exporter.generate_pdf_report()
                
                if pdf_data:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name="datasage_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Failed to generate PDF report")
            else:
                st.error("PDF generation requires ReportLab or WeasyPrint. Please install one of them.")
    
    # Export options
    st.markdown("### ⚙️ Export Options")
    
    with st.expander("📋 What's included in exports"):
        st.markdown("""
        **CSV Export:**
        - Raw dataset in comma-separated format
        - Preserves all data types and values
        - Compatible with Excel, Google Sheets, and other tools
        
        **Excel Export (Multi-sheet):**
        - **Data Sheet**: Complete dataset
        - **Statistics Sheet**: Summary statistics for numeric columns
        - **Data Info Sheet**: Column information and data types
        - **Missing Values Sheet**: Missing data analysis (if applicable)
        
        **PDF Report:**
        - Dataset overview and metrics
        - Column information and data types
        - Statistical summary for numeric variables
        - Data quality assessment
        - Sample data preview
        - Professional formatting for sharing
        """)
    
    # File size information
    memory_usage = df.memory_usage(deep=True).sum()
    st.info(f"📊 Dataset size: {len(df):,} rows × {len(df.columns)} columns | Memory: {memory_usage/1024:.2f} KB")

def get_export_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get export summary information
    
    Args:
        df (pandas.DataFrame): Dataset to analyze
        
    Returns:
        Dict[str, Any]: Export summary
    """
    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_kb': df.memory_usage(deep=True).sum() / 1024,
        'estimated_csv_size_kb': len(df.to_csv(index=False).encode('utf-8')) / 1024,
        'has_missing_values': df.isnull().sum().sum() > 0,
        'has_duplicates': df.duplicated().sum() > 0,
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object', 'category']).columns)
    }
