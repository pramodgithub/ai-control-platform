🧠 AI Control Platform

A structured AI compliance and governance engine built using Retrieval-Augmented Generation (RAG) with schema-enforced LLM outputs and auditability.

🎯 Purpose

This project focuses on:
	•	Structured decision contracts
	•	Evaluation harness
	•	Governance controls
	•	Audit trail & replay
	•	Observability metrics
	•	Production-style API interface

⸻

🏗 Architecture Overview

        Document Ingestion
            ↓
        Chunking + Embedding
            ↓
        pgvector Semantic Storage
            ↓
        Similarity Retrieval
            ↓
        Structured LLM (JSON Schema)
            ↓
        Compliance Decision Model
            ↓
        Evaluation Harness
            ↓
        Governance Risk Scoring

⸻

🔧 Tech Stack
	•	Python
	•	Postgres + pgvector
	•	Pydantic
	•	LLM Structured JSON Output
	•	FastAPI
	•	SQLAlchemy
	•	Modular Service Architecture

⸻

📦 Project Structure

        app/
        ├── ingestion/
        ├── embedding/
        ├── retrieval/
        ├── storage/
        ├── ai/
        ├── models/
        ├── governance/
        ├── evaluation/
        └── replay/

⸻

🧪 Evaluation & Regression Testing

The system includes:
	•	Deterministic evaluation harness
	•	Structured decision validation
	•	Risk classification testing
	•	JSON schema enforcement
	•	Regression testing via test_eval.py

⸻

🔐 Governance Layer

The governance module introduces:
	•	Risk scoring
	•	Human review triggers
	•	Structured decision auditability
	•	Replay capability

⸻

🚀 Roadmap
	•	Add Graph-based retrieval (GraphRAG exploration)
	•	Introduce agent memory layer
	•	Add FastAPI inference endpoint
	•	Add lightweight dashboard for decision inspection
	•	Add CI pipeline for regression testing

⸻

🎯 Why This Project?

Most RAG demos stop at retrieval.

This project focuses on:
	•	Reliability
	•	Structured outputs
	•	Evaluation
	•	Governance
	•	Production-readiness mindset


🚀 Running the API

uvicorn app.api.main:app --reload

Visit
http://localhost:8000/docs

📡 API Endpoints

		POST /evaluate

		Evaluate a compliance document.

		Request:
		{
		"document": "Organization performs periodic risk assessments..."
		}

GET /replay/{id}

Replay a stored compliance decision.

⸻

GET /metrics

Returns governance metrics:
	•	total evaluations
	•	average confidence
	•	human review rate

⸻

🛡 Governance Capabilities
	•	All LLM decisions are persisted
	•	Audit trace with timestamp
	•	Human review tracking
	•	Risk level classification
	•	Decision replay capability
	•	Evaluation metrics monitoring

⸻

🧪 Evaluation Harness

	Static regression tests via:

		python test_eval.py

	Ensures deterministic validation of compliance decisions.