"""
Metrics Dashboard Component

Dark mode optimized metrics dashboard for displaying system statistics.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

class MetricsDashboard:
    """Metrics dashboard component for displaying system statistics."""
    
    @staticmethod
    def display_overview_metrics(articles: List[Dict[str, Any]]):
        """Display overview metrics in cards."""
        # Calculate metrics
        total_articles = len(articles)
        companies = set()
        sources = set()
        avg_relevance = 0
        
        for article in articles:
            companies.update(article.get('companies', []))
            sources.add(article.get('source', 'Unknown'))
            avg_relevance += article.get('relevance_score', 0)
        
        if total_articles > 0:
            avg_relevance = avg_relevance / total_articles
        
        # Create metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Total Articles</h3>
                <h2>{total_articles}</h2>
                <p style="color: #a0aec0; font-size: 0.9rem;">Collected articles</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏢 Companies Found</h3>
                <h2>{len(companies)}</h2>
                <p style="color: #a0aec0; font-size: 0.9rem;">Unique companies</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📰 Sources</h3>
                <h2>{len(sources)}</h2>
                <p style="color: #a0aec0; font-size: 0.9rem;">News sources</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Avg Relevance</h3>
                <h2>{avg_relevance:.2f}</h2>
                <p style="color: #a0aec0; font-size: 0.9rem;">Average score</p>
            </div>
            """, unsafe_allow_html=True)
