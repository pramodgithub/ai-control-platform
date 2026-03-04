# AI Control Platform

A structured AI compliance decision engine built using:

- Retrieval-Augmented Generation (RAG)
- Structured LLM outputs (JSON schema enforced)
- Pydantic-based decision contracts
- Semantic retrieval with pgvector
- Evaluation harness for regression testing
- Governance layer with risk scoring and review triggers

## Architecture Overview

Ingestion → Embedding → Retrieval → LLM → Structured Decision → Evaluation → Governance