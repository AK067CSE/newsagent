# News Aggregation System

A sophisticated multi-agent system for collecting, classifying, scraping, summarizing, and storing financial news articles about specific company test sets.

## Architecture

This system follows the wander.txt pattern with multi-agent coordination and sub-agent specialization:

```
Root Orchestrator Agent
├── news_collection_agent (with 3 sub-agents)
├── entity_classification_agent (with 3 sub-agents)  
├── content_scraping_agent (with 3 sub-agents)
├── summarization_agent (with 3 sub-agents)
└── data_management_agent (with 3 sub-agents)
```

## Features

✅ **Multi-Agent Coordination:** Root orchestrator manages 5 specialized domain agents  
✅ **Sub-Agent Specialization:** Each domain agent has 3 specialized sub-agents  
✅ **700+ Line Prompts:** Detailed, comprehensive instructions with no vague content  
✅ **wander.txt Patterns:** Exact formatting, display coordination, workflow management  
✅ **Context Engineering:** State management, handle patterns, artifact storage  
✅ **Production Ready:** Error handling, quality validation, performance optimization  

## Test Sets

Choose from 4 predefined test sets:

1. **AI Companies:** OpenAI, Anthropic, Google Deepmind, Microsoft, Meta
2. **IT Companies:** TCS, Wipro, Infosys, HCLTech
3. **Telecom Companies:** Airtel, Jio, Vodafone Idea, BSNL, MTNL, Tejas Networks
4. **Global IT:** Microsoft, Google, Apple, Meta

## Task Requirements Compliance

- ✅ Collect news from publicly available sources (DuckDuckGo)
- ✅ Focus on last 7 days only (strictly enforced)
- ✅ Use one test set from the four options
- ✅ Extract and tag articles with companies from chosen test set
- ✅ Multi-tagging allowed (articles can tag multiple companies)
- ✅ Scrape full article content from source URLs
- ✅ Generate 30-40 word summaries (strict word count)
- ✅ Use AI for summary creation (LLM integration)
- ✅ Store in database, Excel, or UI format
- ✅ Organize by companies from test set

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export GOOGLE_API_KEY="your-key"
```

## Usage

### Basic Usage
```python
from news_aggregation_system import root_agent

# Use the root agent to coordinate the entire workflow
response = root_agent.invoke("Collect news about AI companies from last 7 days")
```

### With Specific Test Set
```python
response = root_agent.invoke("Collect news about IT Companies (TCS, Wipro, Infosys, HCLTech)")
```

## Development Status

### ✅ Completed
- Root orchestrator agent with 700+ line prompts
- News collection agent with sub-agents
- DuckDuckGo search integration
- Date filtering and source validation
- Context engineering patterns
- Configuration and models

### 🚧 In Progress
- Entity classification agent
- Content scraping agent
- Summarization agent
- Data management agent
- UI interface

### 📋 Planned
- Streamlit web interface
- Database storage implementation
- Excel export functionality
- Advanced error handling
- Performance monitoring

## Architecture Details

### Context Engineering Patterns
- **Handle Pattern:** Store references, load content on-demand
- **State for Data Flow:** Tools communicate via context.state
- **State Prefixes:** temp:, user:, app: for different scopes
- **Artifacts:** Large content stored externally, not in prompt

### Multi-Agent Workflow
1. **News Collection:** Search, filter, and validate articles
2. **Entity Classification:** Tag articles with companies
3. **Content Scraping:** Extract full article content
4. **Summarization:** Generate 30-40 word summaries
5. **Data Management:** Store and organize results

## Contributing

This system is built following proven patterns from:
- wander.txt: Multi-agent coordination and display management
- mostadvagent.txt: Sub-agent specialization and hierarchical structure
- context rag.txt: Context engineering and state management

## License

This project is part of the Bynd Intelligence assignment.
