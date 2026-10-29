#!/usr/bin/env bash
# PURPOSE: Print the standard PHP diagnostic pattern, and (when
# asked) scaffold diag.php into a PHP project directory. The
# pattern mirrors the other stacks: a diag helper with an emit
# method every refusal, overage, and verdict calls, and a refusal
# counter readable by status surfaces. The scaffold's sink is
# error_log (the one logging facility every PHP runtime has);
# hosted projects swap the sink inside diag.php (for example to a
# Monolog channel), never at call sites.
# MODIFY PER PROJECT: choose the sink per target at the seam, not
# at call sites. Refuses to overwrite an existing diag.php.
# USAGE: php/debug-add.sh [--apply] [project-dir]
# EXIT: 0 pattern printed or scaffold written; 2 no PHP sources
# when applying.
set -u
cat <<'EOF'
PATTERN (adapt names to the project):
  // diag.php
  final class Diag
  {
      public static int $refusals = 0;

      public static function emit(string $event, string $what): void
      {
          if ($event === 'refusal') {
              self::$refusals++;
          }
          error_log('diag ' . $event . ' ' . $what);
      }
  }
  Every refusal path calls Diag::emit('refusal', '...') exactly once.
  The counter lives in Diag so status surfaces can read it.
EOF
if [ "${1:-}" = "--apply" ]; then
  d="${2:-.}"
  ls "$d"/*.php >/dev/null 2>&1 || find "$d" -maxdepth 2 -name '*.php' -not -path '*/vendor/*' | grep -q . || { echo "no .php sources in $d" >&2; exit 2; }
  if [ -f "$d/diag.php" ]; then echo "$d/diag.php already exists"; exit 0; fi
  cat > "$d/diag.php" <<'EOF'
<?php
// Diagnostic channel: every refusal, overage, and verdict emits here.
// The sink is error_log in this scaffold; swap it inside this file
// only (for example to a Monolog channel), never at call sites.
declare(strict_types=1);

final class Diag
{
    public static int $refusals = 0;

    public static function emit(string $event, string $what): void
    {
        if ($event === 'refusal') {
            self::$refusals++;
        }
        error_log('diag ' . $event . ' ' . $what);
    }
}
EOF
  echo "scaffolded $d/diag.php: wire Diag::emit at every refusal point"
fi
