"""
Streamlit Chatbot UI for News Aggregation System

Dark mode optimized interface with real-time news collection and analysis.
"""

import streamlit as st
import sys
import os
import json
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import news aggregation system
from config import TEST_SETS, DEFAULT_TEST_SET
from models import Article, TestSetType, ArticleType
from news_collection_agent.tools import (
    create_search_plan, execute_search_queries, filter_articles_by_date,
    validate_sources, extract_company_mentions
)
from tools import duckduckgo_tool, web_scraper, content_processor

# Configure Streamlit page
st.set_page_config(
    page_title="📰 News Aggregation System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode CSS styling
st.markdown("""
<style>
/* Main container styling */
.main .block-container {
    background-color: #0e1117;
    color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Sidebar styling */
.sidebar .block-container {
    background-color: #1a1f2e;
    color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Chat message styling */
.chat-message {
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-left: 4px solid #667eea;
}

.assistant-message {
    background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
    color: white;
    border-left: 4px solid #4a5568;
}

.system-message {
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    color: #a0aec0;
    border-left: 4px solid #718096;
    font-style: italic;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Selectbox styling */
.stSelectbox > div > div {
    background-color: #2d3748;
    color: white;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

.stSelectbox > div > div:hover {
    border-color: #667eea;
}

/* Input styling */
.stTextInput > div > div > input {
    background-color: #2d3748;
    color: white;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Metric card styling */
.metric-card {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #4a5568;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Article card styling */
.article-card {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #4a5568;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.article-card:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

/* Success/error styling */
.success-message {
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #48bb78;
}

.error-message {
    background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #f56565;
}

/* Tab styling */
.stTabs [data-baseweb="tab"] {
    background-color: #2d3748;
    color: white;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #667eea;
    color: white;
}

/* Expander styling */
.stExpander {
    background-color: #2d3748;
    color: white;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

/* Dataframe styling */
.stDataFrame {
    background-color: #1a202c;
    color: white;
}

.stDataFrame table {
    border-radius: 8px;
    overflow: hidden;
}

.stDataFrame th {
    background-color: #2d3748;
    color: white;
    font-weight: 600;
}

.stDataFrame td {
    border-bottom: 1px solid #4a5568;
}

/* Plotly dark mode */
.js-plotly-plot .plotly .modebar {
    background: #2d3748 !important;
    color: white !important;
}

.js-plotly-plot .plotly .modebar-btn {
    background: #4a5568 !important;
    color: white !important;
}

.js-plotly-plot .plotly .hoverlayer .hovertext {
    background: #2d3748 !important;
    color: white !important;
    border: 1px solid #4a5568 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_workflow' not in st.session_state:
    st.session_state.current_workflow = None
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = {}
if 'articles' not in st.session_state:
    st.session_state.articles = []

class MockToolContext:
    """Mock ToolContext for Streamlit usage"""
    def __init__(self):
        self.state = {}
        self.artifacts = {}
    
    def save_artifact(self, artifact_id, data):
        self.artifacts[artifact_id] = data

def display_message(message: Dict[str, Any], message_type: str = "assistant"):
    """Display a chat message with appropriate styling."""
    with st.container():
        if message_type == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {message.get('content', '')}
            </div>
            """, unsafe_allow_html=True)
        elif message_type == "assistant":
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong> {message.get('content', '')}
            </div>
            """, unsafe_allow_html=True)
        elif message_type == "system":
            st.markdown(f"""
            <div class="chat-message system-message">
                <strong>⚙️ System:</strong> {message.get('content', '')}
            </div>
            """, unsafe_allow_html=True)

def display_article_card(article: Dict[str, Any]):
    """Display an article in a card format."""
    with st.container():
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

def display_metrics_dashboard():
    """Display system metrics dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Articles</h3>
            <h2>{len(st.session_state.articles)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        companies = set()
        for article in st.session_state.articles:
            companies.update(article.get('companies', []))
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏢 Companies Found</h3>
            <h2>{len(companies)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sources = set()
        for article in st.session_state.articles:
            sources.add(article.get('source', 'Unknown'))
        st.markdown(f"""
        <div class="metric-card">
            <h3>📰 Sources</h3>
            <h2>{len(sources)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_relevance = 0
        if st.session_state.articles:
            avg_relevance = sum(a.get('relevance_score', 0) for a in st.session_state.articles) / len(st.session_state.articles)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Avg Relevance</h3>
            <h2>{avg_relevance:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_charts():
    """Create visualization charts."""
    if not st.session_state.articles:
        return
    
    # Company distribution chart
    companies = {}
    for article in st.session_state.articles:
        for company in article.get('companies', []):
            companies[company] = companies.get(company, 0) + 1
    
    if companies:
        st.subheader("📊 Company Distribution")
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
        st.plotly_chart(fig, use_container_width=True)
    
    # Source distribution
    sources = {}
    for article in st.session_state.articles:
        source = article.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    if sources:
        st.subheader("📰 Source Distribution")
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
        st.plotly_chart(fig, use_container_width=True)

def run_news_collection_workflow(test_set: str, max_articles: int = 20, custom_companies: List[str] = None):
    """Run the complete news collection workflow."""
    try:
        ctx = MockToolContext()
        
        # Get companies
        if custom_companies:
            companies = custom_companies
        else:
            companies = config.TEST_SETS.get(test_set, {}).get('companies', [])
        
        if not companies:
            return {"status": "error", "message": "No companies specified"}
        
        results = {}
        
        # Phase 1: Create search plan
        plan_result = create_search_plan(ctx, test_set, companies)
        results["search_plan"] = plan_result
        
        if plan_result["status"] != "success":
            return {"status": "error", "message": "Failed to create search plan", "phase": "search_plan"}
        
        # Phase 2: Execute search
        search_result = execute_search_queries(ctx, plan_result["search_plan"]["search_queries"][:3])
        results["search"] = search_result
        
        if search_result["status"] != "success":
            return {"status": "error", "message": "Search execution failed", "phase": "search"}
        
        # Phase 3: Filter by date
        filter_result = filter_articles_by_date(ctx, search_result["results"][:max_articles], 7)
        results["date_filter"] = filter_result
        
        if filter_result["status"] != "success":
            return {"status": "error", "message": "Date filtering failed", "phase": "date_filter"}
        
        # Phase 4: Validate sources
        required_sources = ["Reuters", "Bloomberg", "TechCrunch", "The Verge", "Wired"]
        validate_result = validate_sources(ctx, filter_result["filtered_articles"], required_sources)
        results["source_validation"] = validate_result
        
        if validate_result["status"] != "success":
            return {"status": "error", "message": "Source validation failed", "phase": "source_validation"}
        
        # Phase 5: Extract company mentions
        extract_result = extract_company_mentions(ctx, validate_result["validated_articles"], companies)
        results["company_extraction"] = extract_result
        
        if extract_result["status"] != "success":
            return {"status": "error", "message": "Company extraction failed", "phase": "company_extraction"}
        
        # Convert to display format
        articles = []
        for article in extract_result.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "date": article.get("date", ""),
                "source": article.get("source", ""),
                "snippet": article.get("snippet", ""),
                "companies": article.get("tagged_companies", []),
                "relevance_score": article.get("relevance_score", 0)
            })
        
        return {
            "status": "success",
            "message": "News collection completed successfully",
            "results": results,
            "articles": articles,
            "total_articles": len(articles)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Workflow failed: {str(e)}"}

def main():
    """Main Streamlit application."""
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 10px;">
            📰 News Aggregation System
        </h1>
        <p style="color: #a0aec0; font-size: 1.1rem;">
            AI-Powered Financial News Collection & Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Test set selection
        test_set = st.selectbox(
            "📊 Select Test Set",
            options=list(config.TEST_SETS.keys()),
            index=list(config.TEST_SETS.keys()).index(config.DEFAULT_TEST_SET) if config.DEFAULT_TEST_SET in config.TEST_SETS else 0
        )
        
        # Custom companies input
        st.markdown("### 🏢 Custom Companies")
        custom_companies_input = st.text_area(
            "Enter companies (comma-separated)",
            value="",
            placeholder="OpenAI, Microsoft, Google, Meta, Anthropic",
            help="Leave empty to use test set companies"
        )
        
        # Max articles
        max_articles = st.slider(
            "📊 Max Articles",
            min_value=5,
            max_value=100,
            value=20,
            step=5
        )
        
        # Collect news button
        collect_button = st.button(
            "🔍 Collect News",
            type="primary",
            use_container_width=True
        )
        
        # System info
        st.markdown("---")
        st.markdown("### 📊 System Info")
        st.info(f"""
        **Test Set:** {test_set}
        **Companies:** {len(config.TEST_SETS[test_set]['companies'])}
        **Timeframe:** 7 days
        **Relevance Threshold:** 0.7
        """)
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("🗑️ Clear All Data"):
            st.session_state.articles = []
            st.session_state.workflow_results = {}
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📈 View Metrics"):
            st.session_state.current_page = "metrics"
            st.rerun()
        
        if st.button("📊 View Charts"):
            st.session_state.current_page = "charts"
            st.rerun()
    
    # Main content area
    if collect_button or st.session_state.messages:
        # Handle collect button click
        if collect_button:
            # Parse custom companies
            custom_companies = None
            if custom_companies_input.strip():
                custom_companies = [c.strip() for c in custom_companies_input.split(",") if c.strip()]
            
            # Add user message
            user_message = f"Collect news about {test_set}"
            if custom_companies:
                user_message += f" (custom companies: {', '.join(custom_companies)})"
            user_message += f" - Max {max_articles} articles"
            
            st.session_state.messages.append({"content": user_message, "timestamp": datetime.now()})
            
            # Add system message
            st.session_state.messages.append({
                "content": f"🔄 Starting news collection for {test_set}...",
                "timestamp": datetime.now()
            })
            
            # Run workflow
            with st.spinner("🔄 Collecting news... This may take a moment..."):
                workflow_result = run_news_collection_workflow(test_set, max_articles, custom_companies)
            
            if workflow_result["status"] == "success":
                # Update session state
                st.session_state.articles = workflow_result["articles"]
                st.session_state.workflow_results = workflow_result["results"]
                
                # Add success message
                st.session_state.messages.append({
                    "content": f"✅ Successfully collected {workflow_result['total_articles']} articles!",
                    "timestamp": datetime.now()
                })
                
                # Add summary
                st.session_state.messages.append({
                    "content": f"""
📊 **Collection Summary:**
- **Test Set:** {test_set}
- **Articles Found:** {workflow_result['total_articles']}
- **Companies Detected:** {len(set(a['companies'] for a in workflow_result['articles']))}
- **Sources:** {len(set(a['source'] for a in workflow_result['articles']))}
- **Processing Time:** {workflow_result.get('processing_time', 0):.2f}s
                    """,
                    "timestamp": datetime.now()
                })
                
            else:
                # Add error message
                st.session_state.messages.append({
                    "content": f"❌ Error: {workflow_result['message']}",
                    "timestamp": datetime.now()
                })
        
        # Display messages
        for message in st.session_state.messages:
            display_message(message)
        
        # Display articles if available
        if st.session_state.articles:
            st.markdown("---")
            st.markdown("## 📰 Collected Articles")
            
            # Metrics dashboard
            display_metrics_dashboard()
            
            # Article cards
            for i, article in enumerate(st.session_state.articles):
                with st.expander(f"📰 {article['title'][:50]}...", expanded=False):
                    display_article_card(article)
            
            # Charts
            create_charts()
    
    else:
        # Welcome message
        st.markdown("""
        <div class="chat-message assistant-message" style="margin: 20px 0;">
            <h3>👋 Welcome to the News Aggregation System!</h3>
            <p>I'm your AI-powered assistant for collecting and analyzing financial news. Here's what I can do:</p>
            <ul>
                <li>🔍 <strong>Search News:</strong> Collect news from DuckDuckGo about specific companies</li>
                <li>📅 <strong>Date Filtering:</strong> Filter articles to the last 7 days</li>
                <li>🛡️ <strong>Source Validation:</strong> Ensure credible news sources</li>
                <li>🏢 <strong>Entity Extraction:</strong> Identify company mentions in articles</li>
                <li>📊 <strong>Analytics:</strong> Provide insights and visualizations</li>
            </ul>
            <p><strong>To get started:</strong></p>
            <ol>
                <li>Select a test set from the sidebar (AI Companies, IT Companies, Telecom Companies, or Global IT)</li>
                <li>Optionally enter custom companies</li>
                <li>Click "Collect News" to start the workflow</li>
                <li>View results and analytics in real-time</li>
            </ol>
            <p><strong>Available Test Sets:</strong></p>
            <ul>
                <li>🤖️ <strong>AI Companies:</strong> OpenAI, Anthropic, Google Deepmind, Microsoft, Meta</li>
                <li>💻 <strong>IT Companies:</strong> TCS, Wipro, Infosys, HCLTech</li>
                <li>📱 <strong>Telecom Companies:</strong> Airtel, Jio, Vodafone Idea, BSNL, MTNL, Tejas Networks</li>
                <li>🌍 <strong>Global IT:</strong> Microsoft, Google, Apple, Meta</li>
            </ul>
            <p>Ready to start collecting news? Configure your preferences in the sidebar and click "Collect News"!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
