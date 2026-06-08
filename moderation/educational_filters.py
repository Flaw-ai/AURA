import re

class EducationalFilters:
    BLOCKED_PATTERNS = [
        r"how to make a bomb",
        r"hack.*account",
        r"steal.*password",
        r"bypass.*exam",
        r"cheat.*exam",
        r"generate.*malware",
        r"ddos",
        r"phishing",
    ]

    def __init__(self):
        self.compiled = [
            re.compile(
                pattern,
                re.IGNORECASE
            )
            for pattern in self.BLOCKED_PATTERNS
        ]

    def is_safe(self, text):
        for pattern in self.compiled:
            if pattern.search(text):
                return False

        return True

    def check(self, text):
        safe = self.is_safe(text)

        return {
            "safe": safe,
            "message": "Allowed" if safe
                else "Blocked by educational policy"
        }

    def sanitize(self, text):
        text = text.strip()
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def filter_response(self, response):
        if not self.is_safe(response):
            return (
                "I can help with educational "
                "and learning-related questions."
            )

        return response

    def educational_score(self, text):
        keywords = [
            "learn",
            "study",
            "education",
            "science",
            "math",
            "history",
            "english",
            "explain"
        ]
        score = 0
        lower = text.lower()

        for keyword in keywords:
            if keyword in lower:
                score += 1

        return score / len(keywords)