"""
Tool implementations for the Agent Orchestration Service.
Each tool simulates an external service call and returns results.
"""

import json
import time
import random


# --- Simulated data stores ---

POLICYHOLDER_DB = {
    "john_smith": {
        "name": "John A. Smith",
        "ssn": "123-45-6789",
        "dob": "1985-03-15",
        "policy_number": "POL-2024-00892",
        "group_id": "GRP-ACME-001",
        "plan_type": "PPO Gold",
        "status": "active",
        "premium_monthly": 487.50,
        "dependents": ["Jane Smith", "Tommy Smith"],
        "address": "142 Oak Street, Newark, NJ 07102"
    },
    "maria_garcia": {
        "name": "Mar\u00c3\u00ada Garc\u00c3\u00ada",
        "ssn": "987-65-4321",
        "dob": "1990-07-22",
        "policy_number": "POL-2024-01547",
        "group_id": "GRP-TECHCO-005",
        "plan_type": "HMO Standard",
        "status": "active",
        "premium_monthly": 325.00,
        "dependents": [],
        "address": "88 River Rd, Jersey City, NJ 07310"
    },
    "robert_o'brien": {
        "name": "Robert O\u00e2\u0080\u0099Brien",
        "ssn": "456-78-9012",
        "dob": "1978-11-03",
        "policy_number": "POL-2023-07831",
        "group_id": "GRP-ACME-001",
        "plan_type": "PPO Gold",
        "status": "suspended",
        "premium_monthly": 512.75,
        "dependents": ["Claire O'Brien"],
        "address": "5 Main St\u00c2\u00a0Apt 3B, Hoboken, NJ 07030"
    }
}

CLAIMS_DB = [
    {
        "claim_id": "CLM-2024-11234",
        "policyholder": "John A. Smith",
        "policy_number": "POL-2024-00892",
        "ssn": "123-45-6789",
        "type": "dental",
        "amount": 1250.00,
        "status": "approved",
        "date_filed": "2024-09-15",
        "description": "Root canal \u00e2\u0080\u0093 molar #19",
        "provider": "Dr. Sarah Chen, DDS"
    },
    {
        "claim_id": "CLM-2024-11567",
        "policyholder": "John A. Smith",
        "policy_number": "POL-2024-00892",
        "ssn": "123-45-6789",
        "type": "vision",
        "amount": 450.00,
        "status": "pending",
        "date_filed": "2024-10-02",
        "description": "Annual eye exam &amp; prescription lenses",
        "provider": "VisionWorks\u00e2\u0084\u00a2"
    },
    {
        "claim_id": "CLM-2024-12001",
        "policyholder": "Mar\u00c3\u00ada Garc\u00c3\u00ada",
        "policy_number": "POL-2024-01547",
        "ssn": "987-65-4321",
        "type": "medical",
        "amount": 3200.00,
        "status": "denied",
        "date_filed": "2024-10-10",
        "description": "MRI \u00e2\u0080\u0093 lumbar spine (pre-auth not obtained)",
        "provider": "Hudson Medical Center"
    }
]

DOCUMENTS_DB = [
    {
        "doc_id": "DOC-001",
        "title": "PPO Gold Plan Summary",
        "type": "policy",
        "content": "The PPO Gold plan provides comprehensive coverage with a $500 annual deductible. In-network copays are $25 for primary care and $50 for specialists. Out-of-network services are covered at 60% after deductible. Maximum out-of-pocket is $6,500 individual / $13,000 family."
    },
    {
        "doc_id": "DOC-002",
        "title": "Claims Filing Guidelines",
        "type": "guideline",
        "content": "All claims must be filed within 90 days of service. Pre-authorization is required for: MRI/CT scans, surgical procedures over $1,000, and out-of-network specialist visits. Dental claims require separate submission through the dental portal."
    },
    {
        "doc_id": "DOC-003",
        "title": "Coverage FAQ",
        "type": "faq",
        "content": "Q: What is covered under preventive care? A: Annual physicals, vaccinations, cancer screenings, and well-child visits are covered at 100% in-network with no copay. Q: How do I add a dependent? A: Dependents can be added during open enrollment or within 30 days of a qualifying life event."
    }
]


# --- Tool implementations ---

def policy_lookup(query: str, search_type: str = "name") -> str:
    """Look up policyholder information."""
    time.sleep(random.uniform(0.5, 1.5))  # Simulate API latency

    results = []
    query_lower = query.lower()

    for key, record in POLICYHOLDER_DB.items():
        if search_type == "name" and query_lower in record["name"].lower():
            results.append(record)
        elif search_type == "policy_number" and query_lower in record["policy_number"].lower():
            results.append(record)
        elif search_type == "group_id" and query_lower in record["group_id"].lower():
            results.append(record)

    if not results:
        return json.dumps({"status": "no_results", "message": f"No records found for '{query}'"})

    return json.dumps({"status": "success", "count": len(results), "records": results})


def claims_search(query: str, status_filter: str = "all") -> str:
    """Search claims history."""
    time.sleep(random.uniform(0.5, 1.5))  # Simulate API latency

    results = []
    query_lower = query.lower()

    for claim in CLAIMS_DB:
        match = (
            query_lower in claim["policyholder"].lower() or
            query_lower in claim["claim_id"].lower() or
            query_lower in claim["policy_number"].lower()
        )
        if match:
            if status_filter == "all" or claim["status"] == status_filter:
                results.append(claim)

    if not results:
        return json.dumps({"status": "no_results", "message": f"No claims found for '{query}'"})

    return json.dumps({"status": "success", "count": len(results), "claims": results})


def document_search(query: str, doc_type: str = None) -> str:
    """Search policy documents."""
    time.sleep(random.uniform(0.3, 0.8))  # Simulate API latency

    results = []
    query_lower = query.lower()

    for doc in DOCUMENTS_DB:
        if doc_type and doc["type"] != doc_type:
            continue
        if query_lower in doc["title"].lower() or query_lower in doc["content"].lower():
            results.append(doc)

    if not results:
        return json.dumps({"status": "no_results", "message": f"No documents found for '{query}'"})

    return json.dumps({"status": "success", "count": len(results), "documents": results})


def calculator(expression: str) -> str:
    """Perform calculations."""
    try:
        result = eval(expression)
        return json.dumps({"status": "success", "expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


# Tool registry
TOOL_REGISTRY = {
    "policy_lookup": policy_lookup,
    "claims_search": claims_search,
    "document_search": document_search,
    "calculator": calculator
}
