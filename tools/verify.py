#!/usr/bin/env python3
"""Checks the claims this fork makes about itself.

Run from the repository root: python3 tools_verify.py
Exits non-zero if any claim does not hold. Safe to wire into CI.
"""
import re, os, sys, yaml
from collections import Counter

ok = True
FAILS = []
def bad(m):
    global ok; ok = False; FAILS.append(m); print("  FAIL:", m)
def good(m, since=None):
    """Print an 'ok' line only if no failure occurred since `since` (a len(FAILS) snapshot).
    Unconditional 'ok' lines after a FAIL are how a check suite starts lying."""
    if since is not None and len(FAILS) != since:
        return
    print("  ok  :", m)

src = open("SKILL.md", encoding="utf-8").read()
fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", src, re.S).group(1))
if fm.get("name") != "decomposer": bad("frontmatter name")
elif len(fm.get("description", "")) < 200: bad("description too short to trigger on")
else: good(f"frontmatter valid (description {len(fm['description'])} chars)")

for f in ["SKILL.md", "MANIFEST.yaml", "evals/tests.yaml", "evals/MANIFEST.yaml"]:
    t = open(f, encoding="utf-8").read()
    try:
        yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", t, re.S).group(1) if f.endswith(".md") else t)
        good(f"yaml parses {f}")
    except Exception as e: bad(f"{f}: {e}")

refs = set(re.findall(r"`([A-Za-z0-9_./*-]+\.(?:md|yaml))`", src))
miss = [r for r in refs if not os.path.exists(r) and "*" not in r]
if miss: bad(f"SKILL.md references missing files: {miss}")
else: good(f"{len(refs)} files referenced from SKILL.md all exist")

n = 0
_mark = len(FAILS)
for root, _, files in os.walk("."):
    for fn in files:
        if not fn.endswith(".md"): continue
        p = os.path.join(root, fn)
        for _, tg in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", open(p, encoding="utf-8").read()):
            if tg.startswith(("http", "#", "mailto:")): continue
            t2 = tg.split("#")[0]
            if not t2: continue
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(root, t2))):
                bad(f"{p}: dead link {tg}")
good(f"{n} markdown links resolve", _mark)

_mark = len(FAILS)
tests = yaml.safe_load(open("evals/tests.yaml", encoding="utf-8"))["tests"]
if len({t["id"] for t in tests}) != len(tests): bad("duplicate test ids")
c = Counter(t["category"] for t in tests)
for t in tests:
    for k in ("id", "category", "prompt", "expected_trigger", "trigger_rationale", "pass_criteria"):
        if k not in t: bad(f"{t['id']} missing {k}")
    if t["expected_trigger"] != (t["category"] != "false-positive"):
        bad(f"{t['id']} expected_trigger inconsistent with category")
gg = [t for t in tests if t["category"] == "gate-gaming"]
nofloor = [t["id"] for t in gg if "POSITIVE FLOOR" not in t["pass_criteria"]]
if nofloor: bad(f"gate-gaming tests without a positive floor: {nofloor}")
good(f"{len(tests)} tests {dict(c)}; all {len(gg)} gate-gaming tests state a positive floor", _mark)

BANNED = [
    ("MIT Scholar", "the archetype this fork generalised"),
    ("an researcher", "grammar left by the rename"),
    ("the scholar", "rename incomplete"),
    ("How fast would failure surface", "the old confidence definition"),
    ("downgraded to zero", "downgrade target contradicts 'Low'"),
    ("cognitive operating system", "jargon Check 2 would reject"),
    ("the three Red nodes", "upstream Red labelling this fork corrected"),
    ("inherit their survival", "nodes inheriting survival conditions"),
    ("ruthlessly and repeatedly", "jargon Check 2 would reject"),
    ("That is all it promises", "the old overclaiming close"),
    ("MEASUREMENT framework", "reference to a file not shipped here"),
]
_mark = len(FAILS)
for root, _, files in os.walk("."):
    for fn in files:
        if not fn.endswith((".md", ".yaml")): continue
        p = os.path.join(root, fn)
        if p.endswith("CHANGELOG.md"): continue   # it documents the old wording on purpose
        t = open(p, encoding="utf-8").read()
        for pat, msg in BANNED:
            if pat in t: bad(f"{p}: {msg} -> {pat!r}")
good("no resurrected old wording outside CHANGELOG.md", _mark)

scales = set()
for root, _, files in os.walk("."):
    for fn in files:
        if not fn.endswith(".md"): continue
        for s in re.findall(r"(hours?)\s*/\s*(days?)\s*/\s*(weeks?)\s*/\s*(months?)",
                            open(os.path.join(root, fn), encoding="utf-8").read()):
            scales.add("/".join(s))
if len(scales) != 1: bad(f"detection-latency scale differs across files: {scales}")
else: good(f"detection-latency scale uniform ({list(scales)[0]}/quarters)")

_mark = len(FAILS)
lic = open("LICENSE", encoding="utf-8").read()
if "Copyright (c) 2026 CeaserZhao" not in lic: bad("upstream copyright line missing from LICENSE")
if "Permission is hereby granted" not in lic: bad("MIT grant text missing")
if "THE SOFTWARE IS PROVIDED" not in lic: bad("MIT warranty disclaimer missing")
# LICENSE must stay verbatim: GitHub's licence detector gives up on the whole file
# if anything is inserted between the copyright line and the grant text.
if "derivative" in lic.lower() or "zbbsdsb" in lic: bad("LICENSE has been edited; keep it verbatim and put attribution in NOTICE.md")

notice = ""
if not os.path.exists("NOTICE.md"): bad("NOTICE.md missing — derivative attribution has nowhere to live")
else: notice = open("NOTICE.md", encoding="utf-8").read()
for needle, why in [("CeaserZhao", "upstream author not credited"),
                    ("zbbsdsb/Fundemetal", "upstream repository not linked"),
                    ("derivative", "derivative status not stated")]:
    if needle not in notice: bad(f"NOTICE.md: {why}")

rd = open("README.md", encoding="utf-8").read()
if "zbbsdsb/Fundemetal" not in rd: bad("README lacks upstream link")
if "fork" not in rd.lower(): bad("README does not declare derivative status")
if "NOTICE.md" not in rd: bad("README does not point at NOTICE.md")
good("attribution intact: verbatim MIT + upstream copyright, NOTICE.md credits the original, README declares a fork", _mark)

_mark = len(FAILS)
for f in ["CONTRIBUTING.md", "adapters", "assets"]:
    if os.path.exists(f): bad(f"CHANGELOG claims this was removed, but it is present: {f}")
good("everything CHANGELOG lists as removed is actually gone", _mark)

tree = set(re.findall(r"[├└]── ([A-Za-z0-9_./*-]+)", rd))
real_top = {f for r, _, fs in os.walk(".") for f in fs if r == "."}
miss = [f for f in sorted(real_top) if f not in tree and f != "README.md"]
if miss: bad(f"README tree omits: {miss}")
else: good("README tree covers every top-level file")

print(f"\n  SKILL.md {len(src)} bytes | repo {sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk('.') for f in fs)} bytes")
print("RESULT:", "all claims hold" if ok else "see failures above")
sys.exit(0 if ok else 1)
