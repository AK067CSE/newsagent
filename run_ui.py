#!/usr/bin/env python3
"""
News Aggregation Streamlit UI Launcher

Run this script to start the Streamlit web interface.
"""

import streamlit
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main function to start the Streamlit UI."""
    print("🎨 Starting News Aggregation Streamlit UI...")
    print("=" * 60)
    
    # Configuration
    print("🎨 Streamlit Configuration:")
    print("   Theme: Dark Mode Optimized")
    print("   Layout: Wide")
    print("   Page Title: News Aggregation System")
    print("   Page Icon: 📰")
    print("=" * 60)
    
    print("🌐 UI Features:")
    print("   🤖 AI Chatbot Interface")
    print("   📊 Real-time News Collection")
    print("   📈 Interactive Analytics Dashboard")
    print("   📰 Article Cards with Details")
    print("   📊 Company Distribution Charts")
    print("   📰 Source Distribution Charts")
    print("   🎨 Dark Mode Optimized Design")
    print("   📱 Responsive Layout")
    print("=" * 60)
    
    print("🚀 Starting Streamlit server...")
    
    try:
        # Start Streamlit app using subprocess
        import subprocess
        import sys
        
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "ui.app",
            "--server.address=0.0.0.0",
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ]
        
        print(f"🚀 Running command: {' '.join(cmd)}")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped by user")
    except Exception as e:
        print(f"❌ Streamlit error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
