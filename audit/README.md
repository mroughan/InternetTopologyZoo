# Topology Zoo data-quality audit

*Copyright © 2026 Eric Parsonage*

Contents of this directory:

| File | What it is |
|---|---|
| `report.pdf` | Typeset summary — start here. |
| `report.md` | Same summary in Markdown (source). |
| `zoo-audit.xlsx` | Full workbook: 4 rollup sheets plus 1 sheet per graph listing every node and every edge, issue rows highlighted. |
| `zoo_audit.py` | The generator. Rerun it any time the corpus changes. |

## What was audited

Every `.graphml` file under `graphml/` (276 in total at time of
writing), producing:

- per-graph node and edge tables with every declared attribute
- location coverage (nodes with / without Latitude and Longitude)
- multigraph detection (parallel edges between the same pair of nodes)
- self-loops
- graph connectivity (number of connected components)
- duplicate / empty / whitespace / control-character labels
- dangling edge endpoints
- out-of-range coordinate values

## Running the script

Requires Python 3 with `openpyxl` and `reportlab`:

```sh
pip install openpyxl reportlab
python audit/zoo_audit.py
```

Outputs land alongside the script. The script expects the GraphML
files to live at `~/InternetTopologyZoo/graphml/`; adjust
`ZOO_DIR` at the top of the script if your layout differs.

## Headline findings

See `report.md` / `report.pdf` for the full numbers, but briefly:

- 276 graphs, 10,952 nodes, 13,976 edges.
- 85 graphs fully located, 175 partial, 16 entirely unlocated.
- 2,137 nodes (≈ 20 %) missing latitude or longitude.
- 0 nodes with an *invalid* coordinate — all missings are absent attrs.
- 96 graphs contain at least one parallel-edge pair (654 across the corpus).
- 2 self-loops archive-wide.
- 23 graphs have more than one connected component.
