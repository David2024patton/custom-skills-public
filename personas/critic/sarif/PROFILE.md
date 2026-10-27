# Critic SARIF Profile (frozen, version critic-sarif-1)

SARIF 2.1.0 is the sole machine form of critic findings. The run verdict
never lives in SARIF; it lives in the evidence bundle verdict.json.

## Frozen properties (section 3.8 properties bag, critic: namespace)

On every result: critic:severity (critical, high, medium, low),
critic:rubricRef, critic:consensus (object: count, of, band),
critic:evidence (array, at least one entry; a finding with no evidence
entry is invalid), critic:smallestFix, critic:confidence (ordinal 1 to 10,
never averaged). On every rule: critic:severity and critic:rubricRef,
preserving the original rubric value.

## Mappings

Severity also maps to SARIF level and rank: critical = error, rank 90 to
100; high = error, rank 80; medium = warning, rank 55; low = note, rank 25.

## Fingerprints and baseline

Both partial fingerprints are always emitted: primaryLocationLineHash
and critic/findingHash. baselineState is all-or-nothing per run: either
every result in the run carries it or none does.

## Validation

sarif-validate.py runs profile lint always, plus the official SARIF
2.1.0 JSON Schema when a schema file and the jsonschema package are
available. The validator itself missing is exit 2, never a pass.
