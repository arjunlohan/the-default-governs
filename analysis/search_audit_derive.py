#!/usr/bin/env python3
"""Search-audit derivation, the single source for every search-audit figure.

Emits BOTH own-camera join rules, named, per the adversarial panel's
reproducibility finding (referee-quant fatal 1):

RULE A (end-of-window): own cameras from latest_usage04262023.csv (April 2024
values); ratio computed over searches with camera_count > 0 and own > 0.
RULE B (contemporaneous-with-zeros): own cameras from the agency_usage series at
the capture date nearest (at or before) the search date; ratio computed over ALL
joined searches including camera_count == 0 (ratio 0).

The paper prints only figures this script emits, with the rule named in the same
sentence. The rule-insensitive figures (median reach 316; 63.2 percent exceed own
count) are preferred for prose.
"""
import csv, re, statistics, collections, bisect, os

_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
BASE = _DATA + os.sep

rows = []
with open(BASE + "public_search_audit20240426.csv", newline="") as f:
    for r in csv.DictReader(f):
        rows.append(r)
ids = {r["search_id"] for r in rows}
agencies = {r["agency"] for r in rows}
users = {r["user_id"] for r in rows}
dates = sorted(r["search_date"][:10] for r in rows if r["search_date"])
print(f"rows {len(rows)}; distinct search_id {len(ids)}; agencies {len(agencies)}; users {len(users)}; dates {dates[0]}..{dates[-1]}")

cams = [int(r["camera_count"]) for r in rows if r["camera_count"].isdigit()]
q = lambda data, p: sorted(data)[int(len(data) * p)]
print(f"camera_count: n={len(cams)}, zero={sum(1 for c in cams if c==0)} ({sum(1 for c in cams if c==0)/len(cams)*100:.1f}%), median={statistics.median(cams):.0f}, median(pos)={statistics.median([c for c in cams if c>0]):.0f}, p75={q(cams,0.75)}, p90={q(cams,0.90)}, max={max(cams)}, >=1000: {sum(1 for c in cams if c>=1000)/len(cams)*100:.1f}%")

# RULE A: end-of-window own cameras
own_a = {}
with open(BASE + "no_latest_usage04262023.csv", newline="") as f:
    lu = list(csv.DictReader(f))
for r in lu:
    v = r["number_of_owned_cameras"]
    own_a[r["agency"]] = int(v) if v.isdigit() else None
ra, ea, ja = [], 0, 0
for r in rows:
    if not r["camera_count"].isdigit(): continue
    c = int(r["camera_count"]); o = own_a.get(r["agency"])
    if not o: continue
    ja += 1
    if c > o: ea += 1
    if c > 0: ra.append(c / o)
print(f"RULE A (end-of-window, zeros excluded): joined={ja}, exceed-own {ea/ja*100:.1f}%, median ratio {statistics.median(ra):.1f}x, >=10x {sum(1 for x in ra if x>=10)/len(ra)*100:.1f}%")

# RULE B: contemporaneous own cameras, zeros included
own_series = collections.defaultdict(list)
with open(BASE + "agency_usage04262023.csv", newline="") as f:
    for r in csv.DictReader(f):
        v = r["number_of_owned_cameras"]
        if v.isdigit():
            own_series[r["agency"]].append(((r["accessed"] or r["updated"])[:10], int(v)))
for a in own_series: own_series[a].sort()
def own_at(agency, date):
    s = own_series.get(agency)
    if not s: return None
    ds = [d for d, _ in s]
    i = bisect.bisect_right(ds, date) - 1
    return s[max(i, 0)][1]
rb, eb, jb = [], 0, 0
for r in rows:
    if not r["camera_count"].isdigit(): continue
    c = int(r["camera_count"]); o = own_at(r["agency"], r["search_date"][:10])
    if not o: continue
    jb += 1
    if c > o: eb += 1
    rb.append(c / o)
print(f"RULE B (contemporaneous, zeros included): joined={jb}, exceed-own {eb/jb*100:.1f}%, median ratio {statistics.median(rb):.1f}x, >=10x {sum(1 for x in rb if x>=10)/len(rb)*100:.1f}%")

reasons = [r["reason"] or "" for r in rows]
no_digit = sum(1 for x in reasons if not re.search(r"\d", x))
short = sum(1 for x in reasons if len(x.strip()) <= 4)
dtt_rule = re.compile(r"\b(demo|test|tests|testing|training)\b", re.I)
dtt = sum(1 for x in reasons if dtt_rule.search(x))
print(f"reasons: no digit {no_digit} ({no_digit/len(reasons)*100:.1f}%), <=4 chars {short} ({short/len(reasons)*100:.1f}%), distinct {len(set(reasons))}, demo/test/training under rule \\b(demo|test|tests|testing|training)\\b case-insensitive: {dtt} ({dtt/len(reasons)*100:.2f}%)")

def audit_flag(v):
    return (v or "").strip() not in ("", "NA", "0")
optin = sum(1 for r in lu if audit_flag(r["public_search_audit"]))
print(f"audit-page opt-in (latest_usage.public_search_audit not blank/NA/0): {optin}/{len(lu)} = {optin/len(lu)*100:.1f}%  [note: the audit CSV holds searches from {len(agencies)} agencies; the {optin} and {len(agencies)} are different instruments' counts, state both]")

def partners(r):
    v = (r["external_organizations_with_access"] or "").strip()
    if v in ("", "NA"): return None
    return len([t for t in v.split(",") if t.strip()])
pop = [(r["agency"], partners(r), r["number_of_owned_cameras"]) for r in lu if partners(r)]
pv = sorted(p for _, p, _ in pop)
print(f"partner lists (comma-token rule): populated {len(pop)}, median {statistics.median(pv):.0f}, p90 {pv[int(len(pv)*0.90)]}, max {pv[-1]}")
for a, p, c in sorted(pop, key=lambda x: -x[1])[:3]:
    print(f"  top: {a}: {p} partners, {c} owned cameras")
