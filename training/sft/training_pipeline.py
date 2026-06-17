from sft.dataset_loader import DatasetLoader
from sft.formatting import ConversationFormatter

class TrainingPipeline:
    def __init__(self, config):
        self.config = config

    def prepare(self):
        loader = DatasetLoader(
            train_path=self.config["dataset"]["train_path"],
            val_path=self.config["dataset"]["val_path"],
            test_path=self.config["dataset"]["test_path"]
        )
        datasets = loader.load()
        loader.print_stats(datasets)
        formatter = ConversationFormatter()
        train_data = (
            formatter.format_dataset(datasets["train"])
        )

        val_data = (
            formatter.format_dataset(datasets["val"])
        )

        return {
            "train": train_data,
            "val": val_data
        }