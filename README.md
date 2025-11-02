# Tech Stack Audit Prompt

<br><br>
<img width="872" height="228" alt="tech-stack-audit visualization" src="https://github.com/user-attachments/assets/1a69d5ed-0a0c-428a-b673-0f1b191a132f" />
<br><br>

`tech-stack-audit` is a reusable LLM prompt. It is designed to be used as a Claude Code slash command.
It leverages browser technologies through the Chrome Dev Tools MCP server to execute tech stack audits and thoroughly inspect, review, and interpret website and martech tools. Then, it creates a well-formatted summary, which is returned to various output channels.

## Benefits

The prompt **reduces time to deliverable** and **increases completeness** when executing front end tech stack audits in the web browser. 

## Instructions for Claude Code usage
1. Clone the prompt to your directory for slash commands, e.g. `~/.claude/commands/`
2. Optional: Refine prompt for specific use case
3. Execute in Claude Code via `/tech-stack-audit url optional-tool-or-category` <br>

The audit summary will be returned to the working directory as a .md file. It can also be exported to other output channels, such as file export, Slack, JIRA, Confluence.
