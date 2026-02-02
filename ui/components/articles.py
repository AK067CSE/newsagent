"""
Article Cards Component

Dark mode optimized article cards for displaying news articles.
"""

import streamlit as st
from typing import List, Dict, Any

class ArticleCards:
    """Article cards component for displaying news articles."""
    
    @staticmethod
    def display_article_card(article: Dict[str, Any], expanded: bool = False):
        """Display an article in a card format."""
        with st.expander(f"📰 {article.get('title', 'No Title')[:50]}...", expanded=expanded):
            st.markdown(f"""
            <div class="article-card">
                <h4>📰 {article.get('title', 'No Title')}</h4>
                <p><strong>📅 Published:</strong> {article.get('date', 'Unknown Date')}</p>
                <p><strong>📰 Source:</strong> {article.get('source', 'Unknown Source')}</p>
                <p><strong>🏢 Companies:</strong> {', '.join(article.get('companies', []))}</p>
                <p><strong>📊 Relevance:</strong> {article.get('relevance_score', 0):.2f}</p>
                <p><strong>📝 Snippet:</strong> {article.get('snippet', 'No snippet available')[:200]}...</p>
                <p><strong>🔗 Link:</strong> <a href="{article.get('url', '#')}" target="_blank" style="color: #667eea;">Read Full Article</a></p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def display_articles_list(articles: List[Dict[str, Any]], max_display: int = 10):
        """Display a list of articles with expandable cards."""
        if not articles:
            st.info("No articles to display")
            return
        
        st.subheader(f"📰 Collected Articles ({len(articles)} total)")
        
        # Display articles with pagination
        for i, article in enumerate(articles[:max_display]):
            ArticleCards.display_article_card(article, expanded=False)
    
    @staticmethod
    def display_article_details(article: Dict[str, Any]):
        """Display detailed article information."""
        st.markdown(f"""
        <div class="article-card">
            <h2>📰 {article.get('title', 'No Title')}</h2>
            <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                <div style="flex: 1;">
                    <p><strong>📅 Published:</strong> {article.get('date', 'Unknown Date')}</p>
                    <p><strong>📰 Source:</strong> {article.get('source', 'Unknown Source')}</p>
                    <p><strong>🔗 URL:</strong> <a href="{article.get('url', '#')}" target="_blank" style="color: #667eea;">{article.get('url', 'No URL')}</a></p>
                </div>
                <div style="flex: 1;">
                    <p><strong>🏢 Companies:</strong></p>
                    <ul>
                    {"".join([f"<li>{company}</li>" for company in article.get('companies', [])])}
                    </ul>
                    <p><strong>📊 Relevance Score:</strong> {article.get('relevance_score', 0):.2f}</p>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <h4>📝 Article Snippet:</h4>
                <p>{article.get('snippet', 'No snippet available')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
