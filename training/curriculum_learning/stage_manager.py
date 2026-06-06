class StageManager:
    STAGES = [
        "easy",
        "medium",
        "hard"
    ]

    def __init__(self, ranker):
        self.ranker = ranker
        self.current_index = 0

    def assign_stage(self, question):
        score = self.ranker.score_question(question)
        return self.ranker.classify(score)

    def current_stage(self):
        return self.STAGES[self.current_index]

    def next_stage(self):
        if (self.current_index < len(self.STAGES) - 1):
            self.current_index += 1

        return self.current_stage()

    def reset(self):
        self.current_index = 0

    def is_final_stage(self):
        return (self.current_index == len(self.STAGES) - 1)

    def get_stages(self):
        return self.STAGES