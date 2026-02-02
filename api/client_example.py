"""
Client Example for News Aggregation API

Demonstrates how to use the API endpoints.
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

class NewsAggregationClient:
    """Client for News Aggregation API."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_health(self) -> Dict[str, Any]:
        """Check API health."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        response = self.session.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()
    
    def get_test_sets(self) -> Dict[str, Any]:
        """Get available test sets."""
        response = self.session.get(f"{self.base_url}/test-sets")
        response.raise_for_status()
        return response.json()
    
    def create_search_plan(self, test_set: str, companies: list = None) -> Dict[str, Any]:
        """Create a search plan."""
        payload = {"test_set": test_set}
        if companies:
            payload["companies"] = companies
        
        response = self.session.post(f"{self.base_url}/search-plan", json=payload)
        response.raise_for_status()
        return response.json()
    
    def search_news(self, test_set: str, max_results: int = 20, companies: str = None) -> Dict[str, Any]:
        """Search for news articles."""
        params = {"test_set": test_set, "max_results": max_results}
        if companies:
            params["companies"] = companies
        
        response = self.session.post(f"{self.base_url}/search-news", params=params)
        response.raise_for_status()
        return response.json()
    
    def collect_news(self, test_set: str, max_articles: int = 20, companies: list = None) -> Dict[str, Any]:
        """Run complete news collection workflow."""
        payload = {"test_set": test_set, "max_articles": max_articles}
        if companies:
            payload["companies"] = companies
        
        response = self.session.post(f"{self.base_url}/collect-news", json=payload)
        response.raise_for_status()
        return response.json()
    
    def collect_news_async(self, test_set: str, max_articles: int = 20, companies: list = None) -> Dict[str, Any]:
        """Start async news collection."""
        payload = {"test_set": test_set, "max_articles": max_articles}
        if companies:
            payload["companies"] = companies
        
        response = self.session.post(f"{self.base_url}/collect-news-async", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of background task."""
        response = self.session.get(f"{self.base_url}/task-status/{task_id}")
        response.raise_for_status()
        return response.json()

def demo_api_usage():
    """Demonstrate API usage."""
    print("🚀 News Aggregation API Demo")
    print("=" * 50)
    
    client = NewsAggregationClient()
    
    try:
        # 1. Check API health
        print("\n🏥 Checking API Health...")
        health = client.get_health()
        print(f"✅ Status: {health['status']}")
        print(f"   Version: {health['version']}")
        
        # 2. Get system stats
        print("\n📊 Getting System Stats...")
        stats = client.get_stats()
        print(f"✅ System: {stats['system']['name']}")
        print(f"   Test Sets: {stats['test_sets']['total']}")
        print(f"   Companies: {stats['test_sets']['total_companies']}")
        
        # 3. Get test sets
        print("\n📋 Getting Test Sets...")
        test_sets = client.get_test_sets()
        print(f"✅ Default: {test_sets['default_test_set']}")
        for test_set in test_sets['test_sets']:
            print(f"   - {test_set}: {test_sets['test_sets'][test_set]['companies']} companies")
        
        # 4. Create search plan
        print("\n📝 Creating Search Plan...")
        plan = client.create_search_plan("AI Companies")
        print(f"✅ Test Set: {plan['test_set']}")
        print(f"   Companies: {plan['companies']}")
        print(f"   Queries: {plan['queries_generated']}")
        
        # 5. Search news
        print("\n🔍 Searching News...")
        search = client.search_news("AI Companies", max_results=10)
        print(f"✅ Status: {search['status']}")
        print(f"   Results: {search['total_results']}")
        print(f"   Processing Time: {search['processing_time']:.2f}s")
        
        if search['articles']:
            print(f"   Sample Article: {search['articles'][0]['title'][:50]}...")
        
        # 6. Collect news (full workflow)
        print("\n🔄 Running Full Workflow...")
        workflow = client.collect_news("AI Companies", max_articles=15)
        print(f"✅ Status: {workflow['status']}")
        print(f"   Phase: {workflow['phase']}")
        print(f"   Processing Time: {workflow['processing_time']:.2f}s")
        
        if workflow['results']:
            print("   Workflow Results:")
            for phase, result in workflow['results'].items():
                if isinstance(result, dict) and 'status' in result:
                    print(f"     - {phase}: {result['status']}")
        
        # 7. Async collection demo
        print("\n⚡ Starting Async Collection...")
        async_task = client.collect_news_async("IT Companies", max_articles=10)
        print(f"✅ Task ID: {async_task['task_id']}")
        print(f"   Status: {async_task['status']}")
        
        # Check task status
        task_id = async_task['task_id']
        for i in range(10):  # Check for 10 seconds
            time.sleep(1)
            status = client.get_task_status(task_id)
            print(f"   Progress: {status.get('progress', 0)}% - {status.get('status', 'unknown')}")
            if status.get('status') in ['completed', 'failed']:
                break
        
        print("\n🎉 Demo Completed Successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demo_api_usage()
