class ResponseRanker:
    def __init__(self):
        pass

    def score_response(self, response):
        score = 0
        words = len(response.split())
        score += min(words / 100, 1.0)
        
        if "\n" in response:
            score += 0.2
        if ":" in response:
            score += 0.1

        return score

    def rank(self, responses):
        ranked = []
        for response in responses:
            ranked.append({
                "response": response,
                "score": self.score_response(response)
            })

        ranked.sort(
            key=lambda x:
            x["score"],
            reverse=True
        )

        return ranked

    def best(self, responses):
        ranked = self.rank(responses)
        return ranked[0]

    def top_k(self, responses, k=3):
        ranked = self.rank(responses)
        return ranked[:k]