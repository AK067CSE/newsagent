"""
Configuration for News Aggregation System

Contains model settings, test set definitions, and system parameters.
"""

# Model Configuration
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_GENERATION_CONFIG = {
    "temperature": 0.1,
    "top_p": 0.8,
    "max_output_tokens": 8192
}

# Test Set Definitions (from task.txt)
TEST_SETS = {
    "IT Companies": {
        "companies": ["TCS", "Wipro", "Infosys", "HCLTech"],
        "description": "Top Indian IT services companies",
        "focus": ["quarterly results", "IT contracts", "digital transformation", "hiring trends"]
    },
    "Telecom Companies": {
        "companies": ["Airtel", "Jio", "Vodafone Idea", "BSNL", "MTNL", "Tejas Networks"],
        "description": "Major Indian telecommunications companies",
        "focus": ["5G rollout", "subscriber numbers", "tariff plans", "regulatory developments"]
    },
    "AI Companies": {
        "companies": ["OpenAI", "Anthropic", "Google Deepmind", "Microsoft", "Meta"],
        "description": "Leading artificial intelligence companies",
        "focus": ["model releases", "partnerships", "enterprise adoption", "AI safety"]
    },
    "Global IT": {
        "companies": ["Microsoft", "Google", "Apple", "Meta"],
        "description": "Major global technology companies",
        "focus": ["earnings", "product launches", "market share", "innovation"]
    }
}

# Default test set (can be overridden by user preference)
DEFAULT_TEST_SET = "AI Companies"

# News Collection Configuration
NEWS_CONFIG = {
    "timeframe_days": 7,
    "max_results_per_query": 100,
    "required_sources": [
        "Reuters", "Bloomberg", "Financial Times", "Wall Street Journal",
        "TechCrunch", "The Verge", "Wired", "VentureBeat",
        "Economic Times", "Business Standard", "Mint"
    ],
    "relevance_threshold": 0.7
}

# Summarization Configuration
SUMMARIZATION_CONFIG = {
    "min_words": 30,
    "max_words": 40,
    "focus_areas": ["financial performance", "business development", "technology innovation"]
}

# Storage Configuration
STORAGE_CONFIG = {
    "default_format": "database",  # Options: database, excel, ui
    "database_path": "news_aggregation.db",
    "excel_path": "news_aggregation_results.xlsx"
}

# DuckDuckGo Search Configuration
SEARCH_CONFIG = {
    "region": "wt-wt",  # Global
    "safesearch": "off",
    "timelimit": "7d"
}
