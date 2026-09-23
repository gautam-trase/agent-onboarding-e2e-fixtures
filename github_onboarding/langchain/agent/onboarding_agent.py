"""Deterministic LangChain runnable: real composition, no provider or model calls."""

import logging

from langchain_core.runnables import RunnableLambda


def total(values: list[int]) -> int:
    """Reduce the fixture input using a real LangChain runnable stage."""
    return sum(values)


def render(value: int) -> str:
    """Render the second stage's deterministic result."""
    return f"langchain-onboarding:{value}"


agent = RunnableLambda(total) | RunnableLambda(render)


def run() -> str:
    """Fail the sandbox run unless both LangChain stages execute correctly."""
    result = agent.invoke([2, 3, 5])
    if result != "langchain-onboarding:10":
        raise RuntimeError(f"LangChain runnable returned an unexpected result: {result!r}")
    logging.getLogger(__name__).info("GitHub onboarding fixture completed: %s", result)
    return result
