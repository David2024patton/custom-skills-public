#!/usr/bin/env bash
# Threat feed refresh: CISA KEV + OSV. Stamps freshness. Run at the START of every security review.
set -u
PYTHON="python3"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON="python"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=py
OUT="${1:-threat-feed.txt}"
echo "=== Threat feed refresh: $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee "$OUT"

echo "--- CISA KEV (Known Exploited Vulnerabilities) ---" | tee -a "$OUT"
KEV=$(curl -fsS --max-time 30 https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json 2>/dev/null)
if [ -n "$KEV" ]; then
  echo "$KEV" | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print('catalogVersion:', d.get('catalogVersion')); print('count:', d.get('count')); print('title:', d.get('title'))" 2>/dev/null     || echo "$KEV" | grep -oE '"(catalogVersion|count|title)":[^,]*' | head -5
else
  echo "UNREACHABLE: CISA KEV feed did not respond. A clean scan on stale feeds is PROVISIONAL."
fi | tee -a "$OUT"

echo "--- OSV: scan committed lockfile if present ---" | tee -a "$OUT"
LOCK=""
for f in go.sum package-lock.json composer.lock Cargo.lock poetry.lock Pipfile.lock; do
  [ -f "$f" ] && LOCK="$f" && break
done
if [ -z "$LOCK" ]; then
  echo "no lockfile found (looked for go.sum, package-lock.json, composer.lock, Cargo.lock, poetry.lock, Pipfile.lock)" | tee -a "$OUT"
elif command -v osv-scanner >/dev/null 2>&1; then
  osv-scanner -L "$LOCK" 2>&1 | tee -a "$OUT"
else
  echo "osv-scanner not installed. Install: go install github.com/google/osv-scanner/cmd/osv-scanner@latest" | tee -a "$OUT"
  echo "or query OSV API: https://api.osv.dev/v1/query" | tee -a "$OUT"
fi
echo "Done. Record this freshness stamp in the report header." | tee -a "$OUT"
