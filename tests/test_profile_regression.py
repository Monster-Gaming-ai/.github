"""Regression guards for profile refresh commit 4618966 (145 agents, Loki Code, newsletter)."""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_README = REPO_ROOT / "profile" / "README.md"
NEWSLETTER_URL = "https://blog.monstergaming.ai/newsletter/"
LOKI_CODE_BLOG_URL = (
    "https://blog.monstergaming.ai/we-built-our-own-ai-coding-cli-in-c-because-ours-got-revoked/"
)
LOKI_SPECS_COMMA_FORMAT = "built in C11, 195 tests, 8.1 MB"

PRE_REFRESH_AGENT_ROUTING = "auto-routes your query to one of 30+ specialist agents"
PRE_REFRESH_INTRO_CAPABILITY_SENTENCE = (
    "Code generation, debugging, optimization, and asset pipelines — purpose-built for"
)
PRE_REFRESH_MONSTER_GPT_PARENTHETICAL = (
    "(shader, animation, netcode, level design, QA, and more)"
)
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


@pytest.mark.parametrize(
    "legacy_capability",
    ("Code generation", "debugging", "optimization", "asset pipelines"),
)
def test_profile_refresh_legacy_capability_terms_not_in_intro(profile_text, legacy_capability):
    """Partial reverts often reintroduce individual pre-refresh capability phrases."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert legacy_capability not in intro


def test_profile_refresh_intro_uses_plural_queries(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "We route your queries through" in intro
    assert "We route your query through" not in intro


def test_profile_refresh_newsletter_dispatch_stays_in_links_section(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]

    dispatch_copy = "weekly dispatch from the engineering floor"
    assert dispatch_copy not in intro
    assert dispatch_copy not in offerings
    assert dispatch_copy in links_section


def test_profile_refresh_loki_blog_url_stays_in_offerings_not_links(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "because-ours-got-revoked" in offerings
    assert "because-ours-got-revoked" not in links_section


def test_profile_refresh_intro_keeps_routing_copy_out_of_sdk_section(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    routing_copy = "shader, animation, netcode, level design, QA"
    assert routing_copy in intro
    assert routing_copy not in sdk_section


def test_profile_refresh_intro_connects_routing_to_engine_support(profile_text):
    """4618966 ties agent routing to engine support in one intro sentence."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "and more — purpose-built for" in intro
    assert "We route your queries through 145+ specialist agents —" in intro


def test_profile_refresh_product_offerings_use_em_dash_separator(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    offering_lines = [
        line for line in offerings.splitlines() if line.startswith("- **[")
    ]
    assert len(offering_lines) == 4

    for line in offering_lines:
        assert " — " in line, f"offering must separate link from description with em dash: {line}"


def test_profile_refresh_monster_gpt_drops_parenthetical_agent_examples(profile_text):
    """4618966 moved agent examples from Monster-GPT line into the intro paragraph."""
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    monster_gpt_line = next(
        line for line in offerings.splitlines() if line.startswith("- **[Monster-GPT]")
    )

    assert PRE_REFRESH_MONSTER_GPT_PARENTHETICAL not in monster_gpt_line
    assert PRE_REFRESH_MONSTER_GPT_PARENTHETICAL not in profile_text


def test_profile_refresh_monster_gpt_avoids_full_pre_refresh_routing_line(profile_text):
    """Partial reverts sometimes restore the old Monster-GPT routing sentence."""
    full_legacy_line = (
        "flagship model that auto-routes your query to one of 30+ specialist agents "
        f"{PRE_REFRESH_MONSTER_GPT_PARENTHETICAL}"
    )

    assert full_legacy_line not in profile_text


def test_profile_refresh_engine_aware_offering_uses_writes_verb(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    codegen_line = next(
        line for line in offerings.splitlines() if "[Engine-aware code generation]" in line
    )

    assert "writes gameplay systems, shaders, networking, and UI that actually compile" in codegen_line


def test_profile_refresh_loki_code_uses_our_open_source_phrasing(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    loki_line = next(line for line in offerings.splitlines() if "[Loki Code]" in line)

    assert "our open-source AI coding CLI" in loki_line


def test_profile_refresh_monster_gpt_name_stays_out_of_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "Monster-GPT" not in intro


def test_profile_refresh_monster_gpt_does_not_link_to_blog_or_quickstart(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    monster_gpt_line = next(
        line for line in offerings.splitlines() if line.startswith("- **[Monster-GPT]")
    )

    assert "blog.monstergaming.ai" not in monster_gpt_line
    assert "quickstart" not in monster_gpt_line
    assert "[Monster-GPT](https://monstergaming.ai)" in monster_gpt_line


def test_profile_refresh_loki_specs_maintain_canonical_order(profile_text):
    """4618966 lists Loki technical claims as C11, test count, then binary size."""
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    c11_idx = loki_line.index("built in C11")
    tests_idx = loki_line.index("195 tests")
    size_idx = loki_line.index("8.1 MB")

    assert c11_idx < tests_idx < size_idx


def test_profile_refresh_disciplines_count_uses_plus_suffix(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "30+ game dev disciplines" in offerings
    assert re.search(r"\b30 game dev disciplines\b", offerings) is None


def test_profile_refresh_newsletter_url_preserves_trailing_slash(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert f"]({NEWSLETTER_URL})" in links_section
    assert "](https://blog.monstergaming.ai/newsletter)" not in links_section


def test_profile_refresh_loki_blog_slug_preserves_full_engineering_path(profile_text):
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    assert "we-built-our-own-ai-coding-cli-in-c-because-ours-got-revoked" in loki_line


def test_profile_refresh_newsletter_line_uses_em_dash_before_dispatch(profile_text):
    """4618966 mirrors pricing-line formatting: em dash before the newsletter tagline."""
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    newsletter_line = next(
        line for line in links_section.splitlines() if line.startswith("- **Newsletter:**")
    )
    assert "— weekly dispatch from the engineering floor" in newsletter_line


def test_profile_refresh_loki_blog_url_preserves_trailing_slash(profile_text):
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    assert f"]({LOKI_CODE_BLOG_URL})" in loki_line
    assert "because-ours-got-revoked)" not in loki_line


def test_profile_refresh_loki_specs_use_comma_separated_format(profile_text):
    """Partial reverts sometimes reorder or drop individual Loki technical claims."""
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    assert LOKI_SPECS_COMMA_FORMAT in loki_line


def test_profile_refresh_intro_avoids_parenthetical_agent_examples(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert PRE_REFRESH_MONSTER_GPT_PARENTHETICAL not in intro
    assert re.search(r"\(shader", intro) is None


def test_profile_refresh_monster_gpt_avoids_your_query_phrasing(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    monster_gpt_line = next(
        line for line in offerings.splitlines() if line.startswith("- **[Monster-GPT]")
    )

    assert "your query" not in monster_gpt_line.lower()


def test_profile_refresh_intro_avoids_full_pre_refresh_capability_sentence(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert PRE_REFRESH_INTRO_CAPABILITY_SENTENCE not in intro


def test_profile_refresh_specialist_agents_across_stays_in_offerings(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    phrase = "specialist agents across"
    assert phrase not in intro
    assert phrase in offerings


def test_profile_refresh_intro_routing_copy_stays_out_of_offerings(profile_text):
    """4618966 moved agent routing narrative into the intro paragraph only."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "We route your queries through" in intro
    assert "We route your queries through" not in offerings


def test_profile_refresh_agent_count_stays_out_of_links_section(profile_text):
    """145+ agents and 30+ disciplines must not leak into the Links section."""
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "145+ specialist agents" not in links_section
    assert "30+ game dev disciplines" not in links_section
