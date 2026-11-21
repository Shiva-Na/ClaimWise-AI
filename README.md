# 🛡️ ClaimWise AI
### Intelligent Insurance Claims Assessment & Investigation Platform

ClaimWise AI is a full-stack, AI-assisted insurance claims assessment platform designed to help insurance teams organize claim information, analyze supporting documents, retrieve relevant policy clauses, identify potential inconsistencies, and support human review.

The platform combines a **React frontend, FastAPI backend, PostgreSQL database, and LangGraph-based assessment workflow** to provide a structured and explainable claim investigation process.

> **Project Status:** Working Portfolio MVP  
> This project is intended for demonstration and educational purposes. Its AI-generated findings and risk scores are decision-support signals, not final insurance decisions.

---

## 🚀 Key Features

### 1. Claim Management
- Create and manage insurance claims.
- Maintain claimant, policy, hospital, and claim information.
- Track claim status and assessment results.
- View individual claim details.

### 2. Intelligent Document Processing
- Upload supporting claim documents.
- Extract text from supported PDF, TXT, and Markdown files.
- Identify document categories.
- Organize extracted information for further assessment.

### 3. AI-Assisted Claim Assessment
- Multi-step assessment workflow powered by LangGraph.
- Document analysis and information extraction.
- Relevant policy clause retrieval.
- Policy-related checks and claim validation.
- Potential inconsistency and risk flag identification.
- Structured assessment findings and recommendations.

### 4. Policy Analysis
- Retrieve relevant policy text using TF-IDF-based lexical retrieval.
- Extract supported policy values such as sum insured and deductible.
- Perform basic policy-related checks.
- Present retrieved clauses for assessment.

### 5. Risk Investigation
- Rule-based checks for potential inconsistencies.
- Heuristic risk scoring.
- Identification of missing information and suspicious patterns.
- Risk classification to support further investigation.

### 6. Human-in-the-Loop Review
- Allow an insurance officer to review AI findings.
- Record review decisions and notes.
- Maintain a human review history.
- Keep final decision-making with the human reviewer.

### 7. Audit Trail & Reporting
- Maintain claim activity history.
- Record document uploads and assessment events.
- Store officer review actions.
- Export assessment findings as JSON.

---

## 🏗️ System Architecture

```text
                 USER
                   |
                   v
          REACT FRONTEND
             (Vite)
                   |
              REST API
                   |
                   v
           FASTAPI BACKEND
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   CLAIM       DOCUMENT     ASSESSMENT
 MANAGEMENT   PROCESSING     SERVICE
                               |
                               v
                       LANGGRAPH WORKFLOW
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
          DOCUMENT          POLICY          CLAIM
          ANALYSIS         RETRIEVAL       VALIDATION
              |                |                |
              +----------------+----------------+
                               |
                               v
                       RISK INVESTIGATION
                               |
                               v
                       CLAIM CALCULATION
                               |
                               v
                       FINAL ASSESSMENT
                               |
                               v
                       HUMAN REVIEW
                               |
                               v
                       AUDIT & REPORTING
                               |
                               v
                         POSTGRESQL
```

---

## 🧠 AI Assessment Workflow

The assessment process is organized into multiple LangGraph nodes.

| Stage | Responsibility |
|---|---|
| Document Analysis | Extract and analyze uploaded document information |
| Policy Retrieval | Retrieve relevant policy text |
| Policy Analysis | Extract policy details and perform basic checks |
| Claim Validation | Identify missing information and inconsistencies |
| Risk Investigation | Calculate heuristic risk indicators |
| Calculation | Perform illustrative claim calculations |
| LLM Explanation | Optionally generate an AI explanation |
| Final Assessment | Prepare structured findings and recommendations |

The workflow produces a structured assessment that can be reviewed by an insurance officer.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| AI Workflow | LangGraph |
| Policy Retrieval | TF-IDF |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| API Documentation | FastAPI / Swagger UI |
| AI Integration | Optional OpenAI API |
| Version Control | Git and GitHub |
| Containerization | Docker Compose |

---

## 📁 Project Structure

```text
ClaimWise-AI/
│
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph workflow nodes
│   │   ├── api/             # REST API routes
│   │   ├── core/            # Application configuration
│   │   ├── db/              # Database connection
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Request and response schemas
│   │   └── services/        # Business logic and services
│   │
│   ├── tests/               # Backend tests
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # API integration
│   │   └── pages/           # Application pages
│   ├── .env.example
│   └── package.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── INTERVIEW_WALKTHROUGH.md
│
├── sample_data/
│   ├── claims/
│   └── policies/
│
├── docker-compose.yml
├── setup_windows.bat
├── start_windows.bat
├── README.md
└── LICENSE
```

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.12
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Shiva-Na/ClaimWise-AI.git
cd ClaimWise-AI
```

### 2. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE claimwise_db;
```

Make sure PostgreSQL is running.

### 3. Set up the backend

Open a terminal inside the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
py -3.12 -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure backend environment variables

Create a copy of the example environment file:

```powershell
Copy-Item .env.example .env
```

Update `backend/.env` with your local configuration:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/claimwise_db
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=storage/uploads
MAX_UPLOAD_MB=20
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

OpenAI integration is optional. Without an API key, the deterministic assessment workflow can still produce findings.

### 5. Start the backend

From the backend directory, with the virtual environment activated:

```bash
python -m uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Set up the frontend

Open a separate terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create the frontend environment file:

```powershell
Copy-Item .env.example .env
```

The frontend environment should contain:

```env
VITE_API_URL=http://localhost:8000/api
```

### 7. Start the frontend

```bash
npm run dev
```

Open the application:

```text
http://localhost:5173
```

Keep both backend and frontend terminals running while using the application.

---

## 🧪 Sample Data

The repository includes synthetic sample documents for demonstration.

```text
sample_data/
├── claims/
│   ├── claim_form_CLM-DEMO.txt
│   ├── discharge_summary_CLM-DEMO.txt
│   ├── hospital_bill_CLM-DEMO.txt
│   └── medical_report_CLM-DEMO.txt
│
└── policies/
    └── sample_health_policy.txt
```

You can use these files to test document upload, text extraction, policy retrieval, and claim assessment.

---

## 🔐 Important Implementation Notes

- Policy retrieval currently uses TF-IDF-based lexical matching, not a vector database or embedding-based semantic search.
- Risk scoring uses heuristic and rule-based checks. It is not a trained fraud detection model.
- PDF processing supports text extraction from selectable-text PDFs. OCR for scanned documents is not currently implemented.
- OpenAI integration is optional.
- Claim calculations are illustrative and should not be treated as actual settlement calculations.
- The application does not replace professional insurance investigation or human decision-making.

---

## 🔮 Future Enhancements

- OCR support for scanned documents.
- Embedding-based semantic policy retrieval.
- Advanced document consistency validation.
- Machine-learning-based fraud risk prediction.
- Authentication and role-based access control.
- Improved duplicate document detection.
- Comprehensive automated testing.
- Cloud deployment and production monitoring.
- Secure multi-user and multi-tenant architecture.

---

## 🎯 Project Objective

The objective of ClaimWise AI is to demonstrate how modern full-stack development, AI workflow orchestration, document processing, and human-in-the-loop systems can be combined to support insurance claim investigation.

The project emphasizes structured workflows, traceable findings, and human oversight rather than fully automated claim approval or rejection.

---

## 👨‍💻 Author

**Shiva Naik**

GitHub: https://github.com/Shiva-Na

**Repository:** https://github.com/Shiva-Na/ClaimWise-AI
