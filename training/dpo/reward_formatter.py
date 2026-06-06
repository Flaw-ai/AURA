import re
from typing import Dict

class RewardFormatter:
    def __init__(self):
        self.educational_keywords = [
            "because",
            "therefore",
            "example",
            "step",
            "formula",
            "explanation",
            "concept",
            "reason",
            "solution",
            "answer"
        ]

    def score_length(self, response: str) -> float:
        words = len(response.split())

        if words < 20:
            return 0.3
        if words < 50:
            return 0.7
        if words < 200:
            return 1.0

        return 0.8

    def score_clarity(self, response: str) -> float:
        sentences = re.split(r"[.!?]", response)

        sentences = [
            s.strip()
            for s in sentences
            if s.strip()
        ]

        if not sentences:
            return 0.0

        avg_words = sum(len(s.split()) for s in sentences) / len(sentences)

        if avg_words < 8:
            return 0.6

        if avg_words < 20:
            return 1.0

        return 0.8

    def score_educational(self, response: str) -> float:
        response = response.lower()
        count = sum(
            keyword in response
            for keyword in self.educational_keywords
        )

        return min(count / 5, 1.0)

    def total_reward(self, response: str) -> Dict:
        length_score = self.score_length(response)
        clarity_score = self.score_clarity(response)
        educational_score = (self.score_educational(response))
        reward = (length_score * 0.2 + clarity_score * 0.4 + educational_score * 0.4)

        return {
            "reward":round(reward, 4),
            "length": round(length_score, 4),
            "clarity": round(clarity_score, 4),
            "educational": round(educational_score, 4)
        }