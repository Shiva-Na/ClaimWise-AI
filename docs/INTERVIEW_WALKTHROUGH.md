# Interview walkthrough

## 90-second project explanation
ClaimWise AI is a multi-agent insurance claim assessment and investigation workspace. An operations user creates a claim and uploads supporting documents and policy wording. The backend extracts text and structured fields, retrieves relevant policy passages, validates required documents and basic identity details, raises transparent anomaly indicators, calculates a limited illustrative amount, and produces a report for a human reviewer. LangGraph coordinates the stages through a shared state. PostgreSQL persists claim records, document metadata, reviews and audit events. An optional OpenAI stage explains findings using only supplied evidence; it does not approve or reject a claim.

## Be precise about current capabilities
- Document extraction: selectable text in PDF/TXT/MD; OCR is not implemented.
- Retrieval: TF-IDF ranking over policy chunks; not embeddings/vector search.
- Agent coordination: LangGraph StateGraph.
- LLM: optional OpenAI summary/reviewer questions; deterministic checks remain primary.
- Fraud: configured anomaly flags, not a trained fraud model.
- Calculation: sum insured cap and deductible only, not full policy adjudication.
- Final decision: human officer.

## Questions to prepare
1. Why did you use LangGraph instead of one large prompt?
2. What is the difference between an LLM and an AI agent?
3. How does your policy retrieval stage work?
4. What is TF-IDF and why did you choose it for this local prototype?
5. How do you avoid treating model output as a binding claim decision?
6. What data is stored in PostgreSQL?
7. How do you handle duplicate or mismatched document information?
8. What happens if the OpenAI API is unavailable?
9. Why are your risk indicators not proof of fraud?
10. What would you add before production deployment?
