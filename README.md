# The Default Governs: Dataset

Research data and analysis scripts for "The Default Governs: Configuration as Policy in Local Government."

**Paper:** [doi.org/10.5281/zenodo.22157318](https://doi.org/10.5281/zenodo.22157318)

**Author:** Arjun Lohan, University of Southern California (lohan@usc.edu)

## What this dataset contains

Five integrated sources documenting how automated license-plate reader (ALPR) data-retention periods are configured across American law enforcement, frozen August 28, 2026.

| Source | File(s) | Records | Period |
|--------|---------|---------|--------|
| Longitudinal portal panel | `no_latest_usage04262023.csv`, `no_agency*.csv` | 36,308 observations, 105 agencies | Jul 2023 to Apr 2024 |
| California recollection | `dataset-2026-wave-*.csv`, `frame_ca.csv` | 102 agencies | Aug 2026 |
| National aggregate (EyesOnFlock) | `eof-snapshot-20260828.csv` | 888 portals | Aug 2026 |
| Search audit corpus | (Zenodo only, 48 MB) | 12,283 searches | 2024 |
| Coded public records | `ccops_roster-*.csv`, `analysis/*.csv` | 16 oversight jurisdictions + deliberation roster | 2021 to 2026 |

The longitudinal panel and national aggregate are the first published datasets of ALPR retention configurations at scale. The coded corpora link configured settings to public deliberation records.

## Key findings from the paper

- 82.5% of 888 Flock Safety portals display exactly 30 days: the vendor's shipped default
- 99.14% of 347 agencies showed zero change in retention settings over nine months
- 96.83% of 347 agencies sat at exactly the camera vendor's shipped 30-day value
- Of 11 surveillance-oversight jurisdictions with an active ALPR programme, 8 never deliberated the retention number
- When the vendor changed its recommended default from 30 to 7 on August 13, 2026, 1.2% of portals displayed the new value fifteen days later

All figures are machine-generated from the deposited data. See the paper for methodology, limitations, and caveats.

## Repository layout

```
data/                         All datasets (frozen 2026-08-28)
  MANIFEST.json               SHA-256 checksums for every file
  README.md                   Per-file provenance and license
  eof-snapshot-20260828.csv   National aggregate: 888 portals
  frame_panel.csv             Longitudinal panel frame
  frame_ca.csv                California recollection frame
  dataset-2026-wave-*.csv     California wave data
  ccops_roster-*.csv          Oversight-jurisdiction roster
  no_*.csv                    News & Observer release files
  bwave-flags-notes.txt       Collection flags and notes
analysis/                     Reproducibility scripts and coded corpora
  eof_landscape.py            National landscape statistics
  f100_kill_test.py           Nine-month immobility derivation
  recluster_draft.py          Operator-clustered California recomputation
  search_audit_derive.py      Search-audit statistics (both ratio rules)
  deliberation_roster.csv     Coded deliberation corpus
  ccops_coding.csv            Oversight-jurisdiction coding
  retention_sentences.csv     Policy-template text corpus
```

## Running the analysis scripts

Prerequisites: Python 3.9+.

```bash
# National landscape (EyesOnFlock snapshot)
python3 analysis/eof_landscape.py

# Nine-month immobility (requires agency_usage04262023.csv from Zenodo)
python3 analysis/f100_kill_test.py

# California operator-clustered cross-section
python3 analysis/recluster_draft.py

# Search-audit derivation (requires large files from Zenodo)
python3 analysis/search_audit_derive.py
```

## Large data files

Two News & Observer files (~110 MB total) are too large for GitHub and ship only in the [Zenodo deposit](https://doi.org/10.5281/zenodo.22157318):

- `agency_usage04262023.csv` (62 MB): longitudinal agency-usage panel
- `public_search_audit20240426.csv` (48 MB): search-audit corpus

Download them from Zenodo and place in `data/` to run `f100_kill_test.py` and `search_audit_derive.py`.

## Data sources and licenses

- **Original datasets** (CC BY 4.0): California recollection, coded corpora, frames
- **News & Observer** (MIT): `no_*` files from the McClatchy/Dukes "private_eyes" release (2024)
- **EyesOnFlock snapshot** (CC BY-SA 4.0): `eof-snapshot-20260828.csv`, attribution to eyesonflock.com
- **Code** (MIT): all analysis scripts

See [LICENSE](LICENSE) for full terms.

## Citation

```bibtex
@article{lohan2026default,
  author  = {Lohan, Arjun},
  title   = {The Default Governs: Configuration as Policy in Local Government},
  year    = {2026},
  doi     = {10.5281/zenodo.22157318},
  note    = {Preprint}
}
```
