#!/usr/bin/env python3
# Regression test: the registry generator must emit manifestRef.
#
# Lane C applied the manifestRef field (value
# "personas/critic/critic.manifest.json") to every registry unit plus the
# top-level manifest_ref key as a direct registry.json edit. The stock
# generator never emitted the field, so lane D's regeneration silently
# dropped it from all 327 units and the field had to be restored by hand.
# This test fails on any generator that drops the field again, and also
# covers the companion behavior: after writing registry.json, the
# generator refreshes the registryHash field inside the critic manifest.
#
# Usage: python3 test_registry_manifestref.py [path-to-build-registry.py]
# Default generator under test: the build-registry.py beside this file.
# Exits: 0 pass, 1 fail, 2 generator not loadable.

import hashlib
import importlib.util
import json
import os
import sys
import tempfile

EXPECTED_REF = "personas/critic/critic.manifest.json"


def load_generator(path):
    spec = importlib.util.spec_from_file_location("build_registry_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    here = os.path.dirname(os.path.abspath(__file__))
    gen_path = argv[0] if argv else os.path.join(here, "build-registry.py")
    if not os.path.isfile(gen_path):
        print("FAIL: generator not found: %s" % gen_path)
        return 2
    try:
        gen = load_generator(gen_path)
    except Exception as e:  # noqa: BLE001 - report any load failure as a fail
        print("FAIL: generator did not load: %s" % e)
        return 2

    failures = []
    with tempfile.TemporaryDirectory() as d:
        write(os.path.join(d, "demo-skill", "SKILL.md"),
              "---\nname: demo-skill\ndescription: \"Demo.\"\nlicense: MIT\n---\n\n# Demo\n")
        write(os.path.join(d, "personas", "demo", "SOUL.md"), "# Demo persona\n")
        reg, _aliases, _warn = gen.build(d, gen.TEST_COMMIT)

    if reg.get("manifest_ref") != EXPECTED_REF:
        failures.append("top-level manifest_ref is %r, expected %r"
                        % (reg.get("manifest_ref"), EXPECTED_REF))
    if not reg["units"]:
        failures.append("fixture build produced no units")
    for u in reg["units"]:
        if u.get("manifestRef") != EXPECTED_REF:
            failures.append("unit %s manifestRef is %r, expected %r"
                            % (u.get("id"), u.get("manifestRef"), EXPECTED_REF))
        elif list(u.keys())[-1] != "manifestRef":
            failures.append("unit %s manifestRef is not the last key (layout drift)"
                            % u.get("id"))

    # Companion behavior: registryHash refresh inside the critic manifest.
    refresh = getattr(gen, "refresh_manifest_hash", None)
    if refresh is None:
        failures.append("generator has no refresh_manifest_hash (registryHash "
                        "would go stale on the next regeneration)")
    else:
        with tempfile.TemporaryDirectory() as d:
            write(os.path.join(d, "registry.json"), "{\"units\": []}\n")
            manifest = {"registryHash": "0" * 64, "registryRef": "../../registry.json"}
            write(os.path.join(d, EXPECTED_REF), json.dumps(manifest, indent=1) + "\n")
            if not refresh(d):
                failures.append("refresh_manifest_hash returned False on a valid fixture")
            else:
                after = json.load(open(os.path.join(d, EXPECTED_REF), encoding="utf-8"))
                want = hashlib.sha256(
                    open(os.path.join(d, "registry.json"), "rb").read()).hexdigest()
                if after.get("registryHash") != want:
                    failures.append("manifest registryHash is %r, expected the "
                                    "registry.json sha256 %r"
                                    % (after.get("registryHash"), want))

    if failures:
        for f in failures:
            print("FAIL: %s" % f)
        return 1
    print("PASS: manifestRef on all %d fixture units, top-level manifest_ref, "
          "and registryHash refresh all hold" % len(reg["units"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
