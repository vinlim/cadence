from google.adk.agents import LlmAgent
from models import deepseek_model
from tools import tavily
from tools.blockonomics_insights import fetch_blockonomics_rss_compact
from utilities import load_instruction


topic_decider_agent = LlmAgent(
    name="topic_decider_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to decide a topic to write on based on report produced by trend_research_agent stored in {trend_report} state"
    ),
    instruction=load_instruction('configs/topic.md'),
    tools=[tavily.tavily_toolset, fetch_blockonomics_rss_compact],
    output_key="topic_decided",
)
