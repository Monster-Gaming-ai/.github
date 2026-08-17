"""Validate GitHub issue form templates added in LUX-1271."""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ISSUE_TEMPLATE_DIR = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"

TEMPLATE_FILES = {
    "bug_report.yml": {
        "name": "Bug Report",
        "description": "Report a bug in this SDK",
        "labels": ["bug"],
        "required_field_ids": {"description", "reproduction"},
    },
    "feature_request.yml": {
        "name": "Feature Request",
        "description": "Suggest a new feature or improvement",
        "labels": ["enhancement"],
        "required_field_ids": {"problem", "solution"},
    },
}


def _load_template(filename: str) -> dict:
    path = ISSUE_TEMPLATE_DIR / filename
    assert path.is_file(), f"missing issue template: {path}"
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@pytest.mark.parametrize("filename,expectations", TEMPLATE_FILES.items())
def test_issue_template_is_valid_github_form(filename, expectations):
    template = _load_template(filename)

    assert template.get("name") == expectations["name"]
    assert template.get("description") == expectations["description"]
    assert template.get("labels") == expectations["labels"]

    body = template.get("body")
    assert isinstance(body, list) and body, "issue form body must be a non-empty list"

    field_ids = set()
    for field in body:
        assert isinstance(field, dict)
        assert field.get("type") in {
            "textarea",
            "input",
            "dropdown",
            "checkboxes",
            "markdown",
        }
        field_id = field.get("id")
        assert isinstance(field_id, str) and field_id.strip()
        field_ids.add(field_id)

        attributes = field.get("attributes")
        assert isinstance(attributes, dict)
        assert isinstance(attributes.get("label"), str) and attributes["label"].strip()

    missing_required = expectations["required_field_ids"] - field_ids
    assert not missing_required, f"missing required fields: {sorted(missing_required)}"


@pytest.mark.parametrize("filename,expectations", TEMPLATE_FILES.items())
def test_issue_template_marks_critical_fields_required(filename, expectations):
    template = _load_template(filename)
    required_ids = expectations["required_field_ids"]

    validated_ids = {
        field["id"]
        for field in template["body"]
        if field.get("validations", {}).get("required") is True
    }

    missing = required_ids - validated_ids
    assert not missing, f"fields must be marked required: {sorted(missing)}"


def test_bug_report_template_targets_reproduction_workflow():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    assert "version" in fields_by_id
    assert "environment" in fields_by_id
    assert fields_by_id["version"]["type"] == "input"
    assert fields_by_id["environment"]["type"] == "input"


@pytest.mark.parametrize("filename", TEMPLATE_FILES.keys())
def test_issue_template_field_ids_are_unique(filename):
    template = _load_template(filename)
    field_ids = [field["id"] for field in template["body"]]

    duplicates = sorted({field_id for field_id in field_ids if field_ids.count(field_id) > 1})
    assert not duplicates, f"duplicate field ids break GitHub forms: {duplicates}"


def test_issue_template_directory_has_expected_templates():
    present = {path.name for path in ISSUE_TEMPLATE_DIR.glob("*.yml")}
    assert present == set(TEMPLATE_FILES.keys())


def test_bug_report_includes_expected_behavior_field_for_triage():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    expected_field = fields_by_id["expected"]
    assert expected_field["type"] == "textarea"
    assert expected_field.get("validations", {}).get("required") is not True


def test_feature_request_includes_alternatives_field():
    template = _load_template("feature_request.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    alternatives = fields_by_id["alternatives"]
    assert alternatives["type"] == "textarea"
    assert alternatives.get("validations", {}).get("required") is not True


@pytest.mark.parametrize(
    "filename,field_id,placeholder_fragment",
    [
        ("bug_report.yml", "version", "0.0.5"),
        ("bug_report.yml", "environment", "Python 3.12"),
    ],
)
def test_bug_report_placeholders_guide_reporters(filename, field_id, placeholder_fragment):
    template = _load_template(filename)
    fields_by_id = {field["id"]: field for field in template["body"]}

    placeholder = fields_by_id[field_id]["attributes"].get("placeholder", "")
    assert placeholder_fragment in placeholder


def test_bug_report_required_fields_include_reporter_guidance():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    description = fields_by_id["description"]["attributes"]
    reproduction = fields_by_id["reproduction"]["attributes"]

    assert "bug" in description["description"].lower()
    assert "reproduce" in reproduction["description"].lower()


def test_feature_request_problem_field_targets_user_need():
    template = _load_template("feature_request.yml")
    problem = next(field for field in template["body"] if field["id"] == "problem")

    assert "problem" in problem["attributes"]["label"].lower()
    assert "problem" in problem["attributes"]["description"].lower()


def test_feature_request_solution_field_is_required_with_guidance():
    template = _load_template("feature_request.yml")
    solution = next(field for field in template["body"] if field["id"] == "solution")

    assert solution.get("validations", {}).get("required") is True
    assert "solution" in solution["attributes"]["label"].lower()
    assert "work" in solution["attributes"]["description"].lower()


def test_bug_report_fields_follow_triage_order():
    template = _load_template("bug_report.yml")
    field_ids = [field["id"] for field in template["body"]]

    assert field_ids == ["description", "reproduction", "expected", "version", "environment"]


def test_feature_request_fields_follow_problem_solution_order():
    template = _load_template("feature_request.yml")
    field_ids = [field["id"] for field in template["body"]]

    problem_idx = field_ids.index("problem")
    solution_idx = field_ids.index("solution")
    alternatives_idx = field_ids.index("alternatives")

    assert problem_idx < solution_idx
    assert solution_idx < alternatives_idx


def test_bug_report_template_has_exactly_five_fields():
    template = _load_template("bug_report.yml")
    assert len(template["body"]) == 5


def test_feature_request_template_has_exactly_three_fields():
    template = _load_template("feature_request.yml")
    assert len(template["body"]) == 3


def test_bug_report_expected_field_guides_triage_without_blocking_submit():
    template = _load_template("bug_report.yml")
    expected = next(field for field in template["body"] if field["id"] == "expected")

    assert expected["type"] == "textarea"
    assert "expect" in expected["attributes"]["description"].lower()
    assert expected.get("validations", {}).get("required") is not True


def test_feature_request_alternatives_field_guides_contributors():
    template = _load_template("feature_request.yml")
    alternatives = next(field for field in template["body"] if field["id"] == "alternatives")

    assert alternatives["type"] == "textarea"
    assert "alternative" in alternatives["attributes"]["label"].lower()
    assert "approach" in alternatives["attributes"]["description"].lower()
    assert alternatives.get("validations", {}).get("required") is not True


def test_bug_report_metadata_fields_are_optional():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    for field_id in ("expected", "version", "environment"):
        field = fields_by_id[field_id]
        assert field.get("validations", {}).get("required") is not True


def test_bug_report_template_scopes_issues_to_sdk():
    template = _load_template("bug_report.yml")

    assert "SDK" in template["description"]


def test_bug_report_environment_placeholder_covers_all_official_sdks():
    template = _load_template("bug_report.yml")
    environment = next(field for field in template["body"] if field["id"] == "environment")
    placeholder = environment["attributes"].get("placeholder", "")

    for runtime_hint in ("Node 22", "Python 3.12", "Rust 1.95"):
        assert runtime_hint in placeholder


def test_feature_request_template_metadata():
    template = _load_template("feature_request.yml")

    assert template["name"] == "Feature Request"
    assert template["description"] == "Suggest a new feature or improvement"
    assert template["labels"] == ["enhancement"]


def test_bug_report_required_fields_are_textareas():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    for field_id in ("description", "reproduction"):
        field = fields_by_id[field_id]
        assert field["type"] == "textarea"
        assert field.get("validations", {}).get("required") is True


def test_feature_request_fields_are_all_textareas():
    template = _load_template("feature_request.yml")

    for field in template["body"]:
        assert field["type"] == "textarea", f"feature request field {field['id']} must be textarea"


def test_bug_report_version_field_labels_sdk_scope():
    template = _load_template("bug_report.yml")
    version = next(field for field in template["body"] if field["id"] == "version")

    assert version["attributes"]["label"] == "SDK Version"
    assert "placeholder" in version["attributes"]


def test_bug_report_environment_field_label():
    template = _load_template("bug_report.yml")
    environment = next(field for field in template["body"] if field["id"] == "environment")

    assert environment["attributes"]["label"] == "Environment"
    assert environment["type"] == "input"


def test_bug_report_required_field_labels_guide_reporters():
    template = _load_template("bug_report.yml")
    fields_by_id = {field["id"]: field for field in template["body"]}

    assert fields_by_id["description"]["attributes"]["label"] == "Describe the bug"
    assert fields_by_id["reproduction"]["attributes"]["label"] == "Steps to reproduce"


def test_feature_request_proposed_solution_label():
    template = _load_template("feature_request.yml")
    solution = next(field for field in template["body"] if field["id"] == "solution")

    assert solution["attributes"]["label"] == "Proposed solution"
    assert solution["attributes"]["description"] == "How would you like this to work?"
