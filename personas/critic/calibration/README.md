# Calibration: seed bank (P-07)

Versioned bank of planted defects used to measure whether the five-critic panel can still find what it claims to find.

## Files

- `seed-bank.json`: the bank handed to the injector. 40 seeds, stratified lens x severity x difficulty (5 lenses x 4 severities x 2 difficulties: local-obvious, cross-file). Carries no expected findings.
- `ground-truth.json`: location and reachability for every seed, plus the expected finding. Kept separate from the bank on purpose. The oracle is maintained independently of the critics' own tooling; consensus among the five is never the oracle.
- `seed-runner.py`: injects the bank into a review copy (never the shipping tree), runs the panel, scores catch per lens, per severity, per critic, and panel union.

## Rules

- Calibration runs blind at least every 10th production pass and after any model, prompt, or checklist change.
- A calibration record without model ID, prompt hash, and checklist hash is void. The runner refuses it (exit 2).
- Report-first: calibration earns gate status only with measured history. Until then the runner reports and never blocks a verdict.
- At least 25 percent of the bank rotates quarterly, sourced from escape postmortems (real defects the panel missed).
- Seed calibration (leading, sensitivity on demand) and escape calibration (lagging, production defects adjudicated for whether the panel had scope to see them) live in separate ledger columns and are never averaged.
- A lens patch ships with its before and after catch delta on this bank, or is labelled unmeasured.
