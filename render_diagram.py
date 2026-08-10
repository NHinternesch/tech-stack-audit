#!/usr/bin/env python3
"""Render a tech-stack architecture diagram to SVG from a JSON spec.

Usage: python3 render_diagram.py spec.json out.svg
See diagram-spec.md for the spec schema.

Layout model: bands run top-to-bottom as a data flow (platform sources → data
layer → consent gate → tag manager → destinations). Bands wrap onto as many
rows as they need, so no vendor is ever dropped. Inter-band edges route through
the gutter immediately above the target band, which clears any intervening rows.
Per-band alignment is what keeps the vertical channels those edges use free of
boxes.
"""
import json
import sys
from xml.sax.saxutils import escape

# Canvas
W = 1460
PAD = 40
LABEL_W = 128                  # left gutter holding band labels
TRUNK_X = PAD + LABEL_W - 26   # vertical dispatch trunk, inside the gutter
CONTENT_X = PAD + LABEL_W + 8
CONTENT_W = W - PAD - CONTENT_X

# Nodes
NODE_W, NODE_H, GAP = 196, 56, 18
PER_ROW = max(1, (CONTENT_W + GAP) // (NODE_W + GAP))

# Band chrome
BAND_TOP_PAD = 26
BAND_BOT_PAD = 14
ROW_GAP = 14
BAND_GAP = 16
TITLE_H = 82

# (key, label, fill, alignment) — order is the vertical flow order.
# Alignment keeps a column clear on one side so band-skipping edges have a lane:
# platform/tagmgmt hug the left, consent hugs the right.
BANDS = [
    ("platform",        "Platform",    "#f4f4f6", "left"),
    ("datalayer",       "Data Layer",  "#eef1f6", "left"),
    ("cmp",             "Consent",     "#f3f0f7", "right"),
    ("tagmgmt",         "Tag Mgmt",    "#f7f3e8", "left"),
    ("cdp",             "Server-Side", "#e9eef5", "left"),
    ("analytics",       "Analytics",   "#ecf3ee", "center"),
    ("personalization", "Experience",  "#f6edf2", "center"),
    ("adtech",          "Adtech",      "#f5eaea", "center"),
    ("misc",            "Other",       "#f7f7f8", "center"),
]
CERT = {"high": "#15803d", "medium": "#b45309", "low": "#94a3b8"}
RANK = {"high": 0, "medium": 1, "low": 2}


def split_rows(items, per_row):
    """Balance items across the fewest rows needed, wider rows first."""
    if len(items) <= per_row:
        return [items]
    n_rows = -(-len(items) // per_row)
    base, extra = divmod(len(items), n_rows)
    rows, i = [], 0
    for r in range(n_rows):
        size = base + (1 if r < extra else 0)
        rows.append(items[i:i + size])
        i += size
    return rows


def layout(nodes):
    """Assign each node a center (x, y). Empty bands are skipped and the
    remaining bands compact upward. Returns (positions, bands, height)."""
    by_cat = {key: [] for key, _, _, _ in BANDS}
    for n in nodes:
        cat = n.get("category", "misc")
        by_cat[cat if cat in by_cat else "misc"].append(n)

    pos, bands = {}, []
    y = TITLE_H
    for key, label, fill, align in BANDS:
        items = by_cat[key]
        if not items:
            continue
        items.sort(key=lambda n: (n.get("order", 99),
                                  RANK.get(n.get("certainty", "low"), 2)))
        rows = split_rows(items, PER_ROW)
        row_y = y + BAND_TOP_PAD
        for row in rows:
            span = len(row) * NODE_W + (len(row) - 1) * GAP
            if align == "left":
                x0 = CONTENT_X
            elif align == "right":
                x0 = CONTENT_X + CONTENT_W - span
            else:
                x0 = CONTENT_X + (CONTENT_W - span) / 2
            for i, node in enumerate(row):
                cx = x0 + i * (NODE_W + GAP) + NODE_W / 2
                pos[node["label"]] = (cx, row_y + NODE_H / 2, node)
            row_y += NODE_H + ROW_GAP
        band_h = BAND_TOP_PAD + len(rows) * NODE_H \
            + (len(rows) - 1) * ROW_GAP + BAND_BOT_PAD
        bands.append({"key": key, "label": label, "fill": fill, "align": align,
                      "y": y, "h": band_h, "rows": rows})
        y += band_h + BAND_GAP
    return pos, bands, int(y + 44)


def rounded(x, y, w, h, r):
    """Rounded-rect path. Used instead of <rect rx> so the certainty accent bar
    can be clipped to the same outline."""
    return (f"M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} "
            f"v{h - 2 * r} a{r},{r} 0 0 1 -{r},{r} h-{w - 2 * r} "
            f"a{r},{r} 0 0 1 -{r},-{r} v-{h - 2 * r} a{r},{r} 0 0 1 {r},-{r} z")


def edge_path(src, dst, bands):
    """Orthogonal path ending pointed into the target so the arrowhead lands
    square. Vertical detours run in the gutter next to the target band, which
    clears any rows between source and target."""
    (xa, ya), (xb, yb) = src, dst
    half = NODE_H / 2
    if abs(ya - yb) < 1:                        # same row
        return (f"M{xa + NODE_W / 2 + 3},{ya} H{xb - NODE_W / 2 - 5}"
                if xb > xa else
                f"M{xa - NODE_W / 2 - 3},{ya} H{xb + NODE_W / 2 + 5}")
    if abs(xa - xb) < 1:                        # same column: straight vertical
        return (f"M{xa},{ya + half} V{yb - half - 2}" if yb > ya
                else f"M{xa},{ya - half} V{yb + half + 2}")
    target = next((b for b in bands if b["y"] <= yb <= b["y"] + b["h"]), None)
    if yb > ya:                                 # downward
        mid = (target["y"] - BAND_GAP / 2) if target else (ya + yb) / 2
        return f"M{xa},{ya + half} V{mid} H{xb} V{yb - half - 2}"
    mid = (target["y"] + target["h"] + BAND_GAP / 2) if target else (ya + yb) / 2
    return f"M{xa},{ya - half} V{mid} H{xb} V{yb + half + 2}"


def render(spec):
    pos, bands, H = layout(spec.get("nodes", []))
    site = escape(spec.get("site", "Site"))
    subtitle = escape(spec.get("subtitle", ""))
    band_by_key = {b["key"]: b for b in bands}

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="Helvetica Neue, Helvetica, '
        'Arial, sans-serif">',
        "  <defs>",
        '    <filter id="sh" x="-30%" y="-30%" width="160%" height="160%">',
        '      <feDropShadow dx="0" dy="1" stdDeviation="1.2" '
        'flood-color="#0f172a" flood-opacity="0.10"/>',
        "    </filter>",
        '    <marker id="bus" viewBox="0 0 10 10" refX="8.5" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#64748b"/>',
        "    </marker>",
    ]
    for name, color in CERT.items():
        o += [
            f'    <marker id="a-{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
            'markerWidth="5.5" markerHeight="5.5" orient="auto">',
            f'      <path d="M0,0 L10,5 L0,10 z" fill="{color}"/>',
            "    </marker>",
        ]
    o += [
        "  </defs>",
        "  <style>",
        "    .t1 { font-size: 21px; font-weight: 700; fill: #0f172a;"
        " letter-spacing: -.2px; }",
        "    .t2 { font-size: 11.5px; fill: #6b7280; }",
        "    .band { font-size: 11px; font-weight: 700; fill: #6b7280;"
        " letter-spacing: .07em; }",
        "    .nm { font-size: 12.5px; font-weight: 600; fill: #111827;"
        " text-anchor: middle; }",
        "    .dt { font-size: 9.5px; fill: #6b7280; text-anchor: middle; }",
        "    .bus { fill: none; stroke: #64748b; stroke-width: 1.4; }",
        "    .lg { font-size: 10.5px; fill: #374151; }",
        "    .fn { font-size: 10px; fill: #6b7280; }",
        "  </style>",
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#fbfbfc"/>',
        f'  <text class="t1" x="{PAD}" y="40">{site} — Technology Stack</text>',
    ]
    if subtitle:
        o.append(f'  <text class="t2" x="{PAD}" y="59">{subtitle}</text>')

    for b in bands:
        o += [
            f'  <rect x="{PAD}" y="{b["y"]}" width="{W - 2 * PAD}" '
            f'height="{b["h"]}" rx="10" fill="{b["fill"]}" stroke="#e8eaee"/>',
            f'  <text class="band" x="{PAD + 14}" y="{b["y"] + 19}">'
            f'{escape(b["label"]).upper()}</text>',
        ]

    # Dispatch bus: one trunk down the left gutter with a single arrow into each
    # fed band — far more legible than one edge per destination vendor.
    fed = [k for k in spec.get("bus", {}).get("bands", []) if k in band_by_key]
    hub = spec.get("bus", {}).get("from")
    has_bus = bool(fed) and hub in pos
    if has_bus:
        hx, hy, _ = pos[hub]
        entries = [band_by_key[k]["y"] + BAND_TOP_PAD + NODE_H / 2 for k in fed]
        o.append(f'  <path class="bus" d="M{hx - NODE_W / 2},{hy} '
                 f'H{TRUNK_X} V{max(entries)}"/>')
        for ey in entries:
            o += [
                f'  <path class="bus" d="M{TRUNK_X},{ey} H{CONTENT_X - 6}" '
                'marker-end="url(#bus)"/>',
                f'  <circle cx="{TRUNK_X}" cy="{ey}" r="2.6" fill="#64748b"/>',
            ]

    for e in spec.get("edges", []):
        src, dst = pos.get(e.get("from")), pos.get(e.get("to"))
        if not src or not dst:
            print(f"skipped edge {e.get('from')} -> {e.get('to')}"
                  " (node not on diagram)", file=sys.stderr)
            continue
        cert = e.get("certainty", "low")
        d = edge_path(src[:2], dst[:2], bands)
        o.append(f'  <path d="{d}" fill="none" stroke="{CERT[cert]}" '
                 f'stroke-width="1.3" marker-end="url(#a-{cert})"/>')

    # Nodes last, so they sit above every connector.
    for b in bands:
        for row in b["rows"]:
            for node in row:
                cx, cy, _ = pos[node["label"]]
                x, y = cx - NODE_W / 2, cy - NODE_H / 2
                col = CERT.get(node.get("certainty", "low"), CERT["low"])
                nid = "c" + str(abs(hash(node["label"])) % 10 ** 8)
                detail = node.get("detail", "")
                sw = 1.6 if node.get("hub") else 1
                stroke = "#94a3b8" if node.get("hub") else "#e2e5ea"
                o += [
                    f'  <clipPath id="{nid}"><path d="'
                    f'{rounded(x, y, NODE_W, NODE_H, 8)}"/></clipPath>',
                    f'  <path d="{rounded(x, y, NODE_W, NODE_H, 8)}" '
                    f'fill="#fff" stroke="{stroke}" stroke-width="{sw}" '
                    'filter="url(#sh)"/>',
                    f'  <g clip-path="url(#{nid})"><rect x="{x}" y="{y}" '
                    f'width="4.5" height="{NODE_H}" fill="{col}"/></g>',
                    f'  <text class="nm" x="{cx + 2}" '
                    f'y="{cy + (-2 if detail else 4)}">'
                    f'{escape(node["label"])}</text>',
                ]
                if detail:
                    o.append(f'  <text class="dt" x="{cx + 2}" y="{cy + 13}">'
                             f'{escape(detail)}</text>')

    ly = H - 20
    o.append(f'  <text class="lg" x="{PAD}" y="{ly}" font-weight="700">'
             "Certainty</text>")
    lx = PAD + 66
    for name, color in CERT.items():
        o += [
            f'  <rect x="{lx}" y="{ly - 8}" width="4.5" height="10" '
            f'fill="{color}"/>',
            f'  <text class="lg" x="{lx + 10}" y="{ly}">'
            f"{name.capitalize()}</text>",
        ]
        lx += 10 + 7 * len(name) + 26  # label width + gap, so entries never collide
    if has_bus:
        o += [
            f'  <rect x="{lx}" y="{ly - 5}" width="18" height="1.4" '
            'fill="#64748b"/>',
            f'  <text class="lg" x="{lx + 25}" y="{ly}">'
            f"{escape(hub)} dispatches every vendor in the band</text>",
        ]
    note = spec.get("note", "")
    if note:
        o.append(f'  <text class="fn" x="{W - PAD}" y="{ly}" '
                 f'text-anchor="end">{escape(note)}</text>')
    o += ["</svg>", ""]
    return "\n".join(o)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    with open(sys.argv[2], "w") as f:
        f.write(render(spec))
    print(f"wrote {sys.argv[2]} ({PER_ROW} nodes per row)")
