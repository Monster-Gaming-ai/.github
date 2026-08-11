"""Regression guards for profile refresh commit 4618966 (145 agents, Loki Code, newsletter)."""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_README = REPO_ROOT / "profile" / "README.md"
NEWSLETTER_URL = "https://blog.monstergaming.ai/newsletter/"

PRE_REFRESH_AGENT_ROUTING = "auto-routes your query to one of 30+ specialist agents"
PRE_REFRESH_ASSET_PIPELINES = "Code generation, debugging, optimization, and asset pipelines"


@pytest.fixture(scope="module")
def profile_text() -> str:
    return PROFILE_README.read_text(encoding="utf-8")


def test_profile_refresh_agent_count_is_145_not_30_in_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "145+ specialist agents" in intro
    assert "30+ specialist agents" not in intro


def test_profile_refresh_dropped_asset_pipeline_bullet(profile_text):
    assert PRE_REFRESH_ASSET_PIPELINES not in profile_text


def test_profile_refresh_replaced_monster_gpt_routing_copy(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert PRE_REFRESH_AGENT_ROUTING not in profile_text
    assert "auto-routes to specialist agents across 30+ game dev disciplines" in offerings


def test_profile_refresh_newsletter_is_fifth_link(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]
    link_lines = [line for line in links_section.splitlines() if line.startswith("- **")]

    assert link_lines[-1].startswith("- **Newsletter:**")
    assert "Man in the Machine" in link_lines[-1]


def test_profile_refresh_agent_counts_are_not_swapped_between_sections(profile_text):
    """145+ agents belong in intro; 30+ disciplines belong in Monster-GPT offering."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "145+ specialist agents" in intro
    assert "145+ specialist agents" not in offerings
    assert "30+ game dev disciplines" in offerings
    assert "30+ game dev disciplines" not in intro


def test_profile_refresh_intro_avoids_legacy_singular_auto_route_copy(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "We route your queries through" in intro
    assert "We auto-route" not in intro
    assert "auto-route your query" not in intro


def test_profile_refresh_loki_code_stays_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "[Loki Code]" not in intro
    assert "open-source AI coding CLI" not in intro


def test_profile_refresh_newsletter_url_stays_in_links_section(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]

    assert NEWSLETTER_URL not in intro
    assert NEWSLETTER_URL not in offerings
    assert NEWSLETTER_URL in links_section


def test_profile_refresh_monster_gpt_line_has_no_agent_routing_examples(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    monster_gpt_line = next(
        line for line in offerings.splitlines() if line.startswith("- **[Monster-GPT]")
    )

    for example in ("shader", "animation", "netcode", "level design"):
        assert example not in monster_gpt_line.lower()


def test_profile_refresh_agent_count_uses_plus_suffix(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "145+ specialist agents" in intro
    assert re.search(r"\b145 specialist agents\b", intro) is None


def test_profile_refresh_compile_claim_stays_in_engine_aware_offering(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    codegen_line = next(
        line for line in offerings.splitlines() if "[Engine-aware code generation]" in line
    )

    assert "that actually compile" in codegen_line
    assert "that actually compile" not in intro
