import time
import logging
from app.evaluation.eval_runner import EvaluationRunner

logger = logging.getLogger(__name__)
runner = EvaluationRunner()

def evaluate_document(document: str):
    start = time.time()

    result = runner.evaluate_document(document)

    latency = round((time.time() - start) * 1000, 2)

    logger.info(
        f"decision={result.decision} "
        f"risk={result.risk_level} "
        f"confidence={result.confidence_score} "
        f"latency_ms={latency}"
    )

    decision_id = save_decision(result)

    result_dict = result.dict()
    result_dict["decision_id"] = decision_id

    return result_dict
   