from dotenv import load_dotenv
import os
load_dotenv()

from app.evaluation.eval_runner import EvaluationRunner

runner = EvaluationRunner()
 
runner.run_static_tests("app/evaluation/test_cases.json")