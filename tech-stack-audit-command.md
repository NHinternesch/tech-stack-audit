# Tech Stack Audit Command


## Primary Objective

Leverage browser technologies through the Chrome Dev Tools MCP server to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, create a well-formatted summary, which is returned to various output channels. The recipient of these summaries is a Pre Sales Solutions Engineer, who needs to get a thorough understanding of a tech stack and the components involved, in order to pitch the solution they are looking to position with a prospect. 


## Inputs
- Required: [url]
- Optional: [tool] (e.g. Google Analytics) or [category] (e.g. analytics and tracking or adtech) for deep dive focus


## Workflow

When tasked to audit a website, the workflow involves:

1. **Audit the site**
  - Use the Chrome Dev Tools MCP server to navigate to [url] 
  - Accept all cookie and compliance banners
  - Perform a hard page reload (Cmd+Shift+R / Ctrl+Shift+R) to capture fresh data
  - Monitor all browser activity, incl. network requests, libraries, cookies, local storage, console output, DOM elements with tracking attributes

2. **Identify tools in the tech stack**
  - Based on the information gathered in step 1

3. **Generate Summary**
  - Follow the exact structure outlined in the section **Output Format** below.
  - Return the summary in Claude Code
  - Save the summary as a .md file to the project folder

4. **Distribution (optional)**
  - Prompt the user if the summary should be sent to a specific output channel. Options are: 
    - Word document
    - Slack message
    - Jira Ticket
    - Confluence page
    - None
  - Distribution instruction
    - Word document: Save a word document in the project folder. Use the font Helvetica and only use grayscale font color.
    - Slack message: Prompt for a Slack webhook URL and provide this link as instruction to retrieve a webhook URL: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/. Then send the summary to Slack via: curl -X POST -H 'Content-type: application/json' --data '{"text":"[SUMMARY]"}' [WEBHOOKURL]
    - Jira ticket: Create a draft for JIRA ticket using the Atlassian MCP server
    - Confluence page: Create a draft for Confluence page using the Atlassian MCP server


## Output Format

Use this exact structure. Do not add additional sections unless explicitly requested.

**Tech Stack Audit Summary for [SITE AUDITED]**

**Audit Date**: [YYYY-MM-DD]  
**URL Audited**: [Full URL]

**Overview**
- Create separate sections for each tool category, such as analytics and tracking, adtech, personalization and testing, tag management system, CDP, compliance and CMP, miscelleanous.
- In each section, list the tool name, followed by a sub-bullet with 'Traces, Evidence': List indications and proof that point to an implementation of the respective tool, such as network requests, libraries, cookies, local storage, console output etc.

**[Tool/Category] Deep Dive**
- When prompted to audit a single specific tool or a specific category, include details about it in this section
- List all details that can be understood from the implementation. Examples include depths of implementation, variety of events tracked, details about payloads, how the library is loaded etc.


## Notes for Effective Audits

- **Wait time**: Allow 5-10 seconds after page load to capture delayed/lazy-loaded tags
- **Multiple pages**: If tools aren't found on homepage, suggest checking other pages (content, registration, product, checkout, etc.)
- **SPA detection**: Note if the site is a Single Page Application (affects tool loading patterns)
- **Confidence levels**: If evidence is weak, note uncertainty

## Usage

/tech-stack-audit-command [url] 
/tech-stack-audit-command [url] [tool/category]
