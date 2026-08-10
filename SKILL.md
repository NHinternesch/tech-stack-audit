---
name: tech-stack-audit
description: "Audit a website's front-end technology stack via browser automation — inspect network requests, cookies, JS globals, and DOM markers to identify analytics, adtech, tag management, CDP, personalization, and consent tools, then produce a formatted summary, a Word document, and optional architecture diagram or Slack/Jira/Confluence output. Use this skill whenever the user asks to audit a website, inspect or research a tech stack, identify tools or vendors on a site, or review a martech implementation."
allowed-tools: Read, Write, Bash, Skill, AskUserQuestion, mcp__chrome-devtools
effort: high
metadata:
  version: 2.2.0
---

# Tech Stack Audit

Audit a website's full technology stack and produce a structured summary.

The reader is a Pre-Sales Solutions Engineer who needs to understand a prospect's
stack and the components involved well enough to position a solution against it.
Write for that reader: name vendors precisely, ground every claim in observed
evidence, and be explicit about what you could not confirm.

## Inputs

- **Required**: `[url]` — the website to audit
- **Optional**: `[tool]` (e.g. "Google Analytics") or `[category]` (e.g. "adtech")
  for a deep-dive focus

## Certainty rubric

Assign to every tool identified. Internal guidance for your own judgement — the
rubric definitions themselves never appear in the summary or the `.docx`, only the
resulting High/Medium/Low rating.

- **High** — direct evidence: network request to a vendor host, vendor cookie, JS
  global, or DOM marker.
- **Medium** — partial or indirect evidence: a single weak signal, an ambiguous
  host, or a vendor inferred from a script loader.
- **Low** — inferred from typical stack patterns rather than evidence on this site.

## Workflow

### Step 1 — Audit the site

1. `navigate_page` to `[url]`.
2. Accept cookie and consent banners — take a snapshot to find them. Consent state
   gates a large share of tags, so tags stay dormant until you accept.
3. Perform hard reload with `navigate_page` (`type: "reload"`, `ignoreCache: true`) to capture a
   cold load with consent granted.
4. Wait 5–10 seconds for delayed and lazy-loaded tags before collecting.
5. Collect evidence:
   - `list_network_requests` — the primary signal. Vendor hosts and payloads.
   - `evaluate_script` — JS globals (`dataLayer`, `ga`, `gtag`, `_satellite`,
     `utag`, `analytics`, `Optimizely`), `document.cookie`, and `localStorage`
     keys.
   - `list_console_messages` — vendor init logs and errors.
   - `take_snapshot` — DOM tracking attributes.

Also note:

- **SPA**: if the site is a Single Page Application, say so — it changes tag
  loading patterns, and route changes may fire tags a single page load misses.
- **Thin results**: if the homepage yields little, audit a product, article,
  registration, or checkout page — commerce and conversion tags concentrate there.
  Offer this rather than reporting an empty stack.

### Step 2 — Identify tools

Group the identified tools by category: Compliance & CMP, Tag Management, CDP,
Analytics & Tracking, Personalization & Testing, Adtech, Miscellaneous. Assign each
a certainty rating per the rubric above.

Distinguish a vendor actually present from one merely referenced — a script that
404s, or a host that only appears in a CSP header or a commented-out tag, is not a
live implementation. Note those separately rather than counting them as findings.

### Conciseness rules

These apply to every output — the inline summary, the `.docx`, and any Slack, Jira,
or Confluence text. They override any instinct to be thorough by adding words.

- **Report only what is present.** Never write that a vendor, category, or signal
  was absent. No "no X was found", no "we did not detect", no empty-category
  headings. A category with nothing in it is simply omitted. The reader infers
  absence from silence; spelling it out is filler.
  - Avoid: "No Optimizely, VWO, AB Tasty, Kameleoon, Adobe Target or Dynamic Yield
    signal was found."
  - One exception: if the user explicitly asked about a specific tool or category,
    a single line stating it is not present answers their question — that is a
    finding, not filler.
- **No prose summary blocks.** Do not open or close with a narrative paragraph
  synthesizing the stack. No "Executive Summary", "Overview" prose, "Key Takeaways",
  "Conclusion", or "Positioning" section. The category listing and any requested
  deep dive are the deliverable.
  - Avoid: "[Site] runs a dual tag-management setup. GTM is present but its
    analytics layer is almost entirely paused; the live measurement platform is…"
- **Top-line findings instead.** Where a summary would go, use at most 3 bullets,
  one line each, stating the findings that most change how a solution is
  positioned — not a restatement of the category list. Fewer than 3 is fine. Zero
  is fine when nothing stands out.
- No filler transitions, no restating a finding in the deep dive that the category
  listing already covered, no meta-commentary on the audit process.

### Step 3 — Summary and document

Follow the **Output Format** below exactly. Produce a word document as the main deliverable. In the inline summary, only state result/success and a brief summary with 3 short bullet points max.

**Word document** — `.docx` in the project folder (the user's cwd). Font
Helvetica, grayscale only, body size 9, headings progressively larger. Invoke the
`docx` skill first if available.

**Clean output.** The project folder ends up with exactly the `.docx`, plus any
diagram file from Step 4. Write helper scripts and intermediate specs to `/tmp` and
remove them after the run — no builder scripts, JSON dumps, logs, or screenshots in
the project folder. Rule of thumb: keep what a tool *returns* as a file; anything
you invented for your own workflow does not belong there.

### Step 4 — Additional outputs (optional)

Ask via `AskUserQuestion` (`multiSelect: true`) which additional outputs the user
wants, offering these options:

| Option | Instructions |
|---|---|
| **Architecture diagram** | Read `diagram-spec.md` (sibling of this file) and follow it. Every vendor from the audit goes on the diagram, each with its account ID or endpoint, and you render then *look* at the result before handing it over. Output: `[site]-tech-stack.svg` in the project folder. |
| **Editable diagram (drawio)** | See the drawio section of `diagram-spec.md`. Output: `[site]-tech-stack.drawio`. |
| **Slack message** | Use the Slack MCP server; prompt for channel or DM. If unavailable, tell the user to install it. |
| **Jira ticket** | Create a draft ticket via the Atlassian MCP server; return the URL. If unavailable, tell the user to install it. |
| **Confluence page** | Create a draft page via the Atlassian MCP server; return the URL. If unavailable, tell the user to install it. |

Confirm the destination before sending anything outward — a Slack post, ticket, or
page is visible to others and awkward to retract.

## Output Format

Use this structure. Do not add sections unless asked — no prose summary section
before, between, or after these.

```
**Tech Stack Audit Summary for [SITE AUDITED]**

**Audit Date**: [YYYY-MM-DD]
**URL Audited**: [Full URL]

**Top-Line Findings** *(omit entirely if nothing stands out)*
- [One line. The finding that most changes how a solution is positioned.]
- [Max 3 bullets total. Fewer is better. No paragraphs.]

**Stack**

[Category — e.g. Analytics & Tracking]
- [Tool Name]
  - Certainty: [High | Medium | Low]
  - Traces & Evidence: [network requests, cookies, JS globals, DOM attributes]

[Repeat only for categories with at least one tool found — omit the rest]

**[Tool/Category] Deep Dive** *(only when a specific tool or category was requested)*
- Depth of implementation
- Events tracked and payload details
- How the library is loaded
- Other implementation-specific observations
```

## Closing

After producing the outputs, reply only with what the user asked for. Do not append
observations, stress-test notes, or critiques of the skill, the diagram spec, or the
audit process — those belong in a separate feedback request, not in deliverables.
