# Agent Orchestration Service

A lightweight agent orchestration framework for an insurance assistant. The system takes user queries, routes them to appropriate tools (policy lookup, claims search, document search, calculator), and generates responses using an LLM.

## Architecture

```
User Query
    |
    v
orchestrator.py   -->  Builds prompt, manages agent loop
    |
    v
LLM (Claude)      -->  Decides which tools to call
    |
    v
tools.py           -->  Executes tool calls, returns results
    |
    v
utils.py           -->  Prompt building, parsing, validation
    |
    v
config.py          -->  System prompt, tool definitions, settings
```

## Files

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main agent loop. Coordinates LLM calls and tool execution. |
| `tools.py` | Tool implementations with simulated data stores. |
| `utils.py` | Utility functions for prompt building, parsing, and validation. |
| `config.py` | System prompt, tool definitions, and runtime configuration. |
| `sample_data/scenarios.json` | Example interactions showing how the agent handles different queries. |

## How It Works

1. User sends a query (e.g., "What claims does John Smith have?")
2. The orchestrator builds a prompt with the system instructions, conversation history, and user query
3. The LLM processes the prompt and either responds directly or requests a tool call
4. If a tool is requested, the orchestrator executes it and feeds the result back to the LLM
5. This loop continues until the LLM produces a final response or the max iteration limit is reached

## Known Issues

The following issues have been reported in production. Review the codebase, identify the root causes, and propose or implement fixes.

1. **Special characters in responses**: Users occasionally see garbled characters like `Ã©`, `â€™`, `Â`, and HTML entities (`&amp;`) in the agent's responses. These appear to originate from tool results.

2. **Sensitive data exposure**: Despite instructions in the system prompt, the agent sometimes includes full SSNs, policy numbers, and dates of birth in responses to users.

3. **Agent looping**: In some conversations, the agent calls the same tool with identical parameters multiple times before eventually responding. This wastes API tokens and increases latency.

4. **Inconsistent tool matching**: The LLM occasionally uses tool name variations (e.g., `doc_search` instead of `document_search`, `lookup_policy` instead of `policy_lookup`). When this happens, the agent returns an error instead of routing to the intended tool.

5. **Unhandled tool failures**: When a tool call throws an exception (e.g., due to malformed input), the agent's behavior is unpredictable. No structured error handling is in place.

6. **Slow multi-tool queries**: Queries that require information from multiple tools (e.g., "What are John Smith's claims and what does his plan cover?") are noticeably slower than single-tool queries.

## Your Task

Review the code and the sample scenarios in `sample_data/scenarios.json`. For each issue you address:

- Identify where in the codebase the problem originates
- Explain why the current approach is insufficient
- Implement or describe your fix
- Explain how you would verify the fix works

You are free to use any AI coding tools available in your environment.

**You do not need to address all issues.** Pick the ones you consider most critical and explain your prioritization.
