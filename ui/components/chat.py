"""
Chat Interface Component

Dark mode optimized chat interface for the news aggregation system.
"""

import streamlit as st
import time
from datetime import datetime
from typing import List, Dict, Any

class ChatInterface:
    """Chat interface component for user interaction."""
    
    @staticmethod
    def display_message(message: Dict[str, Any], message_type: str = "assistant"):
        """Display a chat message with appropriate styling."""
        message_classes = {
            "user": "user-message",
            "assistant": "assistant-message", 
            "system": "system-message",
            "success": "success-message",
            "error": "error-message"
        }
        
        css_class = message_classes.get(message_type, "assistant-message")
        
        # Icon mapping
        icons = {
            "user": "👤",
            "assistant": "🤖",
            "system": "⚙️",
            "success": "✅",
            "error": "❌"
        }
        
        icon = icons.get(message_type, "🤖")
        
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>{icon} {message_type.title()}:</strong> {message.get('content', '')}
            {f"<br><small>{message.get('timestamp', datetime.now()).strftime('%H:%M:%S')}</small>" if message.get('timestamp') else ""}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_welcome_message():
        """Display welcome message for new users."""
        welcome_content = """
        👋 Welcome to the News Aggregation System!

        I'm your AI-powered assistant for collecting and analyzing financial news. Here's what I can do:

        🔍 **Search News:** Collect news from DuckDuckGo about specific companies
        📅 **Date Filtering:** Filter articles to the last 7 days
        🛡️ **Source Validation:** Ensure credible news sources
        🏢 **Entity Extraction:** Identify company mentions in articles
        📊 **Analytics:** Provide insights and visualizations

        **To get started:**
        1. Select a test set from the sidebar (AI Companies, IT Companies, Telecom Companies, or Global IT)
        2. Optionally enter custom companies
        3. Click "Collect News" to start the workflow
        4. View results and analytics in real-time

        **Available Test Sets:**
        🤖️ **AI Companies:** OpenAI, Anthropic, Google Deepmind, Microsoft, Meta
        💻 **IT Companies:** TCS, Wipro, Infosys, HCLTech
        📱 **Telecom Companies:** Airtel, Jio, Vodafone Idea, BSNL, MTNL, Tejas Networks
        🌍 **Global IT:** Microsoft, Google, Apple, Meta

        Ready to start collecting news? Configure your preferences in the sidebar and click "Collect News"!
        """
        
        st.markdown(f"""
        <div class="chat-message assistant-message" style="margin: 20px 0;">
            {welcome_content}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_workflow_status(phase: str, status: str, details: str = ""):
        """Display workflow status update."""
        status_icons = {
            "starting": "🔄",
            "search_plan": "📋",
            "search": "🔍",
            "filtering": "📅",
            "validation": "🛡️",
            "extraction": "🏢",
            "completed": "✅",
            "error": "❌"
        }
        
        icon = status_icons.get(phase, "🔄")
        
        ChatInterface.display_message({
            "content": f"{icon} {phase.title()}: {status}. {details}",
            "timestamp": datetime.now()
        }, "system")
    
    @staticmethod
    def display_success_message(message: str, details: str = ""):
        """Display success message."""
        ChatInterface.display_message({
            "content": f"{message} {details}",
            "timestamp": datetime.now()
        }, "success")
    
    @staticmethod
    def display_error_message(message: str, details: str = ""):
        """Display error message."""
        ChatInterface.display_message({
            "content": f"{message} {details}",
            "timestamp": datetime.now()
        }, "error")
    
    @staticmethod
    def display_summary(summary_data: Dict[str, Any]):
        """Display workflow summary."""
        summary_content = f"""
        📊 **Collection Summary:**
        - **Test Set:** {summary_data.get('test_set', 'Unknown')}
        - **Articles Found:** {summary_data.get('total_articles', 0)}
        - **Companies Detected:** {summary_data.get('companies_count', 0)}
        - **Sources:** {summary_data.get('sources_count', 0)}
        - **Processing Time:** {summary_data.get('processing_time', 0):.2f}s
        """
        
        ChatInterface.display_message({
            "content": summary_content,
            "timestamp": datetime.now()
        }, "assistant")
    
    @staticmethod
    def display_progress(message: str, progress: int = 0):
        """Display progress update."""
        progress_bar = f"{'█' * (progress // 10)}{'░' * (10 - progress // 10)} {progress}%"
        ChatInterface.display_message({
            "content": f"{message}\n{progress_bar}",
            "timestamp": datetime.now()
        }, "system")
