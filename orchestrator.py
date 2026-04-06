"""
Agent Orchestration Service
Main orchestration loop that coordinates between the LLM and available tools.
"""

import json
from config import SYSTEM_PROMPT, TOOL_DEFINITIONS, MAX_ITERATIONS, LLM_MAX_TOKENS
from tools import TOOL_REGISTRY
from utils import build_prompt, parse_tool_call, format_tool_result, validate_response


class AgentOrchestrator:
    """
    Orchestrates multi-turn conversations between a user, an LLM, and a set of tools.
    The LLM decides when and which tools to call. Results are fed back into the
    conversation until the LLM produces a final response.
    """

    def __init__(self, llm_client):
        """
        Initialize the orchestrator.

        Args:
            llm_client: Client for making LLM API calls. Must have a
                       .generate(messages, max_tokens) method.
        """
        self.llm_client = llm_client
        self.conversation_history = []

    def run(self, user_query: str) -> str:
        """
        Process a user query through the agent loop.

        Args:
            user_query: The user's input message.

        Returns:
            The agent's final response string.
        """
        # Build the initial prompt with full history
        messages = build_prompt(
            SYSTEM_PROMPT,
            self.conversation_history,
            user_query
        )

        # Store the user message in history
        self.conversation_history.append({"role": "user", "content": user_query})

        # Agent loop
        for iteration in range(MAX_ITERATIONS):
            # Call the LLM
            llm_response = self.llm_client.generate(messages, max_tokens=LLM_MAX_TOKENS)

            # Check if LLM wants to call a tool
            tool_call = parse_tool_call(llm_response)

            if tool_call is None:
                # No tool call - this is the final response
                validation = validate_response(llm_response)

                # Store assistant response in history
                self.conversation_history.append(
                    {"role": "assistant", "content": llm_response}
                )

                return llm_response

            if "error" in tool_call:
                # Could not parse the tool call, ask LLM to retry
                messages.append({"role": "assistant", "content": llm_response})
                messages.append({
                    "role": "user",
                    "content": f"Error parsing your tool call: {tool_call['error']}. "
                               f"Please try again with the correct format."
                })
                continue

            # Execute the tool
            tool_name = tool_call["tool_name"]
            tool_params = tool_call["parameters"]

            if tool_name in TOOL_REGISTRY:
                tool_function = TOOL_REGISTRY[tool_name]
                tool_result = tool_function(**tool_params)
            else:
                tool_result = f"Error: Unknown tool '{tool_name}'. Available tools: {list(TOOL_REGISTRY.keys())}"

            # Format and add tool result to conversation
            formatted_result = format_tool_result(tool_name, tool_result)
            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "user", "content": formatted_result})

        # If we hit max iterations, return what we have
        return "I apologize, but I was unable to complete your request. Please try again."


def handle_request(user_query: str, llm_client, session_history: list = None) -> dict:
    """
    Entry point for handling an incoming user request.

    Args:
        user_query: The user's message.
        llm_client: LLM client instance.
        session_history: Optional prior conversation history.

    Returns:
        Dict with 'response' and 'status' keys.
    """
    orchestrator = AgentOrchestrator(llm_client)

    if session_history:
        orchestrator.conversation_history = session_history

    response = orchestrator.run(user_query)

    return {
        "response": response,
        "status": "success"
    }


# -------------------------------------------------------------------
# Example usage (not runnable without an LLM client):
#
#   client = SomeLLMClient(api_key="...")
#   result = handle_request("What claims does John Smith have?", client)
#   print(result["response"])
# -------------------------------------------------------------------
