#!/usr/bin/env python3
# =============================================================================
# glang — Topology Zoo GraphML audit generator
#
# Copyright 2026 Eric Parsonage
#
# This software is provided subject to the terms of the included licence.
#
# Author: Eric Parsonage
# =============================================================================
"""Topology Zoo GraphML audit.

Walks every *.graphml file under ~/InternetTopologyZoo/graphml, records
every node's and every edge's attributes, and produces:

  zoo-audit.xlsx  — one sheet per graph plus four cross-graph rollups
  report.md       — human-readable summary of overall data quality
  report.pdf      — typeset version of the same summary

Findings logged:

- nodes missing Latitude or Longitude (either absent, empty, "None",
  "NaN", "null", or outside the valid range)
- non-numeric coordinates where numeric was expected
- self-loops
- parallel edges (same unordered endpoint pair, any direction)
- duplicate node labels within a graph
- edges referring to undefined node ids
- isolated (unconnected) nodes
- nodes with unusual labels (empty, whitespace-only, or containing
  control characters)
- graphs flagged as multigraphs (edgedefault or presence of parallel
  edges)
- attribute-level oddities (mixed types, sentinel placeholders)

Usage:
  /home/eric/.venv/bin/python zoo_audit.py

Output lands in the same directory as this script.
"""
from __future__ import annotations
import os, sys, re, math, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


# ---- config ---------------------------------------------------------

COPYRIGHT = "Copyright © 2026 Eric Parsonage"

ZOO_DIR = Path.home() / "InternetTopologyZoo" / "graphml"
OUT_DIR = Path(__file__).parent
XLSX    = OUT_DIR / "zoo-audit.xlsx"
REPORT  = OUT_DIR / "report.md"
PDF     = OUT_DIR / "report.pdf"

NS = "{http://graphml.graphdrawing.org/xmlns}"

MISSING_SENTINELS = {"", "none", "nan", "null", "undef", "undefined", "-",
                     "na", "n/a", "0.0.0.0"}


# ---- parsing helpers ------------------------------------------------

def tag(elem: ET.Element) -> str:
    return elem.tag.replace(NS, "")


def parse_graphml(path: Path) -> dict:
    """Return a dict describing the file — see call sites for shape."""
    tree = ET.parse(path)
    root = tree.getroot()
    if tag(root) != "graphml":
        raise ValueError(f"{path}: root not <graphml>")

    keys = {}   # key-id -> (attr-name, target)
    for k in root.findall(NS + "key"):
        kid  = k.get("id")
        name = k.get("attr.name") or kid
        trg  = k.get("for") or "all"
        typ  = k.get("attr.type") or "string"
        if kid:
            keys[kid] = {"name": name, "for": trg, "type": typ}

    g = root.find(NS + "graph")
    if g is None:
        raise ValueError(f"{path}: no <graph>")

    edgedefault = g.get("edgedefault") or "directed"
    parsenodeids = g.get("parse.nodeids") or ""

    def data_of(elem, target):
        out = {}
        for d in elem.findall(NS + "data"):
            kid = d.get("key")
            if not kid:
                continue
            key = keys.get(kid)
            if not key:
                continue
            if target and key["for"] not in (target, "all"):
                continue
            out[key["name"]] = (d.text or "").strip()
        return out

    gdata  = data_of(g, "graph")
    nodes  = []
    for n in g.findall(NS + "node"):
        nodes.append({"id": n.get("id"), "attrs": data_of(n, "node")})
    edges  = []
    for e in g.findall(NS + "edge"):
        edges.append({
            "source": e.get("source"),
            "target": e.get("target"),
            "id":     e.get("id"),
            "attrs":  data_of(e, "edge"),
        })

    return {
        "path":         path,
        "name":         path.stem,
        "keys":         keys,
        "graph_data":   gdata,
        "edgedefault":  edgedefault,
        "parse_nodeids": parsenodeids,
        "nodes":        nodes,
        "edges":        edges,
    }


# ---- normalisation / predicate helpers ------------------------------

def is_missing(v) -> bool:
    if v is None:
        return True
    if not isinstance(v, str):
        return False
    s = v.strip().lower()
    return s in MISSING_SENTINELS


def coerce_float(v):
    if is_missing(v):
        return None
    try:
        x = float(v)
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    except (TypeError, ValueError):
        return None


def has_control_chars(s: str) -> bool:
    if not s:
        return False
    for ch in s:
        if unicodedata.category(ch).startswith("C") and ch not in ("\t", "\n"):
            return True
    return False


# ---- per-graph analysis --------------------------------------------

def analyse(parsed: dict) -> dict:
    """Return (per-graph summary, issues list, node rows, edge rows)."""
    name  = parsed["name"]
    nodes = parsed["nodes"]
    edges = parsed["edges"]
    issues = []

    # --- nodes ---
    node_ids = {n["id"] for n in nodes}
    node_label_counts = Counter()
    missing_latlon = []  # (node_id, label, which)
    bad_coords = []      # (node_id, label, kind, raw)
    label_empty = 0
    label_whitespace = 0
    label_control = 0

    for n in nodes:
        a = n["attrs"]
        nid = n["id"]
        label = a.get("label", "")
        node_label_counts[label.strip()] += 1

        if not label:
            label_empty += 1
            issues.append({"category": "node-label-missing", "severity": "warn",
                           "detail": f"node id={nid} has no label attribute"})
        elif label.strip() == "":
            label_whitespace += 1
            issues.append({"category": "node-label-whitespace", "severity": "warn",
                           "detail": f"node id={nid} label is whitespace-only: {label!r}"})
        elif has_control_chars(label):
            label_control += 1
            issues.append({"category": "node-label-control", "severity": "warn",
                           "detail": f"node id={nid} label contains control characters: {label!r}"})

        lat = a.get("Latitude")
        lon = a.get("Longitude")
        fl_lat = coerce_float(lat)
        fl_lon = coerce_float(lon)

        if fl_lat is None and fl_lon is None:
            missing_latlon.append((nid, label, "both"))
        elif fl_lat is None:
            missing_latlon.append((nid, label, "lat"))
            if lat is not None and not is_missing(lat):
                bad_coords.append((nid, label, "Latitude", lat))
        elif fl_lon is None:
            missing_latlon.append((nid, label, "lon"))
            if lon is not None and not is_missing(lon):
                bad_coords.append((nid, label, "Longitude", lon))

        if fl_lat is not None and not (-90.0 <= fl_lat <= 90.0):
            bad_coords.append((nid, label, "Latitude", lat))
            issues.append({"category": "node-lat-out-of-range", "severity": "error",
                           "detail": f"node id={nid} ({label!r}) lat={lat} outside [-90, 90]"})
        if fl_lon is not None and not (-180.0 <= fl_lon <= 180.0):
            bad_coords.append((nid, label, "Longitude", lon))
            issues.append({"category": "node-lon-out-of-range", "severity": "error",
                           "detail": f"node id={nid} ({label!r}) lon={lon} outside [-180, 180]"})

    for lbl, count in node_label_counts.items():
        if count > 1 and lbl:  # whitespace already flagged
            issues.append({"category": "node-label-duplicate", "severity": "warn",
                           "detail": f"label {lbl!r} used by {count} nodes"})

    for nid, label, which in missing_latlon:
        issues.append({"category": f"node-missing-{which}", "severity": "info",
                       "detail": f"node id={nid} ({label!r}) missing {which}"})

    # --- edges ---
    undirected_pair_counts = Counter()
    self_loops = 0
    dangling_src = 0
    dangling_dst = 0
    for e in edges:
        s, t = e["source"], e["target"]
        if s not in node_ids:
            dangling_src += 1
            issues.append({"category": "edge-dangling-source", "severity": "error",
                           "detail": f"edge id={e['id']} source={s} not in node set"})
        if t not in node_ids:
            dangling_dst += 1
            issues.append({"category": "edge-dangling-target", "severity": "error",
                           "detail": f"edge id={e['id']} target={t} not in node set"})
        if s == t:
            self_loops += 1
            issues.append({"category": "edge-self-loop", "severity": "warn",
                           "detail": f"edge id={e['id']} source=target={s}"})
        unordered = tuple(sorted((s, t))) if s and t else (s, t)
        undirected_pair_counts[unordered] += 1

    parallel_edges = sum(c - 1 for c in undirected_pair_counts.values() if c > 1)
    if parallel_edges:
        for pair, c in undirected_pair_counts.items():
            if c > 1:
                issues.append({"category": "edge-parallel", "severity": "info",
                               "detail": f"pair {pair} has {c} edges"})

    # --- connectivity ---
    adj = defaultdict(set)
    for e in edges:
        if e["source"] in node_ids and e["target"] in node_ids:
            adj[e["source"]].add(e["target"])
            adj[e["target"]].add(e["source"])
    isolated_nodes = [n["id"] for n in nodes if n["id"] not in adj]
    for nid in isolated_nodes:
        issues.append({"category": "node-isolated", "severity": "warn",
                       "detail": f"node id={nid} has no edges"})

    # components via BFS
    visited = set()
    components = 0
    for n in nodes:
        nid = n["id"]
        if nid in visited:
            continue
        components += 1
        frontier = [nid]
        while frontier:
            cur = frontier.pop()
            if cur in visited:
                continue
            visited.add(cur)
            frontier.extend(adj.get(cur, ()))
    if components > 1:
        issues.append({"category": "graph-disconnected", "severity": "info",
                       "detail": f"{components} connected components"})

    # multigraph? edgedefault or any parallel
    declared_multi = parsed["edgedefault"] == "undirected" and False  # edgedefault alone isn't multi
    is_multi = parallel_edges > 0

    summary = {
        "graph":                name,
        "nodes":                len(nodes),
        "edges":                len(edges),
        "edgedefault":          parsed["edgedefault"],
        "multigraph?":          "yes" if is_multi else "no",
        "parallel_edges":       parallel_edges,
        "self_loops":           self_loops,
        "missing_lat_or_lon":   len(missing_latlon),
        "bad_coords":           len(bad_coords),
        "isolated_nodes":       len(isolated_nodes),
        "components":           components,
        "duplicate_labels":     sum(1 for c in node_label_counts.values() if c > 1),
        "whitespace_labels":    label_whitespace,
        "empty_labels":         label_empty,
        "control_char_labels":  label_control,
        "dangling_endpoints":   dangling_src + dangling_dst,
        "issues":               len(issues),
    }
    return summary, issues, missing_latlon


# ---- xlsx output ----------------------------------------------------

HEADER_FONT = Font(bold=True)
HEADER_FILL = PatternFill("solid", fgColor="DDDDDD")
ISSUE_FILL  = PatternFill("solid", fgColor="FFE5B4")


def style_header(ws, row=1):
    for c in ws[row]:
        c.font = HEADER_FONT
        c.fill = HEADER_FILL


def autosize(ws):
    for col in ws.columns:
        if not col:
            continue
        try:
            length = max(len(str(c.value)) if c.value is not None else 0 for c in col)
        except ValueError:
            length = 10
        letter = get_column_letter(col[0].column)
        ws.column_dimensions[letter].width = min(max(length + 2, 10), 40)


def write_per_graph_sheet(wb, parsed):
    # Sheet name must be <=31 chars and contain no : \ / ? * [ ]
    name = re.sub(r"[:\\/?*\[\]]", "_", parsed["name"])[:31]
    if name in wb.sheetnames:
        name = (name[:28] + "_2")[:31]
    ws = wb.create_sheet(name)

    ws["A1"] = f"Graph: {parsed['name']}"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = COPYRIGHT
    ws["A2"].font = Font(italic=True, color="666666")

    row = 4
    ws.cell(row, 1, "Graph-level data").font = HEADER_FONT
    row += 1
    ws.cell(row, 1, "edgedefault"); ws.cell(row, 2, parsed["edgedefault"]); row += 1
    for k, v in sorted(parsed["graph_data"].items()):
        ws.cell(row, 1, k); ws.cell(row, 2, v); row += 1

    # --- nodes ---
    row += 1
    ws.cell(row, 1, f"Nodes ({len(parsed['nodes'])})").font = HEADER_FONT
    row += 1

    node_attr_keys = sorted({k for n in parsed["nodes"] for k in n["attrs"].keys()},
                            key=lambda x: (x != "label", x != "Latitude", x != "Longitude", x))
    headers = ["id", *node_attr_keys, "issues"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row, i, h).font = HEADER_FONT
        ws.cell(row, i).fill = HEADER_FILL
    row += 1
    for n in parsed["nodes"]:
        nid = n["id"]
        a = n["attrs"]
        node_issues = []
        lat_raw = a.get("Latitude")
        lon_raw = a.get("Longitude")
        fl_lat = coerce_float(lat_raw)
        fl_lon = coerce_float(lon_raw)
        if fl_lat is None:
            node_issues.append("missing lat" if is_missing(lat_raw) else f"bad lat {lat_raw!r}")
        if fl_lon is None:
            node_issues.append("missing lon" if is_missing(lon_raw) else f"bad lon {lon_raw!r}")
        if fl_lat is not None and not (-90 <= fl_lat <= 90):
            node_issues.append(f"lat out of range {lat_raw}")
        if fl_lon is not None and not (-180 <= fl_lon <= 180):
            node_issues.append(f"lon out of range {lon_raw}")
        if not a.get("label"):
            node_issues.append("no label")
        elif has_control_chars(a["label"]):
            node_issues.append("control chars in label")

        ws.cell(row, 1, nid)
        for i, k in enumerate(node_attr_keys, start=2):
            ws.cell(row, i, a.get(k, ""))
        ws.cell(row, len(headers), "; ".join(node_issues))
        if node_issues:
            for c in ws[row]:
                c.fill = ISSUE_FILL
        row += 1

    # --- edges ---
    row += 1
    ws.cell(row, 1, f"Edges ({len(parsed['edges'])})").font = HEADER_FONT
    row += 1

    edge_attr_keys = sorted({k for e in parsed["edges"] for k in e["attrs"].keys()})
    headers = ["source", "target", "id", *edge_attr_keys, "issues"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row, i, h).font = HEADER_FONT
        ws.cell(row, i).fill = HEADER_FILL
    row += 1

    nids = {n["id"] for n in parsed["nodes"]}
    pair_counts = Counter()
    for e in parsed["edges"]:
        s, t = e["source"], e["target"]
        pair_counts[tuple(sorted((s, t))) if s and t else (s, t)] += 1

    for e in parsed["edges"]:
        edge_issues = []
        s, t = e["source"], e["target"]
        if s not in nids:
            edge_issues.append(f"dangling source {s}")
        if t not in nids:
            edge_issues.append(f"dangling target {t}")
        if s == t:
            edge_issues.append("self-loop")
        if pair_counts[tuple(sorted((s, t))) if s and t else (s, t)] > 1:
            edge_issues.append("parallel")

        ws.cell(row, 1, s)
        ws.cell(row, 2, t)
        ws.cell(row, 3, e["id"])
        for i, k in enumerate(edge_attr_keys, start=4):
            ws.cell(row, i, e["attrs"].get(k, ""))
        ws.cell(row, len(headers), "; ".join(edge_issues))
        if edge_issues:
            for c in ws[row]:
                c.fill = ISSUE_FILL
        row += 1

    autosize(ws)


def _stamp(ws, title):
    ws.cell(1, 1, title).font = Font(bold=True, size=14)
    ws.cell(2, 1, COPYRIGHT).font = Font(italic=True, color="666666")


def write_workbook(entries, all_missing, all_issues, global_summary):
    wb = Workbook()
    # Summary sheet
    ws = wb.active
    ws.title = "Summary"
    _stamp(ws, "Topology Zoo — Summary")
    header_row = 4
    sum_cols = [
        "graph", "nodes", "edges", "edgedefault", "multigraph?",
        "parallel_edges", "self_loops", "missing_lat_or_lon",
        "bad_coords", "isolated_nodes", "components",
        "duplicate_labels", "whitespace_labels", "empty_labels",
        "control_char_labels", "dangling_endpoints", "issues",
    ]
    for i, h in enumerate(sum_cols, start=1):
        ws.cell(header_row, i, h)
    style_header(ws, row=header_row)
    for r, e in enumerate(entries, start=header_row + 1):
        for i, k in enumerate(sum_cols, start=1):
            ws.cell(r, i, e.get(k, ""))
    # Totals row
    total_row = header_row + 1 + len(entries)
    ws.cell(total_row, 1, "TOTALS").font = HEADER_FONT
    for i, k in enumerate(sum_cols, start=1):
        if k in ("graph", "edgedefault", "multigraph?"):
            continue
        vals = [e.get(k, 0) for e in entries if isinstance(e.get(k), (int, float))]
        ws.cell(total_row, i, sum(vals))
        ws.cell(total_row, i).font = HEADER_FONT
    autosize(ws)

    # Missing locations sheet
    ws2 = wb.create_sheet("Missing Locations")
    _stamp(ws2, "Topology Zoo — Missing Locations")
    ws2.cell(4, 1, "graph"); ws2.cell(4, 2, "node_id"); ws2.cell(4, 3, "label"); ws2.cell(4, 4, "missing")
    style_header(ws2, row=4)
    r = 5
    for graph, rows in all_missing.items():
        for (nid, label, which) in rows:
            ws2.cell(r, 1, graph)
            ws2.cell(r, 2, nid)
            ws2.cell(r, 3, label)
            ws2.cell(r, 4, which)
            r += 1
    autosize(ws2)

    # Issues sheet
    ws3 = wb.create_sheet("Issues")
    _stamp(ws3, "Topology Zoo — Issues")
    ws3.cell(4, 1, "graph"); ws3.cell(4, 2, "severity"); ws3.cell(4, 3, "category"); ws3.cell(4, 4, "detail")
    style_header(ws3, row=4)
    r = 5
    for graph, issues in all_issues.items():
        for iss in issues:
            ws3.cell(r, 1, graph)
            ws3.cell(r, 2, iss["severity"])
            ws3.cell(r, 3, iss["category"])
            ws3.cell(r, 4, iss["detail"])
            r += 1
    autosize(ws3)

    # Multigraphs sheet
    ws4 = wb.create_sheet("Multigraphs")
    _stamp(ws4, "Topology Zoo — Multigraphs")
    ws4.cell(4, 1, "graph"); ws4.cell(4, 2, "nodes"); ws4.cell(4, 3, "edges")
    ws4.cell(4, 4, "parallel_edges"); ws4.cell(4, 5, "self_loops")
    style_header(ws4, row=4)
    r = 5
    for e in entries:
        if e["multigraph?"] == "yes":
            ws4.cell(r, 1, e["graph"])
            ws4.cell(r, 2, e["nodes"])
            ws4.cell(r, 3, e["edges"])
            ws4.cell(r, 4, e["parallel_edges"])
            ws4.cell(r, 5, e["self_loops"])
            r += 1
    autosize(ws4)

    return wb


# ---- markdown summary ------------------------------------------------

def write_report(entries, all_issues, global_stats):
    total_graphs  = len(entries)
    total_nodes   = sum(e["nodes"] for e in entries)
    total_edges   = sum(e["edges"] for e in entries)
    total_missing = sum(e["missing_lat_or_lon"] for e in entries)
    total_self    = sum(e["self_loops"] for e in entries)
    total_para    = sum(e["parallel_edges"] for e in entries)
    total_iso     = sum(e["isolated_nodes"] for e in entries)
    total_bad     = sum(e["bad_coords"] for e in entries)
    total_dup     = sum(e["duplicate_labels"] for e in entries)
    total_dang    = sum(e["dangling_endpoints"] for e in entries)
    total_empty   = sum(e["empty_labels"] for e in entries)
    total_ws      = sum(e["whitespace_labels"] for e in entries)
    total_ctrl    = sum(e["control_char_labels"] for e in entries)
    multigraphs   = [e for e in entries if e["multigraph?"] == "yes"]

    completely_located  = sum(1 for e in entries if e["missing_lat_or_lon"] == 0)
    completely_unlocated = sum(1 for e in entries if e["missing_lat_or_lon"] == e["nodes"] and e["nodes"] > 0)
    partially_located    = total_graphs - completely_located - completely_unlocated

    # Issue category rollup
    category_counts = Counter()
    severity_counts = Counter()
    for issues in all_issues.values():
        for i in issues:
            category_counts[i["category"]] += 1
            severity_counts[i["severity"]] += 1

    # Graph sorted lists
    most_nodes = sorted(entries, key=lambda e: e["nodes"], reverse=True)[:10]
    most_missing = sorted(entries, key=lambda e: e["missing_lat_or_lon"], reverse=True)[:10]
    most_multi = sorted(multigraphs, key=lambda e: e["parallel_edges"], reverse=True)[:10]

    lines = []
    A = lines.append
    A("# Topology Zoo data-quality audit\n")
    A(f"*{COPYRIGHT}*\n")
    A(f"Source: `{ZOO_DIR}`  \n")
    A(f"Graphs parsed: **{total_graphs}**  \n")
    A(f"Total nodes: **{total_nodes:,}**  \n")
    A(f"Total edges: **{total_edges:,}**  \n")
    A("")

    A("## Location coverage\n")
    A(f"- **{completely_located}** graphs have every node located (lat + lon).")
    A(f"- **{partially_located}** graphs have a mix of located and unlocated nodes.")
    A(f"- **{completely_unlocated}** graphs have zero located nodes.")
    A(f"- Total nodes missing at least one of lat/lon: **{total_missing:,}**")
    A(f"  ({total_missing * 100.0 / max(total_nodes, 1):.1f}% of all nodes).")
    A(f"- Nodes whose lat/lon value was *provided but invalid* "
      f"(empty string, 'None', 'NaN', out-of-range, non-numeric): **{total_bad}**.")
    A("")

    A("## Graph structure\n")
    A(f"- Multigraphs (at least one pair of parallel edges): **{len(multigraphs)}**.")
    A(f"- Total parallel edges across the archive: **{total_para:,}**.")
    A(f"- Total self-loops: **{total_self}**.")
    A(f"- Graphs with >1 connected component: "
      f"**{sum(1 for e in entries if e['components'] > 1)}**.")
    A(f"- Isolated (edgeless) nodes overall: **{total_iso}**.")
    A(f"- Edges whose source or target was not declared as a node: **{total_dang}**.")
    A("")

    A("## Labels\n")
    A(f"- Nodes without any `label` attribute: **{total_empty}**.")
    A(f"- Nodes whose label is whitespace only: **{total_ws}**.")
    A(f"- Nodes whose label contains control characters: **{total_ctrl}**.")
    A(f"- Graphs containing duplicate labels: "
      f"**{sum(1 for e in entries if e['duplicate_labels'] > 0)}**.")
    A(f"- Total duplicate-label occurrences: **{total_dup}** "
      "(counted as 1 per label that has ≥2 carriers within its graph).")
    A("")

    A("## Issue tally by category\n")
    for cat, c in sorted(category_counts.items(), key=lambda kv: -kv[1]):
        A(f"- `{cat}`: {c}")
    A("")

    A("## Issue tally by severity\n")
    for sev, c in sorted(severity_counts.items(), key=lambda kv: -kv[1]):
        A(f"- `{sev}`: {c}")
    A("")

    A("## Largest graphs\n")
    A("| Graph | Nodes | Edges | Multi? | Missing latlon |")
    A("|---|---:|---:|:---:|---:|")
    for e in most_nodes:
        A(f"| {e['graph']} | {e['nodes']} | {e['edges']} | "
          f"{e['multigraph?']} | {e['missing_lat_or_lon']} |")
    A("")

    A("## Worst location coverage (absolute count)\n")
    A("| Graph | Nodes | Missing | % |")
    A("|---|---:|---:|---:|")
    for e in most_missing:
        pct = e['missing_lat_or_lon'] * 100.0 / max(e['nodes'], 1)
        A(f"| {e['graph']} | {e['nodes']} | {e['missing_lat_or_lon']} | {pct:.1f}% |")
    A("")

    if multigraphs:
        A("## Top multigraphs by parallel-edge count\n")
        A("| Graph | Edges | Parallel pairs |")
        A("|---|---:|---:|")
        for e in most_multi:
            A(f"| {e['graph']} | {e['edges']} | {e['parallel_edges']} |")
        A("")

    A("## How to use the workbook\n")
    A("The companion workbook `zoo-audit.xlsx` has:")
    A("1. **Summary** — one row per graph with the same columns as the totals "
      "at the bottom of this report. The last row is the cross-archive total.")
    A("2. **Missing Locations** — every single node with a missing or invalid "
      "lat/lon across the whole corpus.")
    A("3. **Issues** — every issue found, labelled by severity (error / warn / "
      "info) and category, with the node or edge id in the detail.")
    A("4. **Multigraphs** — the subset of graphs with parallel edges, plus their "
      "edge counts.")
    A("5. **one sheet per graph** — full attribute table for every node and "
      "every edge; rows with problems are highlighted.")
    A("")
    A("## Notes on terminology\n")
    A("- \"Missing lat/lon\" counts a node if *either* of its Latitude or Longitude "
      "attributes is absent, empty, one of the sentinels `None`/`NaN`/`null`/`-`, or "
      "fails numeric coercion.")
    A("- \"Multigraph\" here means *observed* parallel edges, not the GraphML "
      "`parse.multiplegraph` flag (which is rarely set in the Zoo files).")
    A("- \"Duplicate labels\" counts **distinct labels** carried by 2+ nodes; for a "
      "count of *affected nodes* multiply by at least 2.")

    return "\n".join(lines) + "\n"


# ---- PDF rendering --------------------------------------------------
#
# A small markdown-to-PDF using reportlab. Enough to render *this*
# report cleanly: title, two heading levels, bullet lists, GitHub-
# flavoured tables, and inline emphasis (**bold**, `code`). Not a
# general markdown renderer.


def _md_inline_to_rl(text: str) -> str:
    """Convert inline markdown to the limited HTML reportlab accepts."""
    # Escape <, >, & first so we don't touch them inside markdown emphasis.
    out = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', out)
    return out


def render_pdf(md_text: str, out_path: Path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, ListFlowable,
                                    ListItem)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"],
                                 alignment=TA_LEFT, spaceAfter=6)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], spaceBefore=14,
                        spaceAfter=6, textColor=colors.HexColor("#1f2a4e"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceBefore=10,
                        spaceAfter=4, textColor=colors.HexColor("#3c4b7a"))
    body = ParagraphStyle("Body", parent=styles["BodyText"], spaceAfter=4,
                          leading=14)
    mono = ParagraphStyle("Mono", parent=body, fontName="Courier",
                          fontSize=9, textColor=colors.HexColor("#555555"))

    story = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
            i += 1
            continue
        # Title (first # line) vs subsequent ## / ###
        if stripped.startswith("# "):
            story.append(Paragraph(_md_inline_to_rl(stripped[2:]), title_style))
            i += 1
            continue
        if stripped.startswith("## "):
            story.append(Paragraph(_md_inline_to_rl(stripped[3:]), h1))
            i += 1
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(_md_inline_to_rl(stripped[4:]), h2))
            i += 1
            continue
        # Tables: consecutive lines starting with |
        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            # Drop the separator row (--- |---|)
            filtered = [r for r in rows if not all(re.match(r"^:?-+:?$", c) for c in r)]
            if filtered:
                data = [[Paragraph(_md_inline_to_rl(c), body) for c in r]
                        for r in filtered]
                tbl = Table(data, hAlign="LEFT", repeatRows=1)
                tbl.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e8f0")),
                    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOX",        (0, 0), (-1, -1), 0.25, colors.grey),
                    ("INNERGRID",  (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("VALIGN",     (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
                    ("TOPPADDING",    (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))
                story.append(tbl)
                story.append(Spacer(1, 6))
            continue
        # Bulleted list
        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                items.append(ListItem(Paragraph(_md_inline_to_rl(lines[i].lstrip()[2:]), body),
                                      leftIndent=12, bulletColor=colors.HexColor("#3c4b7a")))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet",
                                      leftIndent=18, bulletFontSize=8,
                                      bulletOffsetY=-1))
            story.append(Spacer(1, 4))
            continue
        # Italic-copyright line ("*text*")
        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            story.append(Paragraph(f'<i>{_md_inline_to_rl(stripped.strip("*"))}</i>',
                                   mono))
            i += 1
            continue
        # Regular paragraph
        story.append(Paragraph(_md_inline_to_rl(stripped), body))
        i += 1

    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Topology Zoo data-quality audit",
                            author="Eric Parsonage")
    doc.build(story)


# ---- main ----------------------------------------------------------

def main():
    files = sorted(ZOO_DIR.glob("*.graphml"))
    if not files:
        print(f"No graphml files under {ZOO_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(files)} graphml files from {ZOO_DIR}")

    entries = []       # summary row per graph
    all_issues = {}    # graph -> list of issue dicts
    all_missing = {}   # graph -> list of (nid, label, which)
    wb = Workbook()
    wb.remove(wb.active)

    # Pre-create summary/issues/missing sheets at the end, so per-graph
    # sheets sort nicely in the middle.
    for path in files:
        try:
            parsed = parse_graphml(path)
        except ET.ParseError as ex:
            print(f"  !! parse error in {path.name}: {ex}")
            entries.append({"graph": path.stem, "nodes": 0, "edges": 0,
                            "edgedefault": "?", "multigraph?": "?",
                            "parallel_edges": 0, "self_loops": 0,
                            "missing_lat_or_lon": 0, "bad_coords": 0,
                            "isolated_nodes": 0, "components": 0,
                            "duplicate_labels": 0, "whitespace_labels": 0,
                            "empty_labels": 0, "control_char_labels": 0,
                            "dangling_endpoints": 0, "issues": 1})
            continue
        summary, issues, missing = analyse(parsed)
        entries.append(summary)
        all_issues[path.stem]  = issues
        all_missing[path.stem] = missing
        write_per_graph_sheet(wb, parsed)

    # Insert rollup sheets at position 0..3
    # (write_workbook builds those; we carry wb separately to keep the
    # per-graph sheets we already created.)
    roll = write_workbook(entries, all_missing, all_issues, None)
    # Insert roll sheets at the front of wb (in reverse so order is right)
    for title in ("Multigraphs", "Issues", "Missing Locations", "Summary"):
        if title in roll.sheetnames:
            src = roll[title]
            dst = wb.create_sheet(title=title, index=0)
            for row in src.iter_rows(values_only=False):
                for c in row:
                    nc = dst.cell(row=c.row, column=c.column, value=c.value)
                    nc.font = c.font.copy()
                    nc.fill = c.fill.copy()
            autosize(dst)

    XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(XLSX)
    print(f"  wrote {XLSX}")

    md = write_report(entries, all_issues, None)
    REPORT.write_text(md)
    print(f"  wrote {REPORT}")

    render_pdf(md, PDF)
    print(f"  wrote {PDF}")


if __name__ == "__main__":
    main()
