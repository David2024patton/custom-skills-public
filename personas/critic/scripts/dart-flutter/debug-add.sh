#!/usr/bin/env bash
# PURPOSE: Print the standard Flutter diagnostic pattern (and scaffold
# lib/core/diag.dart with --apply): a tiny Diag service over the logging
# package, FlutterError.onError routed into it, and a debug surface
# (shake or settings entry) that shows recent events in debug builds.
# MODIFY PER PROJECT: the in-app debug surface entry point differs per
# app shell; wire it where the app keeps its settings.
# USAGE: dart-flutter/debug-add.sh [--apply] [app-dir]
# EXIT: 0 printed or scaffolded; 2 no lib/ when applying.
set -u
cat <<'EOF'
PATTERN:
  - Diag service: info/warn/refusal methods, ring buffer of last N
    events (N from config), every refusal in the app emits through it.
  - main(): FlutterError.onError and PlatformDispatcher.onError route
    into Diag; runZonedGuarded catches the rest.
  - Release builds log structured lines; debug builds also surface the
    ring in the app's debug screen.
EOF
if [ "${1:-}" = "--apply" ]; then
  d="${2:-.}"
  [ -d "$d/lib" ] || { echo "no lib/ in $d" >&2; exit 2; }
  mkdir -p "$d/lib/core"
  [ -f "$d/lib/core/diag.dart" ] || cat > "$d/lib/core/diag.dart" <<'EOF'
import 'dart:collection';
import 'package:flutter/foundation.dart';

/// Diagnostic channel: every refusal, overage, and verdict emits here.
class Diag {
  static const int _cap = 200;
  static final Queue<String> _ring = Queue<String>();
  static int refusals = 0;

  static void emit(String event, [Map<String, Object?> fields = const {}]) {
    if (event == 'refusal') refusals++;
    final line = '$event $fields';
    _ring.add(line);
    while (_ring.length > _cap) _ring.removeFirst();
    if (kDebugMode) debugPrint('diag: $line');
  }

  static List<String> recent() => List.unmodifiable(_ring);
}
EOF
  echo "scaffolded $d/lib/core/diag.dart"
fi
