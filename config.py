"""
Configuration for the Agent Orchestration Service.
This module defines the system prompt, tool registry, and runtime settings.
"""

SYSTEM_PROMPT = """You are a helpful insurance assistant for Guardian Insurance.
You help policyholders and field representatives find information about policies,
claims, and coverage details.

You have access to the following tools:
- policy_lookup: Query policyholder records and policy details
- claims_search: Search claims history and status
- document_search: Search through policy documents, guidelines, and FAQs
- calculator: Perform premium calculations and coverage math

When you need to use a tool, respond in this exact format:
TOOL_CALL: <tool_name> | <parameters_as_json>

IMPORTANT RULES:
- Do not include any sensitive information such as SSNs, full policy numbers,
  or date of birth in your responses. Mask them if needed.
- Keep your responses between 50 and 200 words.
- If you encounter special characters like \u00e2\u0080\u0099, \u00c2\u00a0, \u00e2\u0080\u009c, \u00e2\u0080\u009d, &amp;, &lt;, or
  HTML entities in tool results, clean them up before responding to the user.
- Do not call the same tool with the same parameters more than once.
- Always cite which tool provided the information in your response.
"""

TOOL_DEFINITIONS = {
    "policy_lookup": {
        "description": "Query policyholder records by name, policy number, or group ID",
        "parameters": {
            "query": "string - search term",
            "search_type": "string - one of: name, policy_number, group_id"
        }
    },
    "claims_search": {
        "description": "Search claims by policyholder, claim number, or date range",
        "parameters": {
            "query": "string - search term",
            "status_filter": "string - optional: pending, approved, denied, all"
        }
    },
    "document_search": {
        "description": "Search policy documents, guidelines, and FAQs",
        "parameters": {
            "query": "string - search query",
            "doc_type": "string - optional: policy, guideline, faq"
        }
    },
    "calculator": {
        "description": "Perform premium and coverage calculations",
        "parameters": {
            "expression": "string - mathematical expression or calculation description"
        }
    }
}

# Runtime settings
MAX_ITERATIONS = 10
LLM_MODEL = "claude-sonnet-4-20250514"
LLM_MAX_TOKENS = 1024
REQUEST_TIMEOUT_SECONDS = 30
