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


def test_validate_workflow_actions_pin_major_version_tags():
    """Floating action refs (@main) break CI silently when upstream releases change."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    action_steps = [
        step["uses"]
        for step in workflow["jobs"]["test"]["steps"]
        if step.get("uses", "").startswith("actions/")
    ]

    assert action_steps, "workflow must use GitHub Actions for checkout and setup"
    for action_ref in action_steps:
        assert "@v" in action_ref, f"action must pin a major version tag, not float: {action_ref!r}"
        assert "@main" not in action_ref
        assert "@master" not in action_ref


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


EXPECTED_TEST_MODULES = (
    "test_ci_workflow.py",
    "test_community_health.py",
    "test_issue_templates.py",
    "test_profile_readme.py",
    "test_profile_regression.py",
)


def test_validation_suite_includes_all_expected_test_modules():
    """Coverage automation must keep module boundaries — missing files silently drop guards."""
    present = sorted(path.name for path in (REPO_ROOT / "tests").glob("test_*.py"))

    assert present == list(EXPECTED_TEST_MODULES)


def test_requirements_dev_lists_only_test_dependencies():
    requirements = (REPO_ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()
    non_empty = [line for line in requirements if line.strip() and not line.strip().startswith("#")]

    assert non_empty == ["pytest>=8.0,<9", "PyYAML>=6.0,<7"]


def test_validate_workflow_push_trigger_limited_to_main():
    """Push validation should gate main merges, not every branch push."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    triggers = _workflow_triggers(workflow)

    push_trigger = triggers.get("push", {})
    assert push_trigger.get("branches") == ["main"]
    assert "tags" not in push_trigger
    assert "paths" not in push_trigger


def test_validate_workflow_has_only_pull_request_and_push_triggers():
    """Extra triggers (schedule, workflow_dispatch) add CI cost and drift risk."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    triggers = _workflow_triggers(workflow)

    assert set(triggers.keys()) == {"pull_request", "push"}


def test_validate_workflow_omits_elevated_permissions():
    """Validation needs only checkout + pytest — avoid broad GITHUB_TOKEN scopes."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    permissions = workflow.get("permissions")
    assert permissions is None or permissions == {"contents": "read"}


def test_validate_workflow_omits_secrets_and_environment_variables():
    """Org profile CI must not depend on repo secrets or injected env vars."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    assert "env" not in workflow
    assert "secrets" not in workflow

    for step in workflow["jobs"]["test"]["steps"]:
        assert "env" not in step or step["env"] == {}
        run_command = step.get("run", "")
        assert "${{ secrets." not in run_command


def test_validate_workflow_omits_concurrency_block():
    """Concurrency settings can cancel in-flight validation runs and hide regressions."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    assert "concurrency" not in workflow


def test_validate_workflow_job_has_no_strategy_matrix():
    """Single validation path keeps pytest deterministic and CI fast."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    test_job = workflow["jobs"]["test"]

    assert "strategy" not in test_job


def test_validate_workflow_job_has_no_needs_dependencies():
    """Validation must not depend on other jobs — org profile has one CI gate."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    test_job = workflow["jobs"]["test"]

    assert "needs" not in test_job


def test_validate_workflow_steps_do_not_use_continue_on_error():
    """Failed pytest must fail the workflow — continue-on-error hides regressions."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    for step in workflow["jobs"]["test"]["steps"]:
        assert step.get("continue-on-error") is not True


def test_validate_workflow_omits_job_timeout_minutes():
    """Arbitrary job timeouts can flake on slow CI runners and hide real regressions."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    test_job = workflow["jobs"]["test"]

    assert "timeout-minutes" not in test_job


def test_validate_workflow_steps_omit_timeout_minutes():
    """Step-level timeouts can abort pytest mid-run and produce misleading green builds."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    for step in workflow["jobs"]["test"]["steps"]:
        assert "timeout-minutes" not in step


def test_validate_workflow_omits_defaults_run_shell_override():
    """Explicit shell overrides can drift from ubuntu-latest defaults and break pip/pytest paths."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    defaults = workflow.get("defaults", {})
    run_defaults = defaults.get("run", {})

    assert "shell" not in run_defaults


def test_validate_workflow_steps_omit_working_directory():
    """Steps must run from repo root — working-directory overrides break relative test paths."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    for step in workflow["jobs"]["test"]["steps"]:
        assert "working-directory" not in step


def test_validate_workflow_steps_omit_conditional_execution():
    """Conditional steps can skip pytest on certain events and hide profile regressions."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    for step in workflow["jobs"]["test"]["steps"]:
        assert "if" not in step


def test_validate_workflow_has_exactly_four_steps():
    """Partial reverts can drop install or pytest steps while leaving checkout/setup intact."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    assert len(workflow["jobs"]["test"]["steps"]) == 4


def test_validate_workflow_checkout_omits_with_overrides():
    """Checkout overrides can cause shallow clones or credential persistence drift."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    checkout = next(
        step for step in workflow["jobs"]["test"]["steps"]
        if step.get("uses", "").startswith("actions/checkout")
    )

    assert "with" not in checkout


def test_validate_workflow_uses_only_checkout_and_setup_python_actions():
    """Only pinned GitHub Actions should run — third-party actions add supply-chain risk."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    action_steps = [
        step["uses"]
        for step in workflow["jobs"]["test"]["steps"]
        if "uses" in step
    ]

    assert action_steps == ["actions/checkout@v4", "actions/setup-python@v5"]


def test_validate_workflow_pytest_runs_full_suite_without_path_filters():
    """Narrowing pytest scope silently drops entire test modules while CI stays green."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    pytest_step = next(
        step for step in workflow["jobs"]["test"]["steps"]
        if step.get("name") == "Run validation tests"
    )

    run_command = pytest_step["run"].strip()
    assert run_command == "pytest -q"
    assert "tests/" not in run_command
    assert "-k" not in run_command
    assert "--ignore" not in run_command


def test_validate_workflow_omits_job_level_permissions():
    """Job-level permissions can override workflow scopes and widen GITHUB_TOKEN access."""
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    test_job = workflow["jobs"]["test"]

    assert "permissions" not in test_job
