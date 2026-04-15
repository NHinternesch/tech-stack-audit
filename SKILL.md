---
name: tech-stack-audit
description: "Leverage browser technologies through the Chrome Dev Tools MCP server or other browser automation tools to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, create a well-formatted summary, which is returned to various output channels. The recipient of these summaries is a Pre Sales Solutions Engineer, who needs to get a thorough understanding of a tech stack and the components involved, in order to pitch the solution they are looking to position with a prospect. Use this skill whenever the user asks to audit a website, inspect a tech stack, identify tools on a site, review martech implementations, or research a prospect's technology setup."
allowed-tools: Read, Bash, Write, mcp__chrome-devtools, mcp__atlassian, mcp__plugin_slack_slack, mcp__mermaid-mcp, mcp__claude_ai_Mermaid_Chart, mcp__drawio, mcp__claude_ai_Excalidraw
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

### Step 3 — Generate Summary, Document, and Architecture Diagram

Follow the **Output Format** exactly (see below). Then, produce all three default outputs:

**3a. Summary in conversation** — display the formatted summary inline.

**3b. Word document** — save as a `.docx` file to the project folder. Font: Helvetica, grayscale only. Body: size 9, headings progressively larger. Read docx skill first if available.

**3c. Tech stack architecture diagram** — generate a visualization of the findings that shows tools grouped by category and the observed/inferred data flows between them (e.g. CMP → Tag Manager → Analytics / Adtech / Personalization; CDP fan-in and fan-out; server-side vs. client-side splits). Use subgraphs or swimlanes per category, nodes for individual tools, and edges for relationships (e.g. "loaded by", "sends events to", "syncs audiences with").

Detect the first available diagramming option from this priority list and use it:

1. **Mermaid via MCP** — if `mcp__mermaid-mcp__validate_and_render_mermaid_diagram` or `mcp__claude_ai_Mermaid_Chart__validate_and_render_mermaid_diagram` is available, render a Mermaid `flowchart` diagram.
2. **Drawio via MCP** — if `mcp__drawio__open_drawio_mermaid` or `mcp__drawio__open_drawio_xml` is available, open the diagram in Drawio (Mermaid source can be passed through `open_drawio_mermaid`).
3. **Excalidraw via MCP** — if `mcp__claude_ai_Excalidraw__export_to_excalidraw` is available, export the diagram to Excalidraw.
4. **Inline Mermaid artifact** — if executing inside Claude.ai (artifacts supported), emit the Mermaid source in a renderable artifact.
5. **Fallback** — if none of the above are available, **skip auto-generation** and add a **Diagram distribution** row to the Step 4 options table (see below). Note this clearly in the conversation so the user knows why the diagram wasn't produced automatically.

**Clean output.** The project folder should end up containing exactly two kinds of files:

1. The `.docx` from 3b.
2. Any diagram file the chosen tool produces **as its deliverable** — e.g. a rendered PNG/JPG/SVG returned by a Mermaid-render MCP, or a `.drawio` / `.excalidraw` file the tool writes out. Save these if and only if the tool itself emits a file artifact; match the tool's native format.

Do **not** leave behind scratch work:
- No helper scripts (e.g. a `build_docx.py` you authored to call `python-docx`) — write them to `/tmp` and remove after the run.
- No diagram source files written just to feed a tool that opens the diagram elsewhere. For example, `mcp__drawio__open_drawio_mermaid` renders in-browser from a string argument — do not also write the Mermaid to a `.mmd` file in the project folder.
- No intermediate JSON dumps, logs, or screenshots.

The rule of thumb: if the tool *returns* a file (bytes, base64, or a written-out path), keep it. If you had to invent an intermediate file purely for your own workflow, it doesn't belong in the project folder.

### Step 4 — Distribution (Optional)

Ask the user if they'd like to send the summary to an output channel:

| Option | Instructions |
|---|---|
| **Slack message** | Use Slack MCP or Slack integration if available — prompt for destination, e.g. channel or direct message. If unavailable, ask for a webhook URL ([how to get one](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)) and send via: `curl -X POST -H 'Content-type: application/json' --data '{"text":"[SUMMARY]"}' [WEBHOOKURL]` |
| **Jira ticket** | Create a draft Jira ticket using the Atlassian MCP server. Return the URL of the created ticket. If Atlassian MCP server is unavailable, instruct the user to install it for seamless integration.|
| **Confluence page** | Create a draft Confluence page using the Atlassian MCP server. Return the URL of the created page. If Atlassian MCP server is unavailable, instruct the user to install it for seamless integration. |
| **Diagram distribution** *(only shown if no diagramming tool was available in Step 3c)* | The architecture diagram could not be auto-generated because no diagramming tool was detected. Offer the user these setup paths and, once one is enabled, regenerate just the diagram: <br>• **Mermaid MCP server** — install the `mermaid-mcp` server (see [mermaid-mcp on GitHub](https://github.com/mermaid-js)) and restart the Claude Code session. Lightweight, text-based, best for quick flowcharts. <br>• **Drawio MCP server** — install the `drawio-mcp` server for editable, shareable architecture diagrams opened directly in Drawio. Best when the Solutions Engineer wants to hand-edit the diagram before a pitch. <br>• **Mermaid Chart connector** — in Claude.ai, add the Mermaid Chart connector under Settings → Connectors. <br>• **Excalidraw connector** — in Claude.ai, add the Excalidraw connector for hand-drawn style diagrams. <br>• **Run in Claude.ai** — rerun the skill inside Claude.ai, where Mermaid source renders natively as an artifact with no MCP required. <br>As a last resort, output the raw Mermaid source in the conversation so the user can paste it into [mermaid.live](https://mermaid.live) or similar. |
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
  - Traces & Evidence: [network requests, cookies, JS libraries, DOM attributes, etc.]

[Category — e.g. Tag Management]
- [Tool Name]
  - Traces & Evidence: [...]

[Repeat for each category found: Adtech, Personalization & Testing, CDP, Compliance & CMP, Miscellaneous]

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
- **Confidence levels**: If evidence for a tool is weak or indirect, flag it with a confidence note (e.g. "possibly present — weak signal")