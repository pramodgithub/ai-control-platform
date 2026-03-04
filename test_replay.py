from dotenv import load_dotenv
load_dotenv()

from app.replay.replay_engine import ReplayEngine

replay = ReplayEngine()

replay.replay_decision(9)
