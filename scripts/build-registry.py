#!/usr/bin/env python3
"""Build registry.json (and skill-aliases.json) for the collection.

The registry is the machine generated index the collection router routes
over: one canonical record per skill or persona, aliases for duplicate and
recovered copies, license status per unit, category, risk class, and a
content checksum. Each record carries a routing description when one can
be derived: the description falls back from the frontmatter description,
to the sibling skill.yaml description, to (for personas only) the first
content line of SOUL.md. A record whose unit provides none of those
sources carries an empty description. It is NEVER hand edited. Run this
script, review the diff, commit the outputs with the generator.

Usage:
  python3 scripts/build-registry.py [--root .] [--from-commit <sha>]
                                    [--self-test]

Unit detection: a directory holding SKILL.md (skill), a directory holding
skill.yaml without SKILL.md (skill, Muse yaml format), or personas/<name>
holding SOUL.md (persona). A SKILL.md whose frontmatter carries
"pointer-to:" is a pointer, not a routable unit.

Risk class resolution (recorded per unit in risk_source). The full rule,
applied in this exact order, first match wins:
  1. "frontmatter": a frontmatter risk_class value on the unit itself.
  2. "known-map": the KNOWN_RISK map below (from the collection research:
     skills whose studied behavior sends, publishes, pays, books, or
     operates infrastructure, plus studied pins that correct the derived
     result for planning and monitoring skills that move nothing).
  3. "derived": derivation from the skill's own description (the
     frontmatter description; for a SKILL.md unit with no frontmatter
     description, the sibling skill.yaml description in the same folder,
     which is the same skill's declared description in Muse yaml
     format). Action keyword classes are tested in the order below and
     the highest matching class wins:
       destructive: delete, remove, destroy, terminate, wipe
       money: book, buy, purchase, pay, order, checkout, reserve
       external-send: send, publish, post, message, email
       write: create, update, edit, manage, schedule, configure, install
     Matching is case insensitive and inflection aware (books, booked,
     booking match book; payments matches pay) but word bounded, so
     paywall does not match pay and notebook does not match book.
  4. "default": risk_class "write", risk_source "default". The default is
     never "read": an unclassified unit is treated as able to write until
     a study classifies it, and the collection router treats every
     "default" record as confirmation required before any action beyond
     reading, regardless of its listed class.
This same rule is emitted verbatim into both output files as the
"risk_policy" metadata field, so a reader of registry.json or
skill-aliases.json never has to read this source to know it.

generated_from_commit: the outputs are stamped with the commit the tree
was generated from. The stamp comes from --from-commit when given, else
from "git rev-parse HEAD" run in the root. There is no placeholder
fallback: when no commit can be determined the script exits 2 and writes
nothing, because a registry that cannot name its source commit cannot be
trusted or reproduced. The stamp names the private source commit the
registry was generated from; it is not expected to be verifiable from a
public snapshot checkout, and SNAPSHOT.md carries the source to snapshot
mapping at publish.

Aliases: an alias is emitted only when the alias differs from its
canonical id (a self-alias is never emitted), the canonical target is a
canonical record in the scanned tree, and the alias path exists in the
scanned tree. Pointer units therefore produce an alias entry only when
the pointer's own id differs from the id it points to.

License status: "private-only" for the private infrastructure set (never
distributed), else "mit-cleared" when the unit claims MIT (frontmatter or
a folder LICENSE), else "not-cleared". The claim is recorded with its
source; THIRD-PARTY.md remains the human readable license map.

Exit codes: 0 ok, 1 self-test failure, 2 input error.
Diagnostics and validation warnings go to stderr.
"""
import argparse, hashlib, json, os, re, subprocess, sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REGISTRY_FORMAT_VERSION = 1
SKIP_DIRS = {".git", "__pycache__", ".locks", ".hub", "node_modules"}
NAME_RX = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
COMMIT_RX = re.compile(r"^[0-9a-fA-F]{40}$")
TEST_COMMIT = "0123456789abcdef0123456789abcdef01234567"

# Private-only units are NOT listed here. This file ships in the public mirror,
# and a hardcoded set of private skill names in a published generator is itself
# a leak of what is hidden, which the publish gate deliberately blocks. The
# roster has one source of truth: scripts/public-exclude.json in the private
# repo. Read it when present (private repo); when absent (public mirror) the
# set is empty, because the public tree contains no private units to flag.
def _load_private_only():
    cand = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public-exclude.json")
    if not os.path.isfile(cand):
        return set()
    try:
        rels = json.load(open(cand, encoding="utf-8")).get("exclude", [])
    except Exception:
        return set()
    return {os.path.basename(r.rstrip("/")) for r in rels}


PRIVATE_ONLY = _load_private_only()


def _load_risk_overrides():
    """Risk classes for private-only units, read from the private config.

    Same reason as PRIVATE_ONLY: no published file may name a private unit.
    """
    cand = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public-exclude.json")
    if not os.path.isfile(cand):
        return {}
    try:
        return json.load(open(cand, encoding="utf-8")).get("risk_overrides", {})
    except Exception:
        return {}

KNOWN_RISK = {
    # Studied entries carried from the original collection research.
    "github": "write", "github-research": "read",
    "social-publishing": "external-send", "xurl": "external-send",
    "social-content-performance": "write", "himalaya": "external-send",
    "email-inbox-triage": "write",
    "shopping": "money", "product-price-monitor": "read",
    "deep-research": "read", "collection-router": "read",
    "commit-gates": "write", "github-repo-standard": "write",
    # Step 2b additions. Each entry below was added because the unit's own
    # declared description (frontmatter, or the sibling skill.yaml for
    # root skills whose SKILL.md carries no frontmatter) clearly declares
    # the action class named. Money: books, buys, orders, or pays.
    "flight-booking": "money", "hotel-booking": "money",
    "event-tickets": "money", "store-operations": "money",
    "groceries": "money", "restaurant-reservations": "money",
    "trip-transport": "money", "marketplaces": "money",
    "scheduling": "money", "advertising-campaigns": "money",
    # External-send: sends, publishes, posts, messages, or emails.
    "email-management": "external-send", "messaging": "external-send",
    "customer-outreach": "external-send",
    "business-finance": "external-send", "imessage": "external-send",
    "wearables-comms": "external-send", "spoken-audio": "external-send",
    "share-ideas": "external-send", "generate_podcast": "external-send",
    # Write: creates, updates, edits, manages, configures, installs, or
    # operates devices, services, or infrastructure.
    "home-control": "write", "airtable": "write",
    "apple-reminders": "write", "docker-ops": "write",
    "google-workspace": "write", "notion": "write",
    "knowledge-organization": "write", "file-hosting": "write",
    "custom-connector-setup": "write", "computer-use": "write",
    "claude-code": "write", "codex": "write", "opencode": "write",
    "fastmcp": "write", "exec-scripts": "write",
    "tiny-go-web-tool": "write", "app-creation": "write",
    "local-pulse": "write",
    # Studied pins: planning and monitoring skills whose descriptions
    # contain a booking or purchase word for work they track but never
    # perform. The pin keeps derivation from overstating them.
    "flight-tracking": "read", "trip-planning": "write",
    "home-search": "write", "financial-planning": "write",
}

# Merge risk classes for private-only units from the private config. Placed
# after the literal: the overrides file is absent in the public mirror, so the
# published copy keeps only its own public entries.
KNOWN_RISK.update(_load_risk_overrides())
# Canonical copy per the MANIFEST rule, for names that exist twice.
CANONICAL_PATH = {
    "github-repo-standard": "github-repo-standard",
    "commit-gates": "commit-gates",
    "deep-research": "skills/deep-research",
}

# Derivation keyword classes in resolution order, highest first. Each
# stem expands to common inflections; matching stays word bounded.
DERIVED_CLASSES = [
    ("destructive", ["delete", "remove", "destroy", "terminate", "wipe"]),
    ("money", ["book", "buy", "purchase", "pay", "order", "checkout",
               "reserve"]),
    ("external-send", ["send", "publish", "post", "message", "email"]),
    ("write", ["create", "update", "edit", "manage", "schedule",
               "configure", "install"]),
]
_INFLECTIONS = {
    "delete": ["delete", "deletes", "deleted", "deleting"],
    "remove": ["remove", "removes", "removed", "removing"],
    "destroy": ["destroy", "destroys", "destroyed", "destroying"],
    "terminate": ["terminate", "terminates", "terminated", "terminating"],
    "wipe": ["wipe", "wipes", "wiped", "wiping"],
    "book": ["book", "books", "booked", "booking", "bookings"],
    "buy": ["buy", "buys", "bought", "buying"],
    "purchase": ["purchase", "purchases", "purchased", "purchasing"],
    "pay": ["pay", "pays", "paid", "paying", "payment", "payments"],
    "order": ["order", "orders", "ordered", "ordering"],
    "checkout": ["checkout", "checkouts"],
    "reserve": ["reserve", "reserves", "reserved", "reserving",
                "reservation", "reservations"],
    "send": ["send", "sends", "sent", "sending"],
    "publish": ["publish", "publishes", "published", "publishing"],
    "post": ["post", "posts", "posted", "posting"],
    "message": ["message", "messages", "messaged", "messaging"],
    "email": ["email", "emails", "emailed", "emailing"],
    "create": ["create", "creates", "created", "creating"],
    "update": ["update", "updates", "updated", "updating"],
    "edit": ["edit", "edits", "edited", "editing"],
    "manage": ["manage", "manages", "managed", "managing", "management"],
    "schedule": ["schedule", "schedules", "scheduled", "scheduling"],
    "configure": ["configure", "configures", "configured", "configuring"],
    "install": ["install", "installs", "installed", "installing"],
}
_DERIVED_RX = []
for _cls, _stems in DERIVED_CLASSES:
    _forms = sorted({f for s in _stems for f in _INFLECTIONS[s]},
                    key=len, reverse=True)
    _DERIVED_RX.append(
        (_cls, re.compile(r"\b(?:%s)\b" % "|".join(map(re.escape, _forms)),
                          re.IGNORECASE)))

RISK_POLICY = {
    "resolution_order": ["frontmatter", "known-map", "derived", "default"],
    "derived_keyword_classes": [
        {"risk_class": cls, "keywords": stems} for cls, stems in DERIVED_CLASSES
    ],
    "derived_matching": (
        "Case insensitive, inflection aware, word bounded matching over "
        "the skill's own description; the highest matching class in the "
        "order destructive, money, external-send, write wins."
    ),
    "default": {"risk_class": "write", "risk_source": "default"},
    "default_rule": (
        "The default is never read. A record whose risk_source is "
        "default is unclassified and must be treated as confirmation "
        "required before any action beyond reading."
    ),
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


def normalize_tags(raw):
    """Coerce a frontmatter tags value into a list of strings."""
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw] if raw.strip() else []
    if isinstance(raw, (list, tuple)):
        return [str(t) for t in raw]
    return []


def extract_tags(fm):
    """Read a unit's trigger tags from parsed frontmatter, robustly.

    Preferred location is metadata.hermes.tags. Flattened files place
    tags as siblings of hermes under metadata (metadata.tags), and in
    some files metadata.hermes is missing or is not a mapping at all;
    both cases fall back to metadata.tags, then to a top level tags key.
    """
    if not isinstance(fm, dict):
        return []
    meta = fm.get("metadata")
    if isinstance(meta, dict):
        hermes = meta.get("hermes")
        if isinstance(hermes, dict):
            tags = normalize_tags(hermes.get("tags"))
            if tags:
                return tags
        tags = normalize_tags(meta.get("tags"))
        if tags:
            return tags
    return normalize_tags(fm.get("tags"))


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
    meta = fm.get("metadata") if isinstance(fm, dict) else None
    if isinstance(meta, dict):
        hermes = meta.get("hermes")
        if isinstance(hermes, dict) and hermes.get("category"):
            return str(hermes["category"])
        if meta.get("category"):
            return str(meta["category"])
    parts = rel.split("/")
    if parts[0] == "personas":
        return "persona"
    if parts[0] == "skills" and len(parts) > 2:
        return parts[1]
    if parts[0] == "skills":
        return "pipeline"
    return "root"


def derive_risk(description):
    """Return the derived risk class for a description, or None."""
    if not description:
        return None
    for cls, rx in _DERIVED_RX:
        if rx.search(description):
            return cls
    return None


def first_content_line(text):
    """Return the first content line of a persona SOUL.md, or "".

    The first non-empty line that is not only a heading marker wins;
    leading # characters and surrounding whitespace are stripped.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        content = stripped.lstrip("#").strip()
        if not content:
            continue
        return content
    return ""


def resolve_commit(root, from_commit):
    """Determine the source commit, or return None when unavailable."""
    if from_commit:
        commit = str(from_commit).strip()
        return commit if COMMIT_RX.match(commit) else None
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=30)
    except Exception as e:
        diag("git rev-parse failed (%s)" % e)
        return None
    if out.returncode != 0:
        return None
    commit = out.stdout.strip()
    return commit or None


def build(root, from_commit):
    raw = []
    warnings = []
    for rel, kind, main_file in find_units(root):
        sibling_desc = ""
        soul_desc = ""
        if kind == "persona":
            fm, body = parse_frontmatter(open(main_file, encoding="utf-8").read())
            soul_desc = first_content_line(body)
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
            tags = normalize_tags(data.get("tags"))
            fm = data
        else:
            text = open(main_file, encoding="utf-8").read()
            fm, _ = parse_frontmatter(text)
            folder = rel.split("/")[-1]
            uid = str(fm.get("name") or folder)
            desc = str(fm.get("description") or "")
            version = fm.get("version")
            license_field = fm.get("license")
            tags = extract_tags(fm)
            sibling = os.path.join(root, rel, "skill.yaml")
            if os.path.exists(sibling):
                sibling_desc = str(parse_yaml_file(sibling).get(
                    "description") or "")
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
            derived = derive_risk(desc or sibling_desc)
            if derived:
                risk, risk_source = derived, "derived"
            else:
                risk, risk_source = "write", "default"
        if not NAME_RX.match(uid):
            warnings.append("name %r at %s is not spec-shaped; folder name used as id" % (uid, rel))
            uid = folder
        # Description fallback chain: the frontmatter description, else
        # the sibling skill.yaml description, else (personas only, the
        # only branch that sets soul_desc) the first content line of
        # SOUL.md. This chain does not feed risk derivation, which keeps
        # reading desc or sibling_desc exactly as resolved above.
        effective_desc = desc
        if not str(effective_desc).strip():
            effective_desc = sibling_desc
        if not str(effective_desc).strip():
            effective_desc = soul_desc
        effective_desc = str(effective_desc)
        raw.append({
            "id": uid, "name": uid, "kind": kind, "path": rel,
            "category": category_of(rel, fm),
            # Routing descriptions are generated text: whitespace is
            # collapsed and dash punctuation normalized (em dashes and
            # double hyphens become commas) so the generated index never
            # carries punctuation the source frontmatter happens to hold.
            "description": " ".join(effective_desc.split()).replace("\u2014", ", ").replace("--", ", ")[:1000],
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
    # Alias emission rules: never emit a self-alias, never emit an alias
    # whose canonical target is not a canonical record in the scanned
    # tree, and never emit an alias whose path is absent from the tree.
    # Pointer units are covered by the same rules, so a pointer yields
    # an entry only when its own id differs from the id it points to.
    canon_ids = {u["id"] for u in raw if u.get("role") == "canonical"}
    scanned_paths = {u["path"] for u in raw}
    kept_aliases = []
    for a in aliases:
        if a["alias"] == a["canonical_id"]:
            continue
        if a["canonical_id"] not in canon_ids:
            continue
        if a["path"] not in scanned_paths:
            continue
        if not os.path.exists(os.path.join(root, a["path"])):
            continue
        kept_aliases.append(a)
    aliases = kept_aliases
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
        "risk_policy": RISK_POLICY,
        "counts": counts,
        "units": units,
    }
    aliases_doc = {
        "aliases_format_version": 1,
        "generated_from_commit": from_commit,
        "generator": "scripts/build-registry.py",
        "risk_policy": RISK_POLICY,
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
        reg, al, warn = build(d, TEST_COMMIT)
    ok = reg["counts"]["skills"] == 1 and reg["counts"]["personas"] == 1
    ok = ok and reg["generated_from_commit"] == TEST_COMMIT
    ok = ok and al["generated_from_commit"] == TEST_COMMIT
    print("self-test %s: %s" % ("ok" if ok else "FAIL", reg["counts"]))
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="build-registry.py",
        description="Build registry.json and skill-aliases.json for the "
                    "skill collection. Outputs are machine generated and "
                    "must never be hand edited.")
    parser.add_argument("--root", default=".",
                        help="collection tree root (default: current directory)")
    parser.add_argument("--from-commit", default=None, metavar="SHA",
                        help="commit the tree was generated from; when "
                             "omitted, git rev-parse HEAD in the root is "
                             "used, and generation fails when no commit "
                             "can be determined")
    parser.add_argument("--self-test", action="store_true",
                        help="run the built-in fixture self test and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    root = args.root
    if not os.path.isdir(root):
        diag("root is not a directory: %s" % root)
        return 2
    from_commit = resolve_commit(root, args.from_commit)
    if not from_commit:
        diag("cannot determine the source commit: pass --from-commit "
             "<sha> or run inside a git checkout; nothing was written")
        return 2
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
    sys.exit(main())
