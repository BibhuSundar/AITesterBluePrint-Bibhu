# Findings

## Discoveries & Requirements
- **LLM Engine & Integration**: The system must be unified and support both local execution (Ollama, LM Studio) and cloud APIs (OpenAI, Grok, Claude).
- **Inputs**: Users will copy-paste Jira requirements or provide input interactively through a chat interface.
- **Output Format & Target Application**: The system must generate functional and non-functional test cases for API and Web Applications. The final output must be formatted stringently in **Jira format** so users can easily copy/paste into Jira or import seamlessly.
- **Tech Stack**: Backend will be built in Node.js with TypeScript. Frontend will be built in React.js.

## Constraints & Open Questions
- Need to determine exactly what "Jira format" means (e.g. Jira Markdown tables vs CSV import format vs JSON for REST API), but initially we will target Jira Markdown.
