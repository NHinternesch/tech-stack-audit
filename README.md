# Tech Stack Audit

`tech-stack-audit` is an LLM skill for technical front-end audits, orchestrated from Claude Code, Claude Cowork etc. 
It leverages browser technologies through the Chrome Dev Tools MCP server to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, it creates a well-formatted summary, which is returned to various output channels.

## Benefits

The skill **reduces time to deliverable** and **increases completeness** when executing front end tech stack audits in the web browser. 

## Instructions
1. Optional: Refine prompt for specific use case
2. Execute via direct command or trigger phrases. Provide input like URL to audit and optional deep dive tool/category.

The audit summary will be returned to the working directory as a .docx file. It can also be exported to other output channels, such as Slack, JIRA, Confluence.
