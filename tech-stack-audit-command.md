# Tech Stack Audit Command


## Primary Objective

Leverage browser technologies through the Chrome Dev Tools MCP server to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, create a well-formatted summary, which is returned to various output channels. The recipient of these summaries is a Pre Sales Solutions Engineer, who needs to get a thorough understanding of a tech stack and the components involved, in order to pitch the solution they are looking to position with a prospect. 


## Inputs
- Required: url
- Optional: specific tool or specific category for deep dive focus


## Workflow

When tasked to audit a website, the workflow involves:

1. **Audit the site**
  - Navigate to [url]
  - Accept all cookie and compliance banners
  - Reload the page
  - Monitor all browser activity, incl. network requests, libraries, cookies, local storage, console output

2. **Identify tools in the tech stack**
  - Based on the information gathered in step 1

3. **Generate a summary**
  - Strictly follow the structure outlined in the section Output below. Do not include lengthy summaries or recommendations.
  - Return the summary in Claude Code
  - Save the summary as a .md file to the project folder

4. **Distribute the summary (optional)**
  - Prompt the user if the summary should be sent to a specific output channel. Options are: 
    - Word document
    - Slack message
    - Jira Ticket
    - Confluence page
  - If Word document: Save a word document in the project folder. Use the font Helvetica and only use grayscale font color.
  - If Slack message: Prompt for a Slack webhook URL and provide instructions via this link: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/. Then send the summary to Slack via: curl -X POST -H 'Content-type: application/json' --data '{"text":"[SUMMARY]"}' [WEBHOOKURL]
  - If Jira ticket: Create a draft for JIRA ticket using the Atlassian MCP server
  - If Confluence page: Create a draft for Confluence page using the Atlassian MCP server


## Output

When generating the summary, strictly follow this structure:

**Tech Stack Audit Summary for [SITE AUDITED]**

**Overview**
- Table with 3 columns:
  - 1. Tool category: Group the tools into the categories, such as analytics and tracking, adtech, personalization and testing, tag management system, CDP, compliance and CMP, miscelleanous
  - 2. Tool name: State the tool name
  - 3. Traces, evidence: List indications and proof that point to an implementation of the respective tool, such as network requests, libraries, cookies, local storage, console output etc.

**[TOOL/CATEGORY] Deep Dive**
- When prompted to audit a single specific tool or a specific category, include details about it in this section
- List all details that can be understood from the implementation. Examples include depths of implementation, variety of events tracked, details about payloads, how the library is loaded etc.

## Usage
/tech-stack-audit-command [url] [tool/category]
