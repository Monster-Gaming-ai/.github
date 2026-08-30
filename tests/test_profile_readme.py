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

PROFILE_REFRESH_CLAIMS = (
    "We route your queries through",
    "auto-routes to specialist agents",
    "drop-in replacement for OpenAI SDKs",
    "that actually compile",
    "weekly dispatch from the engineering floor",
)

PRODUCT_OFFERING_LINKS = (
    ("[Monster-GPT]", "https://monstergaming.ai"),
    ("[OpenAI-compatible API]", "https://monstergaming.ai/quickstart"),
    ("[Engine-aware code generation]", "https://monstergaming.ai"),
)

CANONICAL_OFFERING_HEADERS = (
    "[Monster-GPT]",
    "[OpenAI-compatible API]",
    "[Engine-aware code generation]",
    "[Loki Code]",
)

LINKS_SECTION_RESOURCES = (
    ("Website", "https://monstergaming.ai"),
    ("Pricing", "https://monstergaming.ai/pricing"),
    ("Quickstart", "https://monstergaming.ai/quickstart"),
    ("Blog", "https://blog.monstergaming.ai"),
    ("Newsletter", "https://blog.monstergaming.ai/newsletter/"),
)

DEPRECATED_PRE_REFRESH_COPY = (
    "Code generation, debugging, optimization, and asset pipelines",
    "auto-routes your query to one of 30+ specialist agents",
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


def test_profile_readme_preserves_agent_routing_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    for claim in PROFILE_REFRESH_CLAIMS:
        assert claim in profile_text, f"missing profile refresh claim: {claim}"

    assert "145+ specialist agents" in intro


@pytest.mark.parametrize("link_text,url", PRODUCT_OFFERING_LINKS)
def test_profile_readme_product_offerings_link_to_correct_destinations(profile_text, link_text, url):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    expected = f"{link_text}({url})"
    assert expected in offerings_section, f"missing or incorrect link for {link_text}"


@pytest.mark.parametrize("deprecated_copy", DEPRECATED_PRE_REFRESH_COPY)
def test_profile_readme_does_not_revert_to_pre_refresh_copy(profile_text, deprecated_copy):
    assert deprecated_copy not in profile_text, (
        f"profile reverted to pre-refresh copy: {deprecated_copy!r}"
    )


def test_profile_readme_newsletter_appears_in_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]

    assert "**Newsletter:** [Man in the Machine]" in links_section
    assert NEWSLETTER_URL in links_section
    assert "weekly dispatch from the engineering floor" in links_section


def test_profile_readme_monster_gpt_disciplines_claim_stays_in_offerings(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "30+ game dev disciplines" not in intro
    assert "30+ game dev disciplines" in offerings


def test_profile_readme_has_four_product_offerings(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    offering_lines = [
        line for line in offerings_section.splitlines() if line.startswith("- **[")
    ]
    assert len(offering_lines) == 4, "profile refresh added Loki Code as a fourth offering"


def test_profile_readme_loki_code_is_fourth_offering(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    offering_lines = [
        line for line in offerings_section.splitlines() if line.startswith("- **[")
    ]
    assert offering_lines[-1].startswith("- **[Loki Code]")
    assert "open-source AI coding CLI" in offering_lines[-1]


def test_profile_readme_intro_positions_platform_above_engine(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "sits above the engine" in intro
    assert "purpose-built for" in intro
    assert "Monster Gaming is an AI platform that sits above the engine" in intro


def test_profile_readme_links_section_has_all_five_resources(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    expected_labels = ("Website", "Pricing", "Quickstart", "Blog", "Newsletter")
    link_lines = [line for line in links_section.splitlines() if line.startswith("- **")]

    assert len(link_lines) == 5
    for label, line in zip(expected_labels, link_lines, strict=True):
        assert line.startswith(f"- **{label}:**")


def test_profile_readme_engine_aware_codegen_claims(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    api_line = next(
        line for line in offerings_section.splitlines() if "[OpenAI-compatible API]" in line
    )
    codegen_line = next(
        line for line in offerings_section.splitlines() if "[Engine-aware code generation]" in line
    )

    assert "game-dev-tuned models" in api_line
    assert "gameplay systems, shaders, networking, and UI" in codegen_line


def test_profile_readme_product_offerings_maintain_canonical_order(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    offering_lines = [
        line for line in offerings_section.splitlines() if line.startswith("- **[")
    ]
    headers = [line[line.index("[") : line.index("]") + 1] for line in offering_lines]

    assert headers == list(CANONICAL_OFFERING_HEADERS)


def test_profile_readme_monster_gpt_leads_with_flagship_claim(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    first_offering = next(
        line for line in offerings_section.splitlines() if line.startswith("- **[")
    )
    assert first_offering.startswith("- **[Monster-GPT]")
    assert "flagship model" in first_offering


def test_profile_readme_loki_code_line_includes_test_count(profile_text):
    loki_line = next(
        (line for line in profile_text.splitlines() if "[Loki Code]" in line),
        None,
    )
    assert loki_line is not None
    assert "195 tests" in loki_line


def test_profile_readme_specialist_examples_stay_in_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    agent_routing_phrase = "shader, animation, netcode, level design, QA"
    assert agent_routing_phrase in intro
    assert agent_routing_phrase not in offerings


@pytest.mark.parametrize("label,url", LINKS_SECTION_RESOURCES)
def test_profile_readme_links_section_pairs_labels_with_urls(profile_text, label, url):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    expected = f"- **{label}:**"
    matching_lines = [line for line in links_section.splitlines() if line.startswith(expected)]
    assert len(matching_lines) == 1, f"missing or duplicated link label: {label}"
    assert f"]({url})" in matching_lines[0], f"{label} must link to {url}"


def test_profile_readme_sdk_table_rows_use_install_code_formatting(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    data_rows = [
        line for line in sdk_section.splitlines() if line.startswith("|") and "Language" not in line and "---" not in line
    ]
    assert len(data_rows) == 3

    for row in data_rows:
        assert "`" in row, f"SDK install command should use code formatting: {row}"


def test_profile_readme_markdown_links_are_balanced(profile_text):
    open_brackets = profile_text.count("](")
    close_parens_after_links = len(re.findall(r"\]\([^)]+\)", profile_text))

    assert open_brackets == close_parens_after_links, "profile contains malformed markdown links"


SDK_TABLE_ROWS = (
    ("TypeScript / JavaScript", "@monstergaming/sdk", "https://www.npmjs.com/package/@monstergaming/sdk"),
    ("Python", "monstergaming", "https://pypi.org/project/monstergaming/"),
    ("Rust", "monstergaming", "https://crates.io/crates/monstergaming"),
)


def test_profile_readme_sdk_table_pairs_packages_with_registry_urls(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    data_rows = [
        line
        for line in sdk_section.splitlines()
        if line.startswith("|") and "Language" not in line and "---" not in line
    ]
    assert len(data_rows) == 3

    for row, (language, package, registry_url) in zip(data_rows, SDK_TABLE_ROWS, strict=True):
        assert language in row
        assert package in row
        assert registry_url in row


def test_profile_readme_sdk_table_maintains_canonical_language_order(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    data_rows = [
        line
        for line in sdk_section.splitlines()
        if line.startswith("|") and "Language" not in line and "---" not in line
    ]
    languages = [row.split("|", maxsplit=3)[1].strip() for row in data_rows]

    assert languages == [language for language, _, _ in SDK_TABLE_ROWS]


def test_profile_readme_loki_code_offering_links_to_blog_not_website(profile_text):
    offerings_section = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings_section = offerings_section.split("## Official SDKs", maxsplit=1)[0]

    loki_line = next(line for line in offerings_section.splitlines() if "[Loki Code]" in line)
    link_target = loki_line.split("[Loki Code]", maxsplit=1)[1].split(")", maxsplit=1)[0]

    assert link_target.startswith("(")
    assert LOKI_CODE_BLOG_URL in link_target
    assert "https://monstergaming.ai" not in link_target


def test_profile_readme_intro_agent_routing_ends_with_and_more(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "level design, QA, and more" in intro


def test_profile_readme_links_use_display_paths_for_nested_routes(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    display_path_links = (
        ("Website", "monstergaming.ai"),
        ("Pricing", "monstergaming.ai/pricing"),
        ("Quickstart", "monstergaming.ai/quickstart"),
        ("Blog", "blog.monstergaming.ai"),
    )
    for label, display_path in display_path_links:
        matching = [line for line in links_section.splitlines() if line.startswith(f"- **{label}:**")]
        assert len(matching) == 1
        assert f"[{display_path}]" in matching[0]


def test_profile_readme_intro_identifies_ai_platform(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "Monster Gaming is an AI platform" in intro


def test_profile_readme_loki_code_is_open_source(profile_text):
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    assert "open-source" in loki_line
    assert "AI coding CLI" in loki_line


def test_profile_readme_newsletter_uses_branded_display_text_not_path_style(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    newsletter_line = next(
        line for line in links_section.splitlines() if line.startswith("- **Newsletter:**")
    )
    assert "[Man in the Machine]" in newsletter_line
    assert "[blog.monstergaming.ai/newsletter/]" not in newsletter_line


def test_profile_readme_loki_technical_specs_stay_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    for spec in ("195 tests", "8.1 MB", "built in C11"):
        assert spec not in intro, f"Loki Code spec {spec!r} must stay in offerings section"


def test_profile_readme_monster_gpt_line_excludes_agent_count(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    monster_gpt_line = next(
        line for line in offerings.splitlines() if line.startswith("- **[Monster-GPT]")
    )
    assert "145+ specialist agents" not in monster_gpt_line


def test_profile_readme_newsletter_name_stays_in_links_section(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]

    assert "Man in the Machine" not in intro
    assert "Man in the Machine" not in offerings
    assert "Man in the Machine" in links_section


def test_org_profile_readme_lives_at_github_required_path():
    """GitHub org profiles require profile/README.md at the repository root."""
    path = REPO_ROOT / "profile" / "README.md"
    assert path.is_file(), "org profile must be at profile/README.md for GitHub to display it"


def test_profile_readme_non_unreal_engines_remain_plain_text_in_intro(profile_text):
    """Only Unreal Engine is hyperlinked; Unity, Godot, and bespoke stay plain text."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "[Unreal Engine](https://monstergaming.ai)" in intro
    assert "[Unity]" not in intro
    assert "[Godot]" not in intro
    assert "[bespoke engines]" not in intro
    assert "Unity, Godot, and bespoke engines" in intro


def test_profile_readme_openai_drop_in_claim_stays_in_offerings(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "drop-in replacement for OpenAI SDKs" not in intro
    assert "drop-in replacement for OpenAI SDKs" in offerings


def test_profile_readme_sections_appear_in_document_order(profile_text):
    what_we_build = profile_text.index("## What We Build")
    official_sdks = profile_text.index("## Official SDKs")
    links = profile_text.index("## Links")

    assert what_we_build < official_sdks < links


def test_profile_readme_has_exactly_three_h2_sections(profile_text):
    h2_headings = [line for line in profile_text.splitlines() if line.startswith("## ")]
    assert h2_headings == ["## What We Build", "## Official SDKs", "## Links"]


def test_profile_readme_luxedeum_link_only_in_footer(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    body = profile_text.split("## What We Build", maxsplit=1)[1]
    body_before_footer = body.split("A [Luxedeum]", maxsplit=1)[0]

    assert "luxedeum.com" not in intro
    assert "luxedeum.com" not in body_before_footer
    assert "A [Luxedeum](https://luxedeum.com) company." in profile_text


def test_profile_readme_sdk_table_package_names_are_hyperlinked(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    expected_links = (
        "[@monstergaming/sdk](https://www.npmjs.com/package/@monstergaming/sdk)",
        "[monstergaming](https://pypi.org/project/monstergaming/)",
        "[monstergaming](https://crates.io/crates/monstergaming)",
    )
    for link in expected_links:
        assert link in sdk_section, f"missing hyperlinked package name: {link}"


def test_profile_readme_loki_blog_url_stays_out_of_sdk_section(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert LOKI_CODE_BLOG_URL not in sdk_section
    assert "[Loki Code]" not in sdk_section


def test_profile_readme_pricing_url_stays_in_links_section(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]

    pricing_url = "https://monstergaming.ai/pricing"
    assert pricing_url not in intro
    assert pricing_url not in offerings
    assert pricing_url in links_section


def test_profile_readme_newsletter_url_stays_out_of_sdk_section(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert NEWSLETTER_URL not in sdk_section
    assert "Man in the Machine" not in sdk_section


def test_profile_readme_blog_homepage_url_stays_in_links_section(profile_text):
    """Blog homepage URL belongs in Links; Loki Code may link to a specific blog post."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    blog_homepage = "](https://blog.monstergaming.ai)"
    assert blog_homepage not in intro
    assert blog_homepage not in sdk_section
    assert blog_homepage in links_section


@pytest.mark.parametrize(
    "install_command",
    ("npm install @monstergaming/sdk", "pip install monstergaming", "cargo add monstergaming"),
)
def test_profile_readme_sdk_install_commands_stay_in_sdk_section(profile_text, install_command):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert install_command in sdk_section
    assert install_command not in intro
    assert install_command not in offerings
    assert install_command not in links_section


def test_profile_readme_flagship_claim_stays_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "flagship model" not in intro
    assert "flagship model" in offerings


def test_profile_readme_game_dev_tuned_claim_stays_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "game-dev-tuned models" not in intro
    assert "game-dev-tuned models" in offerings


def test_profile_readme_quickstart_url_stays_out_of_sdk_section(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    quickstart_url = "https://monstergaming.ai/quickstart"
    assert quickstart_url not in sdk_section


def test_profile_readme_loki_blog_url_preserves_revoked_post_path(profile_text):
    """Loki Code must link to the specific engineering blog post, not a truncated path."""
    loki_line = next(line for line in profile_text.splitlines() if "[Loki Code]" in line)

    assert "because-ours-got-revoked" in loki_line
    assert LOKI_CODE_BLOG_URL in loki_line


def test_profile_readme_intro_lists_engines_in_canonical_order(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    unreal_idx = intro.index("Unreal Engine")
    unity_idx = intro.index("Unity")
    godot_idx = intro.index("Godot")
    bespoke_idx = intro.index("bespoke engines")

    assert unreal_idx < unity_idx < godot_idx < bespoke_idx


def test_profile_readme_intro_has_no_product_offering_bullets(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    offering_bullets = [line for line in intro.splitlines() if line.startswith("- **[")]
    assert not offering_bullets, "product offerings belong under ## What We Build, not intro"


def test_profile_readme_loki_blog_url_stays_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert LOKI_CODE_BLOG_URL not in links_section
    assert "because-ours-got-revoked" not in links_section


def test_profile_readme_gameplay_systems_claim_stays_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    codegen_claim = "gameplay systems, shaders, networking, and UI"
    assert codegen_claim not in intro
    assert codegen_claim in offerings


def test_profile_readme_agent_count_stays_out_of_sdk_section(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert "145+ specialist agents" not in sdk_section
    assert "30+ game dev disciplines" not in sdk_section


def test_profile_readme_auto_routes_phrase_stays_in_offerings_not_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    assert "auto-routes to specialist agents" not in intro
    assert "auto-routes to specialist agents" in offerings


def test_profile_readme_engine_aware_codegen_links_to_main_site_not_quickstart(profile_text):
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]

    codegen_line = next(
        line for line in offerings.splitlines() if "[Engine-aware code generation]" in line
    )

    assert "[Engine-aware code generation](https://monstergaming.ai)" in codegen_line
    assert "quickstart" not in codegen_line


def test_profile_readme_intro_is_single_paragraph(profile_text):
    """Org profile intro should stay one paragraph for clean GitHub rendering."""
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    paragraph_lines = [
        line
        for line in intro.splitlines()
        if line.strip() and line.startswith("Monster Gaming is")
    ]
    assert len(paragraph_lines) == 1


def test_profile_readme_tagline_immediately_follows_title(profile_text):
    lines = profile_text.splitlines()

    assert lines[0] == "# Monster Gaming"
    assert lines[1] == ""
    assert lines[2] == "**AI-powered game development platform.**"


def test_profile_readme_has_no_h3_subsections(profile_text):
    h3_headings = [line for line in profile_text.splitlines() if line.startswith("### ")]
    assert not h3_headings, "org profile should use only H1/H2 headings"


def test_profile_readme_luxedeum_footer_is_last_nonblank_line(profile_text):
    nonblank_lines = [line for line in profile_text.splitlines() if line.strip()]
    assert nonblank_lines[-1] == "A [Luxedeum](https://luxedeum.com) company."


def test_profile_readme_pricing_line_uses_em_dash_before_free_tier(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    pricing_line = next(
        line for line in links_section.splitlines() if line.startswith("- **Pricing:**")
    )
    assert "— free tier available" in pricing_line


def test_profile_readme_routing_copy_stays_out_of_offerings_and_links(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    routing_copy = "We route your queries through"
    assert routing_copy in intro
    assert routing_copy not in offerings
    assert routing_copy not in links_section


def test_profile_readme_agent_count_stays_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "145+ specialist agents" not in links_section
    assert "30+ game dev disciplines" not in links_section


def test_profile_readme_compile_claim_stays_out_of_sdk_section(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]

    assert "that actually compile" not in sdk_section


def test_profile_readme_openai_drop_in_stays_out_of_sdk_and_links_sections(profile_text):
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    sdk_section = sdk_section.split("## Links", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    claim = "drop-in replacement for OpenAI SDKs"
    assert claim not in sdk_section
    assert claim not in links_section


def test_profile_readme_loki_code_name_stays_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "[Loki Code]" not in links_section
    assert "open-source AI coding CLI" not in links_section


def test_profile_readme_agent_routing_examples_stay_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    agent_routing_phrase = "shader, animation, netcode, level design, QA"
    assert agent_routing_phrase not in links_section


def _sdk_section(profile_text: str) -> str:
    sdk_section = profile_text.split("## Official SDKs", maxsplit=1)[1]
    return sdk_section.split("## Links", maxsplit=1)[0]


def test_profile_readme_routing_copy_stays_out_of_sdk_section(profile_text):
    assert "We route your queries through" not in _sdk_section(profile_text)


def test_profile_readme_auto_routes_phrase_stays_out_of_sdk_and_links_sections(profile_text):
    phrase = "auto-routes to specialist agents"
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert phrase not in _sdk_section(profile_text)
    assert phrase not in links_section


def test_profile_readme_newsletter_dispatch_stays_out_of_sdk_section(profile_text):
    assert "weekly dispatch from the engineering floor" not in _sdk_section(profile_text)


def test_profile_readme_loki_technical_specs_stay_out_of_sdk_section(profile_text):
    sdk_section = _sdk_section(profile_text)

    for spec in ("built in C11", "195 tests", "8.1 MB"):
        assert spec not in sdk_section, f"Loki Code spec {spec!r} must stay out of SDK section"


def test_profile_readme_open_source_cli_claim_stays_out_of_sdk_section(profile_text):
    assert "open-source AI coding CLI" not in _sdk_section(profile_text)


def test_profile_readme_openai_api_offering_stays_out_of_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "[OpenAI-compatible API]" not in intro
    assert "drop-in replacement for OpenAI SDKs" not in intro


def test_profile_readme_engine_aware_offering_stays_out_of_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "[Engine-aware code generation]" not in intro
    assert "that actually compile" not in intro


def test_profile_readme_loki_technical_specs_stay_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    for spec in ("built in C11", "195 tests", "8.1 MB"):
        assert spec not in links_section, f"Loki Code spec {spec!r} must stay out of Links section"


def test_profile_readme_game_dev_tuned_claim_stays_out_of_sdk_and_links_sections(profile_text):
    claim = "game-dev-tuned models"
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert claim not in _sdk_section(profile_text)
    assert claim not in links_section


def test_profile_readme_sits_above_engine_claim_stays_in_intro_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    claim = "sits above the engine"
    assert claim in intro
    assert claim not in offerings
    assert claim not in _sdk_section(profile_text)
    assert claim not in links_section


def test_profile_readme_purpose_built_for_stays_in_intro_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    claim = "purpose-built for"
    assert claim in intro
    assert claim not in offerings
    assert claim not in _sdk_section(profile_text)
    assert claim not in links_section


def test_profile_readme_engine_aware_offering_stays_out_of_sdk_and_links(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "[Engine-aware code generation]" not in _sdk_section(profile_text)
    assert "[Engine-aware code generation]" not in links_section


def test_profile_readme_openai_api_offering_stays_out_of_sdk_and_links(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "[OpenAI-compatible API]" not in _sdk_section(profile_text)
    assert "[OpenAI-compatible API]" not in links_section


def test_profile_readme_flagship_claim_stays_out_of_sdk_and_links(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "flagship model" not in _sdk_section(profile_text)
    assert "flagship model" not in links_section


def test_profile_readme_compile_claim_stays_out_of_links_section(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "that actually compile" not in links_section


def test_profile_readme_gameplay_systems_claim_stays_out_of_sdk_and_links(profile_text):
    claim = "gameplay systems, shaders, networking, and UI"
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert claim not in _sdk_section(profile_text)
    assert claim not in links_section


def test_profile_readme_writes_verb_stays_out_of_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "writes gameplay systems" not in intro
    assert "writes gameplay systems" not in _sdk_section(profile_text)
    assert "writes gameplay systems" not in links_section


def test_profile_readme_monster_gpt_name_stays_out_of_sdk_and_links_sections(profile_text):
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert "Monster-GPT" not in _sdk_section(profile_text)
    assert "Monster-GPT" not in links_section


def test_profile_readme_quickstart_url_stays_out_of_intro(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]

    assert "https://monstergaming.ai/quickstart" not in intro
    assert "monstergaming.ai/quickstart" not in intro


def test_profile_readme_routing_narrative_appears_once_in_intro_only(profile_text):
    phrase = "We route your queries through"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    body = profile_text.split("## What We Build", maxsplit=1)[1]

    assert profile_text.count(phrase) == 1
    assert phrase in intro
    assert phrase not in body


def test_profile_readme_agent_count_appears_once_in_intro_only(profile_text):
    phrase = "145+ specialist agents"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    body = profile_text.split("## What We Build", maxsplit=1)[1]

    assert profile_text.count(phrase) == 1
    assert phrase in intro
    assert phrase not in body


def test_profile_readme_disciplines_count_appears_once_in_offerings_only(profile_text):
    phrase = "30+ game dev disciplines"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    tail = profile_text.split("## Official SDKs", maxsplit=1)[1]

    assert profile_text.count(phrase) == 1
    assert phrase not in intro
    assert phrase in offerings
    assert phrase not in tail


def test_profile_readme_has_exactly_one_h1_heading(profile_text):
    h1_headings = [line for line in profile_text.splitlines() if line.startswith("# ")]
    assert h1_headings == ["# Monster Gaming"]


def test_profile_readme_tagline_appears_once(profile_text):
    tagline = "**AI-powered game development platform.**"
    assert profile_text.count(tagline) == 1


def test_profile_readme_engineering_floor_phrase_stays_in_links_only(profile_text):
    phrase = "engineering floor"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    sdk_section = _sdk_section(profile_text)

    assert profile_text.count(phrase) == 1
    assert phrase not in intro
    assert phrase not in offerings
    assert phrase not in sdk_section


def test_profile_readme_quickstart_url_appears_in_offerings_and_links_only(profile_text):
    quickstart_url = "https://monstergaming.ai/quickstart"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    sdk_section = _sdk_section(profile_text)
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert profile_text.count(quickstart_url) == 2
    assert quickstart_url not in intro
    assert quickstart_url in offerings
    assert quickstart_url in links_section
    assert quickstart_url not in sdk_section


def test_profile_readme_luxedeum_url_appears_once_in_footer_only(profile_text):
    luxedeum_url = "https://luxedeum.com"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    body_before_footer = profile_text.split("## What We Build", maxsplit=1)[1]
    body_before_footer = body_before_footer.split("A [Luxedeum]", maxsplit=1)[0]

    assert profile_text.count(luxedeum_url) == 1
    assert luxedeum_url not in intro
    assert luxedeum_url not in body_before_footer


MAIN_SITE_URL = "https://monstergaming.ai"
BLOG_HOMEPAGE_URL = "https://blog.monstergaming.ai"
PRICING_URL = "https://monstergaming.ai/pricing"


def _link_targets(profile_text: str) -> list[str]:
    return re.findall(r"\]\((https?://[^)]+)\)", profile_text)


def test_profile_readme_main_site_url_appears_four_times_as_link_target(profile_text):
    """Bare main-site links belong in intro, two offerings, and Website — not SDK or blog paths."""
    main_site_links = [url for url in _link_targets(profile_text) if url == MAIN_SITE_URL]
    assert len(main_site_links) == 4


def test_profile_readme_main_site_url_scoped_to_canonical_sections(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert f"[Unreal Engine]({MAIN_SITE_URL})" in intro
    assert f"[Monster-GPT]({MAIN_SITE_URL})" in offerings
    assert f"[Engine-aware code generation]({MAIN_SITE_URL})" in offerings
    assert f"[monstergaming.ai]({MAIN_SITE_URL})" in links_section


def test_profile_readme_blog_homepage_url_appears_once_in_links_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    sdk_section = _sdk_section(profile_text)
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    blog_link = f"]({BLOG_HOMEPAGE_URL})"
    assert profile_text.count(blog_link) == 1
    assert blog_link in links_section
    assert blog_link not in intro
    assert blog_link not in offerings
    assert blog_link not in sdk_section


def test_profile_readme_pricing_url_appears_once_in_links_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    sdk_section = _sdk_section(profile_text)
    links_section = profile_text.split("## Links", maxsplit=1)[1]
    links_section = links_section.split("A [Luxedeum]", maxsplit=1)[0]

    assert profile_text.count(PRICING_URL) == 1
    assert PRICING_URL in links_section
    assert PRICING_URL not in intro
    assert PRICING_URL not in offerings
    assert PRICING_URL not in sdk_section


def test_profile_readme_unreal_engine_link_appears_once_in_intro_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    body = profile_text.split("## What We Build", maxsplit=1)[1]
    unreal_link = f"[Unreal Engine]({MAIN_SITE_URL})"

    assert profile_text.count(unreal_link) == 1
    assert unreal_link in intro
    assert unreal_link not in body


def test_profile_readme_flagship_model_appears_once_in_offerings_only(profile_text):
    phrase = "flagship model"
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    tail = profile_text.split("## Official SDKs", maxsplit=1)[1]

    assert profile_text.count(phrase) == 1
    assert phrase not in intro
    assert phrase in offerings
    assert phrase not in tail


def test_profile_readme_open_source_appears_once_in_offerings_only(profile_text):
    intro = profile_text.split("## What We Build", maxsplit=1)[0]
    offerings = profile_text.split("## What We Build", maxsplit=1)[1]
    offerings = offerings.split("## Official SDKs", maxsplit=1)[0]
    tail = profile_text.split("## Official SDKs", maxsplit=1)[1]

    assert profile_text.count("open-source") == 1
    assert "open-source" not in intro
    assert "open-source" in offerings
    assert "open-source" not in tail
