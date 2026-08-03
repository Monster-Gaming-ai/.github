"""Regression guards for profile refresh commit 4618966 (145 agents, Loki Code, newsletter)."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_README = REPO_ROOT / "profile" / "README.md"

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
