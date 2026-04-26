---
name: tech-stack-audit
description: "Leverage browser technologies through the Chrome Dev Tools MCP server or other browser automation tools to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, create a well-formatted summary, which is returned to various output channels. The recipient of these summaries is a Pre Sales Solutions Engineer, who needs to get a thorough understanding of a tech stack and the components involved, in order to pitch the solution they are looking to position with a prospect. Use this skill whenever the user asks to audit a website, inspect a tech stack, identify tools on a site, review martech implementations, or research a prospect's technology setup."
allowed-tools: Read, Bash, Write, mcp__chrome-devtools, mcp__atlassian, mcp__plugin_slack_slack
effort: high
---


# Tech Stack Audit

This skill uses the Chrome DevTools MCP server to audit a website's full technology stack and produces a structured summary for Pre-Sales Solutions Engineers preparing to pitch to a prospect.

## Inputs

- **Required**: `[url]` — the website to audit
- **Optional**: `[tool]` (e.g. "Google Analytics") or `[category]` (e.g. "analytics and tracking", "adtech") for a deep-dive focus


## Workflow

When tasked to audit a website, the workflow involves:

### Step 1 - Audit the site
  - Use the Chrome Dev Tools MCP server to navigate to [url]
  - Accept all cookie and compliance banners
  - Perform a hard page reload (Cmd+Shift+R / Ctrl+Shift+R) to capture fresh data
  - Monitor all browser activity, incl. network requests, libraries, cookies, local storage, console output, DOM elements with tracking attributes

### Step 2 — Identify Tools

Based on the data gathered, identify all tools present in the tech stack, grouped by category (analytics, adtech, tag management, CDP, personalization/testing, compliance/CMP, miscellaneous, etc.).

### Step 3 — Generate Summary and Output Document

Follow the **Output Format** exactly (see below). Then, produce both default outputs:

**3a. Summary in conversation** — display the formatted summary inline.

**3b. Word document** — save as a `.docx` file to the project folder. Font: Helvetica, grayscale only. Body: size 9, headings progressively larger. Read docx skill first if available.

**Clean output.** The project folder should end up containing exactly the `.docx` from 3b.

Do **not** leave behind scratch work:
- No helper scripts (e.g. a `build_docx.py` you authored to call `python-docx`) — write them to `/tmp` and remove after the run.
- No intermediate JSON dumps, logs, or screenshots.

The rule of thumb: if a tool *returns* a file (bytes, base64, or a written-out path), keep it. If you had to invent an intermediate file purely for your own workflow, it doesn't belong in the project folder.

### Step 4 — Addditional Output Format and Channels (Optional)

Ask the user if they'd like any additional output formats or output channels and provide a few options:

| Option | Instructions |
|---|---|
| **Architecture diagram** | Generate a hand-authored **SVG** architecture diagram of the audited stack. The diagram is a prospect-facing deliverable, so design quality is a first-class concern — a polished, intentional diagram beats a dense or auto-laid-out one. <br><br>**Two-stage render.** Don't go straight from findings to SVG — build a normalized graph model first, then render from it. This lets the same model also emit drawio XML on request. <br><br>**Stage A — Build the intermediate model.** Translate audit findings into a normalized graph: <br>- **Nodes**: `id`, `label`, `category` (CMP, Tag Management, CDP, Analytics, Personalization, Adtech, Misc), `role` (`hub` or `leaf`), `certainty` (`high`, `medium`, or `low`). <br>- **Edges**: `from`, `to`, `type` (e.g. "loaded by", "sends events to", "syncs audiences with"), `certainty` (`high`, `medium`, or `low`). <br>- **Certainty rubric** — apply consistently: <br>&nbsp;&nbsp;- **High** — direct evidence (network requests, cookies, JS globals, DOM markers from the audit). <br>&nbsp;&nbsp;- **Medium** — partial or indirect evidence (single weak signal, ambiguous host, vendor inferred from a script loader). <br>&nbsp;&nbsp;- **Low** — inferred from typical stack patterns rather than evidence on this site. <br>- Mark **hubs** explicitly — typically the CDP and the central tag manager. Most other nodes hang off them. <br><br>**Stage B — Render SVG (primary, always).** Hand-author the SVG with these rules baked into the output: <br>- **Palette as CSS custom properties** at the top of the `<style>` block: <br>&nbsp;&nbsp;- Category fills: `--cat-cmp`, `--cat-tagmgmt`, `--cat-cdp`, `--cat-analytics`, `--cat-personalization`, `--cat-adtech`, `--cat-misc`. <br>&nbsp;&nbsp;- Certainty colors: `--cert-high` (e.g. solid green), `--cert-medium` (amber), `--cert-low` (muted red/grey). <br>&nbsp;&nbsp;The SE can re-theme by editing these values. <br>- **Reusable classes** defined once and reused: `.box`, `.hub`, `.edge`, `.cert-high`, `.cert-medium`, `.cert-low`, `.swimlane`, `.label`. No inline `style=` overrides on individual elements. <br>- **Color-coded certainty** is the primary confidence encoding — applied to **both** node border (stroke) **and** edge stroke. Every node and edge carries one of the three certainty classes. Use a stroke width of ~2.5px so the certainty color reads at a glance. Do **not** use solid-vs-dashed for certainty; reserve stroke style for other purposes if ever needed. <br>- **Legend** in the top-right of the canvas: small key showing the three certainty colors with labels (High / Medium / Low). Include category swatches too if there's room. <br>- **Swimlanes per category** as `<g>` groups with a light category-tinted fill, ordered top-to-bottom in a logical flow: **Compliance/CMP → Tag Management → CDP → Analytics → Personalization → Adtech → Miscellaneous**. Skip empty bands; do not reorder. <br>- **Hub prominence**: hub nodes are larger (~1.4× leaf size) and sit centered in their band; leaf nodes lay out left-to-right around them. <br>- **Deterministic layout** — do **not** free-form coordinates. Each band has fixed height with consistent padding; tools within a band sit at fixed horizontal spacing; cross-band edges route through a right-side vertical channel to minimize crossings. Boring layout, polished styling. <br>- **Whitespace**: generous padding inside bands and between nodes. A legible diagram beats a complete one — drop low-signal nodes if the canvas gets crowded. <br><br>**Stage C — Render drawio XML (secondary, on request only).** If the user asks for an editable version, walk the same intermediate model and emit drawio XML alongside the SVG. Carry the same palette, hub prominence, and certainty color encoding into the XML. Emit as text — do not call any MCP renderer. <br><br>**Output files**, saved to the project folder: <br>- `[site]-tech-stack.svg` — always, when this option is selected. <br>- `[site]-tech-stack.drawio` — only when the user requests an editable export. <br><br>Do not leave behind helper scripts, intermediate JSON, or scratch sources — the model is built and consumed in the same step. |
| **Slack message** | Use Slack MCP or Slack integration if available — prompt for destination, e.g. channel or direct message. If unavailable, ask for a webhook URL ([how to get one](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)) and send via: `curl -X POST -H 'Content-type: application/json' --data '{"text":"[SUMMARY]"}' [WEBHOOKURL]` |
| **Jira ticket** | Create a draft Jira ticket using the Atlassian MCP server. Return the URL of the created ticket. If Atlassian MCP server is unavailable, instruct the user to install it for seamless integration.|
| **Confluence page** | Create a draft Confluence page using the Atlassian MCP server. Return the URL of the created page. If Atlassian MCP server is unavailable, instruct the user to install it for seamless integration. |
| **None** | Skip distribution |


## Output Format

Use this exact structure. Do not add extra sections unless explicitly requested.

```
**Tech Stack Audit Summary for [SITE AUDITED]**

**Audit Date**: [YYYY-MM-DD]
**URL Audited**: [Full URL]

**Overview**

[Category — e.g. Analytics & Tracking]
- [Tool Name]
  - Certainty: [High | Medium | Low]
  - Traces & Evidence: [network requests, cookies, JS libraries, DOM attributes, etc.]

[Category — e.g. Tag Management]
- [Tool Name]
  - Certainty: [High | Medium | Low]
  - Traces & Evidence: [...]

[Repeat for each category found: Adtech, Personalization & Testing, CDP, Compliance & CMP, Miscellaneous]

Certainty rubric:
- **High** — direct evidence (network requests, cookies, JS globals, DOM markers).
- **Medium** — partial or indirect evidence (single weak signal, ambiguous host, vendor inferred from a script loader).
- **Low** — inferred from typical stack patterns rather than evidence on this site.

**[Tool/Category] Deep Dive** *(only when a specific tool or category was requested)*
- Depth of implementation
- Events tracked and payload details
- How the library is loaded
- Any other implementation-specific observations
```

## Audit Notes

- **Wait time**: Allow 5–10 seconds post-load for delayed/lazy-loaded tags
- **Multiple pages**: If tools aren't found on the homepage, suggest checking product, content, registration, or checkout pages
- **SPA detection**: Note if the site is a Single Page Application — this affects tag loading patterns