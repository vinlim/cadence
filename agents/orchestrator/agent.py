from pathlib import Path
from pydantic import Field
from typing import AsyncGenerator, Dict, Any
from google.genai.types import Content, Part
from google.adk.agents import SequentialAgent, BaseAgent, InvocationContext, LoopAgent
from google.adk.events import Event
from agents.editor_agent.agent import editor_agent
from agents.media_agent.agent import media_agent
from agents.publish_agent.agent import publish_agent
from agents.topic_decider_agent.agent import topic_decider_agent
from agents.trend_research_agent.agent import trend_research_agent
from agents.writer_agent.agent import writer_agent


class SetStateAgent(BaseAgent):
    pairs: Dict[str, Any] = Field(default_factory=dict)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        ctx.session.state.update(self.pairs)
        yield Event(author=self.name, content=Content(parts=[Part(text=f"Setting State for: {self.pairs.keys()}")]))


class DumpStateAgent(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        keys = sorted(ctx.session.state.keys())
        yield Event(author=self.name, content=Content(parts=[Part(text=f"state keys: {keys}")]))


BASE = Path(__file__).resolve().parents[2]
set_state_agent = SetStateAgent(
    name="SetStateAgent",
    pairs={
        "app_system_instruction": (BASE / "configs/system.md").read_text(encoding="utf-8"),
        "user_brand_tone": (BASE / "configs/brand.md").read_text(encoding="utf-8"),
    }
)

editorial_flow = SequentialAgent(
    name='editorial_flow',
    description='Editorial flow that begin with writer agent composing article, then review by editor agent',
    sub_agents=[writer_agent, editor_agent]
)

editorial_revision = LoopAgent(
    name='editorial_revision',
    description='Loop the editorial_flow until the passes editorial score requirements',
    sub_agents=[editorial_flow],
    max_iterations=3
)

root_agent = SequentialAgent(
    name="CadencePipeline",
    description=(
        "Deterministic, non-LLM orchestrator that runs the Cadence pipeline; "
        "manages shared state and enforces gates/retries outside prompts."
    ),
    sub_agents=[
        set_state_agent,
        DumpStateAgent(name='dump_state_agent'),
        trend_research_agent,
        topic_decider_agent,
        editorial_revision,
        media_agent,
        publish_agent,
    ],
)
