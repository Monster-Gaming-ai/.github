"""Validate CI workflow that gates profile and community health regressions."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def test_validate_workflow_exists_and_runs_tests():
    assert WORKFLOW_PATH.is_file(), "validate workflow must exist to enforce tests on PRs"

    with WORKFLOW_PATH.open(encoding="utf-8") as handle:
        workflow = yaml.safe_load(handle)

    assert workflow.get("name") == "Validate org profile"

    triggers = workflow.get("on") or workflow.get(True) or {}
    assert "pull_request" in triggers
    assert "main" in triggers.get("push", {}).get("branches", [])

    jobs = workflow.get("jobs", {})
    assert "test" in jobs

    steps = [step.get("run", "") for step in jobs["test"].get("steps", [])]
    assert any("pytest" in step for step in steps), "workflow must run pytest"
