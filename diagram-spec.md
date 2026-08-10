# Architecture Diagram Spec

Used by the **Architecture diagram** option in Step 4 of `SKILL.md`.

Write a JSON spec, then run the bundled renderer. Do **not** hand-author SVG — the
renderer owns all layout, coordinates, styling, and edge routing.

The diagram must be **complete**: every vendor in the audit appears on it. It also
has to stand on its own — a reader who never opens the `.docx` should still learn
which vendors are in play, how the data reaches them, and how confident you are.

## Spec schema

```json
{
  "site": "example.com",
  "subtitle": "Audited 2026-08-10 · homepage and PDP · 24 vendors observed",
  "note": "Detail lines show observed account IDs / endpoints",
  "bus": {"from": "Tealium iQ", "bands": ["analytics", "personalization", "adtech"]},
  "nodes": [
    {"label": "Tealium iQ", "category": "tagmgmt", "certainty": "high", "hub": true,
     "detail": "profile acme-eu · 19 tags", "order": 0},
    {"label": "Google Analytics 4", "category": "analytics", "certainty": "high",
     "detail": "G-XXXXXXX"}
  ],
  "edges": [
    {"from": "Tealium iQ", "to": "Google Analytics 4", "certainty": "medium"}
  ]
}
```

### Node fields

- `label` — vendor name. Must be unique; it is also the edge join key.
- `category` — one of `platform`, `datalayer`, `cmp`, `tagmgmt`, `cdp`,
  `analytics`, `personalization`, `adtech`, `misc`. Unrecognized values fall back
  to `misc`.
- `certainty` — `high` | `medium` | `low`. Drives the left accent bar and any
  edge/arrowhead color.
- `detail` — **include this on every node.** One short line of the hard evidence:
  account ID, measurement ID, endpoint, or version (`AW-949846414 (+27 mapped)`,
  `projectId 2055`, `collect.example.com`). This is what makes the diagram
  self-contained. Keep it under ~34 characters or it will crowd the box; truncate
  long IDs with `…`.
- `hub` — optional, thickens the box outline. Use for the few nodes most things
  flow through (tag manager, CDP, data layer), not for anything merely important.
- `order` — optional integer controlling left-to-right position within its band
  (lower first; default 99, then certainty). Use it to line up edge endpoints into
  clear vertical channels — see *Keeping edges clean* below.

### Top-level fields

- `subtitle` — audit date, pages covered, vendor count. Renders under the title.
- `note` — bottom-right caption. Use it to explain what `detail` lines contain.
- `bus` — the tag-manager fan-out, see below. Omit if there is no single
  dispatcher.

## Two kinds of connection

**`bus` — the fan-out.** A tag manager typically dispatches a dozen or more
vendors. Drawing one edge per vendor produces a hairball. Instead declare
`bus: {"from": "<hub label>", "bands": ["analytics", "adtech", …]}` and the
renderer draws a single trunk down the left gutter with one arrow into each listed
band, plus a legend line explaining it dispatches every vendor in those bands.

**`edges` — the specific relationships.** Reserve these for connections that are
individually interesting: what populates the data layer, how consent gates the
tag manager, which vendor loads another. `from`/`to` must match a node `label`
exactly; edges naming an absent node are skipped with a warning on stderr.

Draw the edges you have evidence for, not every theoretically possible one. A
dozen explicit edges is usually plenty.

## Band order and data flow

Bands render top-to-bottom in this fixed order, which is itself the data flow:

| Band | Holds |
|---|---|
| `platform` | Commerce platform, front-end framework, CMS, CDN/WAF, image service |
| `datalayer` | The client-side data layer object the tag manager reads |
| `cmp` | Consent management, Consent Mode bridge, CSP reporting |
| `tagmgmt` | Tag managers and tag-delivery libraries |
| `cdp` | Server-side collection, CDP, event streaming |
| `analytics` | Analytics, RUM/APM, session replay |
| `personalization` | Testing, personalization, search/recs, VoC |
| `adtech` | Pixels, conversion tags, affiliate |
| `misc` | Fallback for anything uncategorized |

So: platform systems populate the data layer, consent gates the tag manager, the
tag manager feeds server-side collection and fans out to the destination bands.
Because every band below a source is further down the page, **all your edges
should point downward** — an upward edge usually means a node is in the wrong
band.

## Keeping edges clean

The renderer routes each inter-band edge through the gutter beside the target
band, so it clears intervening rows. What it cannot do is guess which *column* is
free. Two conventions handle that:

1. **Alignment is per band** (built in): `platform`, `datalayer`, `tagmgmt` and
   `cdp` are left-aligned, `cmp` is right-aligned, the destination bands are
   centered. That reserves the left columns as a lane for platform→data
   layer→tag manager edges and keeps consent's edges on the right.
2. **Use `order`** to put an edge's source and target in the same column, or in
   columns that don't collide with a third box. A node with an edge dropping
   several bands should sit in a column that is empty in the bands between.

After rendering, **look at the SVG** before handing it over — open it in the
browser via the chrome-devtools MCP (`new_page` on the `file://` path, then
`take_screenshot` with `fullPage: true`) and check for: edges crossing each other,
edges passing behind a box, band labels colliding with the leftmost column, and
boxes whose `detail` text is clipped. Fix by adjusting `order` or shortening
labels, then re-render and look again.

## Rendering

Write the spec to `/tmp`, render into the project folder, then remove the spec:

```bash
python3 "$SKILL_DIR/render_diagram.py" /tmp/stack.json ./[site]-tech-stack.svg && rm /tmp/stack.json
```

`$SKILL_DIR` is this file's directory. Only the `.svg` belongs in the project
folder — the JSON is scratch.

## What the renderer handles for you

Don't spend reasoning on any of these — they are already guaranteed:

- Bands top-to-bottom in the fixed order above; empty bands are dropped and the
  rest compact upward. Canvas height adapts.
- **Bands wrap onto as many rows as needed — nodes are never dropped or replaced
  with a `+N more` box.** Rows within a band are balanced (5 per row at the
  current width).
- Per-band left/right/center alignment; consistent box size and spacing.
- Nodes sorted within a band by `order`, then by certainty (high first).
- Orthogonal edge paths that end pointing into the target so arrowheads land
  square; vertical detours routed through the band gutter; same-column edges
  collapse to a straight vertical.
- The `bus` trunk, its per-band arrows, and its legend entry.
- Nodes are drawn after all connectors, so no line ever crosses over a box.
- Title, subtitle, note, certainty legend, drop shadows, XML escaping.

## Editable diagram (drawio)

On request only. Reuse the same node/edge model, the same certainty color
encoding, the same band order, and carry the `detail` lines across. Emit drawio
XML as text to `[site]-tech-stack.drawio`. Do not call an MCP renderer.
