"""
News Aggregation System

A sophisticated multi-agent system for collecting, classifying, scraping, 
summarizing, and storing financial news articles about specific company test sets.

Architecture follows wander.txt patterns with context engineering from context rag.txt.
"""

from .agent import root_agent

__all__ = ["root_agent"]
