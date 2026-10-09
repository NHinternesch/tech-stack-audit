# Tech Stack Audit

`tech-stack-audit` is an LLM skill for technical front-end audits. It controls a browser via Chrome DevTools MCP server to inspect a website's martech stack across several page types. The result is a single self-contained HTML report: Architecture diagram, top-line findings, tools by category, tool or category deep dive, and sources.

## Usage

Run `/tech-stack-audit <url> [tool or category]`, or prompt to audit a site's tech stack. The report is written to the working directory.
