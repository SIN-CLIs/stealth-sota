"""Determinismus & Seeding – Reproduzierbare Umfrage-Durchläufe."""
import random, hashlib, json

class Seeder:
    @staticmethod
    def from_survey_id(survey_id: str) -> int:
        h = hashlib.sha256(survey_id.encode()).digest()
        seed = int.from_bytes(h[:4], byteorder="big")
        random.seed(seed)
        return seed

    @staticmethod
    def save_state(filepath: str = "/tmp/rng_state.json"):
        state = {"random": random.getstate()}
        with open(filepath, "w") as f:
            json.dump({"random_state": str(state["random"][:3])}, f)

    @staticmethod
    def get_seed(survey_id: str) -> int:
        return Seeder.from_survey_id(survey_id)
