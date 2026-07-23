# AGENTS.md

## Session start (mandatory)

At the **start of every session**, run the `/session-start` protocol in `.cursor/commands/session-start.md` before doing task work. It bootstraps the agent onto the Monster Gaming AI stack and maximizes reliance on our own infrastructure:

- **HIVE** — shared knowledge / memory (`knowledge_artifacts`): load prior context, write learnings back.
- **MESH** — fleet registry + messaging: register presence, coordinate with peers.
- **COORDINATION** (`luxagentos_http`) — claim tasks, respect locks and gate state.
- **ADRs + rules** — load and treat as binding.

First step is the connectivity probe: `bash scripts/session-start-probe.sh`. Plane endpoints/tokens come from environment/secrets (`LUXAGENTOS_HTTP_URL`/`LUXAGENTOS_TOKEN`, `HIVE_URL`/`HIVE_TOKEN`, `MESH_URL`/`MESH_TOKEN`); if a plane is unreachable, note the gap and continue in degraded mode — never fabricate a connection.

Gate policy: never request approval/smart-mode except destructive **PRE-JAKE gates** (force-push `main`, `DELETE knowledge_artifacts`, spend caps). On an Auto-review block, take an alternate path in the same turn (BUILD SSH hop, Forgejo bare push, HTTP coord via `luxagentos_http`) — never retry the same blocked command in an approval loop. The always-applied rule `.cursor/rules/monster-gaming-stack.mdc` enforces this.

## Cursor Cloud specific instructions

This repository is the **`Monster-Gaming-ai/.github` organization profile / community-health repo**. It is content-only — there is no application, no `package.json`, no build system, no test suite, and no services to run. Do not look for a dev server, backend, or database; none exist here.

What lives here:
- `profile/README.md` — the org profile rendered on the GitHub org page.
- `CONTRIBUTING.md`, `LICENSE` — community-health files.
- `.github/ISSUE_TEMPLATE/*.yml` — GitHub issue-form templates.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template.

Working notes:
- There are no dependencies to install and nothing to "run". Verification means confirming the content parses/renders correctly.
- The only functional artifacts are the GitHub issue-form YAML files. After editing them, validate they are well-formed and keep the required issue-form keys (`name`, `description`, `body`, and a `type` on each `body` item). PyYAML ships with the system Python here, so you can validate quickly, e.g.:
  `python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/ISSUE_TEMPLATE/*.yml')]"`
- Changes to `profile/README.md` only affect how the org profile renders on GitHub; there is nothing to build.
