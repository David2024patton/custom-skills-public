#!/usr/bin/env python3
"""Build registry.json (and skill-aliases.json) for the collection.

The registry is the machine generated index the collection router routes
over: one canonical record per skill or persona, aliases for duplicate and
recovered copies, license status per unit, category, routing description,
risk class, and a content checksum. It is NEVER hand edited. Run this
script, review the diff, commit the outputs with the generator.

Usage:
  python3 scripts/build-registry.py [--root .] [--from-commit <sha>]
                                    [--self-test]

Unit detection: a directory holding SKILL.md (skill), a directory holding
skill.yaml without SKILL.md (skill, Muse yaml format), or personas/<name>
holding SOUL.md (persona). A SKILL.md whose frontmatter carries
"pointer-to:" is a pointer, not a routable unit.

Risk class resolution (recorded per unit in risk_source):
  1. a frontmatter risk_class value,
  2. the KNOWN_RISK map below (from the collection research: skills whose
     studied behavior sends, publishes, pays, or operates infrastructure),
  3. the default "read".
Step-by-step fix work audits the defaults; the source field says which
units still ride on one.

License status: "private-only" for the private infrastructure set (never
distributed), else "mit-cleared" when the unit claims MIT (frontmatter or
a folder LICENSE), else "not-cleared". The claim is recorded with its
source; THIRD-PARTY.md remains the human readable license map.

Exit codes: 0 ok, 1 self-test failure, 2 input error.
Diagnostics and validation warnings go to stderr.
"""
import hashlib, json, os, re, sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REGISTRY_FORMAT_VERSION = 1
SKIP_DIRS = {".git", "__pycache__", ".locks", ".hub", "node_modules"}
NAME_RX = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

PRIVATE_ONLY = {
    "dokploy", "hostinger", "homelab-remote", "local-homelab-remote",
    "alpha-infra", "amd-7900xtx-vllm-server", "ecam_power_and_site_proof",
    "pulse", "local-pulse", "itak-stick-access", "itak-stick-emulator-check",
    "itak-tv-access", "sameday-sms-screener", "superdad-daily-vote",
    "recovered-skill-notes",
}
KNOWN_RISK = {
    "github": "write", "github-research": "read",
    "social-publishing": "external-send", "xurl": "external-send",
    "social-content-performance": "write", "himalaya": "external-send",
    "email-inbox-triage": "write", "dokploy": "destructive",
    "hostinger": "destructive", "alpha-infra": "destructive",
    "shopping": "money", "product-price-monitor": "read",
    "deep-research": "read", "collection-router": "read",
    "commit-gates": "write", "github-repo-standard": "write",
}
# Canonical copy per the MANIFEST rule, for names that exist twice.
CANONICAL_PATH = {
    "github-repo-standard": "github-repo-standard",
    "commit-gates": "commit-gates",
    "deep-research": "skills/deep-research",
}


def diag(msg):
    print("build-registry: %s" % msg, file=sys.stderr)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end]
    if yaml is None:
        return {}, text
    try:
        data = yaml.safe_load(block) or {}
        return (data if isinstance(data, dict) else {}), text[end + 4:]
    except Exception as e:
        diag("frontmatter parse failed (%s)" % e)
        return {}, text


def parse_yaml_file(path):
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(open(path, encoding="utf-8").read()) or {}
        return data if isinstance(data, dict) else {}
    except Exception as e:
        diag("yaml parse failed for %s (%s)" % (path, e))
        return {}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_units(root):
    units = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if "SKILL.md" in files:
            units.append((rel, "skill", os.path.join(dirpath, "SKILL.md")))
        elif "skill.yaml" in files:
            units.append((rel, "skill", os.path.join(dirpath, "skill.yaml")))
        elif rel.startswith("personas/") and "SOUL.md" in files and rel.count("/") == 1:
            units.append((rel, "persona", os.path.join(dirpath, "SOUL.md")))
    return sorted(units)


def category_of(rel, fm):
    meta = fm.get("metadata") or {}
    hermes = meta.get("hermes") or {}
    if hermes.get("category"):
        return str(hermes["category"])
    parts = rel.split("/")
    if parts[0] == "personas":
        return "persona"
    if parts[0] == "skills" and len(parts) > 2:
        return parts[1]
    if parts[0] == "skills":
        return "pipeline"
    return "root"


def build(root, from_commit):
    raw = []
    warnings = []
    for rel, kind, main_file in find_units(root):
        if kind == "persona":
            fm, _ = parse_frontmatter(open(main_file, encoding="utf-8").read())
            folder = rel.split("/")[-1]
            uid = fm.get("name") or folder
            desc = fm.get("description") or ""
            version = fm.get("version")
            license_field = fm.get("license")
            tags = []
        elif main_file.endswith("skill.yaml"):
            data = parse_yaml_file(main_file)
            folder = rel.split("/")[-1]
            uid = str(data.get("name") or folder).replace("_", "-")
            desc = str(data.get("description") or "")
            version = data.get("version")
            license_field = data.get("license")
            tags = data.get("tags") or []
            fm = data
        else:
            text = open(main_file, encoding="utf-8").read()
            fm, _ = parse_frontmatter(text)
            folder = rel.split("/")[-1]
            uid = str(fm.get("name") or folder)
            desc = str(fm.get("description") or "")
            version = fm.get("version")
            license_field = fm.get("license")
            meta = fm.get("metadata") or {}
            tags = (meta.get("hermes") or {}).get("tags") or fm.get("tags") or []
        pointer_to = fm.get("pointer-to")
        folder_license = os.path.exists(os.path.join(root, rel, "LICENSE"))
        if license_field and "MIT" in str(license_field):
            license_status, license_source = "mit-cleared", "frontmatter"
        elif folder_license:
            lic_text = open(os.path.join(root, rel, "LICENSE"), encoding="utf-8",
                            errors="replace").read(400)
            if "MIT" in lic_text:
                license_status, license_source = "mit-cleared", "folder LICENSE"
            else:
                license_status, license_source = "not-cleared", "folder LICENSE (non-MIT)"
        else:
            license_status, license_source = "not-cleared", "none"
        if uid in PRIVATE_ONLY or folder in PRIVATE_ONLY:
            license_status = "private-only"
        if fm.get("risk_class"):
            risk, risk_source = str(fm["risk_class"]), "frontmatter"
        elif uid in KNOWN_RISK:
            risk, risk_source = KNOWN_RISK[uid], "known-map"
        else:
            risk, risk_source = "read", "default"
        if not NAME_RX.match(uid):
            warnings.append("name %r at %s is not spec-shaped; folder name used as id" % (uid, rel))
            uid = folder
        raw.append({
            "id": uid, "name": uid, "kind": kind, "path": rel,
            "category": category_of(rel, fm),
            # Routing descriptions are generated text: whitespace is
            # collapsed and dash punctuation normalized (em dashes and
            # double hyphens become commas) so the generated index never
            # carries punctuation the source frontmatter happens to hold.
            "description": " ".join(desc.split()).replace("—", ", ").replace("--", ", ")[:1000],
            "version": str(version) if version is not None else None,
            "license": str(license_field) if license_field else None,
            "license_status": license_status, "license_source": license_source,
            "risk_class": risk, "risk_source": risk_source,
            "triggers": {"keywords": sorted({str(t) for t in tags} | set(uid.split("-"))),
                         "file_patterns": [], "tool_needs": []},
            "checksum_sha256": sha256_of(main_file),
            "pointer_to": pointer_to,
            "_folder": folder,
        })
    # Roles and aliases: pointers first, then duplicate names, then the
    # recovered local-* copies of canonical skills.
    aliases = []
    by_id = {}
    for u in raw:
        if u["pointer_to"]:
            u["role"] = "pointer"
            u["canonical_id"] = str(u["pointer_to"])
            aliases.append({"alias": u["id"], "canonical_id": u["canonical_id"],
                            "kind": "pointer", "path": u["path"]})
        else:
            by_id.setdefault(u["id"], []).append(u)
    for uid, group in by_id.items():
        if len(group) == 1:
            group[0]["role"] = "canonical"
            continue
        canon_rel = CANONICAL_PATH.get(uid)
        canon = next((g for g in group if g["path"] == canon_rel), group[0])
        for g in group:
            if g is canon:
                g["role"] = "canonical"
            else:
                g["role"] = "duplicate"
                g["canonical_id"] = uid
                aliases.append({"alias": uid, "canonical_id": uid,
                                "kind": "duplicate-copy", "path": g["path"]})
    canon_ids = {u["id"] for u in raw if u.get("role") == "canonical"}
    for u in raw:
        if u.get("role") != "canonical":
            continue
        if u["id"].startswith("local-"):
            target = u["id"][len("local-"):]
            if target in canon_ids:
                u["role"] = "duplicate"
                u["canonical_id"] = target
                aliases.append({"alias": u["id"], "canonical_id": target,
                                "kind": "recovered-copy", "path": u["path"]})
    units = []
    for u in raw:
        u.pop("_folder", None)
        if u.get("pointer_to") is None:
            u.pop("pointer_to", None)
        units.append(u)
    units.sort(key=lambda u: (u["id"], u["path"]))
    aliases.sort(key=lambda a: (a["alias"], a["path"]))
    counts = {
        "skills": sum(1 for u in units if u["kind"] == "skill" and u["role"] == "canonical"),
        "personas": sum(1 for u in units if u["kind"] == "persona" and u["role"] == "canonical"),
        "pointers": sum(1 for u in units if u["role"] == "pointer"),
        "duplicates": sum(1 for u in units if u["role"] == "duplicate"),
        "total_records": len(units),
    }
    registry = {
        "registry_format_version": REGISTRY_FORMAT_VERSION,
        "generated_from_commit": from_commit,
        "generator": "scripts/build-registry.py",
        "counts": counts,
        "units": units,
    }
    aliases_doc = {
        "aliases_format_version": 1,
        "generated_from_commit": from_commit,
        "generator": "scripts/build-registry.py",
        "aliases": aliases,
    }
    return registry, aliases_doc, warnings


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "demo-skill"))
        with open(os.path.join(d, "demo-skill", "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: demo-skill\ndescription: \"Demo.\"\nlicense: MIT\n---\n\n# Demo\n")
        os.makedirs(os.path.join(d, "personas", "demo"))
        with open(os.path.join(d, "personas", "demo", "SOUL.md"), "w", encoding="utf-8") as f:
            f.write("# Demo persona\n")
        reg, al, warn = build(d, "selftest")
    ok = reg["counts"]["skills"] == 1 and reg["counts"]["personas"] == 1
    print("self-test %s: %s" % ("ok" if ok else "FAIL", reg["counts"]))
    return 0 if ok else 1


def parse_args(argv):
    opts = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and "=" in a:
            k, v = a.split("=", 1)
            opts[k] = v
        elif a in ("--root", "--from-commit") and i + 1 < len(argv):
            opts[a] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            opts[a] = True
        i += 1
    return opts


def main(argv):
    opts = parse_args(argv)
    if "--self-test" in opts:
        return self_test()
    root = opts.get("--root", ".")
    if not isinstance(root, str):
        root = "."
    if not os.path.isdir(root):
        diag("root is not a directory: %s" % root)
        return 2
    from_commit = opts.get("--from-commit", "working-tree")
    if not isinstance(from_commit, str):
        from_commit = "working-tree"
    registry, aliases_doc, warnings = build(root, from_commit)
    with open(os.path.join(root, "registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=1, sort_keys=False)
        f.write("\n")
    with open(os.path.join(root, "skill-aliases.json"), "w", encoding="utf-8") as f:
        json.dump(aliases_doc, f, indent=1)
        f.write("\n")
    for w in warnings:
        diag("warning: %s" % w)
    diag("wrote registry.json and skill-aliases.json: %s" % registry["counts"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
