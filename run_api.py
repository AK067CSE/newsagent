#!/usr/bin/env python3
"""
News Aggregation API Server Launcher

Run this script to start the FastAPI server.
"""

import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main function to start the API server."""
    print("🚀 Starting News Aggregation API Server...")
    print("=" * 60)
    
    # Configuration
    host = "0.0.0.0"
    port = 8000
    reload = True  # Enable auto-reload for development
    
    print(f"📍 Server will run on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 ReDoc Documentation: http://{host}:{port}/redoc")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"📊 System Stats: http://{host}:{port}/stats")
    print("=" * 60)
    print("🔧 Configuration:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print(f"   Workers: 1 (development)")
    print("=" * 60)
    print("🎯 Available Endpoints:")
    print("   GET  /                    - Root endpoint")
    print("   GET  /health              - Health check")
    print("   GET  /stats               - System statistics")
    print("   GET  /test-sets           - Get test sets")
    print("   POST /search-plan         - Create search plan")
    print("   POST /search-news         - Search news")
    print("   POST /collect-news       - Collect news (workflow)")
    print("   POST /workflow            - Full workflow")
    print("   POST /collect-news-async  - Async collection")
    print("   GET  /task-status/{{id}}   - Task status")
    print("=" * 60)
    print("🚀 Starting server...")
    
    try:
        # Start the server
        uvicorn.run(
            "api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
