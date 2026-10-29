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
#   3. Every lens has its own Not tested list: for each of the five
#      lenses (code, claims, ux, growth, compliance) the report must
#      carry a distinct "Not tested" heading naming that lens, with at
#      least one list item under it. One combined line naming all five
#      lenses does not satisfy any lens.
#   4. No dangling IDs: every referenced F-, EV-, and U- (unknown) ID is
#      defined somewhere in the report. Evidence IDs are defined only
#      at definition sites (an EV-<n> followed by ":" or "|"); a bare
#      mention is a reference, never a definition.
#   7. Accessibility ceiling disclosure: a report that cites automated
#      accessibility results (axe, a11y) must carry the manifest's
#      a11yCeilingDisclosure, so a clean automated result is never read
#      as WCAG compliance. With --manifest the expected text is read
#      from the manifest; otherwise the shipped disclosure text is
#      required.
#   8. PDF deliverable accessibility (warning class): a report that
#      claims a PDF deliverable must state the deliverable accessibility
#      position (tagged PDF with heading order, Markdown named as the
#      accessible equivalent), per the SOUL output contract.
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
LENSES = ("code", "claims", "ux", "growth", "compliance")
# Fallback text of the manifest a11yCeilingDisclosure (critic.manifest.json);
# --manifest overrides it with the live manifest value.
A11Y_DISCLOSURE = ("Automated checks detect only a subset of WCAG issues. "
                   "This result means no automatically-detectable violations "
                   "were found; it does not mean WCAG compliant.")

def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()

def main():
    ap = argparse.ArgumentParser(description="Mechanical consensus-report checker (P-19)")
    ap.add_argument("--report", required=True)
    ap.add_argument("--manifest", default=None,
                    help="critic.manifest.json to read the a11y ceiling disclosure from")
    args = ap.parse_args()
    try:
        text = Path(args.report).read_text(encoding="utf-8")
    except Exception as e:
        print(json.dumps({"error": f"checker unavailable: cannot read report: {e}"}))
        return 2
    lines = text.splitlines()
    errors, warnings = [], []
    defined_f = set(re.findall(r"\b(F-\d+)\b\s*[:|]", text))
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
    # 3. Not tested per lens: each lens needs its own Not tested heading
    # with at least one list item under it, before the next heading. A
    # single combined line naming all five lenses satisfies none of them.
    heading_at = [i for i, l in enumerate(lines) if re.match(r"\s*#{1,6}\s", l)]
    def section_span(start):
        level = len(re.match(r"\s*(#{1,6})\s", lines[start]).group(1))
        end = len(lines)
        for j in heading_at:
            if j > start and len(re.match(r"\s*(#{1,6})\s", lines[j]).group(1)) <= level:
                end = j; break
        return start, end
    for lens in LENSES:
        found = False
        for i, line in enumerate(lines):
            if line.lstrip().startswith("#") and re.search(r"not tested", line, re.I) \
                    and re.search(rf"\b{lens}\b", line, re.I):
                s, e = section_span(i)
                if any(re.match(r"\s*[-*]\s+\S", lines[k]) for k in range(s + 1, e)):
                    found = True; break
        if not found:
            errors.append(f"missing Not tested list for lens: {lens} "
                          f"(needs its own Not tested heading with at least one list item)")
    # 4. dangling references
    for rid in sorted(set(re.findall(r"\b(F-\d+)\b", text))):
        if rid not in defined_f:
            errors.append(f"dangling finding reference: {rid}")
    for rid in sorted(set(re.findall(r"\b(U-\d+)\b", text))):
        if rid not in defined_u:
            errors.append(f"dangling unknown reference: {rid}")
    # Evidence IDs are defined ONLY at definition sites (EV-<n> followed by
    # ":" or "|"). Every referenced EV ID must be in that definition set;
    # a bare mention never defines the ID it mentions.
    ev_defs = set(re.findall(r"\b(EV-\d+)\b\s*[:|]", text))
    for rid in sorted(set(re.findall(r"\b(EV-\d+)\b", text))):
        if rid not in ev_defs:
            errors.append(f"dangling evidence reference: {rid}")
    # 5. unbounded negatives (warnings)
    for i, line in enumerate(lines, start=1):
        low = " " + line.lower() + " "
        if re.search(r"\b(no|never|none)\b[^.]{0,60}\b(found|present|detected|exist|exists|observed)\b", low) or re.search(r"\bno [a-z ]{2,30}found\b", low):
            if not any(w in low for w in SCOPE_WORDS):
                warnings.append(f"line {i}: unbounded negative, state the examined scope: {line.strip()[:90]}")
    # 7. a11y ceiling disclosure when automated accessibility results are cited
    if re.search(r"\baxe\b|\ba11y\b|automated accessibility", text, re.I):
        disclosure = A11Y_DISCLOSURE
        if args.manifest:
            try:
                disclosure = json.loads(Path(args.manifest).read_text(encoding="utf-8")) \
                    .get("a11yCeilingDisclosure", disclosure)
            except Exception as e:
                errors.append(f"cannot read a11y disclosure from manifest: {e}")
        if norm(disclosure) not in norm(text):
            errors.append("report cites automated accessibility results without the "
                          "a11y ceiling disclosure (a clean automated result is not "
                          "WCAG compliance; carry the manifest disclosure verbatim)")
    # 8. PDF deliverable accessibility (warning class)
    if re.search(r"\bpdf\b", text, re.I) and re.search(r"deliverable|shipped as|attached", text, re.I):
        if not re.search(r"tagged pdf|accessible equivalent|markdown version[^\n]*accessib", text, re.I):
            warnings.append("report claims a PDF deliverable with no deliverable "
                            "accessibility statement (tagged PDF with heading order, "
                            "Markdown named as the accessible equivalent)")
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
