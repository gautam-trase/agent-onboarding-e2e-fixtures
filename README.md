# Agent onboarding E2E fixtures

Public, synthetic LangChain and Google ADK examples for testing GitHub source
import, dependency installation, image builds, and agent execution. Reading these
fixtures requires no GitHub login or credentials. No model API keys are needed.

| Directory | Behavior |
| --- | --- |
| `github_onboarding/langchain` | Composes two LangChain runnable stages and verifies a total of 10. |
| `github_onboarding/adk` | Runs a custom ADK BaseAgent, persists its event, and verifies session state. |
| `github_onboarding/langchain_missing_dependencies` | Deliberately omits requirements.txt to test rejection. |
| `github_onboarding/adk_missing_dependencies` | Deliberately omits requirements.txt to test rejection. |

The valid examples execute real framework code with deterministic results and no
provider calls. Each bundle has a `trase-agent.yaml` manifest whose entrypoint is
`agent.onboarding_agent:run`. The incomplete examples must be rejected before
execution; do not add requirements.txt to those directories.

## Run an example

Both examples take the fixed input `[2, 3, 5]`, calculate its sum through the
framework, verify that it is 10, and return a result. The command-line runner
prints that result as JSON. This is real framework execution; it does not call an
LLM or require any API key, GitHub token, login, or other credential.

Use Python 3.13 and separate virtual environments:

### LangChain

```sh
python3.13 -m venv /tmp/onboarding-langchain
/tmp/onboarding-langchain/bin/python -m pip install -r github_onboarding/langchain/requirements.txt
/tmp/onboarding-langchain/bin/python run_example.py langchain
```

Expected standard output:

```json
{"framework": "langchain", "input": [2, 3, 5], "result": "langchain-onboarding:10"}
```

### Google ADK

```sh
python3.13 -m venv /tmp/onboarding-adk
/tmp/onboarding-adk/bin/python -m pip install -r github_onboarding/adk/requirements.txt
/tmp/onboarding-adk/bin/python run_example.py adk
```

Expected standard output:

```json
{"framework": "adk", "input": [2, 3, 5], "result": "adk-onboarding:10"}
```

Dependencies may emit warnings on standard error. An unexpected framework result
raises an error and exits unsuccessfully rather than printing a success result.

### Tests

Install `pytest` in each environment, then run with its Python interpreter:

```sh
FIXTURE_FRAMEWORK=langchain /tmp/onboarding-langchain/bin/python -m pytest tests/
FIXTURE_FRAMEWORK=adk /tmp/onboarding-adk/bin/python -m pytest tests/
```

CI audits each complete dependency lock for known vulnerabilities, then verifies
the framework entrypoint and the printed JSON for each example.

## Pinning and updating

Consumers should pin a full commit SHA plus a scenario directory, not a moving
branch. Additional branches can hold new cases without changing an existing pin.
Only synthetic test data and public dependencies belong in this repository.

Dependencies are pinned, including transitive packages. To regenerate a lock from
the repository root (requires uv):

```sh
uv pip compile --python-version 3.13 --no-header github_onboarding/langchain/requirements.in -o github_onboarding/langchain/requirements.txt
uv pip compile --python-version 3.13 --no-header github_onboarding/adk/requirements.in -o github_onboarding/adk/requirements.txt
```

Framework references: [LangChain RunnableSequence](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
and [Google ADK](https://github.com/google/adk-python/tree/v2.9.2/src/google/adk).
