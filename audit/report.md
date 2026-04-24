# Topology Zoo data-quality audit

*Copyright © 2026 Eric Parsonage*

Source: `/home/eric/InternetTopologyZoo/graphml`  

Graphs parsed: **276**  

Total nodes: **10,952**  

Total edges: **13,976**  


## Location coverage

- **85** graphs have every node located (lat + lon).
- **175** graphs have a mix of located and unlocated nodes.
- **16** graphs have zero located nodes.
- Total nodes missing at least one of lat/lon: **2,137**
  (19.5% of all nodes).
- Nodes whose lat/lon value was *provided but invalid* (empty string, 'None', 'NaN', out-of-range, non-numeric): **0**.

## Graph structure

- Multigraphs (at least one pair of parallel edges): **96**.
- Total parallel edges across the archive: **654**.
- Total self-loops: **2**.
- Graphs with >1 connected component: **23**.
- Isolated (edgeless) nodes overall: **115**.
- Edges whose source or target was not declared as a node: **0**.

## Labels

- Nodes without any `label` attribute: **20**.
- Nodes whose label is whitespace only: **0**.
- Nodes whose label contains control characters: **0**.
- Graphs containing duplicate labels: **120**.
- Total duplicate-label occurrences: **269** (counted as 1 per label that has ≥2 carriers within its graph).

## Issue tally by category

- `node-missing-both`: 2137
- `edge-parallel`: 498
- `node-label-duplicate`: 266
- `node-isolated`: 115
- `graph-disconnected`: 23
- `node-label-missing`: 20
- `edge-self-loop`: 2

## Issue tally by severity

- `info`: 2658
- `warn`: 403

## Largest graphs

| Graph | Nodes | Edges | Multi? | Missing latlon |
|---|---:|---:|:---:|---:|
| Kdl | 754 | 899 | yes | 28 |
| Cogentco | 197 | 245 | yes | 11 |
| DialtelecomCz | 193 | 151 | no | 15 |
| UsCarrier | 158 | 189 | no | 6 |
| Colt | 153 | 191 | yes | 4 |
| GtsCe | 149 | 193 | no | 8 |
| TataNld | 145 | 194 | yes | 2 |
| Pern | 127 | 129 | no | 119 |
| Ion | 125 | 150 | yes | 22 |
| Deltacom | 113 | 183 | yes | 12 |

## Worst location coverage (absolute count)

| Graph | Nodes | Missing | % |
|---|---:|---:|---:|
| Pern | 127 | 119 | 93.7% |
| Opteglobe | 93 | 93 | 100.0% |
| IntNetworkmap | 89 | 89 | 100.0% |
| AsnetAm | 65 | 64 | 98.5% |
| Garr | 56 | 56 | 100.0% |
| Cudi | 51 | 51 | 100.0% |
| Esnet | 68 | 51 | 75.0% |
| Internode | 66 | 46 | 69.7% |
| Columbus | 70 | 39 | 55.7% |
| Geant | 37 | 37 | 100.0% |

## Top multigraphs by parallel-edge count

| Graph | Edges | Parallel pairs |
|---|---:|---:|
| Ntt | 216 | 153 |
| Deltacom | 183 | 22 |
| Highwinds | 53 | 22 |
| Globenet | 113 | 18 |
| Sunet | 49 | 17 |
| Colt | 191 | 14 |
| Garr201112 | 89 | 14 |
| Garr201201 | 89 | 14 |
| Esnet | 92 | 13 |
| Garr201110 | 87 | 13 |

## How to use the workbook

The companion workbook `zoo-audit.xlsx` has:
1. **Summary** — one row per graph with the same columns as the totals at the bottom of this report. The last row is the cross-archive total.
2. **Missing Locations** — every single node with a missing or invalid lat/lon across the whole corpus.
3. **Issues** — every issue found, labelled by severity (error / warn / info) and category, with the node or edge id in the detail.
4. **Multigraphs** — the subset of graphs with parallel edges, plus their edge counts.
5. **one sheet per graph** — full attribute table for every node and every edge; rows with problems are highlighted.

## Notes on terminology

- "Missing lat/lon" counts a node if *either* of its Latitude or Longitude attributes is absent, empty, one of the sentinels `None`/`NaN`/`null`/`-`, or fails numeric coercion.
- "Multigraph" here means *observed* parallel edges, not the GraphML `parse.multiplegraph` flag (which is rarely set in the Zoo files).
- "Duplicate labels" counts **distinct labels** carried by 2+ nodes; for a count of *affected nodes* multiply by at least 2.
