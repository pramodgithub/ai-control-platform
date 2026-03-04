from dotenv import load_dotenv
load_dotenv()

from app.governance.decision_engine import DecisionEngine

engine = DecisionEngine()

result = engine.evaluate(
    "Vendor stores EU customer data in US data centers without safeguards."
)

print(result.model_dump_json(indent=2))