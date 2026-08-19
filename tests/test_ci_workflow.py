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


def test_validate_workflow_pull_request_triggers_on_all_branches():
    """PR validation must run on every branch, not only main-targeting PRs."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    triggers = _workflow_triggers(workflow)

    pull_request_trigger = triggers["pull_request"]
    assert pull_request_trigger is None or pull_request_trigger == {}


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


def test_validate_workflow_pytest_uses_quiet_flag():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    run_commands = [
        step.get("run", "")
        for step in workflow["jobs"]["test"]["steps"]
        if "run" in step
    ]

    assert any(command.strip() == "pytest -q" for command in run_commands)


def test_validate_workflow_steps_follow_setup_order():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["test"]["steps"]

    checkout_idx = next(
        i for i, step in enumerate(steps) if step.get("uses", "").startswith("actions/checkout")
    )
    setup_python_idx = next(
        i for i, step in enumerate(steps) if step.get("uses", "").startswith("actions/setup-python")
    )
    install_idx = next(i for i, step in enumerate(steps) if step.get("name") == "Install test dependencies")
    pytest_idx = next(i for i, step in enumerate(steps) if step.get("name") == "Run validation tests")

    assert checkout_idx < setup_python_idx < install_idx < pytest_idx


def test_validate_workflow_pip_install_uses_requirements_file():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    install_step = next(
        step for step in workflow["jobs"]["test"]["steps"]
        if step.get("name") == "Install test dependencies"
    )

    assert install_step["run"].strip() == "pip install -r requirements-dev.txt"


def test_validate_workflow_is_sole_ci_gate():
    """Only validate.yml should gate merges; duplicate workflows cause drift."""
    workflows_dir = REPO_ROOT / ".github" / "workflows"
    workflow_files = sorted(path.name for path in workflows_dir.glob("*.yml"))

    assert workflow_files == ["validate.yml"]
