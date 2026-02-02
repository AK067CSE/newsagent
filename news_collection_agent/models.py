"""
Models for News Collection Agent

Defines data structures specific to news collection operations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query string")
    category: str = Field(..., description="Query category (financial, business, technology)")
    priority: int = Field(1, description="Query priority (1=highest)")
    expected_results: int = Field(50, description="Expected number of results")

class SearchPlan(BaseModel):
    test_set: str = Field(..., description="Test set name")
    companies: List[str] = Field(..., description="Companies to search for")
    timeframe_days: int = Field(7, description="Search timeframe in days")
    start_date: str = Field(..., description="Search start date")
    end_date: str = Field(..., description="Search end date")
    search_queries: List[SearchQuery] = Field(..., description="Search queries to execute")
    primary_sources: List[str] = Field(..., description="Primary news sources")
    focus_areas: List[str] = Field(..., description="Priority focus areas")

class ArticleMetadata(BaseModel):
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    date: str = Field(..., description="Publication date")
    source: str = Field(..., description="News source")
    snippet: str = Field(..., description="Article snippet")
    companies: List[str] = Field(default_factory=list, description="Companies mentioned")
    relevance_score: float = Field(0.0, description="Initial relevance score")
    article_type: str = Field("unknown", description="Article type")

class SearchResults(BaseModel):
    search_plan: SearchPlan = Field(..., description="Original search plan")
    total_raw_results: int = Field(0, description="Total raw search results")
    filtered_results: int = Field(0, description="Results after filtering")
    validated_results: int = Field(0, description="Results after validation")
    articles: List[ArticleMetadata] = Field(default_factory=list, description="Validated articles")
    sources_found: List[str] = Field(default_factory=list, description="Sources discovered")
    companies_found: List[str] = Field(default_factory=list, description="Companies found")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class FilterCriteria(BaseModel):
    date_range_start: str = Field(..., description="Start date for filtering")
    date_range_end: str = Field(..., description="End date for filtering")
    min_relevance_score: float = Field(0.7, description="Minimum relevance score")
    required_companies: List[str] = Field(..., description="Required companies")
    exclude_sources: List[str] = Field(default_factory=list, description="Sources to exclude")

class ValidationResult(BaseModel):
    article_id: str = Field(..., description="Article identifier")
    source_credibility: float = Field(0.0, description="Source credibility score")
    content_quality: float = Field(0.0, description="Content quality score")
    validation_status: str = Field(..., description="Validation status")
    validation_reasoning: str = Field(..., description="Reasoning for validation")

class CollectionMetrics(BaseModel):
    total_queries_executed: int = Field(0, description="Total search queries executed")
    total_results_found: int = Field(0, description="Total results found")
    articles_per_company: Dict[str, int] = Field(default_factory=dict, description="Articles per company")
    sources_per_article: Dict[str, int] = Field(default_factory=dict, description="Articles per source")
    average_relevance_score: float = Field(0.0, description="Average relevance score")
    processing_efficiency: float = Field(0.0, description="Processing efficiency score")
