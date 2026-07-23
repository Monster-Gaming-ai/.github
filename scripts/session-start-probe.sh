#!/usr/bin/env bash
# session-start-probe.sh — Monster Gaming stack connectivity probe.
#
# Part of the /session-start bootstrap (see .cursor/commands/session-start.md).
# Reports which stack planes (HIVE, MESH, COORDINATION) are configured and
# reachable from the current agent environment. Never fabricates a connection;
# absent/unreachable planes are reported as degraded so the agent can proceed
# in offline mode. This probe is read-only and always exits 0 (non-blocking).

set -u

# plane | URL var | TOKEN var | health path
PLANES=(
  "COORDINATION|LUXAGENTOS_HTTP_URL|LUXAGENTOS_TOKEN|/healthz"
  "HIVE|HIVE_URL|HIVE_TOKEN|/healthz"
  "MESH|MESH_URL|MESH_TOKEN|/healthz"
)

TIMEOUT="${SESSION_START_PROBE_TIMEOUT:-5}"
have_curl=1
command -v curl >/dev/null 2>&1 || have_curl=0

connected=0
degraded=0

printf '%-14s %-10s %-9s %s\n' "PLANE" "CONFIGURED" "STATUS" "DETAIL"
printf '%-14s %-10s %-9s %s\n' "-----" "----------" "------" "------"

for entry in "${PLANES[@]}"; do
  IFS='|' read -r name url_var tok_var path <<<"$entry"
  url="${!url_var:-}"
  tok="${!tok_var:-}"

  if [ -z "$url" ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "no" "DEGRADED" "$url_var unset — offline mode"
    degraded=$((degraded + 1))
    continue
  fi

  auth=()
  [ -n "$tok" ] && auth=(-H "Authorization: Bearer $tok")

  if [ "$have_curl" -eq 0 ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "UNKNOWN" "curl unavailable — cannot probe $url"
    degraded=$((degraded + 1))
    continue
  fi

  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" "${auth[@]}" "${url%/}${path}" 2>/dev/null)"
  if [ "$code" = "200" ]; then
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "OK" "${url%/}${path} -> 200"
    connected=$((connected + 1))
  else
    printf '%-14s %-10s %-9s %s\n' "$name" "yes" "DEGRADED" "${url%/}${path} -> ${code:-no-response}"
    degraded=$((degraded + 1))
  fi
done

echo
echo "SUMMARY: ${connected} plane(s) connected, ${degraded} degraded/offline."
if [ "$connected" -eq 0 ]; then
  echo "NOTE: No stack planes reachable — proceeding in fully offline mode. Set the plane URL/token vars (or add them as secrets) to enable HIVE/MESH/COORDINATION."
fi
exit 0
