"""
Pydantic models for News Aggregation System

Defines data structures for articles, companies, and workflow state.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TestSetType(str, Enum):
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

class Source(BaseModel):
    name: str = Field(..., description="Source name (e.g., Reuters, Bloomberg)")
    url: Optional[str] = Field(None, description="Source website URL")
    credibility_score: float = Field(1.0, description="Source credibility score (0-1)")

class Article(BaseModel):
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    published_date: Optional[str] = Field(None, description="Publication date")
    source: Source = Field(..., description="News source information")
    snippet: str = Field(..., description="Article snippet or description")
    article_type: ArticleType = Field(..., description="Type of news article")
    tagged_companies: List[str] = Field(default_factory=list, description="Companies tagged in article")
    relevance_score: float = Field(0.0, description="Relevance score (0-1)")
    content_artifact: Optional[str] = Field(None, description="Artifact ID for full content")
    summary: Optional[str] = Field(None, description="30-40 word summary")
    summary_word_count: Optional[int] = Field(None, description="Word count of summary")
    scraping_status: str = Field("pending", description="Content scraping status")
    summarization_status: str = Field("pending", description="Summarization status")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class SearchPlan(BaseModel):
    test_set: TestSetType = Field(..., description="Chosen test set")
    companies: List[str] = Field(..., description="Companies to search for")
    timeframe_days: int = Field(7, description="Search timeframe in days")
    start_date: str = Field(..., description="Search start date")
    end_date: str = Field(..., description="Search end date")
    search_queries: List[str] = Field(..., description="Search queries to execute")
    priority_focus: List[str] = Field(..., description="Priority focus areas")

class SearchResults(BaseModel):
    search_plan: SearchPlan = Field(..., description="Original search plan")
    total_results: int = Field(0, description="Total articles found")
    filtered_results: int = Field(0, description="Articles after filtering")
    validated_results: int = Field(0, description="Articles after source validation")
    articles: List[Article] = Field(default_factory=list, description="Validated articles")
    sources_covered: List[str] = Field(default_factory=list, description="News sources found")
    companies_mentioned: List[str] = Field(default_factory=list, description="Companies found in articles")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class ClassificationResult(BaseModel):
    article_id: str = Field(..., description="Article identifier")
    extracted_companies: List[str] = Field(..., description="Companies extracted from article")
    confidence_scores: Dict[str, float] = Field(..., description="Confidence scores per company")
    final_tags: List[str] = Field(..., description="Final company tags after validation")
    relevance_score: float = Field(0.0, description="Overall relevance score")
    classification_reasoning: str = Field(..., description="Reasoning for classification")

class ScrapingResult(BaseModel):
    article_id: str = Field(..., description="Article identifier")
    scraping_method: str = Field(..., description="Method used for scraping")
    content_length: int = Field(0, description="Length of scraped content")
    artifact_id: Optional[str] = Field(None, description="Artifact ID for stored content")
    scraping_status: str = Field(..., description="Success/failure status")
    error_message: Optional[str] = Field(None, description="Error message if failed")

class SummaryResult(BaseModel):
    article_id: str = Field(..., description="Article identifier")
    summary: str = Field(..., description="Generated summary")
    word_count: int = Field(..., description="Word count of summary")
    quality_score: float = Field(0.0, description="Quality assessment score")
    summarization_method: str = Field(..., description="Method used for summarization")
    validation_status: str = Field(..., description="Validation status")

class StorageResult(BaseModel):
    storage_format: str = Field(..., description="Format used for storage")
    total_articles: int = Field(0, description="Total articles stored")
    storage_location: str = Field(..., description="Location where data was stored")
    file_path: Optional[str] = Field(None, description="File path if stored to file")
    database_table: Optional[str] = Field(None, description="Database table if stored to DB")
    storage_timestamp: datetime = Field(default_factory=datetime.now, description="When storage occurred")

class WorkflowState(BaseModel):
    test_set: TestSetType = Field(..., description="Chosen test set")
    current_phase: str = Field("initialized", description="Current workflow phase")
    search_results: Optional[SearchResults] = Field(None, description="Search phase results")
    classification_results: List[ClassificationResult] = Field(default_factory=list, description="Classification results")
    scraping_results: List[ScrapingResult] = Field(default_factory=list, description="Scraping results")
    summary_results: List[SummaryResult] = Field(default_factory=list, description="Summary results")
    storage_result: Optional[StorageResult] = Field(None, description="Storage results")
    errors: List[str] = Field(default_factory=list, description="Errors encountered during processing")
    start_time: datetime = Field(default_factory=datetime.now, description="Workflow start time")
    end_time: Optional[datetime] = Field(None, description="Workflow end time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class SystemMetrics(BaseModel):
    total_articles_processed: int = Field(0, description="Total articles processed")
    successful_classifications: int = Field(0, description="Successful classifications")
    successful_scrapes: int = Field(0, description="Successful content scrapes")
    successful_summaries: int = Field(0, description="Successful summaries")
    average_relevance_score: float = Field(0.0, description="Average relevance score")
    processing_time_total: float = Field(0.0, description="Total processing time")
    coverage_percentage: float = Field(0.0, description="Coverage of target companies")
    quality_score: float = Field(0.0, description="Overall system quality score")
