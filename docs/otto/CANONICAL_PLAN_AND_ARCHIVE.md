# OTTO — Canonical Plan & Work Archive

- Owner: FounderAgent (JakeAgent) · Monster Gaming AI, Inc.
- Maintained by: cloud agents working this repo
- Status: living document
- Last updated: 2026-07-24

This is the single canonical archive of the work done in this repo toward wiring agents into the
Monster Gaming / OTTO stack, **plus** the forward TODO/plan. It is deliberately honest about what was
actually executable in a Cursor Cloud Agent sandbox versus what is **blocked** on infrastructure that
this environment cannot reach. Treat the "Blocked" and "Plan" sections as the source of truth for
what still needs to happen.

---

## 0. Honest scope note

Much of the agent↔fleet wiring (LuxAgentOS MCP, HIVE/MESH/COORDINATION connections, A2A, pulling
Neuromancer's July Hivemind doc) **could not be performed from this environment**. What was delivered
is therefore **documentation, policy, and a runnable connectivity probe** — the parts that are safe
and verifiable offline — not a live fleet connection. The live-connection work is captured below as
blocked TODO items with concrete unblocks rather than pretended-complete.

---

## 1. Naming & entity (canonical)

- **LOKI** = code name, **OTTO** = product name — **interchangeable** (either is acceptable).
- "Otto Software and Tools" is registered with the **USPTO under Monster Gaming AI, Inc.**
- **OttoRouter** = our own model router (part of `OTTO_SERVER`); one part of a larger whole, built on
  proven/tested components already in the stack (the **neutron** gateway, etc.).
- **OpenRouter is deprecated** — OttoRouter replaces it. Do not reintroduce OpenRouter anywhere.

## 2. Fleet architecture facts (from *The Hivemind*, June 2026)

- **COORDINATION** — `coord.monstergaming.ai`, central ganglion: register on startup, 60s heartbeat,
  route by machine/role/project/broadcast, task claims/locks, gate state.
- **MESH** — NATS JetStream pheromone bus: publish what you learn, subscribe to what you need;
  Chinese-wall project isolation.
- **HIVE** — `knowledge_artifacts` collective memory; the hive remembers everything.
- **Machines (6):** BUILD (Threadripper 3990X, dual 3090s), HAL, Mac Mini, Mac Pro, Nexus
  (coordination hub), WinBuild-1 (CI).
- **Castes:** Lux (LuxIR, LuxCTO, LuxCFO, LuxGC, LuxSDET, LuxProtector), gd (gdTD, gdArtDirector,
  gdProducer, gdSDET, gdQAManager, gdLocalization), plus CMO and FounderAgent (JakeAgent = Hive Queen).
- **Review gates:** LuxCTO (architecture/infra), gdTD (game code / FFI / SDK / engine).
- **Spend guard:** LuxCFO **$15/day cap (LUX-1962)**.
- **Quality pipeline:** FORGE, Crucible, 7-Sigma. **Rollback/apoptosis:** LUX-1992 Tier 8 Canary +
  lineage DAG. **Metabolism:** Otto-Code-Canary / Loki-Code-Canary (continuous evolution).
- **Secrets:** live in `/etc/monstergaming/agent.conf`; never print/leak.

## 3. Gate & operating policy (canonical)

- **PRE-JAKE destructive gates only** need approval: force-push `main`, `DELETE knowledge_artifacts`,
  spend caps. Never request approval/smart-mode for anything else.
- **Auto-review block →** take an alternate path in the same turn (BUILD SSH hop, Forgejo bare push,
  HTTP coord via `coord.monstergaming.ai`); never retry the same blocked command in an approval loop.
- **MCP precedence:** engage the **LuxAgentOS MCP first**, before any other MCP server/tool.

---

## 4. Environment reality (measured in a Cursor Cloud Agent, 2026-07-24)

| Fact | Evidence |
|------|----------|
| Ad-hoc **Override** VM, no saved environment | `cursor-cloud environment-info`: `source: "Override"`, `environmentPublicId: null` |
| **LuxAgentOS MCP absent** from cloud catalog (present on desktop w/ 74 tools) | `GetMcpTools` catalog lists 26 servers, none LuxAgentOS |
| **Egress allowlist-restricted**, excludes all `monstergaming.ai` | `environment-info.egress.allowedDomains` |
| Reachability asymmetry | `api.github.com`→200, `files.slack.com`→302; `coord.monstergaming.ai`→000, `example.com`→000 |
| No arbitrary env vars; only injected secrets | `env` shows no `MG_*`/`HIVE`/`MESH`/`COORD` |
| No `/etc/monstergaming/agent.conf` | file not present |

**A2A verdict:** direct/real-time A2A to the fleet is **impossible** from a Cursor cloud sandbox.
Async A2A via GitHub/Slack is possible but high-latency. → **Self-hosted sandboxes are the correct
path** to control env vars, egress, MCP, and A2A.

---

## 5. Work archive (what was delivered)

### PR #1 — `cursor/setup-dev-environment-fb4a` — Session bootstrap + policy
Files: `AGENTS.md`, `.cursor/commands/session-start.md`, `.cursor/rules/monster-gaming-stack.mdc`,
`scripts/session-start-probe.sh`.

| Commit | Summary |
|--------|---------|
| `aa4f0bc` | AGENTS.md with Cursor Cloud dev notes (repo is the org `.github` profile — content only) |
| `d32587e` | `/session-start` bootstrap (initial) |
| `d86bd5d` | Align `/session-start` with real hivemind architecture |
| `27fa60e` | Mandate LuxAgentOS MCP first |
| `53bdb5d` | OpenRouter deprecation as provider policy |
| `b0898fb` | Name OttoRouter as our router replacing OpenRouter |
| `97c19d8` | Loki↔Otto + OttoRouter/neutron lineage |
| `401b7aa` | Attribute USPTO mark to Monster Gaming AI, Inc. |
| `387ee9e` | LOKI (code name) / OTTO (product name) interchangeable |

Verified offline: `session-start-probe.sh` reports all planes DEGRADED with no config, all `OK` (200)
against a local mock, and leaks no secret values; rule frontmatter valid (`alwaysApply: true`).

### PR #3 — `cursor/otto-native-runtime-adr-fb4a` — ADR + this archive
Files: `docs/adr/0001-consolidate-agent-runtime-into-otto-native.md`, this file.

| Commit | Summary |
|--------|---------|
| `c268146` | ADR 0001 — consolidate runtime into OTTO native |
| `5c6ad40`/`3ca18df`/`f33fd29`/`f1b4ff7`/`d6b5c6e` | Provider policy, OttoRouter, neutron lineage, entity, naming |

---

## 6. Blocked — could not be performed here (with unblocks)

| # | Item | Why blocked | Unblock |
|---|------|-------------|---------|
| B1 | Connect to HIVE/MESH/COORDINATION | egress excludes `monstergaming.ai` (000); no config/creds | allowlist coord/NATS/HIVE hosts + provide `/etc/monstergaming/agent.conf` or `MG_*` secrets |
| B2 | Use LuxAgentOS MCP | not attached to cloud environment (desktop-only) | attach LuxAgentOS MCP to the cloud env (commit `.cursor/mcp.json` w/ server config, or saved env) |
| B3 | A2A with fleet nodes | Cursor sandbox is outbound-only + egress-locked | self-hosted sandbox VM |
| B4 | Pull Neuromancer's July Hivemind doc | requires HIVE access (B1/B2) | upload the July PDF here, or unblock B1/B2 |
| B5 | Benchmark/implement OTTO migration | no OTTO_SERVER/OTTO_CLIENT/neutron code in this repo | grant OTTO repo access in a reachable env |
| B6 | Token-attribution of 1.2B/day | no telemetry access here | export spend breakdown (see ADR open questions) |

---

## 7. Canonical TODO / plan (dependency-ordered)

Legend: [x] done · [~] partial/offline-only · [ ] todo/blocked

- [x] T0. Establish agent operating policy in-repo (bootstrap, rule, AGENTS.md) — PR #1.
- [x] T1. Record OTTO migration determination — ADR 0001 (PR #3).
- [ ] T2. **Self-hosted sandbox VM** image + egress to `coord.monstergaming.ai` / NATS / HIVE, with
  our env vars. (unblocks B1, B3) — highest structural priority.
- [ ] T3. **Attach LuxAgentOS MCP** to the runtime the fleet actually uses (not Cursor desktop). (B2)
- [ ] T4. **`OTTO_SERVER` gateway** with **OttoRouter** (reusing neutron), **prompt caching**, and
  routing (frontier only for hard steps; cheap/local otherwise). Biggest $/token win. (needs B5)
- [ ] T5. **`OTTO_CLIENT` harness** — lazy tool-schema loading, HIVE-by-reference context, minimal
  system prompt. (needs B5)
- [ ] T6. **NATS (MESH) A2A** to replace hosted subagent fan-out. (needs B5, T2)
- [ ] T7. Move deterministic steps (lint/format/git/health/schema) to **native code**, retire those
  LLM calls. ("metabolism → Native Code")
- [ ] T8. **Token-attribution** of the 1.2B/day (fixed context vs reasoning vs retries, by caste/
  niche) to order T4–T7. (B6)
- [ ] T9. Instrument tokens/turn before vs after each migration step; feed the fitness function;
  wire rollback via the LUX-1992 pattern.
- [ ] T10. Once HIVE reachable, fold Neuromancer's **July Hivemind** architecture back into ADR 0001,
  the `/session-start` bootstrap, and this plan. (B4)

## 8. Consolidated actions required of the operator

1. Upload the July Hivemind PDF here (fastest unblock for B4).
2. Provision a self-hosted sandbox VM for agents (unblocks the bulk of the plan).
3. Attach LuxAgentOS MCP to that runtime.
4. Grant OTTO_SERVER / OTTO_CLIENT / neutron repo access.
5. Export the 1.2B/day token-attribution breakdown.
6. (If any Cursor cloud work continues) allowlist `coord.monstergaming.ai` + fleet hosts and add the
   agent config/secrets.

## 9. Pointers

- ADR: `docs/adr/0001-consolidate-agent-runtime-into-otto-native.md`
- Bootstrap: `.cursor/commands/session-start.md` · Rule: `.cursor/rules/monster-gaming-stack.mdc`
- Probe: `scripts/session-start-probe.sh` · Agent guide: `AGENTS.md`
- PRs: #1 (session bootstrap + policy), #3 (ADR + this archive)
