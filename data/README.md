# Dataset: The Default Governs

Frozen 2026-08-28; every file pinned in `MANIFEST.json` (SHA-256). This dataset accompanies the preprint "The Default Governs: Configuration as Policy in Local Government" ([doi.org/10.5281/zenodo.22157318](https://doi.org/10.5281/zenodo.22157318)).

## Contents and licenses

- `no_*.csv`: the News & Observer `private_eyes` release (MIT license; Dukes/McClatchy 2024). The two large files (`agency_usage04262023.csv`, `public_search_audit20240426.csv`) are referenced by checksum in the manifest and ship in the full Zenodo deposit.
- `dataset-2026-wave-*.csv`, `bwave-flags-notes.txt`, `frame_ca.csv`, `frame_panel.csv`: this project's August 2026 California recollection and frames (CC BY 4.0).
- `eof-snapshot-20260828.csv`: derived from the EyesOnFlock API (CC BY-SA 4.0; share-alike honored: this file is released CC BY-SA 4.0 with attribution to eyesonflock.com).
- `ccops_roster-20260826T0335Z.csv` and `../analysis/*.csv`: coded corpora (CC BY 4.0), each row carrying its source URL or key.

## Analysis

The `../analysis/` directory contains scripts that derive key statistics from these files. See the repository README for usage.
