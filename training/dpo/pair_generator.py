class PairGenerator:
    def __init__(self):
        pass

    def create_pair(self, prompt, responses, scores):
        if (len(responses) != len(scores) ):
            raise ValueError("responses and scores mismatch")

        ranked = sorted(
            zip(responses, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        chosen = ranked[0][0]
        rejected = ranked[-1][0]
        
        return {
            "prompt": prompt,
            "chosen": chosen,
            "rejected": rejected
        }

    def batch_generate(self, prompts, response_sets, score_sets):
        pairs = []
        for prompt, responses, scores in zip(prompts, response_sets, score_sets):
            pair = self.create_pair(
                prompt,
                responses,
                scores
            )
            pairs.append(pair)

        return pairs