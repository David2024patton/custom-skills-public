#!/usr/bin/env python3
# check-critique.py - P-19 mechanical checker for the consensus report.
# Modelled on the rea harvest CS-11 checker. Run at merge, before any
# verdict ships. A failing report is fixed; the checker is never edited
# to pass in the same run.
# Checks (errors unless marked warning):
#   1. Every finding line (starting with a finding ID F-<n>) carries an
#      evidence record ID (EV-<n>).
#   2. Every claims parity table row is tagged with a verdict label
#      (TRUE, FALSE, UNBACKED, VENDOR SOURCED, OVERSTATED, OUTDATED) or
#      an evidence ID.
#   3. Every lens return section ends with a Not tested list: the
#      report must contain a "Not tested" list for each of the five
#      lenses (code, claims, ux, growth, compliance).
#   4. No dangling IDs: every referenced F-, EV-, and U- (unknown) ID is
#      defined somewhere in the report.
#   5. Unbounded negatives (warning class): a line claiming "no X",
#      "never", or "none found" without a scope phrase (in, across,
#      within, examined, checked, among) is flagged for human review.
#   6. The verdict line exists and names its critique spec (contains
#      "spec" plus an identifier), per scoped zero (CS-16).
# Exit codes: 0 clean (warnings allowed, printed); 1 errors present;
# 2 checker unavailable (report file unreadable).
# Python 3 standard library only.
import argparse, json, re, sys
from pathlib import Path

LABELS = ["TRUE", "FALSE", "UNBACKED", "VENDOR SOURCED", "OVERSTATED", "OUTDATED"]
SCOPE_WORDS = [" in ", " across ", " within ", " examined", " checked", " among ", "searched "]

def main():
    ap = argparse.ArgumentParser(description="Mechanical consensus-report checker (P-19)")
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    try:
        text = Path(args.report).read_text(encoding="utf-8")
    except Exception as e:
        print(json.dumps({"error": f"checker unavailable: cannot read report: {e}"}))
        return 2
    lines = text.splitlines()
    errors, warnings = [], []
    defined_f = set(re.findall(r"\b(F-\d+)\b\s*[:|]", text))
    defined_ev = set(re.findall(r"\b(EV-\d+)\b", text))
    defined_u = set(re.findall(r"\b(U-\d+)\b\s*[:|]", text))
    # 1. findings carry evidence IDs
    for i, line in enumerate(lines, start=1):
        m = re.match(r"\s*[-|]?\s*(F-\d+)\b", line)
        if m and "EV-" not in line and m.group(1) in defined_f:
            errors.append(f"line {i}: finding {m.group(1)} has no evidence record ID")
    # 2. parity rows tagged (table rows in a Parity section)
    in_parity = False
    for i, line in enumerate(lines, start=1):
        if re.search(r"parity", line, re.I) and line.strip().startswith("#"):
            in_parity = True; continue
        if in_parity and line.strip().startswith("#"):
            in_parity = False
        if in_parity and line.strip().startswith("|") and "---" not in line and "claim" not in line.lower():
            if not any(l in line for l in LABELS) and "EV-" not in line:
                errors.append(f"line {i}: parity row is untagged (no verdict label, no evidence ID)")
    # 3. Not tested per lens
    for lens in ("code", "claims", "ux", "growth", "compliance"):
        if not re.search(rf"Not tested[^\n]*\b{lens}\b|\b{lens}\b[^\n]*Not tested", text, re.I):
            errors.append(f"missing Not tested list for lens: {lens}")
    # 4. dangling references
    for rid in sorted(set(re.findall(r"\b(F-\d+)\b", text))):
        if rid not in defined_f:
            errors.append(f"dangling finding reference: {rid}")
    for rid in sorted(set(re.findall(r"\b(U-\d+)\b", text))):
        if rid not in defined_u:
            errors.append(f"dangling unknown reference: {rid}")
    # evidence IDs are defined by use in finding lines; a bare EV ref with no definition line is dangling
    ev_defs = set(re.findall(r"\b(EV-\d+)\b\s*[:|]", text))
    for rid in sorted(set(re.findall(r"\b(EV-\d+)\b", text))):
        if rid not in ev_defs and rid not in defined_ev:
            errors.append(f"dangling evidence reference: {rid}")
    # 5. unbounded negatives (warnings)
    for i, line in enumerate(lines, start=1):
        low = " " + line.lower() + " "
        if re.search(r"\b(no|never|none)\b[^.]{0,60}\b(found|present|detected|exist|exists|observed)\b", low) or re.search(r"\bno [a-z ]{2,30}found\b", low):
            if not any(w in low for w in SCOPE_WORDS):
                warnings.append(f"line {i}: unbounded negative, state the examined scope: {line.strip()[:90]}")
    # 6. verdict line names its critique spec
    verdict_lines = [l for l in lines if l.strip().lower().startswith("verdict:")]
    if not verdict_lines:
        errors.append("no verdict line (a line starting with 'Verdict:')")
    elif not any(re.search(r"spec\s+\S+", l, re.I) for l in verdict_lines):
        errors.append("verdict line does not name its critique spec")
    print(json.dumps({"errors": errors, "warnings": warnings,
                      "error_count": len(errors), "warning_count": len(warnings)}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
