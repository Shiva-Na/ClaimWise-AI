# ClaimWise AI
## Multi-Agent Insurance Claims Assessment & Investigation Workspace

ClaimWise AI is a full-stack portfolio application demonstrating how an insurance operations team can use document intelligence, policy retrieval, validation rules and AI-assisted explanations to prepare an initial claim investigation for a human reviewer.

**Stack:** React + Vite + custom CSS · FastAPI · PostgreSQL · SQLAlchemy · LangGraph · OpenAI API (optional) · TF-IDF policy retrieval.

> **Safety and scope:** This is a portfolio demonstration, not an insurance adjudication platform. It does not approve, reject, price or settle real claims. Its sample policy and rules are simplified and fictional. A risk indicator is not proof of fraud. Human review is mandatory. Do not upload real customer, health or financial information.

## What is implemented

### Application
- Responsive, custom-designed operations dashboard (React).
- Claim intake, searchable claims register and claim detail workspace.
- Document upload and persistent claim document records.
- Claim assessment, findings panels and report export.
- Human officer review history.
- Activity/audit log.
- PostgreSQL persistence for claims, documents, reviews and audit events.

### Agent workflow
The backend uses a real LangGraph `StateGraph` to orchestrate these stages:
1. **Document intelligence:** extracts PDF/TXT/MD text and structured fields.
2. **Policy retrieval:** chunks policy wording and retrieves relevant passages using TF-IDF similarity.
3. **Policy analysis:** extracts selected numeric terms and relevant clauses; reports uncertainty.
4. **Claim validation:** checks document categories and basic policy/customer mismatches.
5. **Risk investigation:** raises explainable anomaly indicators from configured checks.
6. **Claim calculation:** demonstrates a basic sum-insured cap and deductible calculation.
7. **LLM analyst:** optionally calls OpenAI to summarize only supplied evidence and list reviewer questions.
8. **Final assessment:** consolidates findings into a human-review recommendation.

The deterministic checks continue to work without an OpenAI key. Add your own key to enable the LLM explanation stage. The LLM is not allowed to make the final claim decision.

## Project structure

```text
ClaimWise-AI-Professional/
├── backend/
│   ├── app/
│   │   ├── agents/       # LangGraph state, nodes and workflow
│   │   ├── api/          # FastAPI endpoints
│   │   ├── core/         # Application settings
│   │   ├── db/           # PostgreSQL engine and sessions
│   │   ├── models/       # SQLAlchemy entities
│   │   ├── schemas/      # Request validation
│   │   ├── services/     # Document extraction, RAG retrieval, audit
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── package.json
│   └── .env.example
├── sample_data/
│   ├── policies/
│   └── claims/
├── docs/
└── docker-compose.yml
```

## Prerequisites
- Python 3.11 or 3.12
- Node.js 20 LTS or later
- PostgreSQL 14+ (or Docker Desktop)
- VS Code

## Run locally with your own PostgreSQL

### 1. Create the database

In pgAdmin Query Tool or `psql`:

```sql
CREATE DATABASE claimwise;
```

Use your own PostgreSQL username and password in the backend environment file.

### 2. Configure the backend

Open a terminal at the project root:

**Windows PowerShell**
```powershell
cd backend
Copy-Item .env.example .env
```

**macOS/Linux**
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/claimwise
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=storage/uploads
MAX_UPLOAD_MB=20
```

For LLM-based analyst explanations, add your own OpenAI API key. Without it, all deterministic checks and the LangGraph workflow still run; the UI will indicate that LLM explanation is not enabled. API usage may incur charges.

### 3. Install and run backend

From the `backend` directory:

**Windows**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**macOS/Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend creates the required tables on startup.
- API: http://localhost:8000
- Swagger documentation: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

### 4. Install and run frontend

Open a second VS Code terminal:

```bash
cd frontend
```

Copy the frontend environment file:

**Windows**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux**
```bash
cp .env.example .env
```

Install and start:

```bash
npm install
npm run dev
```

Open http://localhost:5173.

### 5. Run the sample scenario

1. In the dashboard select **New claim**.
2. Enter sample customer `Aditi Sharma`, policy `NSH-2026-00421`, type `Health`, provider `Northstar City Hospital`, amount `285000`.
3. Open the new claim.
4. Upload all four text files from `sample_data/claims/`.
5. Upload `sample_data/policies/sample_health_policy.txt` in the optional policy wording field.
6. Run the assessment.
7. Inspect the document categories, retrieved clauses, validation findings, risk indicators and report.
8. Record a human officer review.
9. Open the claims register and activity log to see persistent data.

The sample files are entirely synthetic. They are provided to exercise the workflow, not to represent a real policy or claim.

## API overview

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Backend and database health |
| GET | `/api/metrics` | Dashboard counts and claim value |
| GET | `/api/claims` | Search and filter claims |
| POST | `/api/claims` | Create claim |
| GET | `/api/claims/{id}` | Claim detail and history |
| POST | `/api/claims/{id}/documents` | Upload and extract documents |
| POST | `/api/claims/{id}/assess` | Execute LangGraph workflow |
| POST | `/api/claims/{id}/review` | Save human officer review |
| GET | `/api/claims/{id}/report` | Retrieve assessment report |
| GET | `/api/activity` | Audit activity feed |

## Tests

From `backend/` with the virtual environment activated:

```bash
pytest -q
```

## Important implementation boundaries

This is a complete runnable portfolio application, but it is not production-certified software:
- Text-based PDFs are supported. Scanned/image-only PDFs need OCR; this build reports when no selectable text is present.
- Document classification is keyword-assisted and should be strengthened with labelled examples and human confirmation.
- Policy retrieval is TF-IDF-based local retrieval, not a vector database or legal policy parser.
- Numeric policy parsing supports only simple labelled amounts.
- Risk checks are transparent rules, not a trained fraud detection model.
- The basic calculation does not model all policy-specific benefits, exclusions, co-pay, room limits, waiting periods or endorsements.
- Authentication, role-based authorization, encryption/key management, malware scanning, tenant isolation and production deployment controls are not included. Do not expose this development app publicly or process real policyholder data.

## GitHub publishing checklist
1. Create a public repository named `ClaimWise-AI`.
2. Keep `.env` files, API keys, uploads and private documents out of Git.
3. Include only synthetic sample data.
4. Add screenshots from your own running application.
5. Run tests and confirm the app starts before publishing.
6. Be prepared to explain each agent, retrieval method, database model, limitation and human-review safeguard.

```bash
git init
git add .
git commit -m "Build ClaimWise AI multi-agent insurance claims workspace"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ClaimWise-AI.git
git push -u origin main
```

## Suggested next improvements
- OCR for scanned claim PDFs.
- Confirmable document classification.
- More robust policy clause extraction and citations.
- Dedicated insurance product rules validated by domain experts.
- Authentication, role-based access and audit integrity.
- Background processing for large documents.
- CI pipeline and expanded integration tests.
