
import json
import re

from app.agents.state import ClaimState
from app.services.documents import extract_structured_fields
from app.services.retrieval import retrieve_relevant_chunks
from app.core.config import settings


REQUIRED = [
    "claim_form",
    "hospital_bill",
    "discharge_summary",
    "medical_report"
]


# 1. Document Intelligence Agent
def document_node(s: ClaimState):
    return {
        "extracted_documents": [
            {
                "filename": d["filename"],
                "document_type": d.get("document_type", "supporting"),
                "fields": extract_structured_fields(d.get("text", "")),
                "text_excerpt": d.get("text", "")[:700]
            }
            for d in s.get("documents", [])
        ]
    }


# 2. Policy Retrieval Agent
def retrieval_node(s: ClaimState):
    c = s["claim"]

    q = (
        f"{c.get('insurance_type')} insurance claim coverage "
        f"exclusions waiting period deductible hospitalization "
        f"{c.get('incident_description', '')}"
    )

    return {
        "retrieved_clauses": retrieve_relevant_chunks(
            q,
            s.get("policy_text", "")
        )
    }


# 3. Policy Analysis Agent
def policy_node(s: ClaimState):
    text = s.get("policy_text", "")
    low = text.lower()

    # Extract numeric values from policy wording
    def num(label):
        patterns = [
            rf'{re.escape(label)}\s*[:\-]\s*(?:INR|RS\.?|₹)?\s*([\d,]+(?:\.\d+)?)',
            rf'{re.escape(label)}\s+(?:INR|RS\.?|₹)\s*([\d,]+(?:\.\d+)?)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return float(
                    match.group(1).replace(",", "")
                )

        return None

    limit = num("sum insured")
    deductible = num("deductible") or 0
    room_rent_limit = num("room rent limit")

    flags = []

    if limit is None:
        flags.append(
            "Numeric sum insured not identified in policy text."
        )

    elif float(s["claim"]["claimed_amount"]) > limit:
        flags.append(
            "Claimed amount exceeds the stated sum insured."
        )

    if not s.get("retrieved_clauses"):
        flags.append(
            "No relevant policy clauses retrieved; "
            "manual policy review required."
        )

    return {
        "policy_analysis": {
            "policy_status_text_found": "active" in low,
            "sum_insured": limit,
            "deductible": deductible,
            "room_rent_limit": room_rent_limit,
            "retrieved_clauses": s.get("retrieved_clauses", []),
            "flags": flags,
            "interpretation_note": (
                "Preliminary keyword and numeric extraction; "
                "not legal policy interpretation."
            )
        }
    }


# 4. Claim Validation Agent
def validation_node(s: ClaimState):
    docs = s.get("extracted_documents", [])

    present = {
        d["document_type"]
        for d in docs
    }

    missing = [
        x for x in REQUIRED
        if x not in present
    ]

    mismatch = []

    for d in docs:
        for field, key in [
            ("policy_number", "policy_number"),
            ("patient_name", "customer_name")
        ]:
            value = d["fields"].get(field)

            if (
                value
                and s["claim"].get(key)
                and value.casefold()
                != str(s["claim"][key]).casefold()
            ):
                mismatch.append(
                    f"{field.replace('_', ' ').title()} "
                    f"mismatch in {d['filename']}."
                )

    dates = []

    if (
        s["claim"].get("admission_date")
        and s["claim"].get("admission_date")
        == s["claim"].get("discharge_date")
    ):
        dates.append(
            "Admission and discharge dates are identical; "
            "verify the stay details."
        )

    return {
        "validation": {
            "required_documents": REQUIRED,
            "received_document_types": sorted(present),
            "missing_documents": missing,
            "mismatch_flags": mismatch,
            "date_flags": dates,
            "complete": not (missing or mismatch or dates)
        }
    }


# 5. Risk Investigation Agent
def risk_node(s: ClaimState):
    c = s["claim"]
    docs = s.get("extracted_documents", [])

    flags = []
    score = 0

    if not docs:
        flags.append("No readable documents supplied.")
        score += 15

    amounts = [
        amount
        for d in docs
        for amount in d["fields"].get("amounts_found", [])
    ]

    if amounts and not any(
        abs(amount - c["claimed_amount"])
        <= max(5, c["claimed_amount"] * 0.02)
        for amount in amounts
    ):
        flags.append(
            "Claimed amount differs from amounts found "
            "in supporting documents."
        )
        score += 20

    if any(
        "duplicate" in d.get("text_excerpt", "").lower()
        for d in docs
    ):
        flags.append(
            "Duplicate wording appears in a document; "
            "verify original invoice."
        )
        score += 15

    if s.get("validation", {}).get("mismatch_flags"):
        flags += s["validation"]["mismatch_flags"]
        score += 20

    if s.get("validation", {}).get("date_flags"):
        flags += s["validation"]["date_flags"]
        score += 10

    score = min(score, 100)

    return {
        "risk_analysis": {
            "score": score,
            "level": (
                "High" if score >= 50
                else "Medium" if score >= 20
                else "Low"
            ),
            "flags": list(dict.fromkeys(flags)),
            "disclaimer": (
                "Risk indicators are not proof of fraud "
                "and must be investigated."
            )
        }
    }


# 6. Claim Calculation Agent
def calculation_node(s: ClaimState):
    amount = float(s["claim"]["claimed_amount"])

    policy = s.get("policy_analysis", {})

    limit = policy.get("sum_insured")

    capped = (
        min(amount, limit)
        if limit is not None
        else amount
    )

    deductible = float(policy.get("deductible") or 0)

    return {
        "calculation": {
            "claimed_amount": round(amount, 2),
            "sum_insured": limit,
            "deductible": round(deductible, 2),
            "illustrative_amount_after_basic_limits": round(
                max(0, capped - deductible), 2
            ),
            "note": (
                "Illustrative arithmetic only; excludes co-pay, "
                "sublimits, exclusions, waiting periods "
                "and endorsements."
            )
        }
    }


# 7. Optional LLM Reasoning Agent
def llm_node(s: ClaimState):
    if not settings.openai_api_key:
        return {
            "llm_assessment": {
                "enabled": False,
                "summary": (
                    "LLM not configured. Deterministic "
                    "agent findings are available."
                )
            }
        }

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.openai_api_key
        )

        payload = {
            k: s.get(k)
            for k in [
                "claim",
                "retrieved_clauses",
                "policy_analysis",
                "validation",
                "risk_analysis",
                "calculation"
            ]
        }

        system = (
            "You are an insurance operations analyst assisting "
            "a human reviewer. Use only supplied evidence. "
            "Never invent policy facts. Never approve or reject "
            "a claim. Explain uncertainty. Return JSON with "
            "summary, evidence_based_observations (array), "
            "questions_for_reviewer (array), limitations."
        )

        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        payload,
                        ensure_ascii=False
                    )
                }
            ]
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return {
            "llm_assessment": {
                "enabled": True,
                **result
            }
        }

    except Exception as e:
        return {
            "llm_assessment": {
                "enabled": False,
                "summary": (
                    "LLM unavailable; deterministic "
                    "findings retained."
                ),
                "explanation": str(e)[:250]
            }
        }


# 8. Final Assessment Agent
def assessment_node(s: ClaimState):
    validation = s["validation"]
    risk = s["risk_analysis"]
    policy = s["policy_analysis"]

    reasons = []

    if validation["missing_documents"]:
        reasons.append(
            "Missing documents: "
            + ", ".join(validation["missing_documents"])
        )

    reasons += validation["mismatch_flags"]
    reasons += validation["date_flags"]
    reasons += risk["flags"]
    reasons += policy["flags"]

    reasons = list(dict.fromkeys(reasons))

    recommendation = (
        "Further investigation required"
        if reasons
        else "Proceed to human officer review"
    )

    status = (
        "Review Required"
        if reasons
        else "Ready for Review"
    )

    llm = s.get("llm_assessment", {})

    return {
        "final_assessment": {
            "recommendation": recommendation,
            "status": status,
            "reasons": reasons,
            "agent_summary": llm.get("summary", ""),
            "evidence_based_observations": llm.get(
                "evidence_based_observations", []
            ),
            "questions_for_reviewer": llm.get(
                "questions_for_reviewer", []
            ),
            "limitations": [
                "Decision-support prototype, not an adjudication system.",
                "Risk indicators are not proof of fraud.",
                "Human verification of policy wording and all calculations is mandatory."
            ]
        }
    }


# Build LangGraph Workflow
def build_graph():
    from langgraph.graph import StateGraph, START, END

    graph = StateGraph(ClaimState)

    nodes = [
        ("document_intelligence", document_node),
        ("policy_retrieval", retrieval_node),
        ("policy_review_node", policy_node),
        ("claim_validation", validation_node),
        ("risk_investigation", risk_node),
        ("claim_calculation", calculation_node),
        ("llm_reasoning", llm_node),
        ("assessment_summary_node", assessment_node)
    ]

    for name, function in nodes:
        graph.add_node(name, function)

    graph.add_edge(START, nodes[0][0])

    for (previous, _), (next_node, _) in zip(
        nodes, nodes[1:]
    ):
        graph.add_edge(previous, next_node)

    graph.add_edge(nodes[-1][0], END)

    return graph.compile()


workflow = build_graph()
