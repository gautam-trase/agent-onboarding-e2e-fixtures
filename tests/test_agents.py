"""Execute each real framework fixture in its own dependency environment."""

import importlib.util
import os
from pathlib import Path


def test_framework_entrypoint_completes():
    framework = os.environ["FIXTURE_FRAMEWORK"]
    assert framework in {"langchain", "adk"}
    path = Path(__file__).parents[1] / "github_onboarding" / framework / "agent/onboarding_agent.py"
    spec = importlib.util.spec_from_file_location("onboarding_agent", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.run() == f"{framework}-onboarding:10"
