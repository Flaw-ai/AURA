class Evaluator:
    def exact_match(
        self,
        predictions,
        references
    ):
        total = len(
            predictions
        )
        correct = 0
        for pred, ref in zip(
            predictions,
            references
        ):
            if (
                pred.strip().lower()
                ==
                ref.strip().lower()
            ):

                correct += 1

        return {
            "accuracy":
            round(
                correct / total,
                4
            )
        }

    def response_length(
        self,
        responses
    ):
        avg = sum(
            len(r.split())
            for r in responses
        ) / len(responses)

        return {
            "avg_words":
            round(avg, 2)
        }