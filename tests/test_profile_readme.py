"""Validate org profile README content from recent profile refresh commits."""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_README = REPO_ROOT / "profile" / "README.md"

REQUIRED_SECTIONS = (
    "## What We Build",
    "## Official SDKs",
    "## Links",
)

SDK_ROWS = (
    ("TypeScript / JavaScript", "@monstergaming/sdk", "npm install @monstergaming/sdk"),
    ("Python", "monstergaming", "pip install monstergaming"),
    ("Rust", "monstergaming", "cargo add monstergaming"),
)

RECENT_PROFILE_CLAIMS = (
    "145+ specialist agents",
    "[Loki Code]",
    "195 tests",
    "[Man in the Machine]",
    "newsletter/",
)

LINKED_RESOURCES = (
    "https://monstergaming.ai",
    "https://monstergaming.ai/pricing",
    "https://monstergaming.ai/quickstart",
    "https://blog.monstergaming.ai",
    "https://luxedeum.com",
)


@pytest.fixture(scope="module")
def profile_text() -> str:
    assert PROFILE_README.is_file(), "org profile README must exist"
    return PROFILE_README.read_text(encoding="utf-8")


def test_profile_readme_has_required_sections(profile_text):
    for section in REQUIRED_SECTIONS:
        assert section in profile_text, f"missing section header: {section}"


def test_profile_readme_preserves_recent_marketing_claims(profile_text):
    for claim in RECENT_PROFILE_CLAIMS:
        assert claim in profile_text, f"missing recently added profile claim: {claim}"


def test_profile_readme_documents_all_official_sdks(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    for language, package, install_command in SDK_ROWS:
        assert language in sdk_section
        assert package in sdk_section
        assert install_command in sdk_section


@pytest.mark.parametrize("url", LINKED_RESOURCES)
def test_profile_readme_includes_core_links(profile_text, url):
    assert url in profile_text


def test_profile_readme_uses_https_links_only(profile_text):
    bare_http_links = re.findall(r"(?<!\()http://[^\s)]+", profile_text)
    assert not bare_http_links, f"profile should not use insecure links: {bare_http_links}"
