# ADR 0001 — Consolidate the agent runtime into OTTO native code

- Status: Proposed
- Date: 2026-07-24
- Deciders: FounderAgent (JakeAgent), LuxCTO
- Context tags: cost, sovereignty, orchestration, sandboxing

## Context

The fleet is burning **~1.2B tokens/day**. A large share of that is not "thinking" — it is
**orchestration overhead** that a hosted agent harness (Cursor/Claude/Gemini/Copilot-style)
re-pays on every turn: a large fixed system prompt, the full MCP tool-schema set, the skills/rules
catalog, `AGENTS.md`, and re-injected file/context payloads. Multiplied across 150+ agents running
continuously (the Otto-Code-Canary / Loki-Code-Canary "metabolism"), the fixed per-turn context
dominates spend.

> Naming: **LOKI** is the code name and **OTTO** is the product name — they are **interchangeable**
> (either is acceptable). "Otto Software and Tools" is registered with the USPTO under Monster Gaming
> AI, Inc.

We do **not** want to build infrastructure around Cursor. We want the runtime to be **OTTO**
(`OTTO_SERVER` / `OTTO_CLIENT`) — our own harness, gateway, and sandbox — so we control the context
budget, the tool ABI, agent-to-agent (A2A) comms, and the environment.

## Observed constraints (measured from a Cursor Cloud Agent, 2026-07-24)

These are facts gathered from inside a live Cursor cloud-agent run on `Monster-Gaming-ai/.github`:

- **Environment is an ad-hoc Override VM** (`source: "Override"`, no saved environment id).
  Its MCP set is the cloud default; **LuxAgentOS MCP is not attached** (desktop MCP connections do
  not propagate to cloud runs — different surface).
- **Egress is allowlist-restricted.** Reachability is asymmetric:
  - `api.github.com` → 200, `files.slack.com` → 302 (allowlisted)
  - `coord.monstergaming.ai` → 000, `example.com` → 000 (connection reset — not allowlisted)
- **No arbitrary env vars.** Only injected secrets; the agent cannot set the environment it runs in.
- **Not peer-addressable.** The VM is outbound-only; no inbound A2A endpoint.

### A2A verdict
- **Direct/real-time A2A from a Cursor cloud sandbox to the fleet is not possible** (no MCP here,
  egress excludes our domains, no inbound).
- **Even async A2A is unreliable from here.** The only allowlisted git host is GitHub, but the fleet
  uses **Forgejo, not GitHub** — so writing to this GitHub repo does not reach the fleet unless a
  human carries it over. Forgejo (and Slack posting) are not reachable/allowlisted from the sandbox.
  There is no dependable A2A channel from a Cursor cloud agent.
- Conclusion: **self-hosted sandboxes are the correct call.** Owning the VM gives us env vars,
  egress, MCP/tool wiring, and a real A2A bus in one move.

## Decision

Move the agent runtime off the hosted harness and onto OTTO native components. Where a step is
deterministic, replace the LLM call with **native code** ("metabolism → Native Code").

1. **OTTO_CLIENT (harness/binary)** — owns context assembly, tool dispatch, and the turn loop.
   Minimal static system prompt; **lazy-load tool schemas**; prune the skills/rules catalog to the
   task; retrieve context **by reference** from HIVE instead of re-injecting.
2. **OTTO_SERVER (OpenAI-compatible gateway)** — routing via **OttoRouter (our own router)**,
   **prompt caching**, context compression, shadow-model comparison. Reserve frontier models for
   hard steps; route cheap/local models for triage, classification, formatting.
   - OttoRouter is **one part of a larger whole** and is built on what is already working and tested
     in our stack (the **neutron** gateway, etc.) — reuse those proven components rather than
     rebuilding.
   - **Provider policy: routing goes through OttoRouter**, which routes to providers and
     local/self-hosted models. **OpenRouter is deprecated and OttoRouter replaces it** — any routing
     config, benchmark, or migration must not reintroduce an OpenRouter dependency.
3. **Native tool ABI** — replace per-turn MCP schema serialization with compiled in-process tools or
   a local tool daemon (Unix socket / gRPC). Tools cost ~0 context until invoked.
4. **A2A over NATS JetStream (MESH)** — real inter-agent messaging in our own network, replacing
   hosted subagent fan-out (which re-injects full context per child).
5. **Self-hosted sandbox VM** — our image, our env vars, our egress policy; HIVE/MESH/COORDINATION
   reachable directly.
6. **Deterministic handlers** — lint, format, file ops, git, schema validation, health probes run as
   plain code/daemons, never model calls.

## Cut list — what leaves Cursor and where it lands

| Cursor-hosted component | OTTO replacement | Primary token lever |
|---|---|---|
| Hosted agent loop + system prompt | `OTTO_CLIENT` harness | Trim + cache fixed per-turn context |
| MCP tool schemas (all servers, every turn) | Native tool ABI / local tool daemon | Load tool defs only on use |
| Skills/rules/AGENTS.md catalog in-context | Retrieve-by-reference from HIVE | Stop re-injecting static docs |
| Subagent/Task fan-out | NATS (MESH) A2A + shared HIVE context | Share context by ref, not by copy |
| Model selection (frontier by default) | `OTTO_SERVER` via **OttoRouter** + shadow eval | Cheap/local models for easy steps |
| Repeated system/tool context | `OTTO_SERVER` prompt caching | Pay ~cache-read, not full re-encode |
| Auto-review/approval retry loops | Native gate policy in harness | Kill wasted re-sends |
| Hosted sandbox (Override VM) | Self-hosted sandbox VM | Control env/egress/MCP/A2A |
| Routine LLM steps (lint/format/git) | Deterministic daemons/binaries | Remove the model call entirely |

## Sequencing (dependency order, not calendar)

1. Self-hosted sandbox VM image + egress to `coord.monstergaming.ai` / NATS / HIVE.
2. `OTTO_SERVER` gateway with prompt caching + routing (biggest immediate $/token win).
3. `OTTO_CLIENT` harness with lazy tool loading + HIVE-by-reference context.
4. NATS A2A to replace subagent fan-out.
5. Migrate deterministic steps to native code; retire the corresponding LLM calls.
6. Instrument tokens/turn before vs after each step; feed the fitness function.

## Consequences

- **Positive:** direct control of the dominant cost driver (fixed context), real A2A, sovereignty
  over env/egress, and a path to fold routine "metabolism" into cheap native code.
- **Negative / risk:** we now own harness reliability, model-provider failover, and sandbox security
  that Cursor currently handles. Needs its own observability and rollback (reuse LUX-1992 pattern).
- **Interop:** Cursor can remain a *human* IDE surface; it just stops being the *fleet* runtime.

### Required safeguards (do not skip)
The cost thesis ("fixed context dominates") is **unproven until token-attribution runs** — gate the
OTTO_SERVER/OTTO_CLIENT/native-code builds on it and record a real $/day baseline + target %. The
migration must also ship: a **security threat model** for self-hosted agents with direct fleet reach
(self-hosting removes Cursor's egress-locked sandbox), **least-privilege/rotated secrets** (not a flat
`agent.conf`), **OttoRouter HA/failover** (it replaces OpenRouter's battle-tested failover and must
not be a fleet-wide SPOF), a **runtime rollback/kill-switch + shadow migration** (distinct from
LUX-1992 lineage apoptosis), and an **observability stack** as a prerequisite for the fitness
function. Residual sovereignty caveat: OTTO still depends on external frontier APIs and their caching
semantics. Detailed list: `docs/otto/CANONICAL_PLAN_AND_ARCHIVE.md` §7a.

## Open questions / needed inputs

- Access to the OTTO_SERVER / OTTO_CLIENT repos and current NATS subject scheme (not in this repo).
- Token-attribution breakdown of the 1.2B/day: fraction that is fixed system/tool context vs.
  genuine reasoning vs. retries. This determines the ordering of wins above.
- Which model providers support prompt caching in our current mix, and cache TTLs.
