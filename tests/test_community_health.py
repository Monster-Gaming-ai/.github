"""Validate community health files added alongside issue templates."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

REDISTRIBUTION_CONDITIONS = (
    ("(a)", "give any other recipients of the Work or"),
    ("(b)", "cause any modified files to carry prominent notices"),
    ("(c)", "retain, in the Source form of any Derivative Works"),
    ("(d)", 'If the Work includes a "NOTICE" text file'),
)


def _license_redistribution_section() -> str:
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    return redistribution.split("   4. Redistribution.", maxsplit=1)[1]


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


def test_contributing_guidelines_pr_focus_uses_em_dash():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    pr_focus_bullet = next(
        line for line in guidelines.splitlines() if "one feature or fix per PR" in line
    )
    assert pr_focus_bullet.strip() == "- Keep PRs focused — one feature or fix per PR"


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


def test_license_contains_remaining_apache_section_titles():
    """Sections 4–7 and 9 must stay intact — partial license files break compliance."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    for section_title in (
        "Redistribution",
        "Submission of Contributions",
        "Trademarks",
        "Disclaimer of Warranty",
        "Accepting Warranty or Additional Liability",
    ):
        assert section_title in license_text


def test_license_includes_apache_license_portal_url():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "http://www.apache.org/licenses/" in license_text.split("END OF TERMS AND CONDITIONS")[0]


def test_license_copyright_notice_includes_compliance_statement():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    notice_block = license_text.split("END OF TERMS AND CONDITIONS", maxsplit=1)[1]

    assert "you may not use this file except in compliance with the License" in notice_block


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


def test_license_end_of_terms_marker_appears_once():
    """Duplicate or missing END marker indicates a bad merge at the notice boundary."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert license_text.count("END OF TERMS AND CONDITIONS") == 1


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


def test_contributing_questions_section_references_discussions():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    questions = contributing.split("## Questions?", maxsplit=1)[1]

    assert "Open a Discussion on this repository" in questions
    assert "dev@monstergaming.ai" in questions


def test_pull_request_template_doc_update_checklist_uses_exact_conditional_wording():
    """Doc checklist item must stay optional — exact wording prevents silent scope creep."""
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    checklist_items = [line for line in template.splitlines() if line.startswith("- [ ]")]

    doc_item = next(item for item in checklist_items if "Documentation updated" in item)
    assert doc_item == "- [ ] Documentation updated (if applicable)"


def test_contributing_guidelines_spdx_bullet_uses_exact_wording():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    first_bullet = next(line for line in guidelines.splitlines() if line.startswith("- "))
    assert first_bullet == "- All new source files must include the Apache-2.0 SPDX header"


def test_contributing_guidelines_test_bullet_uses_exact_wording():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    test_bullet = next(line for line in guidelines.splitlines() if "Write tests" in line)
    assert test_bullet == "- Write tests for new functionality"


def test_gitignore_lists_exactly_three_patterns_in_order():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = [line for line in gitignore.splitlines() if line.strip()]

    assert lines == ["__pycache__/", "*.py[cod]", ".pytest_cache/"]


def test_gitignore_does_not_exclude_tests_directory():
    """Accidental tests/ ignore patterns would make CI pass with zero guards."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = [line.strip() for line in gitignore.splitlines() if line.strip() and not line.startswith("#")]

    for pattern in lines:
        assert pattern not in {"tests/", "tests", "/tests", "/tests/"}, (
            f".gitignore must not exclude the validation suite: {pattern!r}"
        )


def test_gitignore_does_not_exclude_community_health_or_ci_paths():
    """Broad ignore patterns would hide LICENSE, templates, or CI config from git."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    patterns = {
        line.strip()
        for line in gitignore.splitlines()
        if line.strip() and not line.startswith("#")
    }
    forbidden = {
        "LICENSE",
        "CONTRIBUTING.md",
        "profile/",
        "profile/README.md",
        ".github/",
        "tests/",
        "requirements-dev.txt",
        "*.md",
        "*.yml",
    }
    assert not (patterns & forbidden)


def test_pull_request_template_tests_checklist_uses_exact_wording():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    checklist_items = [line for line in template.splitlines() if line.startswith("- [ ]")]

    tests_item = next(item for item in checklist_items if "Tests pass locally" in item)
    assert tests_item == "- [ ] Tests pass locally"


def test_pull_request_template_spdx_checklist_uses_exact_wording():
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    checklist_items = [line for line in template.splitlines() if line.startswith("- [ ]")]

    spdx_item = next(item for item in checklist_items if "SPDX headers present" in item)
    assert spdx_item == "- [ ] SPDX headers present on new files"


def test_license_contains_definitions_section():
    """Section 1 Definitions must stay intact — truncated licenses break legal meaning."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert "   1. Definitions." in license_text
    assert '"License" shall mean the terms and conditions for use, reproduction,' in license_text


def test_license_definitions_include_core_terms():
    """Apache-2.0 section 1 defines terms referenced throughout sections 2–9."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    for term in (
        '"Licensor" shall mean',
        '"Legal Entity" shall mean',
        '"Work" shall mean',
        '"Derivative Works" shall mean',
        '"Contribution" shall mean',
        '"Contributor" shall mean',
    ):
        assert term in definitions, f"missing Apache-2.0 definition for {term!r}"


def test_license_definitions_include_source_and_object_forms():
    """Source/Object form definitions are referenced in sections 2, 4, and redistribution clauses."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"Source" form shall mean' in definitions
    assert "software source code" in definitions
    assert "configuration files" in definitions
    assert '"Object" form shall mean' in definitions
    assert "compiled object code" in definitions


def test_license_definitions_include_you_term():
    """The 'You' definition scopes who may exercise license permissions."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"You" (or "Your") shall mean' in definitions
    assert "exercising permissions granted by this License" in definitions


def test_license_contribution_definition_excludes_not_a_contribution():
    """Section 1 must preserve the 'Not a Contribution' exclusion for compliance tooling."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"Not a Contribution."' in definitions
    assert "excluding communication that is conspicuously marked or otherwise" in definitions


def test_license_redistribution_section_includes_required_conditions():
    """Section 4 redistribution conditions (a)–(d) must stay intact for downstream compliance."""
    redistribution = _license_redistribution_section()

    for _, condition in REDISTRIBUTION_CONDITIONS:
        assert condition in redistribution, f"missing Apache-2.0 redistribution condition: {condition!r}"


@pytest.mark.parametrize("marker,opening_fragment", REDISTRIBUTION_CONDITIONS)
def test_license_redistribution_conditions_preserve_lettered_markers(marker, opening_fragment):
    """Each (a)–(d) marker must stay paired with its opening clause — aggregate loops miss letter drift."""
    redistribution = _license_redistribution_section()

    marker_idx = redistribution.index(marker)
    fragment_idx = redistribution.index(opening_fragment)
    assert marker_idx < fragment_idx, (
        f"condition {marker} must precede its opening clause; partial edits can drop letter markers"
    )


def test_license_redistribution_conditions_appear_in_abcd_order():
    """Section 4 conditions must stay in canonical (a)–(d) order for compliance parsers."""
    redistribution = _license_redistribution_section()
    indices = [redistribution.index(marker) for marker, _ in REDISTRIBUTION_CONDITIONS]

    assert indices == sorted(indices)


def test_license_redistribution_section_has_exactly_four_lettered_markers():
    """Section 4 must contain exactly (a)–(d) — extra or missing markers break compliance tooling."""
    redistribution = _license_redistribution_section()
    markers = [marker for marker, _ in REDISTRIBUTION_CONDITIONS]

    assert redistribution.count("(a)") == 1
    assert redistribution.count("(b)") == 1
    assert redistribution.count("(c)") == 1
    assert redistribution.count("(d)") == 1
    assert all(redistribution.count(marker) == 1 for marker in markers)


def test_license_redistribution_preserves_meet_following_conditions_preamble():
    """Section 4 must preserve the conditions preamble — truncation drops the (a)–(d) list anchor."""
    redistribution = _license_redistribution_section()

    assert "meet the following conditions:" in redistribution


def test_license_redistribution_condition_c_precedes_d_before_modification_clause():
    """Condition (c) must end with '; and' before (d) — deleting (d) leaves a dangling conjunction."""
    redistribution = _license_redistribution_section()

    c_end_idx = redistribution.index("the Derivative Works; and")
    d_idx = redistribution.index('If the Work includes a "NOTICE" text file')
    modification_idx = redistribution.index("You may add Your own copyright statement")

    assert c_end_idx < d_idx < modification_idx


def test_license_redistribution_permits_any_medium_and_form():
    """Section 4 opening must preserve modification and Source/Object form permissions."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "Work or Derivative Works thereof in any medium, with or without" in redistribution
    assert "modifications, and in Source or Object form, provided that You" in redistribution


def test_license_redistribution_preserves_modification_license_clause():
    """Section 4 must preserve the derivative-works modification license carve-out."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    for phrase in (
        "You may add Your own copyright statement to Your modifications and",
        "may provide additional or different license terms and conditions",
        "for use, reproduction, or distribution of Your modifications, or",
        "for any such Derivative Works as a whole, provided Your use,",
        "reproduction, and distribution of the Work otherwise complies with",
        "the conditions stated in this License.",
    ):
        assert phrase in redistribution, (
            f"missing Apache-2.0 modification license clause: {phrase!r}"
        )


def test_license_redistribution_preserves_derivative_attribution_notices_clause():
    """Section 4 must preserve optional attribution notices that cannot modify the License."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "You may add Your own attribution" in redistribution
    assert "notices within Derivative Works that You distribute" in redistribution
    assert "such additional attribution notices cannot be construed" in redistribution
    assert "as modifying the License." in redistribution


def test_license_redistribution_notice_file_does_not_modify_license():
    """Section 4 (d) NOTICE file contents must remain informational only."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "of the NOTICE file are for informational purposes only and" in redistribution
    assert "do not modify the License." in redistribution


def test_license_grant_sections_follow_definitions():
    """Numbered sections must stay in canonical order — reordering breaks compliance tooling."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    definitions_idx = license_text.index("   1. Definitions.")
    copyright_idx = license_text.index("   2. Grant of Copyright License.")
    patent_idx = license_text.index("   3. Grant of Patent License.")

    assert definitions_idx < copyright_idx < patent_idx


def test_license_numbered_sections_follow_full_canonical_order():
    """Sections 1–9 must stay in Apache-2.0 canonical order for compliance parsers."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")

    section_titles = (
        "   1. Definitions.",
        "   2. Grant of Copyright License.",
        "   3. Grant of Patent License.",
        "   4. Redistribution.",
        "   5. Submission of Contributions.",
        "   6. Trademarks.",
        "   7. Disclaimer of Warranty.",
        "   8. Limitation of Liability.",
        "   9. Accepting Warranty or Additional Liability.",
    )
    indices = [license_text.index(title) for title in section_titles]
    assert indices == sorted(indices)


def test_license_copyright_grant_includes_perpetual_worldwide_terms():
    """Section 2 must preserve the irrevocable copyright grant — truncation removes downstream rights."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    copyright_grant = license_text.split("   3. Grant of Patent License.", maxsplit=1)[0]
    copyright_grant = copyright_grant.split("   2. Grant of Copyright License.", maxsplit=1)[1]

    for term in (
        "perpetual",
        "worldwide",
        "non-exclusive",
        "no-charge",
        "royalty-free",
        "irrevocable",
        "reproduce, prepare Derivative Works of",
        "publicly display, publicly perform, sublicense, and distribute",
    ):
        assert term in copyright_grant, f"missing Apache-2.0 copyright grant term: {term!r}"


def test_license_patent_grant_includes_termination_on_litigation():
    """Section 3 patent termination clause must stay intact — edits here change contributor obligations."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    for phrase in (
        "institute patent litigation against any entity",
        "cross-claim or counterclaim in a lawsuit",
        "contributory patent infringement",
        "then any patent licenses",
        "granted to You under this License for that Work shall terminate",
        "as of the date such litigation is filed",
    ):
        assert phrase in patent_grant, f"missing Apache-2.0 patent termination language: {phrase!r}"


def test_license_submission_of_contributions_preserves_default_license_terms():
    """Section 5 binds inbound contributions to Apache-2.0 unless explicitly stated otherwise."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    submission = license_text.split("   6. Trademarks.", maxsplit=1)[0]
    submission = submission.split("   5. Submission of Contributions.", maxsplit=1)[1]

    assert "Unless You explicitly state otherwise" in submission
    assert "shall be under the terms and conditions of" in submission
    assert "this License, without any additional terms or conditions" in submission


def test_license_trademarks_section_restricts_product_name_use():
    """Section 6 must keep trademark restrictions — permissive edits create brand misuse risk."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    trademarks = license_text.split("   7. Disclaimer of Warranty.", maxsplit=1)[0]
    trademarks = trademarks.split("   6. Trademarks.", maxsplit=1)[1]

    assert "This License does not grant permission to use the trade" in trademarks
    assert "names, trademarks, service marks, or product names of the Licensor" in trademarks
    assert "except as required for reasonable and customary use in describing the" in trademarks
    assert "origin of the Work and reproducing the content of the NOTICE file" in trademarks


def test_license_disclaimer_of_warranty_uses_as_is_basis():
    """Section 7 warranty disclaimer must stay intact — notice block alone is insufficient."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    disclaimer = license_text.split("   8. Limitation of Liability.", maxsplit=1)[0]
    disclaimer = disclaimer.split("   7. Disclaimer of Warranty.", maxsplit=1)[1]

    assert 'on an "AS IS" BASIS' in disclaimer
    assert "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND" in disclaimer
    assert "FITNESS FOR A" in disclaimer
    assert "PARTICULAR PURPOSE" in disclaimer


def test_license_disclaimer_of_warranty_lists_title_and_non_infringement():
    """Section 7 implied-warranty list must name TITLE and NON-INFRINGEMENT — FITNESS-only checks miss mid-line deletes."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    disclaimer = license_text.split("   8. Limitation of Liability.", maxsplit=1)[0]
    disclaimer = disclaimer.split("   7. Disclaimer of Warranty.", maxsplit=1)[1]

    assert "implied, including, without limitation, any warranties or conditions" in disclaimer
    assert "of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A" in disclaimer
    assert "risks associated with Your exercise of permissions under this License." in disclaimer


def test_license_limitation_of_liability_preserves_damage_exclusions():
    """Section 8 caps contributor liability — missing clauses weaken downstream protections."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    liability = license_text.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[0]
    liability = liability.split("   8. Limitation of Liability.", maxsplit=1)[1]

    for phrase in (
        "In no event and under no legal theory",
        "whether in tort (including negligence), contract, or otherwise",
        "direct, indirect, special",
        "incidental, or consequential damages",
        "result of this License or out of the use or inability to use the",
        "loss of goodwill",
        "computer failure or malfunction",
        "has been advised of the possibility of such damages",
    ):
        assert phrase in liability, f"missing Apache-2.0 liability exclusion: {phrase!r}"


def test_license_warranty_acceptance_requires_indemnification():
    """Section 9 indemnification clause must stay intact for optional warranty offers."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    warranty = license_text.split("END OF TERMS AND CONDITIONS", maxsplit=1)[0]
    warranty = warranty.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[1]

    assert "While redistributing" in warranty
    assert "the Work or Derivative Works thereof, You may choose to offer" in warranty
    assert "acceptance of support, warranty, indemnity" in warranty
    assert "indemnify," in warranty
    assert "defend, and hold each Contributor harmless" in warranty
    assert "on Your own behalf and on Your sole responsibility" in warranty
    assert (
        "incurred by, or claims asserted against, such Contributor by reason"
        in warranty
    )
    assert "of your accepting any such warranty or additional liability." in warranty


def test_license_copyright_grant_closes_with_source_or_object_form_distribution():
    """Section 2 closing clause scopes distribution media — grant-term loops miss the final sentence."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    copyright_grant = license_text.split("   3. Grant of Patent License.", maxsplit=1)[0]
    copyright_grant = copyright_grant.split("   2. Grant of Copyright License.", maxsplit=1)[1]

    assert (
        "Work and such Derivative Works in Source or Object form." in copyright_grant
    )


def test_license_definitions_include_legal_entity_control_criteria():
    """Legal Entity control definition scopes affiliate obligations in sections 2–9."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"Legal Entity" shall mean the union of the acting entity' in definitions
    assert '"control" means (i) the power, direct or indirect, to cause the' in definitions
    assert "ownership of fifty percent (50%) or more of the" in definitions
    assert "(iii) beneficial ownership of such entity." in definitions


def test_license_derivative_works_excludes_merely_linked_works():
    """Section 1 must preserve the separable/link exclusion — edits widen patent/copyright scope."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "Derivative Works shall not include works that remain" in definitions
    assert "separable from, or merely link (or bind by name) to the interfaces of" in definitions


def test_license_licensor_definition_specifies_copyright_owner():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"Licensor" shall mean the copyright owner or entity authorized by' in definitions
    assert "the copyright owner that is granting the License." in definitions


def test_license_patent_grant_includes_core_permissions():
    """Section 3 patent grant must preserve make/use/sell permissions — truncation removes rights."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    for permission in (
        "patent license to make, have made,",
        "use, offer to sell, sell, import, and otherwise transfer the Work",
        "necessarily infringed by their",
        "Contribution(s) alone or by combination of their Contribution(s)",
    ):
        assert permission in patent_grant, f"missing Apache-2.0 patent grant permission: {permission!r}"


def test_license_contribution_submitted_includes_communication_channels():
    """Section 1 'submitted' definition determines inbound contribution scope."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "electronic, verbal, or written communication sent" in definitions
    assert "communication on electronic mailing lists, source code control systems" in definitions
    assert "issue tracking systems that are managed by, or on behalf of, the" in definitions


def test_license_submission_preserves_separate_license_agreement_clause():
    """Section 5 must preserve separate license agreement carve-out for enterprise contributors."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    submission = license_text.split("   6. Trademarks.", maxsplit=1)[0]
    submission = submission.split("   5. Submission of Contributions.", maxsplit=1)[1]

    assert "Notwithstanding the above, nothing herein shall supersede or modify" in submission
    assert "the terms of any separate license agreement you may have executed" in submission
    assert "with Licensor regarding such Contributions." in submission


def test_license_disclaimer_includes_title_and_non_infringement_warranties():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    disclaimer = license_text.split("   8. Limitation of Liability.", maxsplit=1)[0]
    disclaimer = disclaimer.split("   7. Disclaimer of Warranty.", maxsplit=1)[1]

    assert "TITLE, NON-INFRINGEMENT, MERCHANTABILITY" in disclaimer
    assert "appropriateness of using or redistributing the Work" in disclaimer


def test_license_limitation_includes_computer_failure_damages():
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    liability = license_text.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[0]
    liability = liability.split("   8. Limitation of Liability.", maxsplit=1)[1]

    assert "work stoppage" in liability
    assert "computer failure or malfunction" in liability


def test_contributing_license_section_uses_exact_agreement_wording():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    license_section = contributing.split("## License", maxsplit=1)[1]
    license_section = license_section.split("## Questions?", maxsplit=1)[0].strip()

    assert license_section == (
        "By contributing, you agree that your contributions will be licensed under the Apache-2.0 License."
    )


def test_contributing_quick_start_steps_use_exact_wording():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    quick_start = contributing.split("## Quick Start", maxsplit=1)[1]
    quick_start = quick_start.split("## Guidelines", maxsplit=1)[0]
    steps = [line for line in quick_start.splitlines() if line.strip()[:1].isdigit()]

    assert steps == [
        "1. Fork the repository",
        "2. Create a feature branch: `git checkout -b feat/your-feature`",
        "3. Make your changes",
        "4. Ensure tests pass",
        "5. Submit a pull request",
    ]


def test_contributing_guidelines_code_style_bullet_exact_wording():
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    guidelines = contributing.split("## Guidelines", maxsplit=1)[1]
    guidelines = guidelines.split("## License", maxsplit=1)[0]

    code_style_bullet = next(line for line in guidelines.splitlines() if "code style" in line)
    assert code_style_bullet == "- Follow existing code style and conventions"


def test_license_patent_grant_preserves_except_as_stated_irrevocable_caveat():
    """Section 3 irrevocable caveat limits patent termination — dropping it changes grant scope."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    assert "(except as stated in this section) patent license" in patent_grant


def test_license_patent_grant_scopes_to_licensable_claims():
    """Section 3 must preserve patent-claim scope — truncation broadens or narrows coverage."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    assert "where such license applies only to those patent claims licensable" in patent_grant


def test_license_redistribution_condition_b_preserves_you_changed_files_notice():
    """Section 4(b) modification notice is required for downstream compliance tooling."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "stating that You changed the files" in redistribution


def test_license_redistribution_notice_file_preserves_display_placement_clause():
    """Section 4(d) NOTICE placement options must stay intact — edits drop compliance paths."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "within a display generated by the Derivative Works" in redistribution
    assert "wherever such third-party notices normally appear" in redistribution


def test_license_redistribution_condition_a_preserves_license_copy_requirement():
    """Section 4(a) requires passing the License to recipients — common truncation in forks."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "give any other recipients of the Work or" in redistribution
    assert "Derivative Works a copy of this License; and" in redistribution


def test_license_redistribution_condition_c_preserves_attribution_notice_retention():
    """Section 4(c) attribution retention clause protects upstream notices in derivative works."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "all copyright, patent, trademark, and" in redistribution
    assert "attribution notices from the Source form of the Work," in redistribution
    assert "excluding those notices that do not pertain to any part of" in redistribution


def test_license_redistribution_condition_d_preserves_notice_file_copy_requirement():
    """Section 4(d) requires distributing NOTICE attribution — dropping it breaks Apache compliance."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert 'If the Work includes a "NOTICE" text file as part of its' in redistribution
    assert "include a readable copy of the attribution notices contained" in redistribution


def test_license_redistribution_condition_d_preserves_notice_file_placement_paths():
    """Section 4(d) must list all NOTICE placement options — partial lists drop valid paths."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "within a NOTICE text file distributed" in redistribution
    assert "as part of the Derivative Works;" in redistribution
    assert "within the Source form or" in redistribution
    assert "documentation, if provided along with the Derivative Works;" in redistribution


def test_license_redistribution_condition_d_preserves_addendum_attribution_clause():
    """Section 4(d) addendum clause prevents attribution notices from being construed as relicensing."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    assert "alongside" in redistribution
    assert "or as an addendum to the NOTICE text from the Work, provided" in redistribution
    assert "that such additional attribution notices cannot be construed" in redistribution


def test_license_disclaimer_attributes_warranty_to_each_contributor():
    """Section 7 per-contributor framing distinguishes Licensor vs Contributor liability."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    disclaimer = license_text.split("   8. Limitation of Liability.", maxsplit=1)[0]
    disclaimer = disclaimer.split("   7. Disclaimer of Warranty.", maxsplit=1)[1]

    assert "Licensor provides the Work (and each" in disclaimer
    assert "Contributor provides its Contributions)" in disclaimer


def test_license_copyright_grant_preserves_source_object_form_distribution_clause():
    """Section 2 closing clause authorizes Source/Object distribution — common truncation point."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    copyright_grant = license_text.split("   3. Grant of Patent License.", maxsplit=1)[0]
    copyright_grant = copyright_grant.split("   2. Grant of Copyright License.", maxsplit=1)[1]

    assert "Work and such Derivative Works in Source or Object form." in copyright_grant


def test_license_definition_references_sections_one_through_nine():
    """Section 1 License definition anchors the document — truncation drops scope reference."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"License" shall mean the terms and conditions for use, reproduction,' in definitions
    assert "as defined by Sections 1 through 9 of this document." in definitions


def test_license_work_definition_includes_authorship_and_notice_clause():
    """Work definition body scopes authorship and copyright notice — header-only checks miss truncation."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "work of authorship, whether in Source or" in definitions
    assert "copyright notice that is included in or attached to the work" in definitions
    assert "(an example is provided in the Appendix below)." in definitions


def test_license_contributor_definition_includes_incorporation_clause():
    """Contributor definition body determines who counts as a Contributor for sections 2–5."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert '"Contributor" shall mean Licensor and any individual or Legal Entity' in definitions
    assert "on behalf of whom a Contribution has been received by the Licensor and" in definitions
    assert "subsequently incorporated within the Work." in definitions


def test_license_derivative_works_definition_includes_modification_criteria():
    """Positive Derivative Works criteria must stay intact — exclusion-only tests miss truncation."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "editorial revisions, annotations, elaborations, or other modifications" in definitions
    assert "represent, as a whole, an original work of authorship." in definitions


def test_license_contribution_definition_includes_intentional_submission_clause():
    """Intentional-submission wording binds inbound contributions — channels alone are insufficient."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "that is intentionally" in definitions
    assert "submitted to the Licensor for inclusion in the Work by the copyright owner" in definitions
    assert 'designated in writing by the copyright owner as "Not a Contribution."' in definitions


def test_license_object_form_definition_includes_transformation_examples():
    """Object form examples are referenced in redistribution clauses — dropping them narrows scope."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "generated documentation" in definitions
    assert "conversions to other media types" in definitions


def test_license_grant_sections_open_with_subject_to_license():
    """Sections 2–3 grants must preserve 'Subject to the terms' preamble — common edit point."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    copyright_grant = license_text.split("   3. Grant of Patent License.", maxsplit=1)[0]
    copyright_grant = copyright_grant.split("   2. Grant of Copyright License.", maxsplit=1)[1]
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    assert copyright_grant.startswith(" Subject to the terms and conditions of")
    assert patent_grant.startswith(" Subject to the terms and conditions of")


def test_license_submission_of_contributions_preserves_intentional_submission_wording():
    """Section 5 must preserve intentional-submission phrasing that binds inbound contributions."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    submission = license_text.split("   6. Trademarks.", maxsplit=1)[0]
    submission = submission.split("   5. Submission of Contributions.", maxsplit=1)[1]

    assert "any Contribution intentionally submitted for inclusion in the Work" in submission
    assert "by You to the Licensor shall be under the terms and conditions of" in submission


def test_contributing_questions_section_uses_exact_wording():
    """Questions section must stay a single canonical line — partial matches hide contact drift."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    questions = contributing.split("## Questions?", maxsplit=1)[1].strip()

    assert questions == "Open a Discussion on this repository or reach out at dev@monstergaming.ai."


def test_pull_request_template_review_sections_are_empty_placeholders():
    """Review sections must stay blank — pre-filled boilerplate hides incomplete PR descriptions."""
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")

    what_section = template.split("## How to test", maxsplit=1)[0]
    what_section = what_section.split("## What does this PR do?", maxsplit=1)[1]
    how_section = template.split("## Checklist", maxsplit=1)[0]
    how_section = how_section.split("## How to test", maxsplit=1)[1]

    assert what_section.strip() == ""
    assert how_section.strip() == ""


def test_contributing_test_requirement_aligns_with_validate_workflow():
    """Quick Start step 4 must match an executable CI gate — wording-only checks miss missing workflows."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    workflow_path = REPO_ROOT / ".github" / "workflows" / "validate.yml"

    assert "Ensure tests pass" in contributing
    assert workflow_path.is_file(), "validate.yml must exist to gate the tests CONTRIBUTING requires"
    assert "pytest" in workflow_path.read_text(encoding="utf-8")


def test_pull_request_spdx_checklist_aligns_with_contributing_guidelines():
    """PR and CONTRIBUTING SPDX requirements must stay paired — drift leaves contributors unsure."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")

    assert "Apache-2.0 SPDX header" in contributing
    assert "SPDX headers present on new files" in template


CANONICAL_APACHE_NOTICE_BLOCK = (
    "\n\n   Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming\n\n"
    '   Licensed under the Apache License, Version 2.0 (the "License");\n'
    "   you may not use this file except in compliance with the License.\n"
    "   You may obtain a copy of the License at\n\n"
    "       http://www.apache.org/licenses/LICENSE-2.0\n\n"
    "   Unless required by applicable law or agreed to in writing, software\n"
    '   distributed under the License is distributed on an "AS IS" BASIS,\n'
    "   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
    "   See the License for the specific language governing permissions and\n"
    "   limitations under the License.\n"
)

CANONICAL_PR_CHECKLIST_ITEMS = (
    "- [ ] Tests pass locally",
    "- [ ] Documentation updated (if applicable)",
    "- [ ] SPDX headers present on new files",
)


def test_license_notice_block_matches_canonical_apache_text():
    """Fragment checks miss dropped URL lines or swapped http/https in the notice block."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    notice_block = license_text.split("END OF TERMS AND CONDITIONS", maxsplit=1)[1]

    assert notice_block == CANONICAL_APACHE_NOTICE_BLOCK


def test_license_copyright_holder_aligns_with_profile_luxedeum_attribution():
    """Copyright holder and public org footer must stay paired across legal and marketing surfaces."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    profile_text = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")

    assert "Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming" in license_text
    assert "A [Luxedeum](https://luxedeum.com) company." in profile_text
    assert "Luxedeum" in license_text and "Luxedeum" in profile_text
    assert "Monster Gaming" in license_text and "Monster Gaming" in profile_text


def test_pull_request_template_checklist_matches_canonical_order():
    """Per-item wording checks miss reordering that changes contributor review expectations."""
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    checklist_items = [line for line in template.splitlines() if line.startswith("- [ ]")]

    assert checklist_items == list(CANONICAL_PR_CHECKLIST_ITEMS)


def test_pull_request_tests_checklist_aligns_with_contributing_and_workflow():
    """Quick Start, PR template, and CI must stay a three-way test gate — partial drift hides regressions."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")

    quick_start = contributing.split("## Quick Start", maxsplit=1)[1]
    quick_start = quick_start.split("## Guidelines", maxsplit=1)[0]
    steps = [line for line in quick_start.splitlines() if line.strip()[:1].isdigit()]

    assert steps[3] == "4. Ensure tests pass"
    assert steps[4] == "5. Submit a pull request"
    assert "- [ ] Tests pass locally" in template
    assert "pytest -q" in workflow


def test_contributing_contact_email_stays_out_of_profile_readme():
    """Support email belongs in CONTRIBUTING only — accidental profile exposure is a privacy regression."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    profile_text = (REPO_ROOT / "profile" / "README.md").read_text(encoding="utf-8")

    assert "dev@monstergaming.ai" in contributing
    assert "dev@monstergaming.ai" not in profile_text


EXPECTED_COMMUNITY_HEALTH_PATHS = (
    "LICENSE",
    "CONTRIBUTING.md",
    "profile/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/workflows/validate.yml",
    "requirements-dev.txt",
    ".gitignore",
    "tests",
)


def test_community_health_files_exist_at_expected_paths():
    """LUX-1271 health files must remain present — content tests fail opaquely when a file is deleted."""
    for rel_path in EXPECTED_COMMUNITY_HEALTH_PATHS:
        path = REPO_ROOT / rel_path
        if rel_path == "tests":
            assert path.is_dir(), f"missing validation suite directory: {rel_path}"
        else:
            assert path.is_file(), f"missing community health file: {rel_path}"


EXPECTED_REPO_ROOT_ENTRIES = frozenset(
    {
        ".github",
        ".gitignore",
        "CONTRIBUTING.md",
        "LICENSE",
        "profile",
        "requirements-dev.txt",
        "tests",
    }
)

ALLOWED_TRANSIENT_ROOT_ENTRIES = frozenset({".pytest_cache", "__pycache__"})


def test_repo_root_contains_only_expected_top_level_entries():
    """Stray root files (README.md, package.json) do not update the org profile and confuse CI."""
    present = {path.name for path in REPO_ROOT.iterdir() if path.name != ".git"}
    missing = EXPECTED_REPO_ROOT_ENTRIES - present
    unexpected = present - EXPECTED_REPO_ROOT_ENTRIES - ALLOWED_TRANSIENT_ROOT_ENTRIES

    assert not missing, f"missing expected root entries: {sorted(missing)}"
    assert not unexpected, f"unexpected root entries: {sorted(unexpected)}"


COMMUNITY_HEALTH_TEXT_PATHS = (
    "LICENSE",
    "CONTRIBUTING.md",
    "profile/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/workflows/validate.yml",
    "requirements-dev.txt",
    ".gitignore",
)


@pytest.mark.parametrize("rel_path", COMMUNITY_HEALTH_TEXT_PATHS)
def test_community_health_text_files_use_lf_line_endings(rel_path):
    """CRLF line endings break YAML issue forms and markdown rendering on GitHub."""
    raw = (REPO_ROOT / rel_path).read_bytes()
    assert b"\r\n" not in raw, f"{rel_path} must use LF line endings, not CRLF"


@pytest.mark.parametrize("rel_path", COMMUNITY_HEALTH_TEXT_PATHS)
def test_community_health_text_files_have_no_utf8_bom(rel_path):
    """UTF-8 BOM breaks YAML issue-form parsing and can hide content drift in editors."""
    raw = (REPO_ROOT / rel_path).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"{rel_path} must not start with a UTF-8 BOM"


@pytest.mark.parametrize("rel_path", COMMUNITY_HEALTH_TEXT_PATHS)
def test_community_health_text_files_have_no_trailing_whitespace(rel_path):
    """Trailing whitespace on intro or template lines slips past substring-based guards."""
    text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        assert line == line.rstrip(), (
            f"{rel_path} line {line_number} has trailing whitespace: {line!r}"
        )


def test_license_legal_entity_includes_common_control_definition():
    """Section 1 affiliate scope — middle definition lines were uncaught by single-line deletes."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert (
        "other entities that control, are controlled by, or are under common"
        in definitions
    )
    assert "control with that entity. For the purposes of this definition," in definitions


def test_license_object_form_includes_made_available_clause():
    """Section 1 Object form clause anchors redistribution media definitions."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert "Object form, made available under the License, as indicated by a" in definitions


def test_license_patent_grant_preserves_contribution_combination_and_litigation_trigger():
    """Section 3 combination/litigation sentences — deleting one line left grant terms intact."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    assert "with the Work to which such Contribution(s) was submitted. If You" in patent_grant
    assert (
        "or a Contribution incorporated within the Work constitutes direct"
        in patent_grant
    )


def test_license_redistribution_condition_d_preserves_derivative_notice_placement():
    """Section 4(d) NOTICE placement — per-marker tests missed mid-clause line deletes."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = _license_redistribution_section()

    assert "then any Derivative Works that You distribute must" in redistribution
    assert (
        "within such NOTICE file, excluding any notices that do not"
        in redistribution
    )
    assert "pertain to any part of the Derivative Works, in at least one" in redistribution


def test_license_limitation_preserves_gross_negligence_exception():
    """Section 8 liability cap carve-out — boilerplate deletes were previously uncaught."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    liability = license_text.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[0]
    liability = liability.split("   8. Limitation of Liability.", maxsplit=1)[1]

    assert "unless required by applicable law (such as deliberate and grossly" in liability
    assert "negligent acts) or agreed to in writing, shall any Contributor be" in liability
    assert "other commercial damages or losses), even if such Contributor" in liability


def test_license_accepting_liability_preserves_sole_responsibility_clause():
    """Section 9 indemnity scope — accepting obligations must stay contributor-scoped."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    accepting = license_text.split("   END OF TERMS AND CONDITIONS", maxsplit=1)[0]
    accepting = accepting.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[1]

    assert (
        "or other liability obligations and/or rights consistent with this"
        in accepting
    )
    assert "License. However, in accepting such obligations, You may act only" in accepting


def test_license_legal_entity_preserves_direction_and_management_criterion():
    """Section 1 control definition — contract/management criterion was uncaught by share-ownership checks."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert (
        "direction or management of such entity, whether by contract or"
        in definitions
    )


def test_license_object_form_preserves_mechanical_transformation_scope():
    """Section 1 Object form — translation scope line deletes were uncaught by made-available anchors."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert (
        "transformation or translation of a Source form, including but"
        in definitions
    )


def test_license_derivative_works_preserves_authorship_and_link_exclusion():
    """Section 1 Derivative Works — mid-definition deletes left separable-work guards intact."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert (
        "form, that is based on (or derived from) the Work and for which the"
        in definitions
    )
    assert "the Work and Derivative Works thereof." in definitions


def test_license_contribution_definition_preserves_intentional_submission_scope():
    """Section 1 Contribution/submitted — channel definition middle lines were uncaught."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    definitions = license_text.split("   2. Grant of Copyright License.", maxsplit=1)[0]

    assert (
        "the original version of the Work and any modifications or additions"
        in definitions
    )
    assert (
        "or by an individual or Legal Entity authorized to submit on behalf of"
        in definitions
    )
    assert (
        'the copyright owner. For the purposes of this definition, "submitted"'
        in definitions
    )
    assert (
        "to the Licensor or its representatives, including but not limited to"
        in definitions
    )
    assert (
        "Licensor for the purpose of discussing and improving the Work, but"
        in definitions
    )


def test_license_patent_grant_preserves_perpetual_worldwide_preamble():
    """Section 3 opening grant terms duplicate section 2 — patent-specific termination depends on this block."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    patent_grant = license_text.split("   4. Redistribution.", maxsplit=1)[0]
    patent_grant = patent_grant.split("   3. Grant of Patent License.", maxsplit=1)[1]

    assert (
        "this License, each Contributor hereby grants to You a perpetual,"
        in patent_grant
    )
    assert (
        "worldwide, non-exclusive, no-charge, royalty-free, irrevocable"
        in patent_grant
    )


CANONICAL_CONTRIBUTING = """\
# Contributing to Monster Gaming

We welcome contributions! Here's how to get started.

## Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Ensure tests pass
5. Submit a pull request

## Guidelines

- All new source files must include the Apache-2.0 SPDX header
- Follow existing code style and conventions
- Write tests for new functionality
- Keep PRs focused — one feature or fix per PR

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

## Questions?

Open a Discussion on this repository or reach out at dev@monstergaming.ai.
"""

CANONICAL_PR_TEMPLATE = """\
## What does this PR do?

## How to test

## Checklist
- [ ] Tests pass locally
- [ ] Documentation updated (if applicable)
- [ ] SPDX headers present on new files
"""



CANONICAL_LICENSE = """\
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to the Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by the Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding any notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


def test_license_matches_canonical_document():
    """Full-document guard for Apache-2.0 terms — substring anchors miss multi-line or whitespace drift."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    assert license_text == CANONICAL_LICENSE


def test_contributing_matches_canonical_document():
    """Backstop for fork workflow, test gate, and support contact — substring tests miss holistic drift."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert contributing == CANONICAL_CONTRIBUTING


def test_pull_request_template_matches_canonical_document():
    """Backstop for PR review sections and checklist — reordering sections is easy to miss piecemeal."""
    template = (REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    assert template == CANONICAL_PR_TEMPLATE
