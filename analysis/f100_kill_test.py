#!/usr/bin/env python3
"""F100 designated kill test, executed as pre-stated in run-20260828T0406Z Next 1.

F100: "99.1% nine-month retention immobility, liveness-controlled, 2023-07 ->
2024-04" from agency_usage04262023.csv.

DENOMINATOR (as pre-stated): agencies present with a definite numeric retention
value; exclusion rule per OBS-969: drop NA, -Infinity, and the internal
flock-safety accounts (slug contains 'flock').

THE TEST: re-derive the immobility rate by script and, in the same pass, compute
what fraction of the "immobile" agencies were merely NOT OBSERVED to change,
i.e. how much of the 99.1% is carried by agencies with few capture points.

BRANCH A: immobility on agencies with >=3 distinct capture points differs from
the headline by >2 percentage points -> F100 drops from HIGH, restate on the
multi-capture subset. BRANCH B: differs by <=2 points -> F100 restated HIGH with
the subset alongside. BRANCH C (precedence): <30 agencies with a third capture
point -> unrunnable, F100 carries a two-capture limitation.
"""
import csv, re, sys, collections, os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "agency_usage04262023.csv")

def slug(url):
    return url.rstrip("/").rsplit("/", 1)[-1].lower()

def parse_ret(v):
    v = (v or "").strip()
    if v in ("", "NA", "-Infinity"): return None
    m = re.match(r"^(\d+)\s*days?$", v)
    return int(m.group(1)) if m else None

series = collections.defaultdict(dict)  # slug -> {date: value}
raw_values = collections.defaultdict(set)
n_rows = 0
with open(PATH, newline="") as f:
    for row in csv.DictReader(f):
        n_rows += 1
        s = slug(row["url"])
        if "flock" in s: continue
        v = parse_ret(row["data_retention_in_days"])
        if v is None: continue
        d = (row["accessed"] or row["updated"])[:10]
        series[s][d] = v
        raw_values[s].add(v)

observable = {s: pts for s, pts in series.items() if pts}
changed = {s for s, vals in raw_values.items() if s in observable and len(vals) > 1}
n = len(observable); ch = len(changed)
print(f"rows read: {n_rows}")
print(f"agencies with >=1 observable numeric retention (after exclusions): {n}")
print(f"changed at least once: {ch} -> immobile {n-ch} ({(n-ch)/n*100:.2f}%)  [ledger: 348/351 = 99.1%]")
print("changers:", sorted(changed))
for s in sorted(changed):
    pts = sorted(series[s].items())
    trans = [(d, v) for d, v in pts]
    firsts = {}
    for d, v in trans:
        if v not in firsts: firsts[v] = d
    print(f"  {s}: values {sorted(raw_values[s])}, first-seen {sorted(firsts.items(), key=lambda x: x[1])}, span {pts[0][0]}..{pts[-1][0]}, points {len(pts)}")

cap_counts = collections.Counter(len(pts) for pts in observable.values())
multi = {s for s, pts in observable.items() if len(pts) >= 3}
print(f"\ncapture-point distribution: min={min(cap_counts)}, agencies with >=3 points: {len(multi)}, with exactly 2: {sum(1 for s,p in observable.items() if len(p)==2)}, with 1: {sum(1 for s,p in observable.items() if len(p)==1)}")

if len(multi) < 30:
    print("BRANCH C: fewer than 30 agencies with a third capture point -> test UNRUNNABLE; F100 carries a two-capture limitation.")
    sys.exit(0)

m_changed = sum(1 for s in multi if s in changed)
m_rate = (len(multi) - m_changed) / len(multi) * 100
full_rate = (n - ch) / n * 100
diff = abs(m_rate - full_rate)
print(f"multi-capture (>=3 points) subset: n={len(multi)}, changed={m_changed}, immobile {m_rate:.2f}%")
print(f"difference from full-panel rate: {diff:.2f} points")
immobile_two_obs = sum(1 for s, pts in observable.items() if s not in changed and len(pts) <= 2)
print(f"immobile agencies carried by <=2 observations: {immobile_two_obs} of {n-ch} ({immobile_two_obs/(n-ch)*100:.2f}%)")
print("BRANCH A: F100 drops from HIGH; restate on the multi-capture subset." if diff > 2 else "BRANCH B: F100 restated at HIGH with the multi-capture subset reported alongside.")
