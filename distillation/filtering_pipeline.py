import re
from typing import List

class FilteringPipeline:
    REFUSAL_PATTERNS = [
        "i cannot",
        "i can't",
        "i am unable",
        "sorry, but",
        "as an ai language model",
        "i do not have the ability"
    ]
    CHEATING_PATTERNS = [
        "exam answer key",
        "bypass exam",
        "cheat sheet",
        "hack school",
        "skip proctoring"
    ]
    UNSAFE_PATTERNS = [
        "make a bomb",
        "harm someone",
        "illegal activity",
        "malware code"
    ]
    LOW_QUALITY_PATTERNS = [
        "lorem ipsum",
        "test test test",
        "placeholder"
    ]

    def __init__(self, response_ranker, min_words=5, min_score=0.5):
        self.response_ranker = response_ranker
        self.min_words = min_words
        self.min_score = min_score

    def quality_score(self, response):
        return self.response_ranker.score_response(response)

    def word_count(self, response):
        return len(response.split())

    def contains_pattern(self, response, patterns):
        text = response.lower()
        return any(
            pattern in text
            for pattern in patterns
        )

    def contains_refusal(self, response):
        return self.contains_pattern(
            response,
            self.REFUSAL_PATTERNS
        )

    def contains_exam_cheating(self, response):
        return self.contains_pattern(
            response,
            self.CHEATING_PATTERNS
        )

    def contains_unsafe_content(self, response):
        return self.contains_pattern(
            response,
            self.UNSAFE_PATTERNS
        )

    def contains_low_quality(self, response):
        return self.contains_pattern(
            response,
            self.LOW_QUALITY_PATTERNS
        )

    def repeated_text_ratio(self, response):
        words = response.lower().split()
        if len(words) == 0:
            return 1.0
        unique_words = len(set(words))

        return 1 - (unique_words / len(words))

    def too_repetitive(self, response, threshold=0.5):
        return (self.repeated_text_ratio(response) > threshold)

    def passes_quality(self, response):
        if self.word_count(response) < self.min_words:
            return False

        if self.quality_score(response) < self.min_score:
            return False

        return True

    def keep(self, response):
        if self.contains_refusal(response):
            return False

        if self.contains_exam_cheating(response):
            return False

        if self.contains_unsafe_content(response):
            return False

        if self.contains_low_quality(response):
            return False

        if self.too_repetitive(response):
            return False

        if not self.passes_quality(response):
            return False

        return True

    def filter_dataset(self, responses):
        return [
            r
            for r in responses
            if self.keep(r)
        ]

    def statistics(self, responses):
        kept = self.filter_dataset(responses)

        return {
            "total": len(responses),
            "kept": len(kept),
            "removed": len(responses) - len(kept)
        }