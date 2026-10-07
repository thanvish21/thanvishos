import json
from pathlib import Path
import random

class Engine:
    """Simple game engine – launches a DSA quiz based on detected weakness.

    The game is interactive via the terminal; for now it prints a question
    and expects the user to type an answer.
    """

    def __init__(self, config: dict):
        self.config = config
        self.games_dir = Path(__file__).parents[2] / "learning" / "games"
        self.games_dir.mkdir(parents=True, exist_ok=True)
        # Ensure a sample quiz file exists
        self.sample_quiz_path = self.games_dir / "dsa_quiz.json"
        if not self.sample_quiz_path.is_file():
            sample = {
                "questions": [
                    {"prompt": "What is the time complexity of binary search?", "answer": "O(log n)"},
                    {"prompt": "Define a stack.", "answer": "LIFO data structure"}
                ]
            }
            self.sample_quiz_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")

    def _load_quiz(self):
        data = json.loads(self.sample_quiz_path.read_text(encoding="utf-8"))
        return data.get("questions", [])

    def run(self, args):
        print("=== DSA Quiz Game ===")
        questions = self._load_quiz()
        random.shuffle(questions)
        score = 0
        for q in questions:
            print("\n" + q["prompt"])
            user_answer = input("Your answer: ")
            if user_answer.strip().lower() == q["answer"].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. Expected: {q['answer']}")
        print(f"\nQuiz finished. Score: {score}/{len(questions)}")
