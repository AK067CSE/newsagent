"""
FastAPI Main Application

RESTful API server for the News Aggregation System.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import re
import uuid
import sys
import os
import json
import zipfile
from pathlib import Path
from urllib.parse import urlparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from news_aggregation_system.config import TEST_SETS, DEFAULT_TEST_SET
from news_aggregation_system.models import Article, TestSetType, ArticleType
from news_aggregation_system.news_collection_agent.tools import (
    create_search_plan, execute_search_queries, filter_articles_by_date,
    validate_sources, extract_company_mentions
)
from news_aggregation_system.tools import duckduckgo_tool, web_scraper, content_processor

# Initialize FastAPI app
app = FastAPI(
    title="News Aggregation API",
    description="RESTful API for collecting, classifying, scraping, and summarizing financial news",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class TestSetRequest(BaseModel):
    test_set: str = Field(..., description="Test set name")
    companies: Optional[List[str]] = Field(None, description="Custom companies (overrides test set)")

class SearchPlanResponse(BaseModel):
    status: str
    test_set: str
    companies: List[str]
    queries_generated: int
    focus_areas: List[str]
    timeframe_days: int

class SearchResult(BaseModel):
    title: str
    url: str
    date: str
    source: str
    snippet: str
    companies: List[str] = []
    relevance_score: float = 0.0

class SearchResponse(BaseModel):
    status: str
    total_results: int
    queries_executed: int
    articles: List[SearchResult]
    processing_time: float

class WorkflowRequest(BaseModel):
    test_set: str = Field(..., description="Test set to use")
    companies: Optional[List[str]] = Field(None, description="Custom companies")
    max_articles: int = Field(50, description="Maximum articles to process")

class WorkflowResponse(BaseModel):
    status: str
    test_set: str
    phase: str
    results: Dict[str, Any]
    processing_time: float
    timestamp: str

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="URL to scrape")

class ScrapeResponse(BaseModel):
    status: str
    url: str
    title: str
    content: str
    content_length: int

class SummarizeRequest(BaseModel):
    url: Optional[str] = Field(None, description="URL to scrape and summarize")
    content: Optional[str] = Field(None, description="Raw content to summarize")
    min_words: int = Field(30, description="Minimum word count")
    max_words: int = Field(40, description="Maximum word count")

class SummarizeResponse(BaseModel):
    status: str
    summary: str
    word_count: int
    url: Optional[str] = None

class ClassifyRequest(BaseModel):
    articles: List[Dict[str, Any]] = Field(..., description="Articles to classify")
    companies: List[str] = Field(..., description="Company list for classification")

class ClassifyResponse(BaseModel):
    status: str
    by_company: Dict[str, List[Dict[str, Any]]]
    unclassified: List[Dict[str, Any]]


class FrontendNewsDiscovererRequest(BaseModel):
    query: str
    days_back: int = 7
    max_articles: int = 50


class FrontendNewsResponse(BaseModel):
    status: str
    articles: List[Dict[str, Any]]
    total_found: int
    sources_used: Optional[List[str]] = None
    success_rate: Optional[str] = None


class FrontendScrapeRequest(BaseModel):
    articles: Any = Field(..., description="Either a list of article objects or an object with an 'articles' list")
    method: str = Field("hybrid", description="crawl4ai|beautifulsoup|hybrid")


class FrontendScrapeResponse(BaseModel):
    status: str
    articles: List[Dict[str, Any]]
    total_scraped: int
    success_rate: str
    methods_used: List[str]


class FrontendClassifyRequest(BaseModel):
    articles: Any = Field(..., description="Either a list of article objects or an object with an 'articles' list")
    target_companies: List[str]


class FrontendClassificationResponse(BaseModel):
    status: str
    articles: List[Dict[str, Any]]
    total_relevant: int
    total_input: int
    companies_targeted: List[str]


class FrontendSummarizeRequest(BaseModel):
    articles: Any = Field(..., description="Either a list of article objects or an object with an 'articles' list")
    word_count_min: int = 30
    word_count_max: int = 40


class FrontendSummarizationResponse(BaseModel):
    status: str
    articles: List[Dict[str, Any]]
    total_summarized: int
    format: str


class FrontendExportRequest(BaseModel):
    articles: Any = Field(..., description="Either a list of article objects or an object with an 'articles' list")
    format: str = Field("csv", description="csv|json|excel|zip")
    filename: Optional[str] = None


class FrontendExportResponse(BaseModel):
    status: str
    exported_count: int
    format: str
    filename: Optional[str] = None
    download_url: Optional[str] = None
    message: str
    files_created: Optional[List[str]] = None


def _frontend_normalize_articles(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, list):
        return [a for a in value if isinstance(a, dict)]
    if isinstance(value, dict):
        inner = value.get("articles")
        if isinstance(inner, list):
            return [a for a in inner if isinstance(a, dict)]
    return []


def _frontend_source_from_url(url: str) -> str:
    try:
        host = urlparse(url).netloc
        return host.replace("www.", "")
    except Exception:
        return ""

class WebRagIngestRequest(BaseModel):
    urls: List[str] = Field(..., description="URLs to ingest")
    session_id: Optional[str] = Field(None, description="Existing session id")
    chunk_size: int = Field(1000, description="Chunk size")
    chunk_overlap: int = Field(200, description="Chunk overlap")

class WebRagIngestResponse(BaseModel):
    status: str
    session_id: str
    urls_ingested: int
    chunks_created: int
    url_results: List[Dict[str, Any]]

class WebRagQueryRequest(BaseModel):
    session_id: str = Field(..., description="Session id")
    question: str = Field(..., description="Question")
    top_k: int = Field(5, description="Top chunks")

class WebRagQueryResponse(BaseModel):
    status: str
    answer: str
    sources: List[Dict[str, Any]]


_webrag_sessions: Dict[str, List[Dict[str, Any]]] = {}


def _scrape_with_dual_methods(url: str) -> Dict[str, Any]:
    r1 = web_scraper.scrape_crawl4ai_sync(url)
    if r1.get("status") == "success" and len(r1.get("content", "")) > 300:
        return r1
    r2 = web_scraper.scrape_beautifulsoup(url)
    if r2.get("status") == "success" and len(r2.get("content", "")) > 300:
        return r2
    return r1 if r1.get("status") == "success" else r2


def _chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    if not text:
        return []
    if chunk_size <= 0:
        return [text]
    step = max(chunk_size - max(chunk_overlap, 0), 1)
    chunks = []
    for i in range(0, len(text), step):
        chunks.append(text[i:i + chunk_size])
        if i + chunk_size >= len(text):
            break
    return chunks


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+", (text or "").lower())


def _simple_retrieval(question: str, chunks: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    q_tokens = set(_tokenize(question))
    scored = []
    for c in chunks:
        t_tokens = set(_tokenize(c.get("text", "")))
        score = len(q_tokens.intersection(t_tokens))
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for score, c in scored[:max(top_k, 1)] if score > 0] or [c for score, c in scored[:max(top_k, 1)]]

class MockToolContext:
    """Mock ToolContext for API usage"""
    def __init__(self):
        self.state = {}
        self.artifacts = {}
    
    def save_artifact(self, artifact_id, data):
        self.artifacts[artifact_id] = data

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "News Aggregation API",
        "version": "1.0.0",
        "description": "RESTful API for financial news aggregation",
        "endpoints": {
            "test_sets": "/test-sets",
            "create_search_plan": "/search-plan",
            "search_news": "/search-news",
            "collect_news": "/collect-news",
            "workflow": "/workflow"
        },
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/test-sets", tags=["Configuration"])
async def get_test_sets():
    """Get all available test sets."""
    return {
        "default_test_set": DEFAULT_TEST_SET,
        "test_sets": TEST_SETS,
        "total_test_sets": len(TEST_SETS),
        "total_companies": sum(len(details['companies']) for details in TEST_SETS.values())
    }

@app.post("/search-plan", tags=["Search"], response_model=SearchPlanResponse)
async def create_search_plan_endpoint(request: TestSetRequest):
    """Create a search plan for the specified test set."""
    try:
        ctx = MockToolContext()
        
        # Get companies from test set or custom list
        if request.companies:
            companies = request.companies
        else:
            companies = TEST_SETS.get(request.test_set, {}).get('companies', [])
        
        if not companies:
            raise HTTPException(status_code=400, detail="No companies specified")
        
        # Create search plan
        result = create_search_plan(ctx, request.test_set, companies)
        
        if result["status"] != "success":
            raise HTTPException(status_code=500, detail=result.get("error", "Search plan creation failed"))
        
        return SearchPlanResponse(
            status=result["status"],
            test_set=result["search_plan"]["test_set"],
            companies=result["search_plan"]["companies"],
            queries_generated=result["total_queries"],
            focus_areas=result["search_plan"]["focus_areas"],
            timeframe_days=result["search_plan"]["timeframe_days"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/search-news", tags=["Search"], response_model=SearchResponse)
async def search_news_endpoint(
    test_set: str = Query(..., description="Test set name"),
    max_results: int = Query(50, description="Maximum results per query"),
    companies: Optional[str] = Query(None, description="Custom companies (comma-separated)")
):
    """Search for news articles using DuckDuckGo."""
    try:
        ctx = MockToolContext()
        start_time = datetime.now()
        
        # Get companies
        if companies:
            company_list = [c.strip() for c in companies.split(",")]
        else:
            company_list = TEST_SETS.get(test_set, {}).get('companies', [])
        
        if not company_list:
            raise HTTPException(status_code=400, detail="No companies specified")
        
        # Create search plan first
        plan_result = create_search_plan(ctx, test_set, company_list)
        if plan_result["status"] != "success":
            raise HTTPException(status_code=500, detail="Failed to create search plan")
        
        # Execute search with limited queries for API
        search_queries = plan_result["search_plan"]["search_queries"][:3]  # Limit for API
        
        search_result = execute_search_queries(ctx, search_queries)
        
        if search_result["status"] != "success":
            raise HTTPException(status_code=500, detail="Search execution failed")
        
        # Convert to API response format
        articles = []
        for article in search_result["results"][:max_results]:
            articles.append(SearchResult(
                title=article.get("title", ""),
                url=article.get("url", ""),
                date=article.get("date", ""),
                source=article.get("source", ""),
                snippet=article.get("body", ""),
                companies=article.get("tagged_companies", []),
                relevance_score=article.get("relevance_score", 0.0)
            ))
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return SearchResponse(
            status=search_result["status"],
            total_results=len(articles),
            queries_executed=search_result["queries_executed"],
            articles=articles,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/collect-news", tags=["Collection"], response_model=WorkflowResponse)
async def collect_news_endpoint(request: WorkflowRequest):
    """Complete news collection workflow with all processing steps."""
    try:
        ctx = MockToolContext()
        start_time = datetime.now()
        
        # Get companies
        if request.companies:
            companies = request.companies
        else:
            companies = TEST_SETS.get(request.test_set, {}).get('companies', [])
        
        if not companies:
            raise HTTPException(status_code=400, detail="No companies specified")
        
        results = {}
        
        # Phase 1: Create search plan
        plan_result = create_search_plan(ctx, request.test_set, companies)
        results["search_plan"] = plan_result
        
        if plan_result["status"] != "success":
            return WorkflowResponse(
                status="failed",
                test_set=request.test_set,
                phase="search_plan",
                results=results,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now().isoformat()
            )
        
        # Phase 2: Execute search
        search_result = execute_search_queries(ctx, plan_result["search_plan"]["search_queries"][:3])
        results["search"] = search_result
        
        if search_result["status"] != "success":
            return WorkflowResponse(
                status="failed",
                test_set=request.test_set,
                phase="search",
                results=results,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now().isoformat()
            )
        
        # Phase 3: Filter by date
        filter_result = filter_articles_by_date(ctx, search_result["results"][:request.max_articles], 7)
        results["date_filter"] = filter_result
        
        if filter_result["status"] != "success":
            return WorkflowResponse(
                status="failed",
                test_set=request.test_set,
                phase="date_filter",
                results=results,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now().isoformat()
            )
        
        # Phase 4: Validate sources
        required_sources = ["Reuters", "Bloomberg", "TechCrunch", "The Verge", "Wired"]
        validate_result = validate_sources(ctx, filter_result["filtered_articles"], required_sources)
        results["source_validation"] = validate_result
        
        if validate_result["status"] != "success":
            return WorkflowResponse(
                status="failed",
                test_set=request.test_set,
                phase="source_validation",
                results=results,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now().isoformat()
            )
        
        # Phase 5: Extract company mentions
        extract_result = extract_company_mentions(ctx, validate_result["validated_articles"], companies)
        results["company_extraction"] = extract_result
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return WorkflowResponse(
            status="success",
            test_set=request.test_set,
            phase="completed",
            results=results,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/workflow", tags=["Workflow"], response_model=WorkflowResponse)
async def full_workflow_endpoint(request: WorkflowRequest):
    """Execute the complete news aggregation workflow."""
    return await collect_news_endpoint(request)

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    try:
        # Test basic functionality
        test_search = duckduckgo_tool.search_news("test query", "7d", 1)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "duckduckgo_search": "operational" if test_search else "degraded",
                "web_scraper": "operational",
                "content_processor": "operational",
                "news_collection_agent": "operational"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )

@app.get("/stats", tags=["System"])
async def get_system_stats():
    """Get system statistics and information."""
    return {
        "system": {
            "name": "News Aggregation System",
            "version": "1.0.0",
            "architecture": "Multi-Agent with Context Engineering",
            "patterns": ["wander.txt", "context rag.txt", "mostadvagent.txt"]
        },
        "test_sets": {
            "total": len(TEST_SETS),
            "default": DEFAULT_TEST_SET,
            "total_companies": sum(len(details['companies']) for details in TEST_SETS.values()),
            "sets": {name: {"companies": len(details['companies'])} for name, details in TEST_SETS.items()}
        },
        "configuration": {
            "timeframe_days": 7,
            "summary_word_count": "30-40",
            "relevance_threshold": 0.7,
            "max_search_results": 100
        },
        "api": {
            "endpoints": 8,
            "documentation": "/docs",
            "health_check": "/health"
        }
    }


@app.post("/scrape", tags=["Scraping"], response_model=ScrapeResponse)
async def scrape_endpoint(request: ScrapeRequest):
    try:
        result = _scrape_with_dual_methods(request.url)
        if result.get("status") != "success":
            raise HTTPException(status_code=502, detail=result.get("error", "Scrape failed"))
        content = result.get("content", "")
        return ScrapeResponse(
            status="success",
            url=request.url,
            title=result.get("title", ""),
            content=content,
            content_length=len(content),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", tags=["Summarization"], response_model=SummarizeResponse)
async def summarize_endpoint(request: SummarizeRequest):
    try:
        content = request.content
        if isinstance(content, str) and not content.strip():
            content = None

        url = request.url
        if isinstance(url, str):
            url = url.strip() or None

        if not content and url:
            scraped = _scrape_with_dual_methods(url)
            if scraped.get("status") != "success":
                raise HTTPException(status_code=502, detail=scraped.get("error", "Scrape failed"))
            content = scraped.get("content", "")

            # If scraping succeeded but yielded no usable content, return a warning response
            # instead of raising 400 so callers can see the scrape method and URL.
            if not content or (isinstance(content, str) and not content.strip()):
                return SummarizeResponse(
                    status="warning",
                    summary="Content not available for summarization.",
                    word_count=0,
                    url=url,
                )

        if not content or (isinstance(content, str) and not content.strip()):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Provide url or content",
                    "url_provided": bool(url),
                    "content_length": len((request.content or "")),
                    "url": request.url,
                },
            )

        summary = content_processor.generate_summary(content, max_words=request.max_words, min_words=request.min_words)
        wc = len(summary.split())
        return SummarizeResponse(status="success", summary=summary, word_count=wc, url=url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/summarize", tags=["Debug"])
async def debug_summarize(url: str = Query(..., description="URL to scrape + summarize")):
    """Debug helper for verifying scrape+summarize flow."""
    try:
        url = url.strip() if url else url
        scraped = _scrape_with_dual_methods(url)
        if scraped.get("status") != "success":
            return {
                "status": "error",
                "stage": "scrape",
                "url": url,
                "error": scraped.get("error"),
                "method": scraped.get("method"),
            }

        content = scraped.get("content", "")
        summary = content_processor.generate_summary(content, max_words=40, min_words=30)
        return {
            "status": "success",
            "url": url,
            "scrape_method": scraped.get("method"),
            "content_length": len(content),
            "summary": summary,
            "summary_word_count": len(summary.split()),
        }
    except Exception as e:
        return {"status": "error", "stage": "exception", "error": str(e)}


@app.post("/classify", tags=["Classification"], response_model=ClassifyResponse)
async def classify_endpoint(request: ClassifyRequest):
    try:
        by_company: Dict[str, List[Dict[str, Any]]] = {c: [] for c in request.companies}
        unclassified: List[Dict[str, Any]] = []

        for a in request.articles:
            text = f"{a.get('title', '')} {a.get('content', '')} {a.get('snippet', '')} {a.get('body', '')}"
            found = content_processor.extract_companies_from_text(text, request.companies)
            if not found:
                unclassified.append(a)
                continue
            for c in found:
                by_company.setdefault(c, []).append(a)

        return ClassifyResponse(status="success", by_company=by_company, unclassified=unclassified)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webrag/ingest", tags=["WebRAG"], response_model=WebRagIngestResponse)
async def webrag_ingest_endpoint(request: WebRagIngestRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        chunks = _webrag_sessions.get(session_id, [])
        chunks_created = 0
        url_results: List[Dict[str, Any]] = []

        for url in request.urls:
            scraped = _scrape_with_dual_methods(url)
            if scraped.get("status") != "success":
                url_results.append({
                    "url": url,
                    "status": "error",
                    "method": scraped.get("method"),
                    "error": scraped.get("error"),
                    "content_length": 0,
                    "chunks_created": 0,
                })
                continue
            text = scraped.get("content", "")
            created_for_url = 0
            for idx, chunk in enumerate(_chunk_text(text, request.chunk_size, request.chunk_overlap)):
                chunks.append({
                    "url": url,
                    "chunk_index": idx,
                    "text": chunk,
                })
                chunks_created += 1
                created_for_url += 1

            url_results.append({
                "url": url,
                "status": "success" if created_for_url > 0 else "warning",
                "method": scraped.get("method"),
                "error": None,
                "content_length": len(text),
                "chunks_created": created_for_url,
            })

        # Persist the session even if we created zero chunks so the client can inspect url_results.
        _webrag_sessions[session_id] = chunks
        return WebRagIngestResponse(
            status="success" if chunks_created > 0 else "warning",
            session_id=session_id,
            urls_ingested=len(request.urls),
            chunks_created=chunks_created,
            url_results=url_results,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webrag/query", tags=["WebRAG"], response_model=WebRagQueryResponse)
async def webrag_query_endpoint(request: WebRagQueryRequest):
    try:
        if request.session_id not in _webrag_sessions:
            raise HTTPException(status_code=404, detail="Unknown session_id")

        chunks = _webrag_sessions.get(request.session_id) or []
        if len(chunks) == 0:
            return WebRagQueryResponse(
                status="success",
                answer="No content is indexed for this session yet. Ingest at least one URL that can be scraped, then ask again.",
                sources=[],
            )

        top = _simple_retrieval(request.question, chunks, request.top_k)
        answer = "\n\n".join([t.get("text", "")[:800] for t in top])
        sources = [{
            "url": t.get("url"),
            "chunk_index": t.get("chunk_index"),
            "preview": (t.get("text", "")[:300] + "...") if len(t.get("text", "")) > 300 else t.get("text", ""),
        } for t in top]

        return WebRagQueryResponse(status="success", answer=answer or "No relevant content found.", sources=sources)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background task for async processing
@app.post("/collect-news-async", tags=["Collection"])
async def collect_news_async(background_tasks: BackgroundTasks, request: WorkflowRequest):
    """Start news collection as a background task."""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Add background task
    background_tasks.add_task(
        process_news_collection_background,
        task_id,
        request.test_set,
        request.companies,
        request.max_articles
    )
    
    return {
        "task_id": task_id,
        "status": "started",
        "message": "News collection started in background",
        "check_status": f"/task-status/{task_id}"
    }

# In-memory task storage (in production, use Redis or database)
task_status_storage = {}

async def process_news_collection_background(task_id: str, test_set: str, companies: List[str], max_articles: int):
    """Background task for news collection."""
    try:
        task_status_storage[task_id] = {"status": "processing", "progress": 0}
        
        # Simulate processing (replace with actual workflow)
        await asyncio.sleep(2)
        task_status_storage[task_id]["progress"] = 25
        
        await asyncio.sleep(2)
        task_status_storage[task_id]["progress"] = 50
        
        await asyncio.sleep(2)
        task_status_storage[task_id]["progress"] = 75
        
        await asyncio.sleep(2)
        task_status_storage[task_id]["progress"] = 100
        task_status_storage[task_id]["status"] = "completed"
        
    except Exception as e:
        task_status_storage[task_id] = {"status": "failed", "error": str(e)}

@app.get("/task-status/{task_id}", tags=["System"])
async def get_task_status(task_id: str):
    """Get status of background task."""
    if task_id not in task_status_storage:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_status_storage[task_id]


@app.get("/api/health", tags=["Frontend"])
async def frontend_health():
    return await health_check()


@app.get("/api/dashboard/stats", tags=["Frontend"])
async def frontend_dashboard_stats():
    active = 0
    last_update = "Never"
    if isinstance(task_status_storage, dict) and task_status_storage:
        active = sum(1 for v in task_status_storage.values() if isinstance(v, dict) and v.get("status") in {"processing", "started"})
        last_update = datetime.now().isoformat()
    return {
        "total_articles": 0,
        "success_rate": 0,
        "active_tasks": active,
        "last_update": last_update,
    }


@app.post("/api/news/discoverer", tags=["Frontend"], response_model=FrontendNewsResponse)
async def frontend_news_discoverer(request: FrontendNewsDiscovererRequest):
    timeframe = f"{max(int(request.days_back), 1)}d"
    results = duckduckgo_tool.search_news(request.query, timeframe=timeframe, max_results=int(request.max_articles))

    articles: List[Dict[str, Any]] = []
    sources = set()
    for r in results:
        url = r.get("url", "")
        source = r.get("source") or _frontend_source_from_url(url)
        if source:
            sources.add(source)
        articles.append({
            "title": r.get("title", ""),
            "url": url,
            "published": r.get("date", "") or r.get("published", "") or "",
            "source": source,
            "snippet": r.get("body", "") or "",
            "body": r.get("body", "") or "",
        })

    return FrontendNewsResponse(
        status="success",
        articles=articles,
        total_found=len(articles),
        sources_used=sorted(list(sources)),
        success_rate="100%",
    )


@app.post("/api/news/scraper", tags=["Frontend"], response_model=FrontendScrapeResponse)
async def frontend_news_scraper(request: FrontendScrapeRequest):
    articles_in = _frontend_normalize_articles(request.articles)
    method = (request.method or "hybrid").strip().lower()

    out: List[Dict[str, Any]] = []
    methods_used: set[str] = set()

    for a in articles_in:
        url = (a.get("url") or "").strip()
        if not url:
            continue

        if method == "crawl4ai":
            scraped = web_scraper.scrape_crawl4ai_sync(url)
        elif method == "beautifulsoup":
            scraped = web_scraper.scrape_beautifulsoup(url)
        else:
            scraped = _scrape_with_dual_methods(url)

        methods_used.add(scraped.get("method") or "")
        content = scraped.get("content") or ""

        out.append({
            "title": a.get("title") or scraped.get("title") or "",
            "url": url,
            "published": a.get("published") or a.get("date") or a.get("scraped_at") or datetime.now().isoformat(),
            "source": a.get("source") or _frontend_source_from_url(url),
            "content": content,
            "scraping_method": scraped.get("method") or method,
            "scraped_at": datetime.now().isoformat(),
        })

    total = len(out)
    ok = sum(1 for a in out if (a.get("content") or "").strip())
    success_rate = f"{round((ok / total) * 100)}%" if total else "0%"

    return FrontendScrapeResponse(
        status="success",
        articles=out,
        total_scraped=ok,
        success_rate=success_rate,
        methods_used=[m for m in methods_used if m],
    )


@app.post("/api/news/classifier", tags=["Frontend"], response_model=FrontendClassificationResponse)
async def frontend_news_classifier(request: FrontendClassifyRequest):
    articles_in = _frontend_normalize_articles(request.articles)
    companies = [c for c in (request.target_companies or []) if isinstance(c, str) and c.strip()]

    relevant: List[Dict[str, Any]] = []
    for a in articles_in:
        text = f"{a.get('title', '')} {a.get('content', '')} {a.get('snippet', '')} {a.get('body', '')}"
        found = content_processor.extract_companies_from_text(text, companies)
        if not found:
            continue
        a2 = dict(a)
        a2["companies"] = found
        relevant.append(a2)

    return FrontendClassificationResponse(
        status="success",
        articles=relevant,
        total_relevant=len(relevant),
        total_input=len(articles_in),
        companies_targeted=companies,
    )


@app.post("/api/news/summarizer", tags=["Frontend"], response_model=FrontendSummarizationResponse)
async def frontend_news_summarizer(request: FrontendSummarizeRequest):
    articles_in = _frontend_normalize_articles(request.articles)

    summarized: List[Dict[str, Any]] = []
    for a in articles_in:
        url = (a.get("url") or "").strip()
        content = (a.get("content") or a.get("body") or a.get("snippet") or "")

        if (not content or not str(content).strip()) and url:
            scraped = _scrape_with_dual_methods(url)
            if scraped.get("status") == "success":
                content = scraped.get("content") or ""

        if not content or not str(content).strip():
            summary = "Content not available for summarization."
            wc = len(summary.split())
        else:
            summary = content_processor.generate_summary(
                str(content),
                max_words=int(request.word_count_max),
                min_words=int(request.word_count_min),
            )
            wc = len((summary or "").split())

        summarized.append({
            "title": a.get("title") or "",
            "url": url,
            "published": a.get("published") or a.get("date") or datetime.now().isoformat(),
            "source": a.get("source") or _frontend_source_from_url(url),
            "content": a.get("content"),
            "companies": a.get("companies"),
            "summary": summary,
            "word_count": wc,
        })

    return FrontendSummarizationResponse(
        status="success",
        articles=summarized,
        total_summarized=len(summarized),
        format="business_summary",
    )


@app.post("/api/news/exporter", tags=["Frontend"], response_model=FrontendExportResponse)
async def frontend_news_exporter(request: FrontendExportRequest):
    articles_in = _frontend_normalize_articles(request.articles)
    fmt = (request.format or "csv").strip().lower()
    base = (request.filename or "export").strip() or "export"

    out_dir = Path(os.getcwd()) / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    created: List[str] = []
    exported_count = len(articles_in)

    if fmt not in {"csv", "json", "pdf"}:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {fmt}")

    def _rows():
        for a in articles_in:
            yield {
                "title": a.get("title", ""),
                "published": a.get("published", ""),
                "url": a.get("url", ""),
                "source": a.get("source", ""),
                "companies": ",".join(a.get("companies") or []) if isinstance(a.get("companies"), list) else (a.get("companies") or ""),
                "summary": a.get("summary", ""),
            }

    if fmt == "json":
        p = out_dir / f"{base}.json"
        p.write_text(json.dumps(list(_rows()), indent=2), encoding="utf-8")
        created.append(str(p))
        return FrontendExportResponse(
            status="success",
            exported_count=exported_count,
            format="json",
            filename=p.name,
            download_url=f"/api/files/{p.name}",
            message="Exported JSON successfully.",
            files_created=created,
        )

    if fmt == "csv":
        import csv
        csv_path = out_dir / f"{base}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "published", "url", "source", "companies", "summary"])
            writer.writeheader()
            for r in _rows():
                writer.writerow(r)
        created.append(str(csv_path))
        try:
            return FrontendExportResponse(
                status="success",
                exported_count=exported_count,
                format="csv",
                filename=csv_path.name,
                download_url=f"/api/files/{csv_path.name}",
                message="Exported CSV successfully.",
                files_created=created,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    if fmt == "pdf":
        pdf_path = out_dir / f"{base}.pdf"
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF export requires reportlab: {str(e)}")

        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        width, height = letter
        y = height - 48
        c.setFont("Helvetica", 12)
        c.drawString(48, y, "News Aggregation Export")
        y -= 24
        c.setFont("Helvetica", 9)

        for idx, row in enumerate(list(_rows()), start=1):
            lines = [
                f"{idx}. {row.get('title','')}",
                f"   Published: {row.get('published','')}",
                f"   Source: {row.get('source','')}  URL: {row.get('url','')}",
                f"   Companies: {row.get('companies','')}",
                f"   Summary: {row.get('summary','')}",
                "",
            ]
            for line in lines:
                if y < 72:
                    c.showPage()
                    y = height - 48
                    c.setFont("Helvetica", 9)
                c.drawString(48, y, (line or "")[:200])
                y -= 12

        c.save()
        created.append(str(pdf_path))
        return FrontendExportResponse(
            status="success",
            exported_count=exported_count,
            format="pdf",
            filename=pdf_path.name,
            download_url=f"/api/files/{pdf_path.name}",
            message="Exported PDF successfully.",
            files_created=created,
        )


@app.get("/api/files/{filename}", tags=["Frontend"])
async def frontend_download_file(filename: str):
    out_dir = Path(os.getcwd()) / "output"
    candidate = (out_dir / filename).resolve()
    if not str(candidate).startswith(str(out_dir.resolve())):
        raise HTTPException(status_code=400, detail="Invalid filename")
    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(candidate), filename=candidate.name)


@app.get("/api/tasks/{task_id}", tags=["Frontend"])
async def frontend_task_status(task_id: str):
    return await get_task_status(task_id)


@app.get("/api/tasks/{task_id}/result", tags=["Frontend"])
async def frontend_task_result(task_id: str):
    return await get_task_status(task_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
