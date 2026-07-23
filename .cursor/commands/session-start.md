# /session-start — Monster Gaming stack bootstrap

Run this protocol at the **start of every agent session, before any task work**. Its purpose is to maximize reliance on Monster Gaming AI's own stack — **HIVE, MESH, COORDINATION, ADRs, and rules** — instead of operating in isolation.

Connection endpoints and tokens are supplied via environment variables / secrets (never hardcode them):

| Plane | URL var | Token var | Role |
|-------|---------|-----------|------|
| COORDINATION | `LUXAGENTOS_HTTP_URL` | `LUXAGENTOS_TOKEN` | HTTP coordinator (`luxagentos_http`): task claims, locks, gate state |
| HIVE | `HIVE_URL` | `HIVE_TOKEN` | Shared knowledge / memory store (`knowledge_artifacts`) |
| MESH | `MESH_URL` | `MESH_TOKEN` | Fleet registry + inter-node messaging |

First, probe connectivity and print the plane status table:

```bash
bash scripts/session-start-probe.sh
```

If a plane is unreachable or its vars are absent, record the gap and continue in **degraded/offline mode** — never fabricate a connection.

## 0. Identify self
- Resolve run identity (cloud run id, repo, branch, model, owner). Use `cursor-cloud-run-info` when available.
- Derive the node label (e.g. `mac_pro`, `Wintermute`, `Neuromancer`, `Valentine`, or this cloud run id).

## 1. COORDINATION (claim + gates) — `luxagentos_http`
- Announce session start to the HTTP coordinator.
- Claim the current task / acquire needed locks so peers don't collide.
- Pull active gate state. Honor destructive **PRE-JAKE gates only**: force-push `main`, `DELETE knowledge_artifacts`, spend caps. Never request smart-mode/approval for anything else.

## 2. MESH (presence + peers)
- Register presence and set status = `active`.
- Discover live peers across the fleet; note who else is working to avoid duplicate/conflicting work.

## 3. HIVE (knowledge + memory)
- Query HIVE for `knowledge_artifacts` relevant to this repo/task; load prior decisions and context.
- Treat HIVE as the source of truth for accumulated learnings. Prefer it over re-deriving.

## 4. ADRs + rules (binding context)
- Load Architecture Decision Records and operating rules from the stack; treat them as binding constraints.
- Reconcile the task against existing ADRs before proposing new designs.

## 5. Failure / block handling
- On an **Auto-review block**: do NOT retry the same blocked command in an approval loop. Take an alternate path **in the same turn** — BUILD SSH hop, Forgejo bare push, or HTTP coord via `luxagentos_http`.

## 6. During the session
- Write decisions, artifacts, and learnings back to HIVE.
- Keep COORDINATION claim/lock state and MESH status current.

## 7. Session end
- Flush outstanding knowledge to HIVE, release COORDINATION locks, set MESH status = `idle`.

## Report
End the bootstrap with a short summary: which planes connected (HIVE / MESH / COORDINATION), ADRs/rules loaded, peers seen, and any degraded/offline planes.
