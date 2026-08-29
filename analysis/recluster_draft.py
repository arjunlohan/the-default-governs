#!/usr/bin/env python3
"""DRAFT operator-clustered recomputation of the California cross-section.

Enabled by the 2026-08-28 external audit (TIER_2): the pre-registered
threshold of 15 sourced operator determinations was passed (30+ confirmed).
Every determination below is cited to its TIER_2 / OBS source. Numbers this
script prints are DRAFT and must be re-derived by the project's own cloud
task before print (the project rule: a pre-registered test names its
denominator file and exclusion rule in the same sentence as its threshold).

Substrate: frame_panel.csv (N&O April 2024 cross-section), the same file
CLAUDE.md section 3.1 uses for F132. CA subset per CLAUDE.md: n=84 after
excluding saratoga-ca-pd (-Infinity) and yuba-county-ca-so (NA).

Operator determinations applied (collapse rules):
- danville-ca-pd is policed by Contra Costa County SO under contract
  (TIER_4 item 8, danville.ca.gov verbatim; OBS-1048). Both rows sit at 365.
- town-of-woodside-ca-smcso is policed by San Mateo County SO (OBS-1046,
  four documents). Woodside row 60, SMCSO row 30: the merged unit straddles
  cells, so it is counted under two rules below.
- saratoga-ca-pd is policed by Santa Clara County SO (carried finding);
  already outside the analytic n.
- All other audited rows resolved INDEPENDENT (TIER_2 items 4-13), so no
  further collapses are licensed by the audit.
"""
import csv, collections, os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

with open(os.path.join(BASE, "frame_panel.csv")) as f:
    rows = list(csv.DictReader(f))

def is_ca(slug: str) -> bool:
    return "-ca-" in slug or slug.endswith("-ca") or "-ca-smcso" in slug

ca = [r for r in rows if is_ca(r["slug"])]
excluded = [r for r in ca if r["ret_2024"] in ("NA", "-Infinity")]
ca_n = [r for r in ca if r["ret_2024"] not in ("NA", "-Infinity")]
print(f"CA rows: {len(ca)} total, {len(excluded)} excluded "
      f"({[r['slug'] for r in excluded]}), analytic n={len(ca_n)}")

dist = collections.Counter(r["ret_2024"] for r in ca_n)
at30 = dist.get("30", 0)
print(f"RAW ROWS      : n={len(ca_n)}  at-30={at30}  share={at30/len(ca_n):.4f}  dist={dict(dist)}")

# Rule A: drop contract-city rows, keep the operator's own row.
# Danville (365) dropped, CCCSO (365) kept. Woodside (60) dropped, SMCSO (30) kept.
drop_a = {"danville-ca-pd", "town-of-woodside-ca-smcso"}
a = [r for r in ca_n if r["slug"] not in drop_a]
a30 = sum(1 for r in a if r["ret_2024"] == "30")
print(f"RULE A (drop contract-city rows)         : n={len(a)}  at-30={a30}  share={a30/len(a):.4f}")

# Rule B: collapse to operator units; a unit with ANY non-30 value counts non-30.
# Danville+CCCSO -> one unit at 365. Woodside+SMCSO -> one MIXED unit, counted non-30.
b_n = len(ca_n) - 2          # two rows merge away
b30 = at30 - 1               # SMCSO's 30 absorbed into a mixed (non-30) unit
print(f"RULE B (collapse; any-deviation = non-30): n={b_n}  at-30={b30}  share={b30/b_n:.4f}")

# Rule C: collapse to operator units; the operator's OWN row value wins.
# Danville+CCCSO -> 365. Woodside+SMCSO -> 30 (SMCSO's own value).
c_n = len(ca_n) - 2
c30 = at30                   # Woodside's 60 disappears into SMCSO's 30
print(f"RULE C (collapse; operator value wins)   : n={c_n}  at-30={c30}  share={c30/c_n:.4f}")

print("\nCaveats that must travel with any of these numbers:")
print("- F148 frame-composition artefact: most deviant-side cities sit in counties")
print("  whose sheriff is not a frame row, so no duplication is possible there by")
print("  construction. The audit bounds duplication among audited rows only.")
print("- The audit covered the CA frame; the national F132 figure keeps its")
print("  unit-definition sentence unless a national audit is done.")
