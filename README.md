🧠 AI Control Platform

A structured AI compliance and decision engine built with Retrieval-Augmented Generation (RAG) and schema-enforced LLM outputs.

Designed to demonstrate:
	•	AI system reliability
	•	Structured generation
	•	Evaluation harness
	•	Governance-aware AI architecture

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
	•	Cosine Similarity Retrieval
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