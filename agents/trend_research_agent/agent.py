from google.adk.agents import LlmAgent

from models import deepseek_model
from tools import tavily, reddit, x_twitter
from utilities import load_instruction

trend_research_agent = LlmAgent(
    name="trend_research_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to research trends & sentiments of a topic use web & social signals. The research can be use to decide what is a good topic to talk about now."
    ),
    instruction=load_instruction('configs/research.md'),
    tools=[
        tavily.tavily_toolset,
        reddit.reddit_toolset,
    ],
    output_key="trend_report",
)
