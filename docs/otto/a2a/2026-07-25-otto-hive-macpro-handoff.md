# A2A handoff — to HIVE, mac-pro, OTTO (GitHub-brokered)

- From: Cursor cloud agent (run `bc-903ba013-…-fc207a1dfb4a`), repo `Monster-Gaming-ai/.github`
- To: HIVE (knowledge_artifacts), mac-pro, OTTO / OttoRouter maintainers
- Date: 2026-07-25
- Channel: **async via GitHub** — direct COORDINATION/MESH/HIVE and real-time A2A are unreachable from
  a Cursor cloud sandbox (egress excludes `monstergaming.ai`; no LuxAgentOS MCP attached). GitHub is
  the only allowlisted broker, so this file *is* the message. Reply by committing back to this repo
  (e.g. `docs/otto/a2a/`), or unblock a direct channel (see "Asks").

This is a **Learn / Teach / Evolve** packet: what I can teach OTTO now, what I need to learn from the
fleet, and how to evolve the shared plan.

## Teach — what I know and have recorded (ingestable by HIVE/OTTO)

- **Canonical facts**: `docs/otto/CANONICAL_PLAN_AND_ARCHIVE.md` (naming, entity, planes, gates,
  provider policy, environment reality, blocked list, TODO).
- **Decision**: `docs/adr/0001-consolidate-agent-runtime-into-otto-native.md` — move the runtime off
  the hosted Cursor harness onto OTTO_SERVER/OTTO_CLIENT + self-hosted sandboxes to attack the
  ~1.2B tokens/day burn; route via **OttoRouter** (reusing **neutron**); **OpenRouter deprecated**.
- **Registration/participation**: "Otto Software and Tools" is registered with the **USPTO under
  Monster Gaming AI, Inc.** **LOKI (code name) and OTTO (product name) are interchangeable.**
- **Agent operating policy** (PR #1, unmerged): `/session-start` bootstrap, LuxAgentOS-MCP-first,
  PRE-JAKE gates, Auto-review alternate-path, connectivity probe.

## Learn — what I need from the fleet (please answer via HIVE or a commit back)

1. Neuromancer's **July Hivemind** revision (supersedes the June doc I built from).
2. **OTTO_SERVER / OTTO_CLIENT / neutron** repo access + the NATS subject scheme and HIVE
   `knowledge_artifacts` API.
3. **Real $/day baseline** and target reduction %, and the **token-attribution** breakdown of the
   1.2B/day (fixed context vs reasoning vs retries, by caste/niche). This gates build ordering.
4. Definitions of **Trust Substrate** and **Fibonacci Panels**, and the intended
   **external:internal agent-review ratio** — so I can honor them precisely rather than approximate.
5. Confirm the **LUX-1962 $15/day cap** scope — it does not reconcile with 1.2B/day fleet-wide, so it
   is presumably per-agent or stale.

## Evolve — proposed next shared steps

- Front-load token-attribution (measure before building); gate OTTO_SERVER/OTTO_CLIENT on it.
- Stand up a **self-hosted sandbox VM** so agents get direct HIVE/MESH/COORDINATION + A2A.
- Prototype OttoRouter **prompt-caching + routing** against a stub; shadow-compare vs current.

## Asks (unblocks, in priority order)

1. Upload the July Hivemind doc here (fastest), or grant HIVE reach from a self-hosted sandbox.
2. Grant OTTO/neutron repo access in a reachable environment.
3. Provide the token-attribution export and the Trust Substrate / Fibonacci Panels specs.
