"""Validate community health files added alongside issue templates."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_contributing_guidelines_reference_license_and_tests():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "Apache-2.0" in contributing
    assert "Write tests for new functionality" in contributing
    assert "Ensure tests pass" in contributing


def test_contributing_has_title_and_welcome_message():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert contributing.startswith("# Contributing to Monster Gaming\n")
    assert "We welcome contributions!" in contributing
    assert "Here's how to get started." in contributing


def test_contributing_guidelines_require_code_style():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    assert "Follow existing code style and conventions" in guidelines


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


def test_contributing_questions_section_is_last():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    headings = [line for line in contributing.splitlines() if line.startswith("## ")]

    assert headings[-1] == "## Questions?"
    assert "dev@monstergaming.ai" in contributing.split("## Questions?", maxsplit=1)[1]


def test_pull_request_template_has_release_checklist():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")

    assert "## What does this PR do?" in template
    assert "## How to test" in template
    assert "Tests pass locally" in template
    assert "SPDX headers present on new files" in template
    assert "Documentation updated (if applicable)" in template


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


def test_contributing_guidelines_has_four_bullets():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    guideline_lines = [line for line in guidelines.splitlines() if line.startswith("- ")]
    assert len(guideline_lines) == 4


def test_pull_request_template_sections_follow_review_order():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    headings = [line for line in template.splitlines() if line.startswith("## ")]

    assert headings == ["## What does this PR do?", "## How to test", "## Checklist"]


def test_license_includes_official_license_reference_url():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "http://www.apache.org/licenses/LICENSE-2.0" in license_text


def test_license_contains_copyright_notice_block():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "END OF TERMS AND CONDITIONS" in license_text
    assert "Licensed under the Apache License, Version 2.0" in license_text
    assert "distributed under the License is distributed on an \"AS IS\" BASIS" in license_text


def test_license_copyright_notice_follows_end_of_terms():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    end_marker = "END OF TERMS AND CONDITIONS"
    end_index = license_text.index(end_marker)
    notice_block = license_text[end_index:]

    assert "Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming" in notice_block
    assert "limitations under the License." in notice_block


def test_contributing_license_section_references_apache():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    license_section = contributing.split("## License", maxsplit=1)[1]
    license_section = license_section.split("## Questions", maxsplit=1)[0]

    assert "Apache-2.0 License" in license_section
    assert "licensed under" in license_section.lower()


def test_license_contains_all_nine_apache_sections():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    for section_number in range(1, 10):
        assert f"   {section_number}." in license_text, (
            f"missing Apache-2.0 section {section_number}; license may be truncated"
        )


def test_license_starts_with_apache_version_identifier():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert license_text.startswith("                                 Apache License")
    assert "Version 2.0, January 2004" in license_text.splitlines()[1]


def test_contributing_quick_start_requires_tests_before_pr_submission():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    quick_start = contributing.split("## Quick Start", maxsplit=1)[1]
    quick_start = quick_start.split("## Guidelines", maxsplit=1)[0]

    steps = [line for line in quick_start.splitlines() if line.strip()[:1].isdigit()]
    assert len(steps) == 5
    assert "Ensure tests pass" in steps[3]
    assert "Submit a pull request" in steps[4]


def test_contributing_sections_follow_document_order():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    headings = [line for line in contributing.splitlines() if line.startswith("## ")]

    assert headings == [
        "## Quick Start",
        "## Guidelines",
        "## License",
        "## Questions?",
    ]


def test_contributing_guidelines_spdx_header_is_first_bullet():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    first_bullet = next(line for line in guidelines.splitlines() if line.startswith("- "))
    assert "SPDX header" in first_bullet


def test_license_omits_apache_appendix():
    """Org LICENSE uses the standard notice block, not the optional appendix."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "APPENDIX" not in license_text
    assert "How to apply the Apache License" not in license_text


def test_contributing_quick_start_includes_make_changes_step():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    quick_start = contributing.split("## Quick Start", maxsplit=1)[1]
    quick_start = quick_start.split("## Guidelines", maxsplit=1)[0]

    steps = [line for line in quick_start.splitlines() if line.strip()[:1].isdigit()]
    assert steps[2].strip() == "3. Make your changes"
