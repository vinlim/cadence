from google.adk.agents import LlmAgent
from models import deepseek_model
from tools import tavily, byteplus
from utilities import load_instruction

media_agent = LlmAgent(
    name="media_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to write prompt and generate a cover photo for the approved article"
    ),
    instruction=load_instruction('configs/media.md'),
    tools=[
        tavily.tavily_toolset,
        byteplus.byteplus_generate
    ],
    output_key="feature_image",
)
