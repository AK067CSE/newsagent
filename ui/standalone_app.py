"""
Standalone Streamlit UI for News Aggregation System

No complex imports - self-contained implementation.
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="📰 News Aggregation System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode CSS
st.markdown("""
<style>
.main .block-container {
    background-color: #0e1117;
    color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.sidebar .block-container {
    background-color: #1a1f2e;
    color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

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

.metric-card {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #4a5568;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

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

.stSelectbox > div > div {
    background-color: #2d3748;
    color: white;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

.stTextInput > div > div > input {
    background-color: #2d3748;
    color: white;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

.stSlider > div > div > div > div {
    background-color: #667eea;
}
</style>
""", unsafe_allow_html=True)

# Test sets configuration (hardcoded to avoid imports)
TEST_SETS = {
    "AI Companies": {
        "companies": ["OpenAI", "Anthropic", "Google Deepmind", "Microsoft", "Meta"],
        "description": "Leading artificial intelligence companies"
    },
    "IT Companies": {
        "companies": ["TCS", "Wipro", "Infosys", "HCLTech"],
        "description": "Top Indian IT services companies"
    },
    "Telecom Companies": {
        "companies": ["Airtel", "Jio", "Vodafone Idea", "BSNL", "MTNL", "Tejas Networks"],
        "description": "Major telecommunications companies"
    },
    "Global IT": {
        "companies": ["Microsoft", "Google", "Apple", "Meta"],
        "description": "Global technology giants"
    }
}

DEFAULT_TEST_SET = "AI Companies"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'webrag_session_id' not in st.session_state:
    st.session_state.webrag_session_id = None
if 'webrag_messages' not in st.session_state:
    st.session_state.webrag_messages = []
if 'last_summary' not in st.session_state:
    st.session_state.last_summary = None
if 'last_classification' not in st.session_state:
    st.session_state.last_classification = None
if 'summary_url' not in st.session_state:
    st.session_state.summary_url = ""

def display_message(message: str, message_type: str = "assistant"):
    """Display a chat message with appropriate styling."""
    icons = {
        "user": "👤",
        "assistant": "🤖",
        "system": "⚙️",
        "success": "✅",
        "error": "❌"
    }
    
    icon = icons.get(message_type, "🤖")
    
    st.markdown(f"""
    <div class="chat-message {message_type}-message">
        <strong>{icon} {message_type.title()}:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def display_article_card(article: dict):
    """Display an article in a card format."""
    st.markdown(f"""
    <div class="article-card">
        <h4>📰 {article.get('title', 'No Title')}</h4>
        <p><strong>📅 Published:</strong> {article.get('date', 'Unknown Date')}</p>
        <p><strong>📰 Source:</strong> {article.get('source', 'Unknown Source')}</p>
        <p><strong>📝 Snippet:</strong> {article.get('snippet', 'No snippet available')[:200]}...</p>
        <p><strong>🔗 Link:</strong> <a href="{article.get('url', '#')}" target="_blank" style="color: #667eea;">Read Full Article</a></p>
    </div>
    """, unsafe_allow_html=True)

def display_metrics_dashboard():
    """Display system metrics dashboard."""
    if not st.session_state.articles:
        return
    
    # Calculate metrics
    total_articles = len(st.session_state.articles)
    sources = set()
    for article in st.session_state.articles:
        sources.add(article.get('source', 'Unknown'))
    
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
            <h3>📰 Sources</h3>
            <h2>{len(sources)}</h2>
            <p style="color: #a0aec0; font-size: 0.9rem;">News sources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🏢 Companies</h3>
            <h2>5</h2>
            <p style="color: #a0aec0; font-size: 0.9rem;">Target companies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Relevance</h3>
            <h2>High</h2>
            <p style="color: #a0aec0; font-size: 0.9rem;">Quality score</p>
        </div>
        """, unsafe_allow_html=True)

def create_charts():
    """Create visualization charts."""
    if not st.session_state.articles:
        return
    
    # Source distribution
    sources = {}
    for article in st.session_state.articles:
        source = article.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    if sources:
        st.subheader("📊 Source Distribution")
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

def collect_news_via_api(api_base_url: str, test_set: str, max_articles: int, companies: Optional[list] = None) -> dict:
    """Call the real pipeline via FastAPI."""
    payload = {
        "test_set": test_set,
        "max_articles": max_articles,
    }
    if companies:
        payload["companies"] = companies

    r = requests.post(f"{api_base_url.rstrip('/')}/collect-news", json=payload, timeout=180)
    r.raise_for_status()
    return r.json()


def scrape_via_api(api_base_url: str, url: str) -> dict:
    r = requests.post(f"{api_base_url.rstrip('/')}/scrape", json={"url": url}, timeout=120)
    r.raise_for_status()
    return r.json()


def summarize_via_api(api_base_url: str, url: Optional[str] = None, content: Optional[str] = None, min_words: int = 30, max_words: int = 40) -> dict:
    payload: Dict[str, Any] = {"min_words": min_words, "max_words": max_words}
    if url:
        payload["url"] = url
    if content:
        payload["content"] = content
    r = requests.post(f"{api_base_url.rstrip('/')}/summarize", json=payload, timeout=180)
    r.raise_for_status()
    return r.json()


def _format_http_error(e: Exception) -> str:
    resp = getattr(e, "response", None)
    if resp is None:
        return str(e)
    try:
        return json.dumps(resp.json(), indent=2)
    except Exception:
        try:
            return resp.text
        except Exception:
            return str(e)


def classify_via_api(api_base_url: str, articles: List[Dict[str, Any]], companies: List[str]) -> dict:
    r = requests.post(
        f"{api_base_url.rstrip('/')}/classify",
        json={"articles": articles, "companies": companies},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()


def webrag_ingest_via_api(api_base_url: str, urls: List[str], session_id: Optional[str] = None, chunk_size: int = 1000, chunk_overlap: int = 200) -> dict:
    payload: Dict[str, Any] = {
        "urls": urls,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
    }
    if session_id:
        payload["session_id"] = session_id
    r = requests.post(f"{api_base_url.rstrip('/')}/webrag/ingest", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()


def webrag_query_via_api(api_base_url: str, session_id: str, question: str, top_k: int = 5) -> dict:
    r = requests.post(
        f"{api_base_url.rstrip('/')}/webrag/query",
        json={"session_id": session_id, "question": question, "top_k": top_k},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()


def _get_nested(d: dict, path: list, default):
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default

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

    st.markdown("### 🔌 Backend")
    api_base_url = st.text_input(
        "FastAPI base URL",
        value=st.session_state.get("api_base_url", "http://localhost:8000"),
        help="Start the backend first (see instructions below)."
    )
    st.session_state["api_base_url"] = api_base_url

    col_ping_1, col_ping_2 = st.columns(2)
    with col_ping_1:
        ping = st.button("💚 Health")
    with col_ping_2:
        show_backend_error = st.toggle("Show errors", value=False)

    if ping:
        try:
            rr = requests.get(f"{api_base_url.rstrip('/')}/health", timeout=30)
            rr.raise_for_status()
            st.success("Backend healthy")
        except Exception as e:
            st.error("Backend not reachable")
            if show_backend_error:
                st.exception(e)
    
    # Test set selection
    test_set = st.selectbox(
        "📊 Select Test Set",
        options=list(TEST_SETS.keys()),
        index=list(TEST_SETS.keys()).index(DEFAULT_TEST_SET) if DEFAULT_TEST_SET in TEST_SETS else 0
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
        max_value=50,
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
    **Companies:** {len(TEST_SETS[test_set]['companies'])}
    **Timeframe:** 7 days
    **Relevance Threshold:** 0.7
    """)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🗑️ Clear All Data"):
        st.session_state.articles = []
        st.session_state.messages = []
        st.session_state.last_summary = None
        st.session_state.last_classification = None
        st.rerun()

# Main tabs
tab_collection, tab_summaries, tab_webrag, tab_classification = st.tabs(
    ["📰 News Collection", "📝 Summaries", "🔎 WebRAG Chat", "🏷️ Classification"]
)

# ---------------------------
# Tab 1: Collection
# ---------------------------
with tab_collection:
    st.markdown("### 📰 Agentic News Collection")

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
        
        st.session_state.messages.append(user_message)
        
        # Add system message
        st.session_state.messages.append(f"🔄 Starting news collection for {test_set}...")
        
        # Run workflow
        with st.spinner("🔄 Collecting news via agentic pipeline... This may take a moment..."):
            try:
                api_result = collect_news_via_api(api_base_url, test_set, max_articles, custom_companies)
            except Exception as e:
                st.session_state.messages.append("❌ Backend call failed. Make sure the FastAPI server is running.")
                if show_backend_error:
                    st.session_state.messages.append(f"❌ Details: {e}")
                st.rerun()

        # Pull final articles from pipeline output
        # Pipeline returns nested results; the final enriched list is usually in company_extraction.articles
        extracted = _get_nested(api_result, ["results", "company_extraction", "articles"], [])

        # Fallbacks for debugging / usability
        validated_fallback = _get_nested(api_result, ["results", "source_validation", "validated_articles"], [])
        searched_fallback = _get_nested(api_result, ["results", "search", "results"], [])

        stage_counts = {
            "searched": len(searched_fallback) if isinstance(searched_fallback, list) else 0,
            "date_filtered": int(_get_nested(api_result, ["results", "date_filter", "articles_retained"], 0) or 0),
            "source_validated": int(_get_nested(api_result, ["results", "source_validation", "articles_passed_validation"], 0) or 0),
            "company_extracted": len(extracted) if isinstance(extracted, list) else 0,
        }

        final_list = extracted
        if not final_list and isinstance(validated_fallback, list) and validated_fallback:
            # If extraction is empty, show validated articles so you can see pipeline output.
            final_list = validated_fallback

        articles = []
        for a in final_list:
            articles.append({
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "date": a.get("date", ""),
                "source": a.get("source", ""),
                "snippet": a.get("snippet", a.get("body", "")),
                "companies": a.get("tagged_companies", []),
                "relevance_score": a.get("relevance_score", 0.0),
            })

        st.session_state.articles = articles

        st.session_state.messages.append(f"✅ Successfully collected {len(articles)} articles!")
        st.session_state.messages.append(
            f"""
📊 **Collection Summary:**
- **Backend:** {api_base_url}
- **Test Set:** {test_set}
- **Articles Found:** {len(articles)}
- **Sources:** {len(set(a.get('source', 'Unknown') for a in articles))}

🔎 **Pipeline counts:**
- searched: {stage_counts['searched']}
- date_filtered: {stage_counts['date_filtered']}
- source_validated: {stage_counts['source_validated']}
- company_extracted: {stage_counts['company_extracted']}
            """
        )
        
        st.rerun()

    if st.session_state.messages:
        for message in st.session_state.messages:
            if "✅" in message and "Summary" in message:
                display_message(message, "assistant")
            elif "🔄" in message:
                display_message(message, "system")
            elif "✅" in message:
                display_message(message, "success")
            elif "❌" in message:
                display_message(message, "error")
            else:
                display_message(message, "user")
    else:
        st.markdown(
            """<div class="chat-message assistant-message" style="margin: 10px 0;">
            <strong>How to use:</strong><br>
            1) Pick a test set in the sidebar<br>
            2) Optional: add custom companies<br>
            3) Click <strong>Collect News</strong><br>
            </div>""",
            unsafe_allow_html=True,
        )

    if st.session_state.articles:
        st.markdown("---")
        st.markdown("## 📰 Collected Articles")
        display_metrics_dashboard()

        for article in st.session_state.articles:
            title = article.get('title', '')
            with st.expander(f"📰 {title[:60]}...", expanded=False):
                display_article_card(article)

        create_charts()


# ---------------------------
# Tab 2: Summaries
# ---------------------------
with tab_summaries:
    st.markdown("### 📝 Scrape + 30–40 word Summaries")
    st.caption("Uses backend /summarize (scrapes the URL if content is not provided).")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        url_to_summarize = st.text_input("Article URL", value=st.session_state.summary_url)
    with col_b:
        do_summary = st.button("📝 Generate Summary", use_container_width=True)

    if st.session_state.articles and not url_to_summarize:
        titles = [a.get("title", "") for a in st.session_state.articles]
        pick = st.selectbox("Or pick from collected articles", options=["(select)"] + titles, key="summary_pick")
        if pick != "(select)":
            idx = titles.index(pick)
            url_to_summarize = st.session_state.articles[idx].get("url", "")
            st.session_state.summary_url = url_to_summarize

    # Persist manual edits too
    st.session_state.summary_url = url_to_summarize

    if do_summary:
        if not url_to_summarize.strip():
            st.error("Provide a URL (or pick an article)")
        else:
            with st.spinner("Generating summary..."):
                try:
                    s = summarize_via_api(api_base_url, url=url_to_summarize.strip(), min_words=30, max_words=40)
                    st.session_state.last_summary = s
                except Exception as e:
                    st.error("Summary failed")
                    if show_backend_error:
                        st.code(_format_http_error(e), language="json")

    if st.session_state.last_summary:
        st.success(f"✅ {st.session_state.last_summary.get('word_count', 0)} words")
        st.markdown(f"**Summary:** {st.session_state.last_summary.get('summary', '')}")


# ---------------------------
# Tab 3: WebRAG
# ---------------------------
with tab_webrag:
    st.markdown("### 🔎 WebRAG: Ingest URLs + Chat")
    st.caption("Lightweight WebRAG: scrape → chunk → keyword retrieval → answer from top chunks.")

    urls_text = st.text_area(
        "URLs to ingest (one per line)",
        value="",
        placeholder="https://example.com/article1\nhttps://example.com/article2",
        height=120,
    )
    ingest = st.button("📥 Ingest URLs", use_container_width=True)

    if ingest:
        urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
        if not urls:
            st.error("Provide at least one URL")
        else:
            with st.spinner("Ingesting URLs..."):
                try:
                    resp = webrag_ingest_via_api(api_base_url, urls, session_id=st.session_state.webrag_session_id)
                    st.session_state.webrag_session_id = resp.get("session_id")
                    st.success(f"✅ Ingested. session_id={st.session_state.webrag_session_id} chunks={resp.get('chunks_created', 0)}")
                except Exception as e:
                    st.error("Ingest failed")
                    if show_backend_error:
                        st.exception(e)

    st.markdown("---")
    st.markdown(f"**Session:** `{st.session_state.webrag_session_id}`" if st.session_state.webrag_session_id else "**Session:** (none)")

    q = st.text_input("Ask a question about the ingested web pages")
    ask = st.button("💬 Ask", use_container_width=True)

    if ask:
        if not st.session_state.webrag_session_id:
            st.error("Ingest at least one URL first")
        elif not q.strip():
            st.error("Ask a question")
        else:
            st.session_state.webrag_messages.append({"role": "user", "content": q.strip()})
            with st.spinner("Answering..."):
                try:
                    resp = webrag_query_via_api(api_base_url, st.session_state.webrag_session_id, q.strip(), top_k=5)
                    st.session_state.webrag_messages.append({"role": "assistant", "content": resp.get("answer", "")})
                    st.session_state.webrag_messages.append({"role": "system", "content": json.dumps(resp.get("sources", []), indent=2)})
                except Exception as e:
                    st.session_state.webrag_messages.append({"role": "assistant", "content": "Failed to answer."})
                    if show_backend_error:
                        st.session_state.webrag_messages.append({"role": "system", "content": str(e)})

    for m in st.session_state.webrag_messages[-12:]:
        display_message(m.get("content", ""), m.get("role", "assistant"))


# ---------------------------
# Tab 4: Classification
# ---------------------------
with tab_classification:
    st.markdown("### 🏷️ Classification (Group by Company)")
    st.caption("Uses backend /classify (company matching + variations).")

    if not st.session_state.articles:
        st.info("Collect articles first in the News Collection tab.")
    else:
        companies_for_classification = TEST_SETS.get(test_set, {}).get("companies", [])
        if custom_companies_input.strip():
            companies_for_classification = [c.strip() for c in custom_companies_input.split(",") if c.strip()]

        classify_btn = st.button("🏷️ Run Classification", use_container_width=True)
        if classify_btn:
            with st.spinner("Classifying..."):
                try:
                    resp = classify_via_api(api_base_url, st.session_state.articles, companies_for_classification)
                    st.session_state.last_classification = resp
                except Exception as e:
                    st.error("Classification failed")
                    if show_backend_error:
                        st.exception(e)

        if st.session_state.last_classification:
            by_company = st.session_state.last_classification.get("by_company", {})
            unclassified = st.session_state.last_classification.get("unclassified", [])

            st.markdown("#### Results")
            for company, items in by_company.items():
                if not items:
                    continue
                with st.expander(f"🏢 {company} ({len(items)})", expanded=False):
                    st.dataframe(pd.DataFrame(items), use_container_width=True)

            if unclassified:
                with st.expander(f"❓ Unclassified ({len(unclassified)})", expanded=False):
                    st.dataframe(pd.DataFrame(unclassified), use_container_width=True)
