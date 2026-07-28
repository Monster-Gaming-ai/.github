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

PRODUCT_OFFERINGS = (
    "[Monster-GPT]",
    "[OpenAI-compatible API]",
    "[Engine-aware code generation]",
    "[Loki Code]",
)

SUPPORTED_ENGINES = (
    "Unreal Engine",
    "Unity",
    "Godot",
    "bespoke engines",
)

SDK_REGISTRY_URLS = (
    "https://www.npmjs.com/package/@monstergaming/sdk",
    "https://pypi.org/project/monstergaming/",
    "https://crates.io/crates/monstergaming",
)

LOKI_CODE_TECHNICAL_CLAIMS = (
    "built in C11",
    "8.1 MB",
)

AGENT_ROUTING_INTRO_CLAIMS = (
    "shader",
    "animation",
    "netcode",
    "level design",
    "QA",
)

MONSTER_GPT_CLAIMS = (
    "30+ game dev disciplines",
)

LOKI_CODE_BLOG_URL = (
    "https://blog.monstergaming.ai/we-built-our-own-ai-coding-cli-in-c-because-ours-got-revoked/"
)

NEWSLETTER_URL = "https://blog.monstergaming.ai/newsletter/"


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


def test_profile_readme_has_platform_tagline(profile_text):
    assert "**AI-powered game development platform.**" in profile_text


def test_profile_readme_lists_all_product_offerings(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    for offering in PRODUCT_OFFERINGS:
        assert offering in offerings_section, f"missing product offering: {offering}"


def test_profile_readme_documents_supported_engines(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    for engine in SUPPORTED_ENGINES:
        assert engine in intro, f"missing engine support mention: {engine}"


@pytest.mark.parametrize("registry_url", SDK_REGISTRY_URLS)
def test_profile_readme_links_sdk_package_registries(profile_text, registry_url):
    assert registry_url in profile_text


def test_profile_readme_preserves_loki_code_technical_claims(profile_text):
    loki_line = next(
        (line for line in profile_text.splitlines() if "[Loki Code]" in line),
        None,
    )
    assert loki_line is not None, "Loki Code product line must remain in profile"

    for claim in LOKI_CODE_TECHNICAL_CLAIMS:
        assert claim in loki_line, f"missing Loki Code technical claim: {claim}"


def test_profile_readme_documents_agent_routing_capabilities(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    for claim in AGENT_ROUTING_INTRO_CLAIMS:
        assert claim in intro, f"missing agent routing claim in intro: {claim}"

    for claim in MONSTER_GPT_CLAIMS:
        assert claim in offerings, f"missing Monster-GPT routing claim: {claim}"


def test_profile_readme_mentions_free_tier_pricing(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    assert "free tier available" in links_section


def test_profile_readme_has_org_title(profile_text):
    assert profile_text.startswith("# Monster Gaming\n")


def test_profile_readme_links_loki_code_blog_post(profile_text):
    loki_line = next(
        (line for line in profile_text.splitlines() if "[Loki Code]" in line),
        None,
    )
    assert loki_line is not None
    assert LOKI_CODE_BLOG_URL in loki_line


def test_profile_readme_links_newsletter(profile_text):
    assert NEWSLETTER_URL in profile_text


def test_profile_readme_links_unreal_engine_to_website(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    assert "[Unreal Engine](https://monstergaming.ai)" in intro


def test_profile_readme_includes_luxedeum_attribution(profile_text):
    footer = profile_text.split("## Links", maxsplit=1)[1]
    assert "A [Luxedeum](https://luxedeum.com) company." in footer


def test_profile_readme_sdk_table_has_valid_markdown_structure(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert "| Language | Package | Install |" in sdk_section
    assert "|----------|---------|---------|" in sdk_section
    assert sdk_section.count("|") >= 16, "SDK table should have header plus three language rows"
