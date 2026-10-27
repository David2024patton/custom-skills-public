#!/usr/bin/env python3
# probe-runner.py - P-12 runtime observation and perturbation proof;
# P-13 single-variable claims probes.
# Steps:
#   scenario mode (--scenario FILE): the scenario JSON declares target,
#     input, expected result, failure signal, and stopping condition
#     BEFORE the run. The runner copies the artifact to an isolated
#     temp directory, runs the declared command there, and records
#     output, exit code, process lifetime, and file effects as an
#     evidence record. Static and runtime evidence correlate only
#     through the mapping entry the caller writes from this record.
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
# artifact changed.
# Python 3 standard library only.
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

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
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "")[-4000:], (r.stderr or "")[-2000:], round(time.time() - start, 2)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout", round(time.time() - start, 2)

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
            rc, out, err, secs = run_cmd(sc["command"], copy)
            effects = sorted(str(p.relative_to(copy)) for p in copy.rglob("*") if p.is_file())
            matched = (sc["expected_result"] in out) if sc.get("expect_in_stdout", True) else True
            result = {"mode": "scenario", "scenario": {k: sc[k] for k in ("target", "input", "expected_result", "failure_signal", "stopping_condition")},
                      "exit_code": rc, "lifetime_seconds": secs, "stdout_tail": out, "stderr_tail": err,
                      "files_in_copy_after_run": effects, "expected_result_observed": matched}
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
