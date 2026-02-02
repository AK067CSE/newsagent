"""
Charts Component

Dark mode optimized charts for data visualization.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

class ChartsSection:
    """Charts component for data visualization."""
    
    @staticmethod
    def create_company_distribution_chart(articles: List[Dict[str, Any]]):
        """Create company distribution chart."""
        companies = {}
        for article in articles:
            for company in article.get('companies', []):
                companies[company] = companies.get(company, 0) + 1
        
        if companies:
            fig = px.bar(
                x=list(companies.keys()),
                y=list(companies.values()),
                title="Articles by Company",
                labels={'x': 'Company', 'y': 'Number of Articles'},
                color_discrete_sequence=px.colors.sequential.Purples
            )
            fig.update_layout(
                plot_bgcolor='#1a202c',
                paper_bgcolor='#1a202c',
                font_color='white',
                title_font_color='white',
                xaxis=dict(showgrid=False, tickfont=dict(color='white')),
                yaxis=dict(showgrid=True, gridcolor='#4a5568', tickfont=dict(color='white'))
            )
            return fig
        return None
    
    @staticmethod
    def create_source_distribution_chart(articles: List[Dict[str, Any]]):
        """Create source distribution chart."""
        sources = {}
        for article in articles:
            source = article.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        if sources:
            fig = px.pie(
                values=list(sources.values()),
                names=list(sources.keys()),
                title="Articles by Source"
            )
            fig.update_layout(
                plot_bgcolor='#1a202c',
                paper_bgcolor='#1a202c',
                font_color='white',
                title_font_color='white',
                legend=dict(font=dict(color='white'))
            )
            return fig
        return None
    
    @staticmethod
    def create_relevance_distribution_chart(articles: List[Dict[str, Any]]):
        """Create relevance distribution chart."""
        relevance_ranges = {
            "High (0.8-1.0)": 0,
            "Medium (0.6-0.8)": 0,
            "Low (0.4-0.6)": 0,
            "Very Low (0.0-0.4)": 0
        }
        
        for article in articles:
            relevance = article.get('relevance_score', 0)
            if relevance >= 0.8:
                relevance_ranges["High (0.8-1.0)"] += 1
            elif relevance >= 0.6:
                relevance_ranges["Medium (0.6-0.8)"] += 1
            elif relevance >= 0.4:
                relevance_ranges["Low (0.4-0.6)"] += 1
            else:
                relevance_ranges["Very Low (0.0-0.4)"] += 1
        
        fig = px.bar(
            x=list(relevance_ranges.keys()),
            y=list(relevance_ranges.values()),
            title="Relevance Score Distribution",
            labels={'x': 'Relevance Range', 'y': 'Number of Articles'},
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig.update_layout(
            plot_bgcolor='#1a202c',
            paper_bgcolor='#1a202c',
            font_color='white',
            title_font_color='white',
            xaxis=dict(showgrid=False, tickfont=dict(color='white')),
            yaxis=dict(showgrid=True, gridcolor='#4a5568', tickfont=dict(color='white'))
        )
        return fig
    
    @staticmethod
    def display_all_charts(articles: List[Dict[str, Any]]):
        """Display all charts in tabs."""
        if not articles:
            st.info("No data available for charts")
            return
        
        tab1, tab2, tab3 = st.tabs(["📊 Companies", "📰 Sources", "📈 Relevance"])
        
        with tab1:
            company_chart = ChartsSection.create_company_distribution_chart(articles)
            if company_chart:
                st.plotly_chart(company_chart, use_container_width=True)
                
                # Company stats table
                companies = {}
                for article in articles:
                    for company in article.get('companies', []):
                        companies[company] = companies.get(company, 0) + 1
                
                company_data = []
                for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True):
                    company_data.append({
                        'Company': company,
                        'Articles': count,
                        'Percentage': f"{(count / len(articles) * 100):.1f}%"
                    })
                
                df = pd.DataFrame(company_data)
                st.dataframe(df, use_container_width=True)
        
        with tab2:
            source_chart = ChartsSection.create_source_distribution_chart(articles)
            if source_chart:
                st.plotly_chart(source_chart, use_container_width=True)
                
                # Source stats table
                sources = {}
                for article in articles:
                    source = article.get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                source_data = []
                for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                    source_data.append({
                        'Source': source,
                        'Articles': count,
                        'Percentage': f"{(count / len(articles) * 100):.1f}%"
                    })
                
                df = pd.DataFrame(source_data)
                st.dataframe(df, use_container_width=True)
        
        with tab3:
            relevance_chart = ChartsSection.create_relevance_distribution_chart(articles)
            if relevance_chart:
                st.plotly_chart(relevance_chart, use_container_width=True)
                
                # Relevance stats
                relevance_ranges = {
                    "High (0.8-1.0)": 0,
                    "Medium (0.6-0.8)": 0,
                    "Low (0.4-0.6)": 0,
                    "Very Low (0.0-0.4)": 0
                }
                
                for article in articles:
                    relevance = article.get('relevance_score', 0)
                    if relevance >= 0.8:
                        relevance_ranges["High (0.8-1.0)"] += 1
                    elif relevance >= 0.6:
                        relevance_ranges["Medium (0.6-0.8)"] += 1
                    elif relevance >= 0.4:
                        relevance_ranges["Low (0.4-0.6)"] += 1
                    else:
                        relevance_ranges["Very Low (0.0-0.4)"] += 1
                
                relevance_data = []
                for range_name, count in relevance_ranges.items():
                    relevance_data.append({
                        'Range': range_name,
                        'Articles': count,
                        'Percentage': f"{(count / len(articles) * 100):.1f}%"
                    })
                
                df = pd.DataFrame(relevance_data)
                st.dataframe(df, use_container_width=True)
