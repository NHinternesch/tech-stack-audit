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
| **Architecture diagram** | Generate a hand-authored **SVG** architecture diagram. **Read `diagram-spec.md`** (sibling of this file) for the skeleton, layout constants, edge-routing rule, caps, and worked example. Do **not** free-form layout or styling; fill the skeleton's `<g class="nodes">` and `<g class="edges">` only. Output: `[site]-tech-stack.svg`. |
| **Editable diagram (drawio)** | On request only. Walk the same node/edge mental model used for the SVG and emit drawio XML, carrying over the same palette, swimlane order, and certainty color encoding. Emit as text — do not call any MCP renderer. Output: `[site]-tech-stack.drawio`. |
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

**[Tool/Category] Deep Dive** *(only when a specific tool or category was requested)*
- Depth of implementation
- Events tracked and payload details
- How the library is loaded
- Any other implementation-specific observations
```

**Certainty rubric — internal guidance only; never include in the inline summary or the `.docx`:**
- **High** — direct evidence (network requests, cookies, JS globals, DOM markers).
- **Medium** — partial or indirect evidence (single weak signal, ambiguous host, vendor inferred from a script loader).
- **Low** — inferred from typical stack patterns rather than evidence on this site.

## Audit Notes

- **Wait time**: Allow 5–10 seconds post-load for delayed/lazy-loaded tags
- **Multiple pages**: If tools aren't found on the homepage, suggest checking product, content, registration, or checkout pages
- **SPA detection**: Note if the site is a Single Page Application — this affects tag loading patterns
- **No meta-commentary**: After producing outputs, reply only with what the user asked for. Do not append observations, "stress-test notes", or critiques about the skill itself, the diagram spec, or the auditing process — those belong in a separate feedback request, not in audit deliverables.