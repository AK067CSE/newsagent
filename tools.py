"""
Shared tools for News Aggregation System

Contains DuckDuckGo search, web scraping, and utility functions used across agents.
"""

import os
import asyncio
import sys
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from bs4 import BeautifulSoup
import requests
from google.adk.tools import ToolContext
from google.genai import types

# Set Windows event loop policy for async operations
# Playwright (used by Crawl4AI) may require the Selector event loop to spawn subprocesses on Windows.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Crawl4AI uses Playwright which may not support subprocess creation on some
# Windows + Python 3.13 environments. If disabled, we will automatically fall
# back to BeautifulSoup.
_force_enable_crawl4ai = os.getenv("WEBRAG_FORCE_CRAWL4AI", "").strip().lower() in {"1", "true", "yes", "on"}
_force_disable_crawl4ai = os.getenv("WEBRAG_DISABLE_CRAWL4AI", "").strip().lower() in {"1", "true", "yes", "on"}

CRAWL4AI_ENABLED = (not _force_disable_crawl4ai) and (
    _force_enable_crawl4ai or not (sys.platform == "win32" and sys.version_info >= (3, 13))
)

# Apply nest_asyncio for nested event loops
import nest_asyncio
nest_asyncio.apply()

class DuckDuckGoSearchTool:
    """DuckDuckGo search functionality for news aggregation."""
    
    def __init__(self):
        self.ddgs = DDGS()
    
    def search_news(self, query: str, timeframe: str = "7d", max_results: int = 100, max_retries: int = 4) -> List[Dict[str, Any]]:
        """
        Search DuckDuckGo for news articles.
        
        Args:
            query: Search query string
            timeframe: Time filter (e.g., "7d", "1w")
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with metadata
        """
        last_err: Optional[Exception] = None

        # DDG is rate-limited aggressively (often surfaces as HTTP 202 "Ratelimit").
        # Use small retries with exponential backoff + jitter.
        for attempt in range(max_retries):
            try:
                results = list(self.ddgs.news(
                    keywords=query,
                    region="wt-wt",
                    safesearch="off",
                    timelimit=timeframe,
                    max_results=max_results
                ))

                # Standardize result format
                standardized_results = []
                for result in results:
                    standardized_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "date": result.get("date", ""),
                        "body": result.get("body", ""),
                        "source": self._extract_source_from_url(result.get("url", "")),
                        "query": query
                    })

                return standardized_results

            except Exception as e:
                last_err = e
                msg = str(e)

                is_rate_limit = ("202" in msg) or ("ratelimit" in msg.lower())
                if not is_rate_limit or attempt == max_retries - 1:
                    break

                # Exponential backoff: 1.5s, 3s, 6s, 12s (+ jitter)
                sleep_s = (1.5 * (2 ** attempt)) + random.uniform(0.0, 0.8)
                time.sleep(sleep_s)

        print(f"Error in DuckDuckGo search: {last_err}")
        return []
    
    def _extract_source_from_url(self, url: str) -> str:
        """Extract source name from URL."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace("www.", "").split(".")[0].title()
        except:
            return "Unknown"

class WebScrapingTool:
    """Multi-method web scraping for article content extraction."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_beautifulsoup(self, url: str) -> Dict[str, Any]:
        """
        Scrape webpage using BeautifulSoup.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped content and metadata
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Connection": "keep-alive",
            }
            response = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            # Extract text from relevant tags
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'main'])
            content = ' '.join([elem.get_text(strip=True) for elem in text_elements])
            
            # Clean up whitespace
            content = ' '.join(content.split())
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            return {
                "status": "success",
                "method": "beautifulsoup",
                "title": title_text,
                "content": content,
                "content_length": len(content),
                "url": url
            }
            
        except Exception as e:
            return {
                "status": "error",
                "method": "beautifulsoup",
                "error": str(e),
                "url": url
            }
    
    async def scrape_crawl4ai(self, url: str) -> Dict[str, Any]:
        """
        Scrape webpage using Crawl4AI (async method).
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped content and metadata
        """
        try:
            config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url, config=config)
                
                return {
                    "status": "success",
                    "method": "crawl4ai",
                    "title": result.metadata.get("title", ""),
                    "content": result.markdown,
                    "content_length": len(result.markdown),
                    "url": url
                }
                
        except Exception as e:
            return {
                "status": "error",
                "method": "crawl4ai",
                "error": str(e),
                "url": url
            }
    
    def scrape_crawl4ai_sync(self, url: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for Crawl4AI scraping.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped content and metadata
        """
        if not CRAWL4AI_ENABLED:
            return {
                "status": "error",
                "method": "crawl4ai_sync",
                "error": "Crawl4AI disabled on Windows Python 3.13 due to Playwright subprocess limitations; using BeautifulSoup fallback.",
                "url": url,
            }

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(self.scrape_crawl4ai(url))
        except NotImplementedError as e:
            return {
                "status": "error",
                "method": "crawl4ai_sync",
                "error": f"Crawl4AI/Playwright subprocess unsupported in current event loop: {str(e)}",
                "url": url
            }
        except Exception as e:
            return {
                "status": "error",
                "method": "crawl4ai_sync",
                "error": str(e),
                "url": url
            }
    
    def scrape_with_fallback(self, url: str) -> Dict[str, Any]:
        """
        Scrape URL with multiple fallback methods.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped content and metadata
        """
        # Try Crawl4AI first (best extraction for JS-heavy pages), then fall back to BeautifulSoup.
        result = self.scrape_crawl4ai_sync(url)
        if result.get("status") == "success" and len(result.get("content", "")) > 300:
            return result

        result_bs = self.scrape_beautifulsoup(url)
        if result_bs.get("status") == "success" and len(result_bs.get("content", "")) > 300:
            return result_bs

        # If both are weak/empty, prefer the one that succeeded (even with low content), else return BS error.
        if result.get("status") == "success":
            return result
        if result_bs.get("status") == "success":
            return result_bs
        result = result_bs
        
        # Return error if all methods fail
        return {
            "status": "error",
            "method": "all_methods_failed",
            "error": "All scraping methods failed",
            "url": url
        }

class ContentProcessor:
    """Content processing utilities for news articles."""
    
    @staticmethod
    def extract_companies_from_text(text: str, companies: List[str]) -> List[str]:
        """
        Extract company names from text.
        
        Args:
            text: Text to analyze
            companies: List of companies to look for
            
        Returns:
            List of companies found in text
        """
        found_companies = []
        text_lower = text.lower()
        
        for company in companies:
            # Check for exact company name
            if company.lower() in text_lower:
                found_companies.append(company)
                continue
            
            # Check for common variations
            variations = ContentProcessor._get_company_variations(company)
            for variation in variations:
                if variation.lower() in text_lower:
                    found_companies.append(company)
                    break
        
        return list(set(found_companies))  # Remove duplicates
    
    @staticmethod
    def _get_company_variations(company: str) -> List[str]:
        """Get common variations for company names."""
        variations = {
            "TCS": ["Tata Consultancy Services", "TCS Ltd"],
            "Wipro": ["Wipro Limited", "Wipro Technologies"],
            "Infosys": ["Infosys Limited", "Infosys Technologies"],
            "HCLTech": ["HCL Technologies", "HCLTech Limited"],
            "Airtel": ["Bharti Airtel", "Airtel Limited"],
            "Jio": ["Reliance Jio", "Jio Platforms"],
            "Vodafone Idea": ["Vi", "Vodafone Idea Limited"],
            "BSNL": ["Bharat Sanchar Nigam Limited"],
            "MTNL": ["Mahanagar Telephone Nigam Limited"],
            "Tejas Networks": ["Tejas Networks Limited"],
            "OpenAI": ["OpenAI LP", "OpenAI Inc"],
            "Anthropic": ["Anthropic PBC"],
            "Google Deepmind": ["DeepMind", "Google DeepMind"],
            "Microsoft": ["MSFT", "Microsoft Corporation"],
            "Meta": ["Facebook", "Meta Platforms"],
            "Google": ["Alphabet", "Alphabet Inc", "Google LLC"],
            "Apple": ["Apple Inc", "AAPL"]
        }
        
        return variations.get(company, [])
    
    @staticmethod
    def calculate_relevance_score(text: str, companies: List[str]) -> float:
        """
        Calculate relevance score for article relative to companies.
        
        Args:
            text: Article text
            companies: List of target companies
            
        Returns:
            Relevance score between 0 and 1
        """
        if not companies:
            return 0.0
        
        found_companies = ContentProcessor.extract_companies_from_text(text, companies)
        
        # Base score from company mentions
        company_score = len(found_companies) / len(companies)
        
        # Boost score for multiple mentions
        text_lower = text.lower()
        mention_count = 0
        for company in found_companies:
            variations = ContentProcessor._get_company_variations(company) + [company]
            for variation in variations:
                mention_count += text_lower.count(variation.lower())
        
        # Normalize mention count (cap at 5 mentions per company)
        mention_score = min(mention_count / (len(companies) * 5), 1.0)
        
        # Combine scores
        final_score = (company_score * 0.6) + (mention_score * 0.4)
        
        return min(final_score, 1.0)
    
    @staticmethod
    def generate_summary(content: str, max_words: int = 40, min_words: int = 30) -> str:
        """
        Generate a concise summary from content.
        
        Args:
            content: Full article content
            max_words: Maximum word count
            min_words: Minimum word count
            
        Returns:
            Generated summary
        """
        # Simple extractive summarization
        sentences = content.split('.')
        
        # Filter out very short sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return "Content not available for summarization."
        
        # Take first few sentences until word count is reached
        summary = ""
        word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= max_words:
                summary += sentence + ". "
                word_count += sentence_words
            else:
                # Take part of the sentence if needed
                remaining_words = max_words - word_count
                if remaining_words > 5:
                    words = sentence.split()[:remaining_words]
                    summary += " ".join(words) + "..."
                break
        
        summary = summary.strip()
        
        # Ensure minimum word count
        if len(summary.split()) < min_words:
            # Add more content if available
            if len(sentences) > 0:
                additional = sentences[0][:max_words*6]  # Rough character limit
                summary = additional[:max_words*6].rsplit(' ', 1)[0] + "..."
        
        return summary if summary else "Summary generation failed."

# Tool instances
duckduckgo_tool = DuckDuckGoSearchTool()
web_scraper = WebScrapingTool()
content_processor = ContentProcessor()

# Export tool functions for ADK integration
def search_duckduckgo_news(tool_context: ToolContext, query: str, timeframe: str = "7d") -> dict:
    """Search DuckDuckGo for news articles."""
    try:
        results = duckduckgo_tool.search_news(query, timeframe)
        
        # Store search metadata in state
        tool_context.state["temp:last_search_query"] = query
        tool_context.state["temp:last_search_time"] = datetime.now().isoformat()
        tool_context.state["temp:last_search_results"] = len(results)
        
        return {
            "status": "success",
            "query": query,
            "timeframe": timeframe,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e)
        }

def scrape_article_content(tool_context: ToolContext, url: str) -> dict:
    """Scrape article content using multiple methods."""
    try:
        result = web_scraper.scrape_with_fallback(url)
        
        # Store scraping metadata in state
        tool_context.state["temp:scraped_urls"] = tool_context.state.get("temp:scraped_urls", []) + [url]
        tool_context.state["temp:scraping_success_count"] = tool_context.state.get("temp:scraping_success_count", 0) + (1 if result["status"] == "success" else 0)
        
        # Store content as artifact if successful
        if result["status"] == "success":
            artifact_data = types.Part.from_text(text=result["content"])
            artifact_id = f"article_{hash(url)}.txt"
            tool_context.save_artifact(artifact_id, artifact_data)
            result["artifact_id"] = artifact_id
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": str(e)
        }

def extract_company_entities(tool_context: ToolContext, text: str, companies: list) -> dict:
    """Extract company entities from text."""
    try:
        found_companies = content_processor.extract_companies_from_text(text, companies)
        relevance_score = content_processor.calculate_relevance_score(text, companies)
        
        return {
            "status": "success",
            "found_companies": found_companies,
            "relevance_score": relevance_score,
            "total_companies_searched": len(companies)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def validate_article_date(tool_context: ToolContext, article_date: str, days_limit: int = 7) -> dict:
    """Validate article is within specified timeframe."""
    try:
        # This is a simplified date validation
        # In production, you'd use more sophisticated date parsing
        current_date = datetime.now()
        
        # Try to parse the date (simplified for demo)
        if "ago" in article_date.lower() or "hours" in article_date.lower() or "days" in article_date.lower():
            is_valid = True
        else:
            # For dates with actual date strings, you'd parse them properly
            is_valid = True  # Simplified for demo
        
        return {
            "status": "success",
            "article_date": article_date,
            "is_valid": is_valid,
            "days_limit": days_limit
        }
    except Exception as e:
        return {
            "status": "error",
            "article_date": article_date,
            "error": str(e)
        }
