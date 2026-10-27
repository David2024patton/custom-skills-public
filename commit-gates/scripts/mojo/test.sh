#!/usr/bin/env bash
# PURPOSE: Mojo test gate: run the project's tests in test/ or tests/.
# HONEST TOOLING NOTE: `mojo test` is a real shipped command but
# Modular's current docs mark it DEPRECATED (docs.modular.com/mojo/
# cli/test) in favour of the in-language TestSuite framework with
# user-defined orchestration. This script keeps `mojo test` because
# it is the closest real analogue of the other languages' test
# runners and is the form audit_code uses; a project that has moved
# to TestSuite runners records its own test command in the repo
# RULES page and this gate is replaced by it, not silently skipped.
# MODIFY PER PROJECT: none. The -I . include path matches audit_code
# so tests can import the project's own modules.
# USAGE: mojo/test.sh [dir]
# EXIT: 0 pass; 1 fail or no test directory; 2 mojo toolchain missing.
set -u
cd "${1:-.}" || exit 2
if [ -f pixi.toml ] && command -v pixi >/dev/null 2>&1; then MOJO="pixi run mojo"
elif command -v mojo >/dev/null 2>&1; then MOJO="mojo"
else echo "mojo not found (install Mojo, or pixi with a Mojo project)" >&2; exit 2; fi
if [ -d test ]; then T="test"
elif [ -d tests ]; then T="tests"
else echo "no test/ or tests/ directory: add tests, or record the exception in the repo RULES page" >&2; exit 1; fi
$MOJO test -I . "$T"
