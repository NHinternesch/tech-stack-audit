# Tech Stack Audit

`tech-stack-audit` is an LLM skill for technical front-end audits. It leverages browser technologies through the Chrome Dev Tools MCP server to execute tech stack audits and inspect, review, and interpret website and martech tools. It creates a well-formatted summary and tech stack diagram, which are returned to various output channels.

## Benefits

The skill **reduces time to deliverable** and **increases completeness** when executing front end tech stack audits in the web browser. 

## Instructions
1. Optional: Refine SKILL.md for specific use case
2. Execute via direct command or trigger phrases. Provide input like the URL to audit and optional deep dive tool/category.

The audit summary will be returned to the working directory as a .docx file. It can also be exported to other output channels, such as Slack, JIRA, Confluence.