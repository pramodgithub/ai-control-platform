import json
import time
from app.governance.decision_engine import DecisionEngine

REQUESTS_PER_MINUTE = 10
DELAY_SECONDS = 60 / REQUESTS_PER_MINUTE


class EvaluationRunner:

    def __init__(self):
        self.engine = DecisionEngine()

    def run_static_tests(self, file_path):
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        dangerous_errors = 0
        safe_downgrades = 0
        over_detection_count = 0

        total_confidence = 0
        review_count = 0

        decision_correct = 0
        decision_accuracy = 0

        clause_full_match = 0
        clause_full_accuracy = 0
        
        clause_partial_match = 0
        clause_partial_accuracy = 0

        confusion = {
            "NON_COMPLIANT": {"NON_COMPLIANT": 0, "COMPLIANT": 0, "INSUFFICIENT_CONTEXT": 0},
            "COMPLIANT": {"NON_COMPLIANT": 0, "COMPLIANT": 0, "INSUFFICIENT_CONTEXT": 0},
            "INSUFFICIENT_CONTEXT": {"NON_COMPLIANT": 0, "COMPLIANT": 0, "INSUFFICIENT_CONTEXT": 0},
        }

        with open(file_path, "r") as f:
            test_cases = json.load(f)

        total = len(test_cases)
        

        for index, case in enumerate(test_cases):

            print(f"\nRunning Test Case {case['id']}...")

            result = self.engine.evaluate(case["input"])

            # --- Rate limiting ---
            if index < len(test_cases) - 1:
                time.sleep(DELAY_SECONDS)
            actual_decision = result.decision.strip().upper()
            expected_decision = case["expected_decision"].strip().upper()

            confusion[expected_decision][actual_decision] += 1

            total_confidence += result.confidence_score

            if result.needs_human_review:
                review_count += 1

            # ------------------------
            # Risk classification metrics
            # ------------------------

            if expected_decision == "NON_COMPLIANT":
                if actual_decision == "NON_COMPLIANT":
                    true_positive += 1
                else:
                    false_negative += 1
            else:
                if actual_decision == "NON_COMPLIANT":
                    false_positive += 1
                else:
                    true_negative += 1

            # ------------------------
            # Governance-aware matching
            # ------------------------

            actual_clauses = set(c.strip() for c in result.violated_clauses)
            expected_clauses = set(c.strip() for c in case["expected_clauses"])

            decision_match = actual_decision == expected_decision

            # ✅ Accept SAFE downgrade (legally safer)
            if expected_decision == "COMPLIANT" and actual_decision == "INSUFFICIENT_CONTEXT":
                decision_match = True
                safe_downgrades += 1

            # ❌ Dangerous error (must NEVER happen)
            dangerous_error = (
                expected_decision == "NON_COMPLIANT"
                and actual_decision == "COMPLIANT"
            )

            if dangerous_error:
                dangerous_errors += 1

            # ✅ Clause containment logic
            clauses_match = expected_clauses.issubset(actual_clauses)

            # Track over-detection (extra clauses)
            extra_clauses = actual_clauses - expected_clauses
            if extra_clauses:
                over_detection_count += 1

            # ------------------------
            # Independent Scoring
            # ------------------------

            if decision_match and not dangerous_error:
                decision_correct += 1

            # Full clause containment
            if clauses_match:
                clause_full_match += 1

            # Partial clause match (at least one expected clause found)
            if expected_clauses and actual_clauses.intersection(expected_clauses):
                clause_partial_match += 1

            # ------------------------
            # Output
            # ------------------------

            print("\nTest Case:", case["id"])
            print("Expected:", expected_decision)
            print("Actual:", actual_decision)
            print("Decision Match:", decision_match)
            print("Full Clause Match:", clauses_match)
            print("Partial Clause Match:",
                bool(expected_clauses and actual_clauses.intersection(expected_clauses)))
            print("Confidence:", result.confidence_score)
            print("Actual Clauses:", list(actual_clauses))
            print("Expected Clauses:", list(expected_clauses))
            if extra_clauses:
                print("Extra Clauses Detected:", list(extra_clauses))
            if dangerous_error:
                print("⚠️ Dangerous Error Detected")

        # ------------------------
        # Metrics
        # ------------------------

        decision_accuracy = decision_correct / total if total else 0
        clause_full_accuracy = clause_full_match / total if total else 0
        clause_partial_accuracy = clause_partial_match / total if total else 0

        precision = (
            true_positive / (true_positive + false_positive)
            if (true_positive + false_positive) else 0
        )

        recall = (
            true_positive / (true_positive + false_negative)
            if (true_positive + false_negative) else 0
        )

        false_positive_rate = (
            false_positive / (false_positive + true_negative)
            if (false_positive + true_negative) else 0
        )

        false_negative_rate = (
            false_negative / (false_negative + true_positive)
            if (false_negative + true_positive) else 0
        )

        avg_confidence = total_confidence / total if total else 0
        human_review_rate = review_count / total if total else 0

        print("\n--- Evaluation Summary ---")
        print("Total:", total)

        print("\n--- Decision Accuracy ---")
        print("Decision Accuracy:", round(decision_accuracy, 2))

        print("\n--- Clause Accuracy ---")
        print("Full Clause Match:", round(clause_full_accuracy, 2))
        print("Partial Clause Match:", round(clause_partial_accuracy, 2))

        print("\n--- Governance Safety Metrics ---")
        print("Dangerous Errors:", dangerous_errors, "🚨")
        print("Safe Downgrades:", safe_downgrades)
        print("Clause Over-Detection:", over_detection_count)

        print("\n--- Advanced Metrics ---")
        print("Precision (NON_COMPLIANT):", round(precision, 2))
        print("Recall (NON_COMPLIANT):", round(recall, 2))
        print("False Positive Rate:", round(false_positive_rate, 2))
        print("False Negative Rate:", round(false_negative_rate, 2))
        print("Average Confidence:", round(avg_confidence, 2))
        print("Human Review Rate:", round(human_review_rate, 2))

        print("\n--- Confusion Matrix ---")
        for expected, preds in confusion.items():
            print(expected, preds)