# Architecture Diagram Spec

Used by the **Architecture diagram** option in Step 4 of `SKILL.md`. Hand-author by filling the skeleton — never free-form coordinates or invent classes.

**Mental model first.** Before writing SVG, list each tool inline as `{label, category, certainty, hub?}` and each connection as `{from, to, certainty}`. No serialized intermediate file.

**Certainty rubric** — applied to both node stroke and edge stroke:
- **High** — direct evidence (network requests, cookies, JS globals, DOM markers).
- **Medium** — partial or indirect evidence (single weak signal, ambiguous host, vendor inferred from a script loader).
- **Low** — inferred from typical stack patterns rather than evidence on this site.

## Layout constants

| | Value |
|---|---|
| Canvas | `viewBox="0 0 1200 720"` |
| Title | `x=40, y=36` |
| Band height | `80`; bands start every `90` (10px gap) |
| Node | `w=170, h=50`, corner radius `8` |
| Node `x` for index `i` (0-based) | `60 + i*180` — max 6 per band: `60, 240, 420, 600, 780, 960` |
| Node `y` (top edge) | `band_center − 25` |
| Label `text` | `x = node_x + 85`, `y = node_top + 30` |
| Legend | `transform="translate(880, 36)"` — single horizontal row in the title strip, never below `y=40` |

Bands top-to-bottom — **skip empty bands; never reorder**:

| Category | Band top `y` | Center `y` | Node top `y` |
|---|---|---|---|
| Compliance / CMP | 60 | 100 | 75 |
| Tag Management | 150 | 190 | 165 |
| CDP | 240 | 280 | 255 |
| Analytics | 330 | 370 | 345 |
| Personalization | 420 | 460 | 435 |
| Adtech | 510 | 550 | 525 |
| Miscellaneous | 600 | 640 | 615 |

## Edge routing — one rule, no exceptions

End every path with the segment that points into the target so the arrowhead lands correctly:

- **Within-band** (same band): `d="M (x_a+85) y H (x_b−85)"` — arrow lands on target's left edge.
- **Cross-band downward**: `d="M x_a (y_a+25) H x_b V (y_b−25)"` — arrow lands on target's top edge.
- **Cross-band upward**: `d="M x_a (y_a−25) H x_b V (y_b+25)"` — arrow lands on target's bottom edge.

`(x_a, y_a)` and `(x_b, y_b)` are node centers. When source and target share a column, the `H` segment is a no-op and can be dropped.

## Caps

- **Max 6 nodes per band.** If more, keep the highest-certainty 5 and add a `+N more` box at index 5.
- **Hubs** (typically the CDP and the central tag manager) sit in the same grid; visual prominence comes from `class="box hub cert-..."` (thicker stroke), not from special positioning.

## Skeleton

Copy verbatim. Replace `[SITE]`. Delete bands with no nodes. Populate only `<g class="nodes">` and `<g class="edges">`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" font-family="Helvetica, Arial, sans-serif">
  <style>
    :root {
      --cat-cmp: #f5f1f8; --cat-tagmgmt: #faf7ed; --cat-cdp: #eef2f7;
      --cat-analytics: #eef5f1; --cat-personalization: #f7eef3;
      --cat-adtech: #f6ecec; --cat-misc: #f7f7f8;
      --cert-high: #15803d; --cert-medium: #b45309; --cert-low: #94a3b8;
      --ink: #374151;
    }
    .bg { fill: #fafafa; }
    .band rect { stroke: #e5e7eb; stroke-width: 1; }
    .band-label { font-size: 11px; fill: #6b7280; font-weight: 600;
                  text-transform: uppercase; letter-spacing: .05em; }
    .box { fill: #fff; stroke-width: 2; rx: 8; ry: 8; filter: url(#shadow); }
    .hub { stroke-width: 3; }
    .label { font-size: 13px; fill: var(--ink); text-anchor: middle; }
    .edge { fill: none; stroke-width: 2.5; }
    .cert-high   { stroke: var(--cert-high); }
    .cert-medium { stroke: var(--cert-medium); }
    .cert-low    { stroke: var(--cert-low); }
    .title { font-size: 18px; font-weight: 600; fill: var(--ink); }
    .legend-text { font-size: 11px; fill: var(--ink); }
  </style>
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="1" stdDeviation="1.5"
                    flood-color="#000" flood-opacity="0.12"/>
    </filter>
    <marker id="arrow-high" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--cert-high)"/>
    </marker>
    <marker id="arrow-medium" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--cert-medium)"/>
    </marker>
    <marker id="arrow-low" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--cert-low)"/>
    </marker>
  </defs>

  <rect class="bg" x="0" y="0" width="1200" height="720"/>

  <text class="title" x="40" y="36">[SITE] — Tech Stack</text>

  <g class="band"><rect x="40" y="60"  width="1120" height="80" fill="var(--cat-cmp)"/>
    <text class="band-label" x="52" y="76">Compliance / CMP</text></g>
  <g class="band"><rect x="40" y="150" width="1120" height="80" fill="var(--cat-tagmgmt)"/>
    <text class="band-label" x="52" y="166">Tag Management</text></g>
  <g class="band"><rect x="40" y="240" width="1120" height="80" fill="var(--cat-cdp)"/>
    <text class="band-label" x="52" y="256">CDP</text></g>
  <g class="band"><rect x="40" y="330" width="1120" height="80" fill="var(--cat-analytics)"/>
    <text class="band-label" x="52" y="346">Analytics</text></g>
  <g class="band"><rect x="40" y="420" width="1120" height="80" fill="var(--cat-personalization)"/>
    <text class="band-label" x="52" y="436">Personalization</text></g>
  <g class="band"><rect x="40" y="510" width="1120" height="80" fill="var(--cat-adtech)"/>
    <text class="band-label" x="52" y="526">Adtech</text></g>
  <g class="band"><rect x="40" y="600" width="1120" height="80" fill="var(--cat-misc)"/>
    <text class="band-label" x="52" y="616">Miscellaneous</text></g>

  <g class="nodes">
    <!-- <rect class="box cert-high" x="60" y="165" width="170" height="50"/>
         <text class="label" x="145" y="195">Tool Name</text> -->
  </g>

  <g class="edges">
    <!-- <path class="edge cert-high" d="M ..." marker-end="url(#arrow-high)"/> -->
  </g>

  <g class="legend" transform="translate(880, 36)">
    <text class="legend-text" x="0"   y="0" font-weight="700">Certainty:</text>
    <line x1="65"  y1="-4" x2="85"  y2="-4" stroke="var(--cert-high)"   stroke-width="2.5"/>
    <text class="legend-text" x="91"  y="0">High</text>
    <line x1="130" y1="-4" x2="150" y2="-4" stroke="var(--cert-medium)" stroke-width="2.5"/>
    <text class="legend-text" x="156" y="0">Medium</text>
    <line x1="215" y1="-4" x2="235" y2="-4" stroke="var(--cert-low)"    stroke-width="2.5"/>
    <text class="legend-text" x="241" y="0">Low</text>
  </g>
</svg>
```

## Worked example

Three nodes (GTM → Segment hub → GA4), two cross-band edges in the same column. Pattern-match shape and indentation:

```svg
<g class="nodes">
  <rect class="box cert-high"     x="60" y="165" width="170" height="50"/>
  <text class="label" x="145" y="195">Google Tag Manager</text>

  <rect class="box hub cert-high" x="60" y="255" width="170" height="50"/>
  <text class="label" x="145" y="285">Segment</text>

  <rect class="box cert-medium"   x="60" y="345" width="170" height="50"/>
  <text class="label" x="145" y="375">Google Analytics 4</text>
</g>

<g class="edges">
  <!-- GTM (center 145,190) → Segment (145,280): same column, V only -->
  <path class="edge cert-high"   d="M 145 215 V 255" marker-end="url(#arrow-high)"/>
  <!-- Segment (145,280) → GA4 (145,370): same column, V only -->
  <path class="edge cert-medium" d="M 145 305 V 345" marker-end="url(#arrow-medium)"/>
</g>
```

For an offset cross-band edge — e.g. Segment at `x=145` to an Adtech tool at `x=600`:
`d="M 145 305 H 600 V 525"` with `marker-end="url(#arrow-...)"`.
