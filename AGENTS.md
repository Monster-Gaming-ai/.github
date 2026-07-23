# AGENTS.md

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
