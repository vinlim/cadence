from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from models import deepseek_model
from tools import blockonomics_insights, reddit, tavily, x_twitter
from utilities import load_instruction


def exit_loop(tool_context: ToolContext):
    """
    Tool to exit the loop once the editor_agent review score passes
    :param tool_context:
    """
    tool_context.actions.escalate = True
    return {"ok": True}


editor_agent = LlmAgent(
    name="editor_agent",
    model=deepseek_model.terminus,
    description=(
        "Agent to review marketing article writen by writer_agent to ensure content quality, content accuracy, brand tone, guardrail are met. Failing the threshold, the agent will reject the article."
    ),
    instruction=load_instruction('configs/editor.md'),
    tools=[
        exit_loop,
        tavily.tavily_toolset,
        blockonomics_insights.fetch_blockonomics_rss_compact,
        reddit.reddit_toolset,
    ],
    output_key="review_report",
)
