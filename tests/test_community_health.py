"""Validate community health files added alongside issue templates."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_contributing_guidelines_reference_license_and_tests():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "Apache-2.0" in contributing
    assert "Write tests for new functionality" in contributing
    assert "Ensure tests pass" in contributing


def test_license_is_apache_2():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "Apache License" in license_text
    assert "Version 2.0" in license_text


def test_license_copyright_holder():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming" in license_text


def test_contributing_includes_contact_channel():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "dev@monstergaming.ai" in contributing
    assert "Open a Discussion" in contributing


def test_pull_request_template_has_release_checklist():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")

    assert "## What does this PR do?" in template
    assert "## How to test" in template
    assert "Tests pass locally" in template
    assert "SPDX headers present on new files" in template


def test_contributing_documents_fork_and_branch_workflow():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "Fork the repository" in contributing
    assert "git checkout -b feat/your-feature" in contributing
    assert "Submit a pull request" in contributing


def test_contributing_requires_spdx_headers_on_new_files():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "SPDX header" in contributing
    assert "one feature or fix per PR" in contributing


def test_contributing_quick_start_has_five_step_workflow():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    quick_start = contributing.split("## Quick Start", maxsplit=1)[1]
    quick_start = quick_start.split("## Guidelines", maxsplit=1)[0]

    for step in ("1.", "2.", "3.", "4.", "5."):
        assert step in quick_start


def test_license_contains_standard_apache_sections():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    for section in (
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
        "Grant of Copyright License",
        "Grant of Patent License",
        "Limitation of Liability",
    ):
        assert section in license_text


def test_pull_request_template_checklist_has_three_items():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    checklist_items = [line for line in template.splitlines() if line.startswith("- [ ]")]

    assert len(checklist_items) == 3
    assert any("Tests pass locally" in item for item in checklist_items)
    assert any("Documentation updated" in item for item in checklist_items)
    assert any("SPDX headers present" in item for item in checklist_items)


def test_gitignore_excludes_python_test_artifacts():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    for pattern in ("__pycache__/", ".pytest_cache/", "*.py[cod]"):
        assert pattern in gitignore
