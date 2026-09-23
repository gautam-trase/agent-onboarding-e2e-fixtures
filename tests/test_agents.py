"""Execute each real framework fixture in its own dependency environment."""

import importlib.util
import os
import json
import subprocess
import sys
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


def test_command_prints_final_result():
    framework = os.environ["FIXTURE_FRAMEWORK"]
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parents[1] / "run_example.py"), framework],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout) == {
        "framework": framework,
        "input": [2, 3, 5],
        "result": f"{framework}-onboarding:10",
    }
