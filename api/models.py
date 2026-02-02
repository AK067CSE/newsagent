"""
API Models for FastAPI Server

Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TestSetEnum(str, Enum):
    IT_COMPANIES = "IT Companies"
    TELECOM_COMPANIES = "Telecom Companies"
    AI_COMPANIES = "AI Companies"
    GLOBAL_IT = "Global IT"

class ArticleType(str, Enum):
    FINANCIAL_NEWS = "Financial News"
    EARNINGS = "Earnings"
    PRODUCT_LAUNCH = "Product Launch"
    PARTNERSHIP = "Partnership"
    ACQUISITION = "Acquisition"
    TECHNOLOGY = "Technology"
    MARKET_ANALYSIS = "Market Analysis"
    REGULATORY = "Regulatory"

class TestSetRequest(BaseModel):
    test_set: TestSetEnum = Field(..., description="Test set name")
    companies: Optional[List[str]] = Field(None, description="Custom companies (overrides test set)")

class SearchPlanRequest(BaseModel):
    test_set: TestSetEnum = Field(..., description="Test set name")
    companies: List[str] = Field(..., description="Companies to search for")
    timeframe_days: int = Field(7, description="Search timeframe in days")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    timeframe: str = Field("7d", description="Time filter (e.g., '7d', '1w')")
    max_results: int = Field(50, description="Maximum results to return")

class ArticleResponse(BaseModel):
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    date: str = Field(..., description="Publication date")
    source: str = Field(..., description="News source")
    snippet: str = Field(..., description="Article snippet")
    companies: List[str] = Field(default_factory=list, description="Companies mentioned")
    relevance_score: float = Field(0.0, description="Relevance score (0-1)")
    article_type: Optional[ArticleType] = Field(None, description="Article type")

class SearchResponse(BaseModel):
    status: str = Field(..., description="Search status")
    total_results: int = Field(..., description="Total results found")
    query: str = Field(..., description="Search query used")
    timeframe: str = Field(..., description="Time filter used")
    articles: List[ArticleResponse] = Field(..., description="Search results")
    processing_time: float = Field(..., description="Processing time in seconds")

class WorkflowRequest(BaseModel):
    test_set: TestSetEnum = Field(..., description="Test set to use")
    companies: Optional[List[str]] = Field(None, description="Custom companies")
    max_articles: int = Field(50, description="Maximum articles to process")
    include_scraping: bool = Field(False, description="Include content scraping")
    include_summarization: bool = Field(False, description="Include summarization")

class WorkflowStep(BaseModel):
    phase: str = Field(..., description="Workflow phase name")
    status: str = Field(..., description="Phase status")
    articles_processed: int = Field(0, description="Articles processed in this phase")
    processing_time: float = Field(0.0, description="Processing time for this phase")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")

class WorkflowResponse(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    status: str = Field(..., description="Overall workflow status")
    test_set: str = Field(..., description="Test set used")
    current_phase: str = Field(..., description="Current workflow phase")
    phases: List[WorkflowStep] = Field(..., description="All workflow phases")
    total_articles: int = Field(0, description="Total articles processed")
    final_articles: List[ArticleResponse] = Field(default_factory=list, description="Final processed articles")
    processing_time: float = Field(..., description="Total processing time")
    timestamp: str = Field(..., description="Completion timestamp")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")

class TaskStatus(BaseModel):
    task_id: str = Field(..., description="Task identifier")
    status: str = Field(..., description="Task status (pending, processing, completed, failed)")
    progress: int = Field(0, description="Progress percentage (0-100)")
    current_phase: str = Field("", description="Current phase")
    total_phases: int = Field(5, description="Total number of phases")
    started_at: str = Field(..., description="Task start time")
    completed_at: Optional[str] = Field(None, description="Task completion time")
    error: Optional[str] = Field(None, description="Error message if failed")
    result: Optional[Dict[str, Any]] = Field(None, description="Task result")

class HealthResponse(BaseModel):
    status: str = Field(..., description="System health status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    uptime: str = Field(..., description="System uptime")
    components: Dict[str, str] = Field(..., description="Component status")
    memory_usage: Optional[Dict[str, Any]] = Field(None, description="Memory usage statistics")

class StatsResponse(BaseModel):
    system: Dict[str, Any] = Field(..., description="System information")
    test_sets: Dict[str, Any] = Field(..., description="Test set statistics")
    configuration: Dict[str, Any] = Field(..., description="Configuration details")
    api: Dict[str, Any] = Field(..., description="API statistics")
    performance: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: str = Field(..., description="Error details")
    timestamp: str = Field(..., description="Error timestamp")
    path: str = Field(..., description="Request path")

class SuccessResponse(BaseModel):
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: str = Field(..., description="Response timestamp")
