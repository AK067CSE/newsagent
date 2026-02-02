"""
Tools for News Collection Agent

Specialized tools for news search, filtering, and validation.
"""

from google.adk.tools import ToolContext
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re

# Import parent tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools import search_duckduckgo_news, validate_article_date

def create_search_plan(tool_context: ToolContext, test_set: str, companies: List[str]) -> dict:
    """
    Create a detailed search plan for the specified test set and companies.
    
    Args:
        tool_context: ADK tool context
        test_set: Test set name
        companies: List of companies to search for
        
    Returns:
        Detailed search plan with queries and focus areas
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Generate search queries based on test set
        search_queries = []
        
        if test_set == "AI Companies":
            search_queries = [
                {"query": f"{company} AI news last 7 days", "category": "technology", "priority": 1}
                for company in companies
            ]
            # Add specific AI-related queries
            search_queries.extend([
                {"query": "OpenAI GPT model release December 2024", "category": "technology", "priority": 1},
                {"query": "Anthropic Claude AI updates last week", "category": "technology", "priority": 1},
                {"query": "Google Deepmind Gemini AI recent news", "category": "technology", "priority": 1},
                {"query": "Microsoft AI Copilot enterprise adoption", "category": "business", "priority": 1},
                {"query": "Meta LLaMA open source AI December", "category": "technology", "priority": 1}
            ])
            
        elif test_set == "IT Companies":
            search_queries = [
                {"query": f"{company} quarterly results Q4 2024", "category": "financial", "priority": 1}
                for company in companies
            ]
            # Add IT-specific queries
            search_queries.extend([
                {"query": "TCS Wipro Infosys HCLTech digital transformation deals", "category": "business", "priority": 1},
                {"query": "Indian IT services AI partnerships December 2024", "category": "technology", "priority": 1},
                {"query": "IT sector hiring trends layoffs 2024", "category": "business", "priority": 2}
            ])
            
        elif test_set == "Telecom Companies":
            search_queries = [
                {"query": f"{company} 5G rollout December 2024", "category": "technology", "priority": 1}
                for company in companies
            ]
            # Add telecom-specific queries
            search_queries.extend([
                {"query": "India 5G deployment subscriber growth 2024", "category": "business", "priority": 1},
                {"query": "Airtel Jio Vodafone Idea tariff plans competition", "category": "business", "priority": 1},
                {"query": "BSNL MTNL 4G 5G revival government funding", "category": "business", "priority": 1}
            ])
            
        elif test_set == "Global IT":
            search_queries = [
                {"query": f"{company} earnings December 2024 quarter", "category": "financial", "priority": 1}
                for company in companies
            ]
            # Add global IT queries
            search_queries.extend([
                {"query": "Microsoft Google Apple Meta AI competition 2024", "category": "technology", "priority": 1},
                {"query": "Big Tech antitrust regulatory challenges December", "category": "regulatory", "priority": 1},
                {"query": "cloud computing market share AWS Azure GCP", "category": "business", "priority": 1}
            ])
        
        # Define focus areas based on test set
        focus_areas = {
            "AI Companies": ["model releases", "partnerships", "enterprise adoption", "AI safety", "funding"],
            "IT Companies": ["quarterly results", "digital transformation", "AI/ML investments", "hiring trends"],
            "Telecom Companies": ["5G rollout", "subscriber numbers", "tariff plans", "regulatory developments"],
            "Global IT": ["earnings", "product launches", "market share", "innovation", "regulatory"]
        }
        
        # Primary sources
        primary_sources = [
            "Reuters", "Bloomberg", "Financial Times", "Wall Street Journal",
            "TechCrunch", "The Verge", "Wired", "VentureBeat",
            "Economic Times", "Business Standard", "Mint"
        ]
        
        search_plan = {
            "test_set": test_set,
            "companies": companies,
            "timeframe_days": 7,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "search_queries": search_queries,
            "primary_sources": primary_sources,
            "focus_areas": focus_areas.get(test_set, []),
            "status": "created"
        }
        
        # Store search plan in state
        tool_context.state["temp:search_plan"] = search_plan
        tool_context.state["temp:search_plan_created"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "search_plan": search_plan,
            "total_queries": len(search_queries),
            "focus_areas_count": len(focus_areas.get(test_set, []))
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "test_set": test_set
        }

def execute_search_queries(tool_context: ToolContext, search_queries: List[Dict[str, Any]]) -> dict:
    """
    Execute multiple search queries and aggregate results.
    
    Args:
        tool_context: ADK tool context
        search_queries: List of search queries with metadata
        
    Returns:
        Aggregated search results
    """
    try:
        all_results = []
        query_stats = {}
        
        for query_info in search_queries:
            query = query_info["query"]
            category = query_info["category"]
            
            # Execute search
            search_result = search_duckduckgo_news(tool_context, query, "7d")
            
            if search_result["status"] == "success":
                # Add category and query info to each result
                for result in search_result["results"]:
                    result["search_category"] = category
                    result["search_query"] = query
                    result["search_priority"] = query_info.get("priority", 1)
                
                all_results.extend(search_result["results"])
                query_stats[query] = len(search_result["results"])
            else:
                query_stats[query] = 0
        
        # Store results in state
        tool_context.state["temp:raw_search_results"] = all_results
        tool_context.state["temp:query_statistics"] = query_stats
        tool_context.state["temp:search_completed"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "total_results": len(all_results),
            "queries_executed": len(search_queries),
            "query_statistics": query_stats,
            "results": all_results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def filter_articles_by_date(tool_context: ToolContext, articles: List[Dict[str, Any]], days_limit: int = 7) -> dict:
    """
    Filter articles to include only those within the specified date range.
    
    Args:
        tool_context: ADK tool context
        articles: List of articles to filter
        days_limit: Number of days to include
        
    Returns:
        Filtered articles and statistics
    """
    try:
        filtered_articles = []
        removed_articles = []
        cutoff_date = datetime.now() - timedelta(days=days_limit)
        
        for article in articles:
            article_date_str = article.get("date", "")
            
            # Validate article date
            date_validation = validate_article_date(tool_context, article_date_str, days_limit)
            
            if date_validation["status"] == "success" and date_validation["is_valid"]:
                filtered_articles.append(article)
            else:
                removed_articles.append({
                    "article": article,
                    "reason": "date_outside_range",
                    "date": article_date_str
                })
        
        # Store filtering results in state
        tool_context.state["temp:date_filtered_articles"] = filtered_articles
        tool_context.state["temp:date_filtered_count"] = len(filtered_articles)
        tool_context.state["temp:date_removed_count"] = len(removed_articles)
        
        return {
            "status": "success",
            "total_before_filtering": len(articles),
            "articles_removed": len(removed_articles),
            "articles_retained": len(filtered_articles),
            "cutoff_date": cutoff_date.strftime("%Y-%m-%d"),
            "filtered_articles": filtered_articles,
            "removed_articles": removed_articles
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def validate_sources(tool_context: ToolContext, articles: List[Dict[str, Any]], required_sources: List[str], min_credibility: float = 0.5) -> dict:
    """
    Validate article sources and filter by credibility.
    
    Args:
        tool_context: ADK tool context
        articles: List of articles to validate
        required_sources: List of preferred sources
        
    Returns:
        Validated articles and source analysis
    """
    try:
        validated_articles = []
        source_stats = {}
        credibility_scores = {}
        
        # Define source credibility scores
        source_credibility = {
            "Reuters": 1.0,
            "Bloomberg": 1.0,
            "Financial Times": 1.0,
            "Wall Street Journal": 1.0,
            "Associated Press": 0.95,
            "Dow Jones": 0.95,
            "TechCrunch": 0.9,
            "The Verge": 0.9,
            "Wired": 0.9,
            "VentureBeat": 0.9,
            "Economic Times": 0.85,
            "Business Standard": 0.85,
            "Mint": 0.85
        }
        
        for article in articles:
            source = article.get("source", "Unknown")
            
            # Get credibility score
            credibility = source_credibility.get(source, 0.5)
            
            # Count source statistics
            if source not in source_stats:
                source_stats[source] = 0
            source_stats[source] += 1
            
            # Include article if:
            # - It is from an explicitly required source, OR
            # - It meets the minimum credibility threshold (default 0.5 to avoid dropping most DDG sources)
            if (source in required_sources) or (credibility >= min_credibility):
                article["source_credibility"] = credibility
                validated_articles.append(article)
            
            # Track credibility scores
            if source not in credibility_scores:
                credibility_scores[source] = []
            credibility_scores[source].append(credibility)
        
        # Store validation results in state
        tool_context.state["temp:source_validated_articles"] = validated_articles
        tool_context.state["temp:source_statistics"] = source_stats
        tool_context.state["temp:credibility_scores"] = credibility_scores
        
        # Calculate average credibility correctly
        if credibility_scores:
            all_scores = []
            for scores in credibility_scores.values():
                all_scores.extend(scores)
            average_credibility = sum(all_scores) / len(all_scores)
        else:
            average_credibility = 0
        
        return {
            "status": "success",
            "total_articles_validated": len(articles),
            "articles_passed_validation": len(validated_articles),
            "articles_failed_validation": len(articles) - len(validated_articles),
            "source_statistics": source_stats,
            "average_credibility": average_credibility,
            "validated_articles": validated_articles
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def extract_company_mentions(tool_context: ToolContext, articles: List[Dict[str, Any]], target_companies: List[str]) -> dict:
    """
    Extract company mentions from articles and calculate relevance scores.
    
    Args:
        tool_context: ADK tool context
        articles: List of articles to analyze
        target_companies: List of companies to look for
        
    Returns:
        Articles with company mentions and relevance scores
    """
    try:
        articles_with_companies = []
        company_stats = {}
        
        for article in articles:
            snippet_text = article.get('snippet') or article.get('body') or ""
            text_to_analyze = f"{article.get('title', '')} {snippet_text}"
            found_companies = []
            
            # Check for each company
            for company in target_companies:
                if company.lower() in text_to_analyze.lower():
                    found_companies.append(company)
                    
                    # Count company statistics
                    if company not in company_stats:
                        company_stats[company] = 0
                    company_stats[company] += 1
            
            # Calculate relevance score
            relevance_score = len(found_companies) / len(target_companies) if target_companies else 0
            
            # Include article if it mentions at least one company
            if found_companies:
                article["tagged_companies"] = found_companies
                article["relevance_score"] = relevance_score
                articles_with_companies.append(article)
        
        # Store results in state
        tool_context.state["temp:company_extracted_articles"] = articles_with_companies
        tool_context.state["temp:company_statistics"] = company_stats
        
        return {
            "status": "success",
            "total_articles_analyzed": len(articles),
            "articles_with_companies": len(articles_with_companies),
            "companies_found": list(company_stats.keys()),
            "company_statistics": company_stats,
            "articles": articles_with_companies
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
