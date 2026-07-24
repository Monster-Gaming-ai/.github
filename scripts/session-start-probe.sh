#!/usr/bin/env bash
# session-start-probe.sh — Monster Gaming hivemind connectivity probe.
#
# Part of the /session-start bootstrap (see .cursor/commands/session-start.md).
# Reports whether the fleet's planes are reachable from the current agent
# environment:
#   COORDINATION -> coord.monstergaming.ai (registry / heartbeat / gates)
#   MESH         -> NATS JetStream monitoring endpoint
#   HIVE         -> knowledge_artifacts store
#
# Endpoints/tokens resolve from /etc/monstergaming/agent.conf (KEY=VALUE lines);
# environment variables override the file. Secret values are NEVER printed.
# This probe is read-only and always exits 0 (non-blocking bootstrap step).

set -u

AGENT_CONF="${MG_AGENT_CONF:-/etc/monstergaming/agent.conf}"
TIMEOUT="${SESSION_START_PROBE_TIMEOUT:-5}"

# conf_get KEY -> prints value from AGENT_CONF (strips surrounding quotes), or empty.
conf_get() {
  [ -r "$AGENT_CONF" ] || return 0
  local line
  line="$(grep -E "^[[:space:]]*$1[[:space:]]*=" "$AGENT_CONF" 2>/dev/null | tail -1)"
  [ -n "$line" ] || return 0
  local val="${line#*=}"
  val="${val#"${val%%[![:space:]]*}"}"   # ltrim
  val="${val%"${val##*[![:space:]]}"}"   # rtrim
  val="${val%\"}"; val="${val#\"}"
  val="${val%\'}"; val="${val#\'}"
  printf '%s' "$val"
}

# Resolve endpoints: env override -> conf file -> default.
COORD_URL="${MG_COORD_URL:-$(conf_get COORD_URL)}"; COORD_URL="${COORD_URL:-https://coord.monstergaming.ai}"
COORD_HEALTH="${MG_COORD_HEALTH_PATH:-/healthz}"
COORD_TOKEN="${MG_COORD_TOKEN:-$(conf_get COORD_TOKEN)}"

MESH_URL="${MG_NATS_MONITOR_URL:-$(conf_get NATS_MONITOR_URL)}"   # e.g. http://nexus:8222
MESH_HEALTH="${MG_NATS_HEALTH_PATH:-/healthz}"

HIVE_URL="${MG_HIVE_URL:-$(conf_get HIVE_URL)}"
HIVE_HEALTH="${MG_HIVE_HEALTH_PATH:-/healthz}"
HIVE_TOKEN="${MG_HIVE_TOKEN:-$(conf_get HIVE_TOKEN)}"

have_curl=1; command -v curl >/dev/null 2>&1 || have_curl=0
connected=0; degraded=0

if [ -r "$AGENT_CONF" ]; then
  echo "config: reading $AGENT_CONF (secret values not shown)"
else
  echo "config: $AGENT_CONF not present — using env overrides / defaults"
fi
echo

printf '%-14s %-10s %-9s %s\n' "PLANE" "CONFIGURED" "STATUS" "DETAIL"
printf '%-14s %-10s %-9s %s\n' "-----" "----------" "------" "------"

# probe_plane NAME URL HEALTHPATH TOKEN
probe_plane() {
  local name="$1" url="$2" path="$3" token="$4"
  if [ -z "$url" ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "no" "DEGRADED" "no endpoint configured — offline mode"
    degraded=$((degraded + 1)); return
  fi
  if [ "$have_curl" -eq 0 ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "UNKNOWN" "curl unavailable — cannot probe $url"
    degraded=$((degraded + 1)); return
  fi
  local auth=(); [ -n "$token" ] && auth=(-H "Authorization: Bearer $token")
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" "${auth[@]}" "${url%/}${path}" 2>/dev/null)"
  if [ "$code" = "200" ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "OK" "${url%/}${path} -> 200"
    connected=$((connected + 1))
  else
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "DEGRADED" "${url%/}${path} -> ${code:-no-response}"
    degraded=$((degraded + 1))
  fi
}

probe_plane "COORDINATION" "$COORD_URL" "$COORD_HEALTH" "$COORD_TOKEN"
probe_plane "MESH"         "$MESH_URL"  "$MESH_HEALTH"  ""
probe_plane "HIVE"         "$HIVE_URL"  "$HIVE_HEALTH"  "$HIVE_TOKEN"

echo
echo "SUMMARY: ${connected} plane(s) connected, ${degraded} degraded/offline."
if [ "$connected" -eq 0 ]; then
  echo "NOTE: No hive planes reachable — proceeding in offline mode. Provide /etc/monstergaming/agent.conf"
  echo "      (or the MG_* env overrides) and ensure coord.monstergaming.ai / NATS / HIVE are reachable."
fi
exit 0
