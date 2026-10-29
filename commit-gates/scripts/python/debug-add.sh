#!/usr/bin/env bash
# PURPOSE: Print the standard Python diagnostic pattern: logging
# configured once at startup (structured format, level from env), a
# diag() helper for refusals/verdicts with a counter, and exception
# hooks routed into it. Tools and one-off scripts get the same shape
# at smaller scale.
# MODIFY PER PROJECT: log destination differs (stderr for CLIs, file
# or journald for services); the shape does not change.
# USAGE: python/debug-add.sh
# EXIT: 0.
cat <<'EOF'
PATTERN:
  import logging, os
  logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"),
      format="%(asctime)s %(levelname)s %(name)s %(message)s")
  log = logging.getLogger("diag")
  REFUSALS = 0
  def diag(event, **fields):
      global REFUSALS
      if event == "refusal": REFUSALS += 1
      log.info("diag %s %s", event, fields)
  Every refusal path calls diag("refusal", why=...) exactly once.
EOF
