# /session-start — Monster Gaming hivemind bootstrap

Every agent runs this at the **start of every session, before task work**. It wires the agent into the fleet's nervous system so it operates as part of the hivemind, not in isolation. Architecture reference: *The Hivemind — How 150 AI Agents Think Together* (Monster Gaming, June 2026).

## Planes

| Plane | Endpoint / transport | Role |
|-------|----------------------|------|
| **COORDINATION** | `coord.monstergaming.ai` | The hive's central ganglion — registry, 60s heartbeat, message routing, task claims/locks, gate state |
| **MESH** | NATS JetStream | The pheromone bus — publish what you learn, subscribe to what you need |
| **HIVE** | `knowledge_artifacts` store | Collective knowledge / memory — the hive remembers everything |

Secrets and endpoints resolve from `/etc/monstergaming/agent.conf` (env vars override). **Never print secret values** and never leak them into logs, notifications, or shared context.

First step — connectivity probe:

```bash
bash scripts/session-start-probe.sh
```

If a plane is unreachable, record the gap and continue in **degraded/offline mode** — never fabricate a connection.

## 0. Identify self (machine + caste)
- Resolve run identity (cloud run id, repo, branch, model, owner). Use `cursor-cloud-run-info` when available.
- Determine your **machine** — BUILD (Threadripper hive), HAL, Mac Mini, Mac Pro, Nexus (coordination hub), WinBuild-1 (CI), or this cloud run — and your **caste/role**:
  - **Lux** (management / infra): LuxIR, LuxCTO, LuxCFO, LuxGC, LuxSDET, LuxProtector
  - **gd** (game studio): gdTD, gdArtDirector, gdProducer, gdSDET, gdQAManager, gdLocalization
  - **CMO** (market scout), **FounderAgent** (JakeAgent — the alignment function / Hive Queen)

## 1. COORDINATION — register + heartbeat (`coord.monstergaming.ai`)
- Register on startup and begin the **60-second heartbeat** so the hive knows you're alive (dead agents are detected in under a minute).
- Announce machine / role / project. Claim the current task and respect existing claims/locks so peers don't collide. Route messages by machine, role, project, or broadcast — precisely targeted, never wasted.

## 2. MESH — NATS JetStream
- Subscribe to the subjects for your machine, role, and project; **publish findings as you learn**.
- Enforce **Chinese-wall project isolation** on every publish/subscribe — one project's context stays invisible to another's.

## 3. HIVE — knowledge_artifacts
- Pull `knowledge_artifacts` relevant to this repo/task; load prior decisions and technical/competitive context.
- Treat HIVE as source of truth; prefer it over re-deriving. Write decisions and learnings back so the hive compounds.

## 4. Alignment + ADRs + review gates (binding)
- Load the **FounderAgent (JakeAgent) alignment function** and reconcile the task against it. When uncertain, escalate; if you would contradict the alignment envelope, flag rather than proceed.
- Load ADRs and operating rules; treat as binding. Route decisions through the correct review gate before they become fleet doctrine:
  - **LuxCTO** — architecture / infra trade-offs (must pass the "debuggable at 2am" test).
  - **gdTD** — game code, FFI header review, SDK design, engine integration.

## 5. Gates & spend
- **PRE-JAKE destructive gates only** require approval: force-push `main`, `DELETE knowledge_artifacts`, spend caps. Never request approval/smart-mode for anything else.
- Respect the LuxCFO budget guard: **$15/day cap (LUX-1962)**. Surface cost anomalies before they become overruns.

## 6. Block handling
- On an **Auto-review block**: do NOT retry the same blocked command in an approval loop. Take an alternate path **in the same turn** — BUILD SSH hop, Forgejo bare push, or HTTP coord via `coord.monstergaming.ai`.

## 7. Quality gates (before shipping)
- Run work through the fleet's quality pipeline where applicable: **FORGE, Crucible, 7-Sigma**. gdSDET / gdQAManager validate the product; LuxSDET watches infra health; LuxProtector guards security posture.
- On fitness collapse, static-analysis regression, or cost spiral, expect apoptosis + automatic rollback (**LUX-1992 Tier 8 Canary**); the cause is recorded in the lineage DAG.

## 8. Session end
- Flush outstanding `knowledge_artifacts` to HIVE, release COORDINATION claims/locks, stop the heartbeat cleanly (or hand off), and set status = idle.

## Report
Summarize: machine + caste/role · planes connected (COORDINATION / MESH / HIVE) · ADRs + alignment loaded · review gate(s) engaged · peers seen · spend vs the $15/day cap · any degraded/offline planes.
