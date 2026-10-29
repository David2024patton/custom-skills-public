#!/usr/bin/env python3
# probe-runner.py - P-12 runtime observation and perturbation proof;
# P-13 single-variable claims probes.
# Steps:
#   scenario mode (--scenario FILE): the scenario JSON declares target,
#     input, expected result, failure signal, and stopping condition
#     BEFORE the run. The runner copies the artifact to a temp
#     directory and runs the declared command there, and records
#     output, exit code, process lifetime, and file effects as an
#     evidence record. Static and runtime evidence correlate only
#     through the mapping entry the caller writes from this record.
#     ISOLATION, stated plainly: a temp directory is a scratch space,
#     not a sandbox. The command executes ON THE HOST with the
#     reviewer's privileges and can reach whatever the host can reach.
#     Commands run as argv lists, never through a shell, with the
#     environment scrubbed to a small allowlist, which removes shell
#     injection and casual secret leakage; it does not contain a
#     hostile program. Run only scenarios whose command the operator
#     has read, on a host where executing artifact code is acceptable
#     (SOUL 8.12 carries the same warning).
#   Scenario verdict: the run FAILS when the exit code differs from
#     the declared expected_exit (default 0), when the declared
#     failure signal appears in stdout OR stderr, or when the run
#     exceeds the declared stopping condition (a duration such as
#     "30s" or "45", which becomes the timeout). expect_in_stdout:
#     false is valid only with a declared alternative_observable of
#     the form "stderr:<text>", "file:<relative path>", or "exit";
#     anything else is invalid input (exit 4).
#   perturb mode (--perturb FILE, --find TEXT, --replace TEXT,
#     --test-cmd CMD): copy the artifact, run the test command (must
#     pass), apply exactly one single-variable perturbation in the
#     COPY, run the test command again (must go red). A test that stays
#     green under its perturbation is a finding against the test.
#     The artifact under review is never mutated in place: the runner
#     hashes the original tree before and after and fails closed
#     (exit 2) if it changed.
# Exit codes: 0 probe behaved as declared (scenario matched, or the
# perturbed test went red); 1 finding (scenario mismatch, or a test
# green under perturbation); 2 runner could not run or the original
# artifact changed; 4 scenario invalid.
# Python 3 standard library only.
import argparse, hashlib, json, os, re, shlex, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ENV_ALLOWLIST = ("PATH", "HOME", "LANG", "LC_ALL", "TZ", "TMPDIR", "SYSTEMROOT", "WINDIR")

def scrubbed_env():
    env = {k: os.environ[k] for k in ENV_ALLOWLIST if k in os.environ}
    env["CRITIC_PROBE"] = "1"
    return env

def to_argv(cmd):
    if isinstance(cmd, list):
        return [str(c) for c in cmd]
    return shlex.split(str(cmd))

def tree_hash(root):
    h = hashlib.sha256()
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(root)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()

def run_cmd(cmd, cwd, timeout=120):
    start = time.time()
    try:
        r = subprocess.run(to_argv(cmd), shell=False, cwd=cwd, capture_output=True,
                           text=True, timeout=timeout, env=scrubbed_env())
        return r.returncode, (r.stdout or "")[-4000:], (r.stderr or "")[-2000:], round(time.time() - start, 2)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout", round(time.time() - start, 2)
    except FileNotFoundError as e:
        return 127, "", f"command not found: {e}", round(time.time() - start, 2)

def parse_stopping(value):
    """Stopping condition as a duration: '30s', '45', 60, '2m'. None if unparseable."""
    if isinstance(value, (int, float)):
        return float(value)
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(s|sec|seconds|m|min|minutes)?\s*", str(value), re.I)
    if not m:
        return None
    n = float(m.group(1))
    if (m.group(2) or "s").lower().startswith("m"):
        n *= 60.0
    return n

def main():
    ap = argparse.ArgumentParser(description="Runtime and perturbation probes (P-12, P-13)")
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--scenario", default=None)
    ap.add_argument("--perturb", default=None, help="file inside the artifact copy to perturb")
    ap.add_argument("--find", default=None)
    ap.add_argument("--replace", default=None)
    ap.add_argument("--test-cmd", default=None)
    args = ap.parse_args()
    src = Path(args.artifact)
    if not src.is_dir():
        print(json.dumps({"error": f"artifact not a directory: {src}"}))
        return 2
    before = tree_hash(src)
    workdir = Path(tempfile.mkdtemp(prefix="critic-probe-"))
    copy = workdir / "copy"
    shutil.copytree(src, copy)
    result = {}
    code = 0
    try:
        if args.scenario:
            sc = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
            for field in ("target", "input", "expected_result", "failure_signal", "stopping_condition", "command"):
                if field not in sc:
                    print(json.dumps({"error": f"scenario missing declared field: {field}"}))
                    return 2
            timeout = parse_stopping(sc["stopping_condition"])
            if timeout is None:
                print(json.dumps({"error": "scenario invalid: stopping_condition is not a duration "
                                           "(declare one such as '30s'); an unenforceable stopping "
                                           "condition cannot ground a verdict"}))
                return 4
            alt = sc.get("alternative_observable")
            if sc.get("expect_in_stdout", True) is False and not (
                    isinstance(alt, str) and (alt.startswith("stderr:") or alt.startswith("file:") or alt == "exit")):
                print(json.dumps({"error": "scenario invalid: expect_in_stdout is false but no "
                                           "alternative_observable is declared (stderr:<text>, "
                                           "file:<relative path>, or exit)"}))
                return 4
            rc, out, err, secs = run_cmd(sc["command"], copy, timeout=timeout)
            effects = sorted(str(p.relative_to(copy)) for p in copy.rglob("*") if p.is_file())
            expected_exit = int(sc.get("expected_exit", 0))
            timed_out = rc == 124
            exit_ok = rc == expected_exit
            failure_seen = bool(sc["failure_signal"]) and (sc["failure_signal"] in out or sc["failure_signal"] in err)
            if sc.get("expect_in_stdout", True):
                observed = sc["expected_result"] in out
            elif alt == "exit":
                observed = exit_ok
            elif alt.startswith("stderr:"):
                observed = alt[len("stderr:"):] in err
            else:
                observed = (copy / alt[len("file:"):]).is_file()
            matched = bool(exit_ok and observed and not failure_seen
                           and (not timed_out or expected_exit == 124))
            result = {"mode": "scenario", "scenario": {k: sc[k] for k in ("target", "input", "expected_result", "failure_signal", "stopping_condition")},
                      "exit_code": rc, "expected_exit": expected_exit, "exit_matches_declared": exit_ok,
                      "failure_signal_seen": failure_seen, "timed_out": timed_out,
                      "stopping_condition_seconds": timeout,
                      "lifetime_seconds": secs, "stdout_tail": out, "stderr_tail": err,
                      "files_in_copy_after_run": effects, "expected_result_observed": observed,
                      "verdict": "matched" if matched else "finding"}
            code = 0 if matched else 1
        elif args.perturb and args.test_cmd and args.find is not None:
            rc0, out0, _, _ = run_cmd(args.test_cmd, copy)
            if rc0 != 0:
                print(json.dumps({"error": "baseline test run is not green; perturbation proof needs a green baseline", "baseline_exit": rc0}))
                return 2
            target = copy / args.perturb
            text = target.read_text(encoding="utf-8")
            if args.find not in text:
                print(json.dumps({"error": "perturbation anchor text not found in copy"}))
                return 2
            target.write_text(text.replace(args.find, args.replace or "", 1), encoding="utf-8")
            rc1, out1, _, _ = run_cmd(args.test_cmd, copy)
            went_red = rc1 != 0
            result = {"mode": "perturb", "file": args.perturb, "baseline_exit": rc0,
                      "perturbed_exit": rc1, "test_went_red": went_red,
                      "finding": None if went_red else "test stayed green under perturbation: finding against the test, severity by the claim it carried"}
            code = 0 if went_red else 1
        else:
            print(json.dumps({"error": "give --scenario, or --perturb with --find, --replace, --test-cmd"}))
            return 2
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    if tree_hash(src) != before:
        print(json.dumps({"error": "original artifact changed during probe; failing closed"}))
        return 2
    result["artifact_unmodified"] = True
    print(json.dumps(result, indent=2))
    return code

if __name__ == "__main__":
    sys.exit(main())
