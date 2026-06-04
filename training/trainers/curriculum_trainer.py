from trainers.base_trainer import BaseTrainer

class CurriculumTrainer(
    BaseTrainer
):
    def __init__(
        self,
        config
    ):
        super().__init__(config)

    def load_dataset(self):
        self.logger.info(
            "Loading curriculum stages..."
        )

    def build_model(self):
        self.logger.info(
            "Loading model..."
        )

    def train(self):
        stages = [
            "easy",
            "medium",
            "hard"
        ]

        for stage in stages:
            self.logger.info(
                f"Training stage: {stage}"
            )

    def evaluate(self):

        return {
            "curriculum":
            "completed"
        }