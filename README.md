# Cadence

An autonomous AI-powered content creation pipeline that researches, writes, reviews, and publishes marketing articles for Blockonomics.

## What is Cadence?

Cadence is an intelligent multi-agent system built with Google's Agent Development Kit (ADK) that automates the entire content creation workflow. The system autonomously:

- **Researches** current trends and market sentiment using web and social signals
- **Decides** on optimal topics based on research findings and existing content
- **Writes** high-quality, SEO-optimized marketing articles
- **Reviews** content for quality, accuracy, and brand alignment
- **Generates** custom cover images for articles
- **Publishes** finished content to Ghost CMS automatically

## Key Features

- **🤖 Multi-Agent Architecture**: Six specialized AI agents working in coordination
- **📊 Real-Time Research**: Integrates with Tavily, Reddit, and Twitter for trend analysis
- **✍️ Professional Writing**: Creates human-like content optimized for SEO and AEO
- **🔍 Quality Assurance**: Automated editorial review with scoring system
- **🎨 Visual Content**: AI-generated cover images using BytePlus
- **📱 Auto-Publishing**: Direct integration with Ghost CMS
- **🔒 Privacy-First**: Aligns with Blockonomics' privacy-focused brand values

## Agent Pipeline

The system runs through a sequential pipeline of specialized agents:

1. **Trend Research Agent** - Analyzes market trends and sentiment
2. **Topic Decider Agent** - Selects optimal topics based on research
3. **Writer Agent** - Creates long-form marketing articles  
4. **Editor Agent** - Reviews content for quality and brand compliance
5. **Media Agent** - Generates custom cover images
6. **Publish Agent** - Publishes to Ghost CMS with feature images

## Prerequisites

- Python 3.8+
- UV package manager
- Node.js (for Ghost MCP integration)
- Required API keys (see [Environment Setup](#environment-setup))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vinlim/cadence.git
   cd cadence
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp agents/orchestrator/.env.example agents/orchestrator/.env
   # Edit .env file with your API keys
   ```

## Environment Setup

Create a `.env` file in `agents/orchestrator/` with the following variables:

```bash
# Google AI
GOOGLE_GENAI_USE_VERTEXAI=false
GOOGLE_API_KEY=your_google_api_key

# Language Models
OPENROUTER_API_KEY=your_openrouter_api_key

# Research Tools
TAVILY_API_KEY=your_tavily_api_key

# Social Media
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Image Generation
ARK_API_KEY=your_byteplus_ark_api_key

# Publishing
GHOST_CONTENT_API_KEY=your_ghost_content_api_key
GHOST_ADMIN_API_KEY=your_ghost_admin_api_key
GHOST_API_URL=https://your-ghost-site.com
```

## Usage

### Running the Complete Pipeline

```python
from agents.orchestrator.agent import root_agent
from google.adk.agents import Session

# Create a new session and run the pipeline
session = Session()
result = await root_agent.run_async(session)
```

### Running Individual Agents

```python
from agents.trend_research_agent.agent import trend_research_agent
from agents.writer_agent.agent import writer_agent

# Run trend research
session = Session()
research_result = await trend_research_agent.run_async(session)

# Run writer with research context
writing_result = await writer_agent.run_async(session)
```

## Configuration

### Brand Configuration

Edit `configs/brand.md` to customize the brand voice and guidelines:

- Company information and values
- Brand tone requirements
- Content restrictions and guidelines

### Agent Instructions

Each agent's behavior can be customized by editing files in the `configs/` directory:

- `research.md` - Research methodology and focus areas
- `topic.md` - Topic selection criteria
- `writer.md` - Writing style and requirements
- `editor.md` - Review standards and scoring
- `media.md` - Image generation guidelines
- `publish.md` - Publishing workflow

## Project Structure

```
cadence/
├── agents/                 # AI agent implementations
│   ├── orchestrator/      # Main pipeline orchestrator
│   ├── trend_research_agent/  # Market research agent
│   ├── topic_decider_agent/   # Topic selection agent
│   ├── writer_agent/      # Content writing agent
│   ├── editor_agent/      # Content review agent
│   ├── media_agent/       # Image generation agent
│   └── publish_agent/     # Publishing agent
├── configs/               # Agent instructions and brand guidelines
├── models/                # Language model configurations
├── tools/                 # External API integrations
│   ├── tavily.py         # Web search integration
│   ├── reddit.py         # Reddit API integration
│   ├── x_twitter.py      # Twitter API integration
│   ├── ghost.py          # Ghost CMS integration
│   ├── byteplus.py       # Image generation API
│   └── blockonomics_insights.py  # Company blog feed
├── utilities.py           # Helper functions
└── requirements.txt       # Python dependencies
```

## Dependencies

Key dependencies include:

- **google-adk**: Agent Development Kit for multi-agent orchestration
- **litellm**: Universal LLM interface
- **fastmcp**: Model Context Protocol implementation
- **tweepy**: Twitter API integration
- **feedparser**: RSS feed processing
- **requests**: HTTP client
- **pydantic**: Data validation and serialization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Add type hints to all function signatures
- Update agent instructions in `configs/` when modifying behavior
- Test individual agents before running the full pipeline
- Ensure all API keys are properly configured before testing

## Support

- **Documentation**: Review agent instructions in the `configs/` directory
- **Issues**: Report bugs and feature requests on GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and ideas

## Architecture Notes

Cadence uses Google's Agent Development Kit (ADK) to implement a sophisticated multi-agent system. The orchestrator manages state between agents and handles retry logic, while individual agents focus on specific tasks within the content creation pipeline.

The system is designed to be deterministic and reliable, with built-in error handling and quality gates to ensure high-quality output that meets Blockonomics' brand standards.

---

*Cadence automates content creation while maintaining the quality and authenticity that your audience expects.*
