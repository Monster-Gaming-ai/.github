"""Validate CI workflow gates profile and template regressions on merge."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def _workflow_triggers(workflow: dict) -> dict:
    """PyYAML parses unquoted `on` as boolean True."""
    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict), "workflow must declare trigger events"
    return triggers


def test_validate_workflow_runs_on_pull_request_and_main_push():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    triggers = _workflow_triggers(workflow)

    assert "pull_request" in triggers
    assert triggers["push"]["branches"] == ["main"]


def test_validate_workflow_executes_pytest():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    test_job = workflow["jobs"]["test"]

    step_names = [step.get("name", "") for step in test_job["steps"]]
    run_commands = [step.get("run", "") for step in test_job["steps"] if "run" in step]

    assert any("pytest" in command for command in run_commands)
    assert any("requirements-dev.txt" in command for command in run_commands)
    assert "Install test dependencies" in step_names
    assert "Run validation tests" in step_names


def test_validate_workflow_pins_python_version():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    setup_python = next(
        step for step in workflow["jobs"]["test"]["steps"] if step.get("uses", "").startswith("actions/setup-python")
    )

    assert setup_python["with"]["python-version"] == "3.12"
    assert setup_python["with"]["cache"] == "pip"


def test_validate_workflow_has_display_name():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert workflow.get("name") == "Validate org profile"


def test_validate_workflow_uses_checkout_and_pip_cache_path():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["test"]["steps"]

    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout"))
    setup_python = next(step for step in steps if step.get("uses", "").startswith("actions/setup-python"))

    assert checkout["uses"] == "actions/checkout@v4"
    assert setup_python["with"]["cache-dependency-path"] == "requirements-dev.txt"


def test_validate_workflow_job_runs_on_ubuntu_latest():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert workflow["jobs"]["test"]["runs-on"] == "ubuntu-latest"


def test_requirements_dev_lists_pytest_and_pyyaml():
    requirements = (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8")

    assert "pytest" in requirements
    assert "PyYAML" in requirements


def test_requirements_dev_pins_compatible_major_versions():
    requirements = (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8")

    assert "pytest>=8.0,<9" in requirements
    assert "PyYAML>=6.0,<7" in requirements


def test_validate_workflow_has_single_test_job():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    assert set(workflow["jobs"].keys()) == {"test"}


def test_validate_workflow_uses_setup_python_v5():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    setup_python = next(
        step for step in workflow["jobs"]["test"]["steps"] if step.get("uses", "").startswith("actions/setup-python")
    )

    assert setup_python["uses"] == "actions/setup-python@v5"
