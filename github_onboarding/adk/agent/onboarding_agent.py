"""Deterministic ADK custom agent using its real invocation and event lifecycle."""

import asyncio
import logging
from collections.abc import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.sessions import InMemorySessionService


class SumAgent(BaseAgent):
    """A custom ADK agent that computes a result without an LLM."""

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event]:
        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            actions=EventActions(state_delta={"total": sum(ctx.session.state["values"])}),
        )


agent = SumAgent(name="onboarding_probe")


async def complete() -> str:
    """Drive the public ADK invocation API and persist its emitted state change."""
    sessions = InMemorySessionService()
    session = await sessions.create_session(
        app_name="onboarding_probe", user_id="fixture", state={"values": [2, 3, 5]}
    )
    ctx = InvocationContext(
        invocation_id="onboarding-fixture",
        agent=agent,
        session=session,
        session_service=sessions,
    )
    count = 0
    async for event in agent.run_async(ctx):
        if event.author != agent.name:
            raise RuntimeError(f"Unexpected ADK event author: {event.author!r}")
        await sessions.append_event(session=session, event=event)
        count += 1
    stored = await sessions.get_session(
        app_name="onboarding_probe", user_id="fixture", session_id=session.id
    )
    if count != 1 or stored is None or stored.state.get("total") != 10:
        raise RuntimeError("ADK did not persist the expected total from its single event")
    return "adk-onboarding:10"


def run() -> str:
    """Fail the sandbox run unless the custom ADK agent completes correctly."""
    result = asyncio.run(complete())
    logging.getLogger(__name__).info("GitHub onboarding fixture completed: %s", result)
    return result
