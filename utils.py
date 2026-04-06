"""
Utility functions for the Agent Orchestration Service.
"""

import json
import re


def build_prompt(system_prompt: str, conversation_history: list, user_query: str) -> list:
    """
    Build the full message payload for the LLM.
    Combines system prompt, conversation history, and the new user query.
    """
    messages = [{"role": "system", "content": system_prompt}]

    # Add entire conversation history
    for turn in conversation_history:
        messages.append(turn)

    # Add the new user message directly
    messages.append({"role": "user", "content": user_query})

    return messages


def parse_tool_call(llm_response: str) -> dict:
    """
    Parse the LLM's response to extract tool call information.
    Expected format: TOOL_CALL: <tool_name> | <parameters_as_json>
    Returns None if no tool call is found.
    """
    if "TOOL_CALL:" not in llm_response:
        return None

    try:
        tool_line = None
        for line in llm_response.split("\n"):
            if "TOOL_CALL:" in line:
                tool_line = line.strip()
                break

        if not tool_line:
            return None

        # Extract everything after "TOOL_CALL:"
        call_content = tool_line.split("TOOL_CALL:")[1].strip()

        # Split on pipe to get tool name and params
        parts = call_content.split("|", 1)
        tool_name = parts[0].strip()
        params = json.loads(parts[1].strip()) if len(parts) > 1 else {}

        return {"tool_name": tool_name, "parameters": params}

    except (json.JSONDecodeError, IndexError) as e:
        return {"error": f"Failed to parse tool call: {str(e)}"}


def format_tool_result(tool_name: str, result: str) -> str:
    """
    Format a tool's result for inclusion in the conversation.
    """
    return f"[Tool: {tool_name}] Result:\n{result}"


def validate_response(response: str) -> dict:
    """
    Validate the final response before sending to user.
    Returns validation result with any issues found.
    """
    issues = []

    if not response or len(response.strip()) == 0:
        issues.append("empty_response")

    if len(response) > 5000:
        issues.append("response_too_long")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "response": response
    }


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars per token approximation)."""
    return len(text) // 4
