"""Validate GitHub issue form templates added in LUX-1271."""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ISSUE_TEMPLATE_DIR = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"

TEMPLATE_FILES = {
    "bug_report.yml": {
        "labels": ["bug"],
        "required_field_ids": {"description", "reproduction"},
    },
    "feature_request.yml": {
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

    assert isinstance(template.get("name"), str) and template["name"].strip()
    assert isinstance(template.get("description"), str) and template["description"].strip()
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
