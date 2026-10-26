#!/usr/bin/env python3
"""Repo structure tool for the github skill.

Audits, scaffolds, and repairs a repo against the planned file
standard owned by the github-repo-standard skill. The standard's
machine readable form is github-repo-standard/assets/
repo-standard-manifest.json at the root of this collection; pass
--manifest to point elsewhere.

Modes:
  audit           read only (default). Reports present, missing,
                  header missing, and cross-reference breaks.
  scaffold        creates missing standard files from the templates.
                  Dry run by default; --apply writes. Never overwrites
                  a non-empty file. Writes the answers file
                  .repo-standard.yaml at the repo root on apply.
  repair-headers  inserts a missing instruction header into an
                  existing standard file. Dry run by default, with the
                  proposed change printed; --apply writes.

Exit codes: 0 completed and conformant (or plan printed), 1 audit
found the repo non conformant, 2 usage errors. Diagnostics go to
stderr. Python 3 standard library only.
"""
import argparse, json, re, sys
from datetime import date
from pathlib import Path

MARKER_DEFAULT = "INSTRUCTIONS FOR THIS FILE"


def err(msg):
    print(f"repo-structure: {msg}", file=sys.stderr)


def load_manifest(path):
    if path is None:
        here = Path(__file__).resolve()
        candidates = [here.parents[4] / "github-repo-standard" / "assets" / "repo-standard-manifest.json",
                      Path.cwd() / "github-repo-standard" / "assets" / "repo-standard-manifest.json"]
        path = next((c for c in candidates if c.exists()), None)
    if path is None or not Path(path).exists():
        err("manifest not found; pass --manifest with the path to repo-standard-manifest.json")
        sys.exit(2)
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")), Path(path)
    except json.JSONDecodeError as exc:
        err(f"manifest is not valid JSON: {exc}")
        sys.exit(2)


def template_root(manifest_path, manifest):
    root = manifest_path.parent.parent
    return root


def header_block(template_text):
    if template_text.startswith("<!--"):
        end = template_text.find("-->")
        if end != -1:
            return template_text[:end + 3] + "\n"
    return None


def cross_ref_breaks(repo, manifest):
    breaks = []
    todo = repo / "TODO.md"
    plan = repo / "PLAN.md"
    todo_re = re.compile(manifest.get("todo_id_regex", r"^T-\d+\.\d+$"))
    if todo.exists():
        for i, line in enumerate(todo.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = re.match(r"\s*- \[[ x]\] (T-[\w.]+)", line)
            if m and "(PLAN S" not in line:
                breaks.append(f"TODO.md:{i} item {m.group(1)} names no PLAN section")
            if m and not todo_re.match(m.group(1)) and not re.match(r"^T-P\.\d+$", m.group(1)):
                breaks.append(f"TODO.md:{i} item id {m.group(1)} does not match the TODO id pattern (parked items use T-P.<n>)")
    if plan.exists():
        for i, line in enumerate(plan.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = re.match(r"## (S(\d+))\b", line)
            if m and int(m.group(2)) >= 3 and "TODO Phase" not in line and "Open questions" not in line:
                breaks.append(f"PLAN.md:{i} section {m.group(1)} names no TODO phase")
    return breaks


def audit(repo, manifest):
    marker = manifest.get("instruction_header_marker", MARKER_DEFAULT)
    rows, breaks = [], []
    for rec in manifest["standard_files"] + manifest.get("machinery_files", []):
        p = repo / rec["path"]
        if not p.exists():
            rows.append((rec["path"], "MISSING")); breaks.append(f"{rec['path']} is missing"); continue
        if rec.get("instruction_header_marker") and marker not in p.read_text(encoding="utf-8", errors="replace"):
            rows.append((rec["path"], "HEADER MISSING")); breaks.append(f"{rec['path']} lacks its instruction header"); continue
        rows.append((rec["path"], "present"))
    breaks += cross_ref_breaks(repo, manifest)
    return rows, breaks


def render(template_text, variables):
    out = template_text
    for key, val in variables.items():
        out = out.replace(f"<{key}>", val).replace("{{" + key + "}}", val)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit, scaffold, or repair a repo against the github-repo-standard planned file standard.")
    ap.add_argument("mode", nargs="?", default="audit", choices=["audit", "scaffold", "repair-headers"])
    ap.add_argument("--repo", default=".", help="target repo path (default: current directory)")
    ap.add_argument("--manifest", default=None, help="path to repo-standard-manifest.json")
    ap.add_argument("--apply", action="store_true", help="write changes (default is a dry run that prints the change list)")
    ap.add_argument("--write", action="store_true", help="alias for --apply")
    args = ap.parse_args(argv)
    apply_changes = args.apply or args.write
    repo = Path(args.repo)
    if not repo.is_dir():
        err(f"repo path is not a directory: {repo}"); return 2
    manifest, mpath = load_manifest(args.manifest)
    troot = template_root(mpath, manifest)
    marker = manifest.get("instruction_header_marker", MARKER_DEFAULT)

    if args.mode == "audit":
        rows, breaks = audit(repo, manifest)
        for path, state in rows:
            print(f"{state:15} {path}")
        for b in breaks:
            err(f"break: {b}")
        if breaks:
            print(f"NON CONFORMANT: {len(breaks)} break(s)"); return 1
        print("CONFORMANT"); return 0

    if args.mode == "scaffold":
        variables = {"Project Name": repo.resolve().name, "Project Name in exact brand casing": repo.resolve().name}
        answers = repo / ".repo-standard.yaml"
        if answers.exists():
            for line in answers.read_text(encoding="utf-8", errors="replace").splitlines():
                if ":" in line and not line.startswith(" "):
                    k, v = line.split(":", 1); variables[k.strip()] = v.strip()
        changes = []
        for rec in manifest["standard_files"] + manifest.get("machinery_files", []):
            target = repo / rec["path"]
            tpl = troot / rec["template"]
            if target.exists() and target.stat().st_size > 0:
                continue
            if not tpl.exists():
                err(f"template missing, cannot scaffold {rec['path']}: {tpl}"); return 2
            changes.append(rec["path"])
            if apply_changes:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(render(tpl.read_text(encoding="utf-8"), variables), encoding="utf-8")
        for c in changes:
            print(("created " if apply_changes else "would create ") + c)
        if apply_changes:
            lines = [f"structure_format_version: {manifest['structure_format_version']}",
                     f"template_version: {manifest.get('template_version', 'unknown')}",
                     f"date: {date.today().isoformat()}", "variables:"]
            lines += [f"  {k}: {v}" for k, v in sorted(variables.items())]
            if not answers.exists():
                answers.write_text("\n".join(lines) + "\n", encoding="utf-8")
                print("wrote .repo-standard.yaml")
        elif not changes:
            print("nothing to create; repo already carries every standard file")
        return 0

    if args.mode == "repair-headers":
        changed = 0
        for rec in manifest["standard_files"]:
            if not rec.get("instruction_header_marker"):
                continue
            target = repo / rec["path"]
            if not target.exists():
                continue
            text = target.read_text(encoding="utf-8", errors="replace")
            if marker in text:
                continue
            tpl = troot / rec["template"]
            block = header_block(tpl.read_text(encoding="utf-8")) if tpl.exists() else None
            if block is None:
                err(f"no header block in template for {rec['path']}"); return 2
            changed += 1
            print(f"{'repaired ' if apply_changes else 'would repair '}{rec['path']}: insert instruction header ({len(block)} chars) before line 1")
            if apply_changes:
                target.write_text(block + text, encoding="utf-8")
        if not changed:
            print("no headers to repair")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
