---
name: tech-stack-audit
description: "Audits a website's front-end technology stack in a live browser by inspecting network traffic, cookies, JS globals and the data layer across several page types, then produces a single self-contained HTML report with an architecture diagram. Use when the user asks to audit a website, inspect or research a tech stack, identify the analytics, adtech, tag management, CDP, personalization or consent vendors on a site, or review a martech implementation."
allowed-tools: Read, Write, mcp__chrome-devtools, mcp__playwright
effort: high
metadata:
  version: 4.2.0
---

# Tech Stack Audit

Audit a website's technology stack in a live browser and deliver one HTML report.

The reader is a pre-sales solutions engineer. They need to understand a prospect's
stack well enough to position a solution against it. Name vendors precisely, ground
every claim in observed evidence, and say plainly what you could not confirm.

## Inputs

A URL and, optionally, a focus: a tool (such as "Google Analytics") or a category
(such as "adtech"). If no URL is given, ask for one.

## Browser

Use whichever browser-control tool you have: Chrome DevTools MCP, Playwright MCP or
another. You need to navigate, run JavaScript in the page and get its result, click,
and take screenshots. Listing network requests with headers helps some targeted
checks; without it, record those checks under Not covered. With no browser tool, say
so and stop.

## Deliverable

Produce one self-contained HTML file named `<site>-tech-stack-audit-<YYYY-MM-DD>.html`,
where `<site>` is the domain with dots replaced by hyphens. Save it wherever your
environment puts files for the user, and keep any scratch files out of that place.
Don't publish, upload or send the report anywhere.

When you're done, reply with where the report is and up to three one-line findings.

## Certainty rubric

Rate every tool. The report shows only the High, Medium or Low rating.

- **High**: direct evidence. A request to a vendor host, a vendor cookie, a JS global, or a vendor ID in a live request.
- **Medium**: partial evidence. A single weak signal, an ambiguous host, a stub with no traffic, or a vendor inferred from a loader.
- **Low**: inferred from typical stack patterns rather than seen on this site.

A vendor that is referenced but not live is not a finding. That covers a script that
404s, a host seen only in a CSP header, and a config entry with no traffic. List
these on one `Referenced, not live` row in Sources.

## Workflow

### 1. Page digest

Your evidence comes from one JavaScript evaluation per page that returns a compact
JSON digest of a few KB. A raw network request list on a busy page runs to tens of
KB, so keep it for targeted checks. Write the digest function once, then reuse the
exact same text on every page so the digests are comparable. Make it:

- **Wait and scroll.** First call `performance.setResourceTimingBufferSize(5000)`,
  because browsers keep only 250 resource entries by default. Scroll to the bottom
  to trigger lazy tags. Then poll `performance.getEntriesByType("resource")` every
  500 ms until the count is stable for 2.5 s, with a 12 s cap.
- **Hosts.** List each resource hostname with its request count, initiator types
  and two or three sample paths. Flag `responseStatus >= 400`, because a 404'd
  vendor isn't live.
- **IDs.** Regex `GTM-`, `G-`, `AW-`, `DC-` and `UA-` IDs out of resource URLs and
  inline scripts, and add the keys of `google_tag_manager`.
- **Globals.** Take the names in `Object.getOwnPropertyNames(window)` that are absent
  from a freshly appended blank iframe's window. This catches vendors without
  needing a list.
- **Data layer.** Cover `dataLayer`, any custom GTM data layer
  (`google_tag_manager[id].dataLayer.name`), `adobeDataLayer`, `digitalData` and
  `utag_data`. Return event names with counts, the union of keys, and one sample
  push with string values truncated.
- **Consent state.** Read `google_tag_data.ics.entries`, `OnetrustActiveGroups`,
  `Cookiebot.consent` and `__tcfapi("ping")` (with a 1.5 s timeout), only to confirm
  that consent is fully granted.
- **Cookies and storage.** Use `cookieStore.getAll()` for name, domain and lifetime
  (from `expires`), or `document.cookie` names where it's missing. Add the
  `localStorage` and `sessionStorage` key names. Never return cookie or storage
  values.
- **Page.** Return the URL, the title, framework markers (`__NEXT_DATA__`,
  `ng-version`, `__NUXT__`, `drupalSettings` and so on), iframe hosts, and the
  timezone. On the homepage, also return up to 60 internal links with their text,
  for choosing page types.

Entries dropped before the digest runs are lost. If your tool can inject a script
before page load, set the buffer size there too. Otherwise treat exactly 250 entries
as truncated and take that page's hosts from the network request list.

### 2. Accept all consent first

The audit assumes full consent, so every tool fires and gets used before you collect
anything. Open the URL in a fresh browser context with no cookies and accept every
consent and cookie banner. In page JavaScript, find the visible button, searching open
shadow roots too, whose text means accept all in the site's language ("Accept all",
"Allow all", "Alle akzeptieren"), then `.click()` it. If the banner sits in a
cross-origin iframe, click it through the tool's page snapshot instead.

Then reload, bypassing the cache if your tool can, so tags load cold with consent
granted, and check in the digest that consent is fully granted. Accept any banner
that appears on a later page too. Every page uses this one context.

### 3. Page types

Always audit several page types, because commerce, content and conversion tags
concentrate away from the homepage. From the homepage links, pick at least three
distinct types the site has (the homepage counts as one), and at most six:

| Site model | Page types |
|---|---|
| Publisher / media | home, section, article, video or live page, subscription or offer page |
| E-commerce | home, category or listing, product (PDP), search results, cart |
| Lead-gen, finance, SaaS | home, product or service, pricing or quote start, blog or content article, sign-up or contact page |

Run the digest on each page in the same context. Don't log in, submit forms, enter
personal data or buy anything; stop at the first step of a funnel.

A framework marker alone doesn't make a site a single-page app. Check first whether
internal links do full loads: each page shows a fresh `dataLayer` and
`performance.getEntriesByType("navigation")[0].type` is `"navigate"`. Only if they
don't, change route client-side once and report whether pageviews or data-layer pushes
fire.

### 4. Targeted checks

Use these sparingly. Always filter network request lists by resource type and keep
them short.

- **Focus tools.** Read real payloads and live configuration. For GA4, take event
  names and parameters from `/g/collect` URLs, and from POST bodies when events are
  batched. For SDKs, use public config getters such as
  `DD_RUM.getInitConfiguration()` or a vendor's config global. Without a focus, do
  this for the tag manager and the main analytics tool.
- **Server-set cookies.** Read `Set-Cookie` on a first-party collector, such as a
  server-side GTM endpoint, or on the main document. A first-party HttpOnly
  identifier survives Safari's 7-day cap on JS-set cookies, which matters for
  positioning. A document's request detail can include the full HTML body, so read
  it only when needed.
- **Third-party cookies.** Check one request per major ad or ID vendor rather than
  all of them.
- **Cross-origin iframes.** The digest can't see requests made inside them. When an
  ad or widget iframe matters, list its requests filtered by type.

### 5. Write the report

Fill in the template below and save the report.

## Report

The structure is fixed. Always render these five sections in this order, even when
one is thin:

1. **Architecture**: the diagram.
2. **Top-line findings**: one to three single-line bullets, chosen for what most
   changes how a solution is positioned. Examples are first-party or server-side
   collection, a dual tag manager, a rich or missing data layer, or a competitor's
   product in place.
3. **Tools by category**: every tool, one line each. That's a certainty chip, the
   precise vendor and product name, and one evidence sentence covering hosts, IDs,
   cookies, and the page types where it appears. Use these
   categories, in this order, and leave out empty ones: Compliance & CMP, Tag
   Management, CDP & Server-Side, Analytics & Tracking, Personalization & Testing,
   Adtech, Platform & Hosting, Miscellaneous.
4. **`<Focus>` Deep Dive**, or **Stack Deep Dive** without a focus: one block per
   focus tool. Without a focus, cover the tag manager, the CMP and the main analytics
   tool. Use label/value rows: evidence, events and parameters, configuration, load
   path, cookies, data layer, and customization level (low, medium or high).
5. **Sources**: every URL audited with its page type. Then coverage rows: session
   date and environment, what wasn't covered, server-set cookies, and `Referenced,
   not live`.

The data layer and cookies have no sections of their own. They are part of the
investigation, and each finding sits with the tool it belongs to. It goes in a Deep
Dive row for focus tools, otherwise in a clause of the tool's one line. Data-layer
structure belongs to the tag manager. Call out cookie lifetimes over 13 months (395
days).

Writing rules:

- **Report what is present.** Leave out empty categories, and never write that a vendor
  was "not found". The exception: when the user asked about a specific tool or
  category, one line saying it isn't present answers their question.
- **No narrative prose.** Write no summary, overview, conclusion or recommendations
  beyond the five sections.
- **Evidence over adjectives.** Every line and row carries concrete traces.
- **Don't repeat yourself.** A Deep Dive tool's line in Tools by category says what it
  is and where it was seen. The detail belongs in its rows.
- **Privacy.** Never put cookie values, user identifiers, emails or tokens in the
  report.

### Template

Copy this verbatim and replace only the `{…}` placeholders and the repeated blocks.
The CSS fixes the look: Helvetica, warm neutrals, certainty chips and hairline rows.

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{site} – Tech Stack Audit · {9 Oct 2026}</title>
<style>
:root{--page:#fbfaf9;--ink:#251f21;--ink-2:#585254;--hairline:#eae9ea}
*{box-sizing:border-box}
body{margin:0;padding:24px 16px;background:#f4efec;color:var(--ink);font:14px/24px "Helvetica Neue",Helvetica,Arial,sans-serif}
.card{max-width:1040px;margin:0 auto;padding:40px 24px 48px;background:var(--page);display:flex;flex-direction:column;gap:48px}
h1,h2{margin:0;font-weight:400;line-height:1.1}h1{font-size:30px}h2{font-size:21px}
h3{font-size:14px;line-height:22px;font-weight:600;margin:0 0 4px;padding-bottom:4px;border-bottom:1px solid var(--hairline)}
.group{display:flex;flex-direction:column;gap:20px;min-width:0}.findings{margin:0;padding-left:20px}
.dwrap{overflow-x:auto}.diagram{width:100%;min-width:760px;height:auto;display:block}
.diagram .bt{font-size:12.5px;font-weight:600;fill:var(--ink)}.diagram .bs{font-size:10px;fill:var(--ink-2)}
.diagram .lay{font-size:10.5px;letter-spacing:.06em;font-weight:600;fill:var(--ink-2);paint-order:stroke;stroke:var(--page);stroke-width:6px}
.diagram .ar{fill:none;stroke:var(--ink-2);stroke-width:1.2}.diagram .ah,.diagram .dot{fill:var(--ink-2)}
.cat,.dd{margin:0 0 18px}.dd h3{display:flex;align-items:center;gap:10px}
.tool,.spec>div{display:grid;grid-template-columns:64px 1fr;gap:10px;padding:7px 0;border-bottom:1px solid var(--hairline);font-size:12.5px;line-height:19px}
.spec{margin:0}.spec>div{grid-template-columns:170px 1fr}.spec dd{margin:0;overflow-wrap:anywhere}.spec+.spec{margin-top:20px}.line,.spec dt{color:var(--ink-2)}
.chip{display:inline-block;text-align:center;font-size:11px;font-weight:600;line-height:20px;border-radius:10px;padding:0 6px;min-width:54px}
.chip.high{background:#dff3e4;color:#14532d}.chip.medium{background:#fdf0cf;color:#6b4e00}.chip.low{background:#e9e9ec;color:#444}
@media (max-width:600px){.spec>div{grid-template-columns:1fr;gap:2px}body{padding:12px 8px}.card{padding:28px 16px}}
@media print{body{background:#fff;padding:0}.card{max-width:none}.dwrap{overflow:visible}.diagram{min-width:0}}
</style></head>
<body><main class="card">
<header><h1>{site} – Tech Stack Audit · {9 Oct 2026}</h1></header>

<section class="group"><h2>Architecture</h2><div class="dwrap">
<svg class="diagram" viewBox="0 0 992 {H}" role="img" aria-label="Architecture of the observed {site} stack">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" class="ah"/></marker></defs>
{arrows, then layer labels, then boxes — see Diagram}
</svg></div></section>

<section class="group"><h2>Top-line findings</h2><ul class="findings">
<li>{finding}</li>
</ul></section>

<section class="group"><h2>Tools by category</h2>
<section class="cat"><h3>{Category}</h3>
<div class="tool"><span class="chip high">High</span><div><strong>{Vendor product}</strong> <span class="line">{evidence sentence}</span></div></div>
</section>
</section>

<section class="group"><h2>{Focus} Deep Dive</h2>
<div class="dd"><h3><span class="chip high">High</span>{Vendor product}</h3>
<dl class="spec"><div><dt>{Label}</dt><dd>{value}</dd></div></dl></div>
</section>

<section class="group"><h2>Sources</h2>
<dl class="spec"><div><dt>{Page type}</dt><dd>{URL}</dd></div></dl>
<dl class="spec"><div><dt>{Session | Not covered | Server-set cookies | Referenced, not live}</dt><dd>{value}</dd></div></dl>
</section>
</main></body></html>
```

### Diagram

Every tool in Tools by category gets a box, plus one box for the data layer object. The
diagram shows the data flow top to bottom, so all arrows point down.

**Layers.** Stack these as horizontal bands in this order and skip empty ones. Number
the ones you keep from 1, with a `class="lay"` label in capitals ("1 SITE & PLATFORM"):

| Layer | Holds | Fill / stroke |
|---|---|---|
| Site & platform | CMS, framework, CDN, RUM bundled in the app | `#eef1f4` / `#596b7b` |
| Data layer | the data layer object(s) | `#e4f4f1` / `#29786b` |
| Consent | CMP, bot defense | `#f0e9fa` / `#7352a0` |
| Tag management | tag managers, Consent Mode | `#e4f4f1` / `#29786b` |
| Server-side & CDP | server-side tagging, CDP, event streaming | `#fde7ed` / `#a94762` |
| Analytics | analytics, session replay | `#e8efff` / `#315fa8` |
| Personalization & testing | testing, personalization, recs | `#e5f3fa` / `#357795` |
| Adtech | pixels, conversion tags, ad serving | `#fff0db` / `#9a6419` |
| Other | chat, widgets, everything else | `#f1efee` / `#7a7476` |

**Boxes.** Give boxes in a layer equal size and spacing, wrapping to a new row when
a layer is full. Each box holds the name (`class="bt"`) and one detail line, such as an
account ID, container or endpoint (`class="bs"`). Use a solid stroke for high
certainty, `stroke-dasharray="4 3"` for medium and `"1.5 2.5"` for low. Draw the data
layer and tag manager boxes with a heavier stroke as hubs.

**Arrows.** Use `class="ar"` with `marker-end="url(#ah)"`. Draw them only for
evidenced relationships, such as platform → data layer, data layer → tag manager,
CMP → Consent Mode, and tag manager → server-side. Show the tag manager's dispatch to
vendor layers as one rail down the left margin, with a branch per layer, not one arrow
per vendor. Place connected boxes in the same column where you can.

**Draw order:** arrows first, then layer labels (their halo masks lines passing behind),
then boxes. Set `{H}` to fit the content.

### Check before handing over

Load the report in the browser and take a full-page screenshot.
Check that:

- all five sections are present, in order;
- every tool in Tools by category has a box;
- no box text is clipped;
- no arrow crosses a box;
- no section repeats another.

Fix anything that fails, then close every page you opened.
