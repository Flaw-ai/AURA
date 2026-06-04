from trainers.base_trainer import BaseTrainer

class DPOTrainer(BaseTrainer):
    def __init__(self, config):
        super().__init__(config)

    def load_dataset(self):
        self.logger.info(
            "Loading DPO dataset..."
        )

    def build_model(self):
        self.logger.info(
            "Loading model..."
        )

    def train(self):
        self.logger.info(
            "Running DPO training..."
        )

    def evaluate(self):
        return {
            "status": "dpo_eval"
        }