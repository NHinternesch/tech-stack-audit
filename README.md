# Tech Stack Audit Prompt

<br><br>
<img width="872" height="228" alt="tech-stack-audit visualization" src="https://github.com/user-attachments/assets/1a69d5ed-0a0c-428a-b673-0f1b191a132f" />
<br><br>

`tech-stack-audit` is an LLM skill. It is designed to be used in combination with browser automation MCPs / tools, such as Chrome Dev Tools or Playwright.
It leverages browser technologies to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, it creates a well-formatted technical summary, which is returned to various output channels. 

## Benefits

The prompt **reduces time to deliverable** and **increases completeness** when executing front end tech stack audits in the web browser. 

## Instructions for Claude Code usage
1. Optional: Refine prompt for specific use case
2.  Execute skill. For direct execution, use /tech-stack-audit command. Otherwise, invoke with trigger phrases like "audit mydomain.com for analytics tools" or "review the tech stack on mydomain.com".

The audit summary will be returned to the working directory as a .md file. It can also be exported to other output channels, such as file export, Slack, JIRA, Confluence.
