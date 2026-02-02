"""
News Collection Agent - Main coordinator

Handles news search planning, execution, filtering, and validation following wander.txt patterns.
"""

from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.load_memory_tool import load_memory_tool
from google.adk.tools import FunctionTool
from ..config import DEFAULT_MODEL, DEFAULT_GENERATION_CONFIG
from .tools import (
    create_search_plan,
    execute_search_queries,
    filter_articles_by_date,
    validate_sources,
    extract_company_mentions
)
from .prompt import (
    NEWS_PLANNER_INSTR,
    NEWS_SEARCHER_INSTR,
    NEWS_FILTER_INSTR,
    NEWS_VALIDATOR_INSTR,
    NEWS_COLLECTION_AGENT_INSTR
)

# ============================================================================
# NEWS SUB-AGENTS (Following mostadvagent.txt pattern)
# ============================================================================

news_planner = LlmAgent(
    model=DEFAULT_MODEL,
    name="news_planner",
    description="Create detailed news search plans from user requests and test set requirements",
    instruction=NEWS_PLANNER_INSTR,
    tools=[
        FunctionTool(create_search_plan)
    ]
)

news_searcher = LlmAgent(
    model=DEFAULT_MODEL,
    name="news_searcher",
    description="Execute news searches using DuckDuckGo tools to find actual financial news articles",
    instruction=NEWS_SEARCHER_INSTR,
    tools=[
        FunctionTool(execute_search_queries)
    ]
)

news_filter = LlmAgent(
    model=DEFAULT_MODEL,
    name="news_filter",
    description="Filter search results by date, relevance, and quality criteria",
    instruction=NEWS_FILTER_INSTR,
    tools=[
        FunctionTool(filter_articles_by_date)
    ]
)

news_validator = LlmAgent(
    model=DEFAULT_MODEL,
    name="news_validator",
    description="Validate news sources and filter credible financial publications",
    instruction=NEWS_VALIDATOR_INSTR,
    tools=[
        FunctionTool(validate_sources),
        FunctionTool(extract_company_mentions)
    ]
)

# ============================================================================
# MAIN NEWS COLLECTION AGENT (Following wander.txt pattern)
# ============================================================================

news_collection_system = Agent(
    model=DEFAULT_MODEL,
    name="news_collection_system",
    description="Complete news collection coordination handling planning, searching, filtering, and validation for financial news aggregation",
    instruction=NEWS_COLLECTION_AGENT_INSTR,
    tools=[
        AgentTool(agent=news_planner),
        AgentTool(agent=news_searcher),
        AgentTool(agent=news_filter),
        AgentTool(agent=news_validator),
        load_memory_tool
    ],
    generate_content_config=DEFAULT_GENERATION_CONFIG
)

# Export the main system
__all__ = ["news_collection_system"]
