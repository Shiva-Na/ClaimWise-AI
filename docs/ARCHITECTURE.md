# ClaimWise AI — Architecture Notes

## Request lifecycle
1. React submits claim metadata to FastAPI.
2. FastAPI validates fields with Pydantic and persists the claim in PostgreSQL.
3. Supporting files are size/type checked, extracted, classified and stored under the claim reference.
4. The assessment endpoint loads persisted document text and policy wording.
5. LangGraph executes the claim workflow as a shared typed state.
6. Nodes return structured outputs; the API persists findings, risk indicators, recommendation and audit event.
7. React renders agent outputs and allows a reviewer to record a human decision.

## Data model
- `claims`: core case record and latest assessment snapshot.
- `claim_documents`: original file metadata, storage path and extracted text.
- `human_reviews`: append-only officer decision history.
- `audit_events`: operational event trail.

## Trust boundaries
- Deterministic rules calculate configured indicators; an LLM is only an optional explanatory stage.
- Policy passages are retrieved from supplied wording and surfaced to the reviewer.
- A model response is not treated as a coverage decision.
- Human review is a separate, persisted action.

## Why LangGraph
The state graph gives explicit nodes, shared state and a visible sequence. This makes the workflow easier to inspect and test than one large prompt that claims to do everything.
