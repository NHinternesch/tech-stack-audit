---
name: tech-stack-audit
description: Leverage browser technologies through the Chrome Dev Tools MCP server or other browser automation tools to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, create a well-formatted summary, which is returned to various output channels. The recipient of these summaries is a Pre Sales Solutions Engineer, who needs to get a thorough understanding of a tech stack and the components involved, in order to pitch the solution they are looking to position with a prospect.  Use this skill whenever the user asks to audit a website, inspect a tech stack, identify tools on a site, review martech implementations, or research a prospect's technology setup.
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

### Step 3 — Generate Summary
 
Follow the **Output Format** exactly (see below). Then:
- Display the summary in the conversation
- Save it as a `.md` file to the project folder
 
### Step 4 — Distribution (Optional)
 
Ask the user if they'd like to send the summary to an output channel:
 
| Option | Instructions |
|---|---|
| **Word document** | Save `.docx` to project folder. Font: Helvetica, grayscale only. Body: size 9, headings progressively larger. Read docx skill first if available. |
| **Slack message** | Use Slack MCP if available — prompt for channel. If unavailable, ask for a webhook URL ([how to get one](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)) and send via: `curl -X POST -H 'Content-type: application/json' --data '{"text":"[SUMMARY]"}' [WEBHOOKURL]` |
| **Jira ticket** | Create a draft Jira ticket using the Atlassian MCP server |
| **Confluence page** | Create a draft Confluence page using the Atlassian MCP server |
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
