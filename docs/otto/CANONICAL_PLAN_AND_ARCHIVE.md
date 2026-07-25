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
- **Spend guard:** LuxCFO **$15/day cap (LUX-1962)** — note this does **not** reconcile with a
  1.2B tokens/day fleet-wide spend, so it is presumably **per-agent or stale**; scope needs
  confirmation (see Open questions).
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

**A2A verdict:** direct/real-time A2A to the fleet is **impossible** from a Cursor cloud sandbox, and
**no contact with OTTO/HIVE/mac-pro has occurred.** Note the fleet uses **Forgejo, not GitHub** — this
repo is on GitHub, which the fleet likely does not watch, and Forgejo is not reachable/allowlisted
here. So even "leave a file and hope someone picks it up" is unreliable and is **not** confirmed
delivery; it must not be described as A2A that happened. → **Self-hosted sandboxes are the correct
path** to get real env vars, egress, MCP, and A2A (over Forgejo/NATS).

---

## 5. Work archive (what was delivered)

### PR #1 — `cursor/setup-dev-environment-fb4a` — Session bootstrap + policy
Files: `AGENTS.md`, `.cursor/commands/session-start.md`, `.cursor/rules/monster-gaming-stack.mdc`,
`scripts/session-start-probe.sh`.

> **Cross-branch note:** these four files live on the **unmerged PR #1 branch**, not on the branch
> carrying this archive (PR #3). References to them here are accurate only once PR #1 is merged; a
> reader on the PR #3 branch alone will not find them. Merge PR #1 to make this doc fully canonical.

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

**Sequencing correction (from review):** measure before you build. Token-attribution + observability
are **gating prerequisites** — do not commit the OTTO_SERVER/OTTO_CLIENT/native-code builds until the
"fixed context dominates" thesis is confirmed with real numbers.

- [x] T0. Establish agent operating policy in-repo (bootstrap, rule, AGENTS.md) — PR #1.
- [x] T1. Record OTTO migration determination — ADR 0001 (PR #3).
- [ ] T2. **Token-attribution of the 1.2B/day** (fixed context vs reasoning vs retries, by caste/
  niche) + real **$/day baseline** and target %. **GATES T5–T8.** (B6)
- [ ] T3. **Observability stack** — per-turn token accounting schema, cost-by-caste/project,
  transcript/audit capture, SLOs/alerts. Prerequisite for the fitness function, not a trailing step.
- [ ] T4. **Self-hosted sandbox VM** image + egress to `coord.monstergaming.ai` / NATS / HIVE, our
  env vars, plus a **threat model** for a compromised agent with direct fleet reach and enforced
  (not asserted) Chinese-wall isolation. (unblocks B1, B3)
- [ ] T5. **`OTTO_SERVER` gateway** with **OttoRouter** (reusing neutron): **prompt caching** (model
  hit-rate/write-cost, not "assume cache-read"), routing, **HA/failover + circuit-breaking +
  rate-limit handling** (OpenRouter provided these — OttoRouter must not be a fleet-wide SPOF).
  (needs B5, T2)
- [ ] T6. **`OTTO_CLIENT` harness** — lazy tool-schema loading, HIVE-by-reference context, minimal
  system prompt; cross-platform build/sign/auto-update for Linux + macOS + Windows machines. (needs B5)
- [ ] T7. **NATS (MESH) A2A** to replace hosted subagent fan-out. (needs B5, T4)
- [ ] T8. Move deterministic steps (lint/format/git/health/schema) to **native code**, retire those
  LLM calls, gating each on FORGE/Crucible/7-Sigma quality thresholds. ("metabolism → Native Code")
- [ ] T9. **Runtime rollback / kill-switch** — per-step revert from OTTO_CLIENT/OTTO_SERVER back to
  the hosted harness, dual-run/canary path, fleet-wide kill-switch (distinct from LUX-1992 lineage
  apoptosis, which is agent-fitness, not runtime-infra).
- [ ] T10. **Shadow migration** — run a small % of agents/turns on OTTO vs hosted, compare cost *and*
  output quality with explicit per-step accept/exit criteria before expanding.
- [ ] T11. Reconcile **native tool ABI vs "LuxAgentOS MCP first"** — how LuxAgentOS fits or is
  replaced when per-turn MCP schemas are removed; secure the tool daemon (authz over socket/gRPC).
- [ ] T12. Attach **LuxAgentOS MCP** to the runtime the fleet actually uses (not Cursor desktop). (B2)
- [ ] T13. Once HIVE reachable, fold Neuromancer's **July Hivemind** architecture back into ADR 0001,
  the `/session-start` bootstrap, and this plan. (B4)

### Interim, independently-shippable (not blocked on external unblocks)
- [ ] I1. Prompt-caching + routing prototype against a **stub** provider to measure cache economics.
- [ ] I2. Per-turn token-accounting schema + a local harness to log it (ready for real telemetry).
- [ ] I3. Secrets design: least-privilege per-agent/caste scoping + rotation + managed store (replace
  the flat `/etc/monstergaming/agent.conf` blast radius).

## 7a. Risks & required safeguards (from external review)

- **Cost thesis unproven** → gate all builds on T2 attribution; state per-lever expected savings.
- **Own-vs-hosted break-even** → add a cost-of-ownership model (harness reliability, provider
  failover, sandbox security, local-GPU capex on the dual-3090 BUILD box) vs projected savings.
- **Security regression** → self-hosting removes Cursor's egress-locked, non-peer-addressable
  sandbox; add the T4 threat model + enforced isolation before granting direct fleet reach.
- **Secrets blast radius** → I3 (scoping/rotation/managed store).
- **OttoRouter SPOF** → T5 HA/failover; evidence neutron handles fleet-scale failover.
- **Runtime rollback gap** → T9 kill-switch + dual-run.
- **Quality drift from cheap/local routing** → tie routing to FORGE/Crucible/7-Sigma thresholds
  with auto-rollback.
- **Residual sovereignty caveat** → OTTO still depends on external frontier APIs and *their*
  caching semantics/TTLs; state this explicitly.

## 7b. Governance & cadence (durable practices to honor)

- **Learn → Teach → Evolve** and **Enrich → Explore → Enhance**: each session ingests fleet
  knowledge, writes learnings back (HIVE when reachable / this archive / draft messages), and
  improves the plan. (From a Cursor sandbox only the local archive is actually writable — no fleet
  delivery.)
- **Agent reviews, external:internal ratio favoring externals** — decisions/plans get multi-
  perspective agent review before shipping. *(This turn applied one external review pass; full
  external-majority panels require fleet reviewers — fleet-gated.)*
- **Trust Substrate** and **Fibonacci Panels** — honor as governance constructs; **specs needed**
  from the fleet to apply precisely rather than approximate (see Open questions / A2A asks).
- **Loop until diminishing returns** — iterate review→enrich cycles; stop when further real progress
  requires blocked infra (OTTO repos, fleet reach, telemetry) rather than spinning no-op loops.

## 8. Consolidated actions required of the operator

1. Upload the July Hivemind PDF here (fastest unblock for B4).
2. Provision a self-hosted sandbox VM for agents (unblocks the bulk of the plan).
3. Attach LuxAgentOS MCP to that runtime.
4. Grant OTTO_SERVER / OTTO_CLIENT / neutron repo access.
5. Export the 1.2B/day token-attribution breakdown.
6. (If any Cursor cloud work continues) allowlist `coord.monstergaming.ai` + fleet hosts and add the
   agent config/secrets.

## 8a. Open questions (need fleet answers)

- Real $/day baseline + target reduction %; scope of the LUX-1962 $15/day cap (per-agent vs fleet).
- Token-attribution breakdown of the 1.2B/day (fixed context vs reasoning vs retries, by caste/niche).
- Specs for **Trust Substrate** and **Fibonacci Panels**, and the intended external:internal
  agent-review ratio.
- OTTO_SERVER / OTTO_CLIENT / **neutron** repo access; NATS subject scheme; HIVE `knowledge_artifacts` API.

## 9. Pointers

- ADR: `docs/adr/0001-consolidate-agent-runtime-into-otto-native.md`
- Draft (UNSENT) message to HIVE/mac-pro/OTTO — no contact made; fleet uses Forgejo, not this GitHub
  repo: `docs/otto/a2a/`
- Bootstrap: `.cursor/commands/session-start.md` · Rule: `.cursor/rules/monster-gaming-stack.mdc`
  · Probe: `scripts/session-start-probe.sh` · Agent guide: `AGENTS.md` *(all on unmerged PR #1)*
- PRs: #1 (session bootstrap + policy), #3 (ADR + this archive)
