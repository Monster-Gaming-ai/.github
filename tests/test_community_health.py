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
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    redistribution = license_text.split("   5. Submission of Contributions.", maxsplit=1)[0]
    redistribution = redistribution.split("   4. Redistribution.", maxsplit=1)[1]

    for condition in (
        "give any other recipients of the Work or",
        "cause any modified files to carry prominent notices",
        "retain, in the Source form of any Derivative Works",
        'If the Work includes a "NOTICE" text file',
    ):
        assert condition in redistribution, f"missing Apache-2.0 redistribution condition: {condition!r}"


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


def test_license_limitation_of_liability_preserves_damage_exclusions():
    """Section 8 caps contributor liability — missing clauses weaken downstream protections."""
    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    liability = license_text.split("   9. Accepting Warranty or Additional Liability.", maxsplit=1)[0]
    liability = liability.split("   8. Limitation of Liability.", maxsplit=1)[1]

    for phrase in (
        "In no event and under no legal theory",
        "direct, indirect, special",
        "incidental, or consequential damages",
        "loss of goodwill",
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
