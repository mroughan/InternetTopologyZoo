# Topology Zoo data-quality audit

*Copyright © 2026 Eric Parsonage*

Contents of this directory:

| File | What it is |
|---|---|
| `report.pdf` | Typeset summary — start here. |
| `report.md` | Same summary in Markdown (source). |
| `zoo-audit.xlsx` | Full workbook: rollup sheets plus 1 sheet per graph listing every node and every edge, issue rows highlighted. |
| `zoo_audit.py` | The generator. Rerun it any time the corpus changes. |

## What was audited

Every `.graphml` file under `graphml/` (276 in total at time of
writing), producing:

- per-graph node and edge tables with every declared attribute
- location coverage (nodes with / without Latitude and Longitude)
- node classification: real internal routers vs Rj45 stubs (`Internal == 0`) vs switches (`hyperedge == 1`), plus the count of edges connecting to other networks
- multigraph detection (parallel edges between the same pair of nodes)
- self-loops
- graph connectivity (number of connected components)
- duplicate / empty / whitespace / control-character labels
- dangling edge endpoints
- out-of-range coordinate values
- live geonames enrichment: every real internal node is looked up against the cities500 dataset, by reverse geocoding from lat/lon when present and by name+country otherwise; matched country, place name and population are written to the workbook

## Workbook sheets

- **Summary** — one row per graph, totals row at the bottom.
- **Missing Locations** — every node missing or carrying invalid lat/lon.
- **Issues** — every issue found, by severity and category.
- **Real-node Populations** — one row per real internal node with the matched cities500 record and population.
- **Partial Resolution** — to-do list of graphs that resolved most of their real internal nodes but missed a handful, sorted easiest-first.
- **Multigraphs** — graphs with parallel edges.
- **One sheet per graph** — full node and edge tables, problem rows highlighted.

## Running the script

Requires Python 3 with `openpyxl`, `reportlab` and `numpy`:

```sh
pip install openpyxl reportlab numpy
python audit/zoo_audit.py
```

Outputs land alongside the script. The script expects the GraphML
files to live at `~/InternetTopologyZoo/graphml/`; adjust
`ZOO_DIR` at the top of the script if your layout differs.

The first run downloads the geonames cities500 dataset (~10 MB) into
`~/.cache/glang/geonames/`; subsequent runs reuse the cache.

## Headline findings

See `report.md` / `report.pdf` for the full numbers, but briefly:

- 276 graphs, 10,952 nodes, 13,976 edges.
- 9,751 real internal nodes, 975 Rj45 stubs, 226 switch nodes; 1,037 edges connect to a network beyond the graph.
- 85 graphs fully located, 175 partial, 16 entirely unlocated; 2,137 nodes (≈ 20 %) missing at least one of lat/lon.
- 0 nodes with an *invalid* coordinate — all missings are absent attrs.
- 8,847 of 9,751 real internal nodes (90.7 %) resolved against cities500; 211 of 276 graphs (76.4 %) have 100 % of their real internal nodes resolved.
- 96 graphs contain at least one parallel-edge pair (654 across the corpus).
- 2 self-loops archive-wide.
- 23 graphs have more than one connected component.
