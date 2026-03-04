from app.ai.llm_gateway import LLMGateway
from app.retrieval.retriever import retrieve_similar_clauses
from app.governance.schema import ComplianceDecision
from app.storage.logger import log_decision
from app.governance.risk_engine import compute_risk
from app.governance.clause_filter import filter_relevant_clauses
from google import genai
import os
import json
from dotenv import load_dotenv
load_dotenv()
#from app.llm.providers.llm_gateway import LLMGateway

class DecisionEngine:

    def __init__(self):
        self.llm = LLMGateway()
    #    print("LLM object:", self.llm)
    #    print("Has generate_json:", hasattr(self.llm, "generate_json"))

  #  def _call_llm(self, prompt: str):
   #     return self.llm.generate(prompt=prompt, temperature=0.0)

    def evaluate(self, user_input: str) -> ComplianceDecision:
            # Step 1: vector retrieval
            retrieved = retrieve_similar_clauses(user_input, top_k=5)

            # Step 2: similarity gap filter
            filtered = self._dynamic_gap_filter(retrieved)

            # Step 3: semantic relevance filter
            filtered = filter_relevant_clauses(
                self.llm,
                user_input,
                filtered
            )

            if not filtered:
                decision_json = {
                    "decision": "INSUFFICIENT_CONTEXT",
                    "violated_clauses": [],
                    "explanation": "No sufficiently relevant policy clauses found.",
                    "confidence_score": 0.2,
                    "risk_level": "LOW",
                    "needs_human_review": True
                }

                return ComplianceDecision(**decision_json)
            else:
                clauses_text = "\n\n".join(
                    [f"{r.policy_id}-{r.clause_id}: {r.clause_text}" for r in filtered]
                )

                prompt = self._build_prompt(user_input, clauses_text)

                # Step 4: LLM decision
                decision_json = self._get_llm_decision(prompt)

                # Step 5: risk computation
                risk_level = compute_risk(decision_json.get("violated_clauses", []))
                decision_json["risk_level"] = risk_level

                # Step 6: confidence & review logic
                CONFIDENCE_THRESHOLD = 0.75
                confidence = decision_json.get("confidence_score", 0)

                needs_review = confidence < CONFIDENCE_THRESHOLD
                decision_json["needs_human_review"] = needs_review

                # Controlled downgrade rule
                if (
                    decision_json["decision"] == "NON_COMPLIANT"
                    and confidence < CONFIDENCE_THRESHOLD
                ):
                    decision_json["decision"] = "INSUFFICIENT_CONTEXT"

                # Step 7: audit logging
                log_decision(
                    user_input=user_input,
                    retrieved=[r.clause_id for r in retrieved],
                    filtered=[r.clause_id for r in filtered],
                    prompt=prompt if filtered else None,
                    raw_response=decision_json,   # store structured response
                    decision=decision_json,
                    model_name=self.llm.model,
                    embedding_provider=os.getenv("EMBEDDING_PROVIDER")
                )
                
                return ComplianceDecision(**decision_json)

    def _dynamic_gap_filter(self, results):

            """
                    Layer: Vector retrieval
                    Purpose: Remove weak similarity matches

                    Removes:
                    ❌ clauses that are too far in embedding space
                    ❌ noise from vector search
                    Keeps:
                    ✔ semantically close candidates
            """

            if not results:
                return []

            GAP_THRESHOLD = 0.15

            filtered = [results[0]]

            for i in range(1, len(results)):
                gap = results[i].distance - results[i-1].distance
                if gap < GAP_THRESHOLD:
                    filtered.append(results[i])
                else:
                    break

            return filtered

    def _get_llm_decision(self, prompt: str) -> dict:
            """
            Calls LLM gateway and ensures safe structured output.
            """
            try:
                response = self.llm.generate_json(prompt)

                # safety defaults
                response.setdefault("decision", "INSUFFICIENT_CONTEXT")
                response.setdefault("violated_clauses", [])
                response.setdefault("explanation", "No explanation provided.")
                response.setdefault("confidence_score", 0.5)

                return response

            except Exception as e:
                return {
                    "decision": "INSUFFICIENT_CONTEXT",
                    "violated_clauses": [],
                    "explanation": f"LLM error: {str(e)}",
                    "confidence_score": 0.0
                }

    def _build_prompt(self, user_input, clauses_text):
        return f"""
                You are a compliance decision engine.

                User Input:
                {user_input}

                Relevant Policy Clauses:
                {clauses_text}

                Based only on the clauses provided, return a JSON object with:
                - decision (COMPLIANT | NON_COMPLIANT | INSUFFICIENT_CONTEXT)
                - violated_clauses (list of clause IDs that are DIRECTLY violated)
                - Include at most 2 violated clauses.
                - If more appear relevant, select the most directly violated.
                - For each violated clause, you MUST briefly explain why it is violated.
                - Do NOT include clauses that are only loosely related.
                - explanation
                - confidence_score (0 to 1)

                Return ONLY valid JSON.
                """