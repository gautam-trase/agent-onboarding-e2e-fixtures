"""Run one deterministic framework example and print its final result as JSON."""

import argparse
import importlib.util
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("framework", choices=("langchain", "adk"))
    args = parser.parse_args()
    path = (
        Path(__file__).parent
        / "github_onboarding"
        / args.framework
        / "agent/onboarding_agent.py"
    )
    spec = importlib.util.spec_from_file_location("onboarding_agent", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load example: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run()
    print(json.dumps({"framework": args.framework, "input": [2, 3, 5], "result": result}))


if __name__ == "__main__":
    main()
