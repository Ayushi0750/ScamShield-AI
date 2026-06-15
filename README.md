

# ScamShield-AI

**AI-powered scam detection platform** for internship and job postings — protecting job seekers from fraudulent opportunities.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)
[![DistilBERT](https://img.shields.io/badge/DistilBERT-fine--tuned-orange)](https://huggingface.co/docs/transformers/model_doc/distilbert)
[![Supabase](https://img.shields.io/badge/Supabase-pgvector-3b82f6)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

[GitHub Repository](https://github.com/Ayushi0750/ScamShield-AI)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Real Response Example](#real-response-example)
- [Chrome Extension](#chrome-extension)
- [Current Limitations](#current-limitations)
- [Roadmap](#roadmap)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [License](#license)
- [Author](#author)

---

## Overview

ScamShield-AI helps students, fresh graduates, and job seekers avoid fake internships and recruitment scams by analyzing:

- Job descriptions
- Recruiter information
- Compensation claims
- Communication patterns
- Historical scam data

The system combines rule-based detection, DistilBERT machine learning, Retrieval-Augmented Generation (RAG) with pgvector, recruiter trust scoring, and fraud ring detection into one explainable platform.

---

## Features

| Feature | Description |
|--------|-------------|
| Rule-Based Detection | 75+ scam indicators (fees, urgency, fake salaries, etc.) |
| DistilBERT Classifier | Fine-tuned transformer model |
| Hybrid Scoring | Rules and ML combined for higher reliability |
| RAG (pgvector) | Retrieves similar scam postings as evidence |
| Recruiter Trust Score | Email domain and company verification |
| Fraud Ring Detection | Graph-based network analysis |
| Explainable AI | Shows why a posting is flagged |
| Chrome Extension | Supports LinkedIn, Internshala, Naukri, Indeed |
| React Dashboard | Visual analytics and history |

---

## How It Works

```
Job Posting Input
       ↓
Rule Engine (75+ rules)
       ↓
DistilBERT ML Model
       ↓
Hybrid Scoring Engine
       ↓
RAG (Similar scam retrieval)
       ↓
Recruiter Trust + Fraud Graph
       ↓
Final Scam Assessment + Explanation
```

---

## Tech Stack

### Backend
- FastAPI
- Python 3.10+
- SQLAlchemy + PostgreSQL

### Machine Learning
- DistilBERT (Hugging Face)
- Scikit-learn
- Sentence Transformers (all-MiniLM-L6-v2)

### Vector Database
- Supabase + pgvector

### Frontend
- React.js
- HTML/CSS/JS

### Extension
- Chrome Extension API

---

## Architecture

```
+-------------+     +--------------+     +-------------+
| React Dash  |---->|   FastAPI    |---->| PostgreSQL  |
| Chrome Ext  |<----|   Backend    |<----|  + pgvector |
+-------------+     +--------------+     +-------------+
                           |
              +------------+------------+
              v            v            v
         Rule Engine   DistilBERT     RAG Retriever
                        Model
              |            |            |
              +------------+------------+
                           v
                Hybrid Scoring Engine
                           |
                           v
                Recruiter Trust + Fraud Graph
                           |
                           v
                    Final Assessment
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ayushi0750/ScamShield-AI.git
cd ScamShield-AI
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment variables

Create a `.env` file inside `/backend`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://user:pass@localhost:5432/scamshield
MODEL_PATH=./models/distilbert_scam_model
```

### 4. Run FastAPI server

```bash
uvicorn main:app --reload
```

API docs: `http://localhost:8000/docs`

### 5. Frontend setup

```bash
cd ../frontend
npm install
npm start
```

### 6. Chrome Extension (Developer Mode)

1. Open `chrome://extensions`
2. Enable Developer mode
3. Click Load unpacked
4. Select `/extension` folder

---

## API Usage

### Endpoint

```
POST /api/analyze
```

### Request body

```json
{
  "text": "Earn ₹50,000 weekly. Pay ₹2,000 registration fee before joining."
}
```

---

## Real Response Example

This is an actual response from the current working system.

```json
{
  "prediction": "SCAM",
  "confidence": 75.79,
  "risk_level": "MEDIUM",
  "agreement_status": "AGREE",
  "rule_prediction": "SCAM",
  "ml_prediction": "SCAM",
  "ml_score": 95.00,
  "rag_score": 66.90,
  "similar_cases": [
    {
      "text": "Data Entry Operator Hiring made easy for Digital Jobs BIPIO...",
      "similarity": 69.87
    },
    {
      "text": " QUICK CASH - IMMEDIATE HIRING  Hey Student!...",
      "similarity": 65.96
    }
  ],
  "scam_indicators": [
    "Urgency Manipulation — Uses urgency pressure tactics",
    "Missing Company Identity — Lacks verified company identity"
  ],
  "master_risk_analysis": {
    "final_score": 58.92,
    "final_label": "HIGH_RISK",
    "agreement_status": "AGREE",
    "breakdown": {
      "rule_score": 45,
      "email_score": 40,
      "domain_score": 40,
      "trust_score": 50,
      "trust_risk_score": 50,
      "fraud_ring_score": 0,
      "rule_override_applied": false
    },
    "details": {
      "email": {
        "email": "unknown@unverified.com",
        "reputation": "UNKNOWN",
        "risk_score": 40
      },
      "domain": {
        "reputation": "UNKNOWN",
        "risk_score": 40
      },
      "rings": [
        {
          "cluster_id": 0,
          "risk_score": 0,
          "label": "SAFE",
          "size": 4
        }
      ]
    }
  }
}
```

> **Note on risk levels**: The outer `risk_level` shows `"MEDIUM"` while the detailed analysis shows `"HIGH_RISK"` — this reflects the actual hybrid scoring logic where multiple signals are weighted differently.

---

## Chrome Extension

**Supported platforms:**
- LinkedIn
- Internshala
- Naukri
- Indeed

**How to use:**
1. Install extension in developer mode
2. Navigate to any job or internship posting
3. Click the extension icon
4. View scam risk instantly

---

## Current Limitations

Transparent documentation of current system state.

| Area | Status |
|------|--------|
| DistilBERT accuracy | Trained but not 100% accurate |
| RAG retrieval quality | Working but not perfect |
| LLM / LangChain | Not implemented |


---

## Roadmap

**Completed:**
- Rule engine (75+ rules)
- DistilBERT training
- Hybrid scoring
- RAG with pgvector
- Recruiter trust score
- Fraud ring detection
- Chrome extension (basic)
- React dashboard

**Upcoming:**
- Model fine-tuning improvements
- Multi-language support


---

## Project Structure

```
ScamShield-AI/
├── backend/
│   ├── api/              # FastAPI routes
│   ├── models/           # DistilBERT and ML models
│   ├── services/         # Rule engine, hybrid scoring
│   ├── rag/              # pgvector retrieval
│   ├── trust_scoring/    # Recruiter trust
│   ├── fraud_graph/      # Fraud ring detection
│   └── main.py
├── frontend/
│   ├── src/
│   └── package.json
├── extension/
│   ├── manifest.json
│   ├── content.js
│   └── popup.html
├── datasets/
├── training/
├── notebooks/
└── README.md
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_KEY` | Yes | Supabase anon or public key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `MODEL_PATH` | No | Path to DistilBERT model |



---

## License

**MIT License** — Free for educational, research, and portfolio use.  
No warranty implied. Model accuracy is not guaranteed.

---

## Author

**Built by Ayushi Tiwari** to demonstrate AI-powered fraud detection, full-stack development, and real-time scam analysis.

[![GitHub](https://img.shields.io/badge/GitHub-Ayushi0750-181717?logo=github)](https://github.com/Ayushi0750)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ayushi%20Tiwari-0A66C2?logo=linkedin)](https://www.linkedin.com/in/ayushi-tiwari-977602347)


If this project helped you, consider giving it a star on [GitHub](https://github.com/Ayushi0750/ScamShield-AI).
```



