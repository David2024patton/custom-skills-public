# Calibration: seed bank (P-07)

Versioned bank of planted defects used to measure whether the five-critic panel can still find what it claims to find.

## Files

- `seed-bank.json`: the bank handed to the injector. 40 seeds, stratified lens x severity x difficulty (5 lenses x 4 severities x 2 difficulties: local-obvious, cross-file). Each insertion is realistic defective content for its lens (a route handler with no auth check, a percentage with no provenance, a pre-checked consent box), written so the defect sits on the first inserted line. The review copy carries no seed IDs, no class labels, and no markers of any kind: there is nothing in the copy that identifies a line as planted.
- `ground-truth.json`: location and reachability for every seed, plus the expected finding. Kept separate from the bank on purpose. The oracle is maintained independently of the critics' own tooling; consensus among the five is never the oracle.
- `seed-runner.py`: injects the bank into a review copy (never the shipping tree), runs the panel, scores catch per lens, per severity, per critic, and panel union. A catch requires a finding line naming the target file, a line within 3 of the defect line, and the defect class token; a bare seed ID in the output scores nothing.
- `make-fixture.py`: generates the clean fixture artifact the ground truth points at.

## The fixture

The ground truth names locations such as `fixture-app/code/module-01.txt:13`. That tree is generated, not hand-maintained:

```
python3 make-fixture.py --out fixture-app
```

Every module file carries exactly 12 clean lines, so each seed's defect lands on line 13 of its target in the review copy. The content is ordinary and defect-free for its lens, and a few lines are cross-reference anchors (the original wording of a quotation, the full-year figures, the governing 72-hour commitment) that the cross-file seeds point at from sibling modules. The runner verifies the injected line against the ground truth for every seed and refuses to score when they disagree, so editing the fixture without regenerating the truth fails loudly instead of mis-scoring quietly. Pass the fixture-app directory itself as `--artifact`; the runner strips the bank-relative `fixture-app/` prefix when resolving targets.

## Custody of the ground truth

The operator holds the authoritative ground-truth copy OUTSIDE the ingested tree and passes its path to the runner. A run scored against a ground-truth file that sits inside the tree under review is invalid: the panel could read the oracle, so the measurement proves nothing. The runner detects that case, prints a warning, and marks the report `valid: false` with `custody_ok: false`. The copy of ground-truth.json that ships in this folder is the authoring copy; the run's authoritative copy lives with the operator.

## The fixture critic

`--use-fixture-critic` runs a built-in detector with a per-class signature table (a handler block with no auth token, SQL built by concatenation, a tap target under 44px, a strengthened quotation found by cross-file comparison, and so on). It proves the harness plumbing end to end: injection lands where the truth says, detectors can find the planted patterns, scoring matches on file, line, and class. It is not evidence about a real panel, and its catch rate must never be quoted as panel skill: a signature table written against the bank's own classes will of course catch the bank.

## Rules

- Calibration runs blind at least every 10th production pass and after any model, prompt, or checklist change.
- A calibration record without model ID, prompt hash, and checklist hash is void. The runner refuses it (exit 2).
- Report-first: calibration earns gate status only with measured history. Until then the runner reports and never blocks a verdict.
- At least 25 percent of the bank rotates quarterly, sourced from escape postmortems (real defects the panel missed).
- Seed calibration (leading, sensitivity on demand) and escape calibration (lagging, production defects adjudicated for whether the panel had scope to see them) live in separate ledger columns and are never averaged.
- A lens patch ships with its before and after catch delta on this bank, or is labelled unmeasured.
