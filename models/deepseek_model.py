import os

from google.adk.models.lite_llm import LiteLlm

terminus = LiteLlm(
    model="openrouter/deepseek/deepseek-v3.1-terminus",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)
