#!/usr/bin/env python3
"""Render a tech-stack architecture diagram to SVG from a JSON spec.

Usage: python3 render_diagram.py spec.json out.svg
See diagram-spec.md for the spec schema.
"""
import json
import sys
from xml.sax.saxutils import escape

BANDS = [
    ("cmp", "Compliance / CMP", "#f5f1f8"),
    ("tagmgmt", "Tag Management", "#faf7ed"),
    ("cdp", "CDP", "#eef2f7"),
    ("analytics", "Analytics", "#eef5f1"),
    ("personalization", "Personalization", "#f7eef3"),
    ("adtech", "Adtech", "#f6ecec"),
    ("misc", "Miscellaneous", "#f7f7f8"),
]
CERT = {"high": "#15803d", "medium": "#b45309", "low": "#94a3b8"}
RANK = {"high": 0, "medium": 1, "low": 2}
MAX_PER_BAND = 6
NODE_W, NODE_H, HALF = 170, 50, 85


def layout(nodes):
    """Assign each node a center (x, y). Empty bands are skipped and the
    remaining bands compact upward. Returns (positions, band_rows, height)."""
    by_cat = {key: [] for key, _, _ in BANDS}
    for n in nodes:
        cat = n.get("category", "misc")
        by_cat.setdefault(cat if cat in by_cat else "misc", []).append(n)

    pos, rows = {}, []
    top = 60
    for key, label, fill in BANDS:
        row = by_cat[key]
        if not row:
            continue
        row.sort(key=lambda n: RANK.get(n.get("certainty", "low"), 2))
        if len(row) > MAX_PER_BAND:
            overflow = len(row) - (MAX_PER_BAND - 1)
            row = row[: MAX_PER_BAND - 1] + [
                {"label": f"+{overflow} more", "certainty": "low"}
            ]
        n_row = len(row)
        cy = top + 40
        for i, node in enumerate(row):
            # Centers a row of n_row boxes on the 1200-wide canvas.
            cx = (690 - 90 * n_row) + i * 180
            pos[node["label"]] = (cx, cy, node)
        rows.append((label, fill, top, row))
        top += 90
    return pos, rows, max(top + 30, 200)


def edge_path(a, b):
    """Path that always ends with the segment pointing into the target, so the
    arrowhead lands square. Horizontals run in the 10px band gutter."""
    (xa, ya), (xb, yb) = a, b
    if ya == yb:  # within band
        return f"M {xa + HALF + 3} {ya} H {xb - HALF - 3}"
    if xa == xb:  # same column: straight vertical, no gutter detour
        return (f"M {xa} {ya + 25} V {yb - 25}" if yb > ya
                else f"M {xa} {ya - 25} V {yb + 25}")
    if yb > ya:  # downward
        return f"M {xa} {ya + 25} V {ya + 45} H {xb} V {yb - 25}"
    return f"M {xa} {ya - 25} V {ya - 45} H {xb} V {yb + 25}"


def render(spec):
    pos, rows, h = layout(spec.get("nodes", []))
    site = escape(spec.get("site", "Site"))
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}"'
        ' font-family="Helvetica, Arial, sans-serif">',
        "  <style>",
        "    .band rect { stroke: #e5e7eb; stroke-width: 1; }",
        "    .band-label { font-size: 11px; fill: #6b7280; font-weight: 600;",
        "                  text-transform: uppercase; letter-spacing: .05em; }",
        "    .box { fill: #fff; stroke-width: 1.25; rx: 8; ry: 8;"
        " filter: url(#shadow); }",
        "    .hub { stroke-width: 2; }",
        "    .label { font-size: 13px; fill: #374151; text-anchor: middle; }",
        "    .edge { fill: none; stroke-width: 1.25; }",
        "    .title { font-size: 18px; font-weight: 600; fill: #374151; }",
        "    .legend-text { font-size: 11px; fill: #374151; }",
    ]
    for name, color in CERT.items():
        out.append(f"    .cert-{name} {{ stroke: {color}; }}")
    out += [
        "  </style>",
        "  <defs>",
        '    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feDropShadow dx="0" dy="1" stdDeviation="1.5"'
        ' flood-color="#000" flood-opacity="0.12"/>',
        "    </filter>",
    ]
    for name, color in CERT.items():
        out += [
            f'    <marker id="arrow-{name}" viewBox="0 0 10 10" refX="9"'
            ' refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            f'      <path d="M0,0 L10,5 L0,10 z" fill="{color}"/>',
            "    </marker>",
        ]
    out += [
        "  </defs>",
        f'  <rect fill="#fafafa" x="0" y="0" width="1200" height="{h}"/>',
        f'  <text class="title" x="40" y="36">{site} — Tech Stack</text>',
    ]

    for label, fill, top, _ in rows:
        out += [
            f'  <g class="band"><rect x="40" y="{top}" width="1120"'
            f' height="80" fill="{fill}"/>',
            f'    <text class="band-label" x="52" y="{top + 12}">'
            f"{escape(label)}</text></g>",
        ]

    out.append('  <g class="nodes">')
    for _, _, _, row in rows:
        for node in row:
            cx, cy, _ = pos[node["label"]]
            cert = node.get("certainty", "low")
            hub = " hub" if node.get("hub") else ""
            out += [
                f'    <rect class="box{hub} cert-{cert}" x="{cx - HALF}"'
                f' y="{cy - 25}" width="{NODE_W}" height="{NODE_H}"/>',
                f'    <text class="label" x="{cx}" y="{cy + 5}">'
                f'{escape(node["label"])}</text>',
            ]
    out.append("  </g>")

    out.append('  <g class="edges">')
    for e in spec.get("edges", []):
        src, dst = pos.get(e.get("from")), pos.get(e.get("to"))
        if not src or not dst:
            print(f"skipped edge {e.get('from')} -> {e.get('to')}"
                  " (node not on diagram)", file=sys.stderr)
            continue
        cert = e.get("certainty", "low")
        d = edge_path(src[:2], dst[:2])
        out.append(f'    <path class="edge cert-{cert}" d="{d}"'
                   f' marker-end="url(#arrow-{cert})"/>')
    out.append("  </g>")

    out += [
        '  <g class="legend" transform="translate(880, 36)">',
        '    <text class="legend-text" x="0" y="0" font-weight="700">'
        "Certainty:</text>",
    ]
    lx = 65
    for name, color in CERT.items():
        out += [
            f'    <line x1="{lx}" y1="-4" x2="{lx + 20}" y2="-4"'
            f' stroke="{color}" stroke-width="1.25"/>',
            f'    <text class="legend-text" x="{lx + 26}" y="0">'
            f"{name.capitalize()}</text>",
        ]
        lx += 26 + 7 * len(name) + 22  # label width + gap, so entries never collide
    out += ["  </g>", "</svg>", ""]
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    with open(sys.argv[2], "w") as f:
        f.write(render(spec))
    print(f"wrote {sys.argv[2]}")
