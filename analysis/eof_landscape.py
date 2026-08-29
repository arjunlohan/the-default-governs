#!/usr/bin/env python3
"""The August 2026 landscape: single source of truth for every figure derived
from the EyesOnFlock snapshot (flock-paper/data/eof-snapshot-20260828.csv,
CC BY-SA 4.0, fetched 2026-08-28).

Denominator rule, stated once and used everywhere: portals with a POSITIVE
integer camera count and a parseable retention value. Zero-camera and
unparseable-camera portals are excluded; empty retention is excluded from the
percentage base.

Churn disclosure (prints below): the camera filter is IMPERFECT. In the only
validated overlap (102 slugs cross-read against the 2026 CA wave), 3 portals the
wave correctly records as empty/churned (el-cerrito-ca-pd, cancelled June 2026,
among them) pass this filter with a displayed retention and positive cameras.
That 3/102 band, scaled, implies roughly 2-3 percent zombie portals biased
toward inflating the 30-mass, so the 30-share prints as an UPPER BOUND with
this sentence attached.
"""
import csv, collections, os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "eof-snapshot-20260828.csv")

rows = list(csv.DictReader(open(PATH)))
def cams(r):
    try: return int(r["total_cameras"])
    except (TypeError, ValueError): return None
def ret(r):
    v = (r["data_retention_days"] or "").strip()
    return int(v) if v.isdigit() else None

n_total = len(rows)
zero = [r for r in rows if cams(r) == 0]
unparse = [r for r in rows if cams(r) is None]
live = [r for r in rows if (cams(r) or 0) > 0]
base = [r for r in live if ret(r) is not None]
print(f"portals {n_total}: positive-camera {len(live)}, zero-camera {len(zero)}, camera unparseable/redacted {len(unparse)}")
print(f"percentage base (positive cameras AND parseable retention): n={len(base)}")

dist = collections.Counter(ret(r) for r in base)
for k in sorted(dist, key=lambda x: -dist[x]):
    print(f"  {k}: {dist[k]} ({dist[k]/len(base)*100:.1f}%)")
print(f"HEADLINES: at 30 = {dist.get(30,0)}/{len(base)} = {dist.get(30,0)/len(base)*100:.1f}% (UPPER BOUND, churn band ~3%); at 21 = {dist.get(21,0)} ({dist.get(21,0)/len(base)*100:.1f}%); at 7 = {dist.get(7,0)} ({dist.get(7,0)/len(base)*100:.1f}%)")

st21 = collections.Counter(r["state"] for r in base if ret(r) == 21)
print("21-day by state:", dict(sorted(st21.items(), key=lambda kv: -kv[1])))
tot_by_state = collections.Counter(r["state"] for r in base)
for s in ("VA", "WA", "CT", "ME"):
    print(f"  {s}: {st21.get(s,0)}/{tot_by_state.get(s,0)} in-base portals at 21 (uptake gradient, not 'instant')")
print("7-day portals (positive cameras):", [(r["slug"], r["state"], cams(r)) for r in base if ret(r) == 7])
print("zero-camera portals displaying 7 (excluded churn):", [(r["slug"], r["state"]) for r in zero if ret(r) == 7])
print("known false-negative named: el-cerrito-ca-pd (cancelled June 2026 per bwave notes) passes the filter:",
      [(r["slug"], ret(r), cams(r)) for r in rows if r["slug"] == "el-cerrito-ca-pd"])
