"""
Simple Streamlit UI for News Aggregation System
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Simple test imports
try:
    from config import TEST_SETS, DEFAULT_TEST_SET
    from tools import duckduckgo_tool
    from news_collection_agent.tools import create_search_plan
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure page
st.set_page_config(page_title="News Aggregation", page_icon="📰", layout="wide")

# Dark mode CSS
st.markdown("""
<style>
.main {background-color: #0e1117; color: white;}
.sidebar {background-color: #1a1f2e; color: white;}
.stButton > button {background: #667eea; color: white;}
.metric-card {background: #2d3748; color: white; padding: 20px; border-radius: 10px;}
.article-card {background: #1a202c; color: white; padding: 15px; border-radius: 8px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("## 📰 News Aggregation System")
st.markdown("### AI-Powered Financial News Collection")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    test_set = st.selectbox("Test Set", list(TEST_SETS.keys()))
    max_articles = st.slider("Max Articles", 5, 50, 20)
    
    collect_button = st.button("🔍 Collect News", type="primary")

# Main content
if collect_button:
    st.markdown("### 🔄 Collecting News...")
    
    try:
        # Test basic functionality
        companies = TEST_SETS[test_set]['companies']
        st.success(f"✅ Test set: {test_set}")
        st.info(f"🏢 Companies: {', '.join(companies)}")
        
        # Test search
        with st.spinner("Searching for news..."):
            results = duckduckgo_tool.search_news(f"{companies[0]} news last 7 days", "7d", 5)
        
        st.success(f"✅ Found {len(results)} articles")
        
        # Display results
        for result in results[:3]:
            st.markdown(f"""
            <div class="article-card">
                <h4>📰 {result.get('title', 'No title')}</h4>
                <p>📰 Source: {result.get('source', 'Unknown')}</p>
                <p>📅 Date: {result.get('date', 'Unknown')}</p>
                <p>📝 {result.get('body', 'No snippet')[:150]}...</p>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.markdown("""
    ### 👋 Welcome!
    
    Select a test set and click "Collect News" to start.
    
    **Available Test Sets:**
    - 🤖 AI Companies: OpenAI, Anthropic, Google Deepmind, Microsoft, Meta
    - 💻 IT Companies: TCS, Wipro, Infosys, HCLTech
    - 📱 Telecom Companies: Airtel, Jio, Vodafone Idea, BSNL, MTNL, Tejas Networks
    - 🌍 Global IT: Microsoft, Google, Apple, Meta
    """)
