"""
Root Orchestrator Agent for News Aggregation System

Coordinates all specialized agents following wander.txt patterns.
"""

from google.adk.agents import Agent
from google.adk.tools.load_memory_tool import load_memory_tool
from .config import DEFAULT_MODEL
from .prompt import NEWS_AGGREGATION_ORCHESTRATOR_INSTR

# Import specialized agents (will be created in subsequent steps)
# For now, we'll create placeholder imports
try:
    from news_collection_agent.agent import news_collection_system
except ImportError:
    news_collection_system = None

try:
    from entity_classification_agent.agent import entity_classification_system
except ImportError:
    entity_classification_system = None

try:
    from content_scraping_agent.agent import content_scraping_system
except ImportError:
    content_scraping_system = None

try:
    from summarization_agent.agent import summarization_system
except ImportError:
    summarization_system = None

try:
    from data_management_agent.agent import data_management_system
except ImportError:
    data_management_system = None

# Create list of available agents
available_agents = [
    agent for agent in [
        news_collection_system,
        entity_classification_system,
        content_scraping_system,
        summarization_system,
        data_management_system
    ] if agent is not None
]

# Root orchestrator agent
root_agent = Agent(
    name="news_aggregation_orchestrator",
    model=DEFAULT_MODEL,
    description="News aggregation system specializing in collection, classification, scraping, summarization, and data management",
    instruction=NEWS_AGGREGATION_ORCHESTRATOR_INSTR,
    sub_agents=available_agents,
    tools=[load_memory_tool]
)

# Export the root agent
__all__ = ["root_agent"]
