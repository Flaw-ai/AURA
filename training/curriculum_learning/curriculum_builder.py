from difficulty_ranker import (DifficultyRanker)

class CurriculumBuilder:
    def __init__(self):
        self.ranker = (DifficultyRanker())

    def build(self, dataset):
        curriculum = {
            "easy": [],
            "medium": [],
            "hard": []
        }

        for sample in dataset:
            question = (
                sample["messages"][0]
                ["content"]
            )

            score = (self.ranker.score_question(question))
            stage = (self.ranker.classify(score))
            curriculum[stage].append(sample)

        return curriculum

    def statistics(self, curriculum):
        return {
            "easy": len(curriculum["easy"]),
            "medium": len(curriculum["medium"]),
            "hard":len(curriculum["hard"])
        }