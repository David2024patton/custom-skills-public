# Actions Workflows: Run Lifecycle and Diagnosis

Route here for any Actions run or workflow problem: a red run, a stuck
run, a manual dispatch, a rerun decision.

## Hard rules

- Read the failed step's log first. Never rerun blind, and never report
  a run green from the run list alone: read the run back.
- Rerun failed jobs only, first (`gh run rerun --failed`). A full rerun
  is for when the failure is in setup or the runner itself.
- Classify every failure before acting: infra, flaky suspect, or real.
  The classification, with its evidence line, is part of the report.
- Cancelling a run is a write against shared state. Cancel only the run
  you were asked about, by ID, and read its state back.

## Run lifecycle

```bash
gh run list --limit 20                                  # recent runs
gh run list --workflow ci.yml --branch <branch>         # one workflow
gh run view <RUN_ID>                                    # jobs and steps
gh run watch <RUN_ID>                                   # wait for completion
gh run view <RUN_ID> --log-failed                       # failed step logs
gh run rerun <RUN_ID> --failed                          # failed jobs only
gh run cancel <RUN_ID>                                  # then read back:
gh run view <RUN_ID> --json status,conclusion
gh workflow run <workflow>.yml --ref <branch> -f key=value   # dispatch with inputs
gh workflow list                                        # dispatchable workflows
```

Every command above ends in a read-back: after a rerun or a dispatch,
list runs again and name the new run ID and its state. A dispatch that
produced no run is a failure to report, not a success to assume.

## Classification loop

1. Read the failed step's log tail. Name the exact step and line.
2. Infra: runner loss, network fetch failures to registries, disk or
   permission errors in setup, GitHub side incidents. Evidence: the log
   line names the environment, not the code. Action: rerun failed only.
3. Flaky suspect: the same step passed on the same commit before, or
   the failure is timing, ordering, or an external service's transient
   error, and no code path in the diff touches it. Action: rerun failed
   only, once, and record the suspicion. A second identical failure
   reclassifies it as real.
4. Real: the failing assertion, compile error, or lint hit maps to code
   in the change. Action: fix the code; a rerun without a fix is noise.

## Done

The run in question is read back in its final state, the classification
and its evidence line are stated, and any rerun or dispatch is named by
its new run ID.

## Worked example EX-A1: a red CI run diagnosed end to end

```bash
gh run list --branch fix/login --limit 5
# 8123456789  completed  failure  CI  fix/login
gh run view 8123456789 --log-failed | tail -100
# step "go test ./...": FAIL: TestSessionExpiry, expected 401, got 200
```

Classification: real. The failing test names behavior changed in this
branch's diff; no environment error appears in the log. The fix lands
in the session code, a new run is pushed, and the read-back is:

```bash
gh run list --branch fix/login --limit 1
# 8123456790  completed  success  CI  fix/login
```

Report: run 8123456789, real failure in TestSessionExpiry, fixed in
the named commit, verified by run 8123456790 read back as success.
