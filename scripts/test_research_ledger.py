#!/usr/bin/env python3
"""Regression tests for skills/deep-research/scripts/research_ledger.py.

Finding NEW3b-01: add-hop writes the sequence number under the key
"hop" (cmd_add_hop), while cmd_lint read it under the key "n", so the
duplicate and sequential hop checks never fired and every CLI-built
ledger carried a spurious "some hops carry no sequence number" warning.

The canonical script is imported by path for the lint checks. Asserts:

  (1) a ledger with two hops both numbered 1 fails lint with the
      duplicate hop error and a nonzero exit;
  (2) a ledger with hops numbered 1 and 3 fails lint with the
      sequential numbering error and a nonzero exit;
  (3) a ledger built through the CLI's own add-hop path (run as a
      subprocess against the canonical script) lints with no
      "some hops carry no sequence number" warning.

Prints one PASS or FAIL line per test and exits nonzero on any failure.
Run: python3 scripts/test_research_ledger.py
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANONICAL = os.path.join(
    ROOT, "skills", "deep-research", "scripts", "research_ledger.py")

RESULTS = []


def report(name, ok, detail=""):
    RESULTS.append((name, ok))
    print("%s: %s%s" % ("PASS" if ok else "FAIL", name,
                         (" (%s)" % detail) if detail else ""))


def load_canonical():
    spec = importlib.util.spec_from_file_location(
        "research_ledger", CANONICAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cli(args):
    return subprocess.run([sys.executable, CANONICAL] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True, timeout=120)


def make_hop(number):
    return {
        "hop": number,
        "mode": "seed",
        "action": "fixture action %s" % number,
        "result": "fixture result",
        "next": "",
        "at": "2026-10-26T00:00:00",
    }


def make_ledger(hop_numbers):
    return {
        "version": 2,
        "question": "fixture question",
        "effort": "quick",
        "domain": "",
        "gate_g_waiver": None,
        "deliverable": "",
        "created": "2026-10-26T00:00:00",
        "hops": [make_hop(n) for n in hop_numbers],
        "evidence": [
            {
                "id": "E0001",
                "title": "Fixture source",
                "url": "https://example.org/fixture",
                "publisher": "Fixture",
                "date": "2026-10-26",
                "tier": "A",
                "stance": "supports",
                "claim": "fixture claim",
                "locator": "",
                "interest": "none",
                "access": "full",
                "kind": "",
                "repo_stars": "",
                "repo_license": "",
                "repo_last_activity": "",
                "repo_fit_note": "",
                "repo_technique": "",
            }
        ],
        "claims": [
            {
                "id": "C0001",
                "claim": "fixture claim",
                "importance": "medium",
                "status": "probable",
                "evidence": ["E0001"],
                "source_tier": "A",
                "locator": "",
                "freshness": "",
                "counterevidence_checked": "yes",
                "counterevidence": "",
                "access": "full",
                "final_wording": "fixture claim",
            }
        ],
    }


def write_run(base, name, hop_numbers):
    run_dir = os.path.join(base, name)
    os.makedirs(run_dir)
    with open(os.path.join(run_dir, "ledger.json"), "w",
              encoding="utf-8") as fh:
        json.dump(make_ledger(hop_numbers), fh, indent=2)
        fh.write("\n")
    with open(os.path.join(run_dir, "report.md"), "w",
              encoding="utf-8") as fh:
        fh.write("# fixture question\n\nFixture finding [E0001].\n")
    return run_dir


def lint_via_import(module, run_dir):
    buf = io.StringIO()
    args = argparse.Namespace(run_dir=run_dir, allow_warnings=False)
    with contextlib.redirect_stdout(buf):
        rc = module.cmd_lint(args)
    return rc, buf.getvalue()


def test_duplicate_hops(module, base):
    run_dir = write_run(base, "duplicate", [1, 1])
    rc, out = lint_via_import(module, run_dir)
    ok = rc != 0 and "duplicate hop numbers present" in out
    report("two hops both numbered 1 fail lint with the duplicate "
           "hop error and a nonzero exit", ok,
           "exit=%d out=%s" % (rc, out.strip().replace("\n", "; ")[:300]))


def test_non_sequential_hops(module, base):
    run_dir = write_run(base, "non-sequential", [1, 3])
    rc, out = lint_via_import(module, run_dir)
    ok = rc != 0 and "hop numbering is not sequential" in out
    report("hops numbered 1 and 3 fail lint with the sequential "
           "numbering error and a nonzero exit", ok,
           "exit=%d out=%s" % (rc, out.strip().replace("\n", "; ")[:300]))


def test_cli_built_ledger_has_no_unnumbered_warning(base):
    out_dir = os.path.join(base, "cli-out")
    os.makedirs(out_dir)
    proc = run_cli(["init", "--question", "fixture question",
                    "--out-dir", out_dir, "--effort", "quick"])
    if proc.returncode != 0:
        report("ledger built through the CLI add-hop path lints with "
               "no unnumbered hop warning", False,
               "init exited %d: %s" % (proc.returncode,
                                       proc.stderr.strip()[:200]))
        return
    run_dir = proc.stdout.strip().splitlines()[-1].strip()
    for i in (1, 2):
        proc = run_cli(["add-hop", "--run-dir", run_dir,
                        "--mode", "seed",
                        "--action", "fixture action %d" % i,
                        "--result", "fixture result"])
        if proc.returncode != 0:
            report("ledger built through the CLI add-hop path lints "
                   "with no unnumbered hop warning", False,
                   "add-hop exited %d: %s" % (
                       proc.returncode, proc.stderr.strip()[:200]))
            return
    proc = run_cli(["add-evidence", "--run-dir", run_dir,
                    "--title", "Fixture source",
                    "--url", "https://example.org/fixture",
                    "--publisher", "Fixture",
                    "--date", "2026-10-26",
                    "--tier", "A",
                    "--claim", "fixture claim"])
    if proc.returncode != 0:
        report("ledger built through the CLI add-hop path lints with "
               "no unnumbered hop warning", False,
               "add-evidence exited %d: %s" % (
                   proc.returncode, proc.stderr.strip()[:200]))
        return
    proc = run_cli(["add-claim", "--run-dir", run_dir,
                    "--claim", "fixture claim",
                    "--importance", "medium",
                    "--status", "probable",
                    "--evidence", "E0001",
                    "--tier", "A",
                    "--counterevidence-checked", "yes",
                    "--final-wording", "fixture claim"])
    if proc.returncode != 0:
        report("ledger built through the CLI add-hop path lints with "
               "no unnumbered hop warning", False,
               "add-claim exited %d: %s" % (
                   proc.returncode, proc.stderr.strip()[:200]))
        return
    with open(os.path.join(run_dir, "report.md"), "w",
              encoding="utf-8") as fh:
        fh.write("# fixture question\n\nFixture finding [E0001].\n")
    proc = run_cli(["lint", "--run-dir", run_dir])
    out = (proc.stdout or "") + (proc.stderr or "")
    ok = ("some hops carry no sequence number" not in out
          and proc.returncode == 0)
    report("ledger built through the CLI add-hop path lints with no "
           "unnumbered hop warning", ok,
           "exit=%d out=%s" % (proc.returncode,
                               out.strip().replace("\n", "; ")[:300]))


def main():
    if not os.path.isfile(CANONICAL):
        report("canonical research_ledger.py exists at the imported "
               "path", False, CANONICAL)
        print("test_research_ledger: 0 passed, 1 failed")
        return 1
    module = load_canonical()
    with tempfile.TemporaryDirectory() as base:
        test_duplicate_hops(module, base)
        test_non_sequential_hops(module, base)
        test_cli_built_ledger_has_no_unnumbered_warning(base)
    failed = [n for n, ok in RESULTS if not ok]
    print("test_research_ledger: %d passed, %d failed"
          % (len(RESULTS) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
