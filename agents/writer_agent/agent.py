from google.adk.agents import LlmAgent
from pydantic import BaseModel
from models import deepseek_model
from tools import blockonomics_insights, reddit, tavily
from utilities import load_instruction


class TopicOut(BaseModel):
    title: str
    content: str


writer_agent = LlmAgent(
    name="writer_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to write a marketing article for the company"
    ),
    instruction=load_instruction('configs/writer.md'),
    tools=[
        tavily.tavily_toolset,
        blockonomics_insights.fetch_blockonomics_rss_compact,
        reddit.reddit_toolset
    ],
    output_schema=TopicOut,
    output_key="drafted_article",
)
