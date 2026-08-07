# Architecture Diagram Spec

Used by the **Architecture diagram** option in Step 4 of `SKILL.md`.

Write a JSON spec, then run the bundled renderer. Do **not** hand-author SVG — the
renderer owns all layout, coordinates, styling, and edge routing.

## Spec schema

```json
{
  "site": "example.com",
  "nodes": [
    {"label": "Google Tag Manager", "category": "tagmgmt", "certainty": "high", "hub": true},
    {"label": "Google Analytics 4", "category": "analytics", "certainty": "high"}
  ],
  "edges": [
    {"from": "Google Tag Manager", "to": "Google Analytics 4", "certainty": "medium"}
  ]
}
```

- `category` — one of `cmp`, `tagmgmt`, `cdp`, `analytics`, `personalization`,
  `adtech`, `misc`. Anything unrecognized falls back to `misc`.
- `certainty` — `high` | `medium` | `low`. Drives node stroke, edge stroke, and
  arrowhead color.
- `hub` — optional, thickens the stroke. Use for the CDP and the central tag
  manager: the nodes most things flow through.
- `edges` — `from`/`to` must match a node `label` exactly. Edges naming a node
  that isn't on the diagram are skipped with a warning on stderr.

Data flow direction: CMP gates the tag manager, the tag manager feeds the CDP, the
CDP fans out to analytics/personalization/adtech. Draw the edges you have evidence
for, not every theoretically possible one.

## Rendering

Write the spec to `/tmp`, render into the project folder, then remove the spec:

```bash
python3 "$SKILL_DIR/render_diagram.py" /tmp/stack.json ./[site]-tech-stack.svg && rm /tmp/stack.json
```

`$SKILL_DIR` is this file's directory. Only the `.svg` belongs in the project
folder — the JSON is scratch.

## What the renderer handles for you

Don't spend reasoning on any of these — they are already guaranteed:

- Category bands top-to-bottom in fixed order; empty bands are dropped and the
  rest compact upward. Canvas height adapts.
- Node rows centered horizontally; consistent box size and spacing.
- Nodes sorted within a band by certainty (high first).
- **Max 6 per band** — beyond that, the top 5 by certainty are kept and a
  `+N more` box is added.
- Edge paths that always end pointing into the target so arrowheads land square;
  horizontals routed through the band gutter; same-column edges collapse to a
  straight vertical.
- Title, certainty legend, drop shadows, XML escaping.

## Editable diagram (drawio)

On request only. Reuse the same node/edge model and the same certainty color
encoding, carry over the band order above, and emit drawio XML as text to
`[site]-tech-stack.drawio`. Do not call an MCP renderer.
