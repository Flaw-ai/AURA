from sft.dataset_loader import (DatasetLoader)
from sft.formatting import (ConversationFormatter)

class TrainingPipeline:
    def __init__(self, dataset_path):

        self.dataset_path = (dataset_path)

    def prepare(self):

        loader = DatasetLoader(self.dataset_path)
        dataset = loader.load()
        stats = loader.statistics(dataset)

        print("\nDATASET STATS")
        print(stats)

        split = (
            loader
            .train_val_split(
                dataset
            )
        )

        formatter = (
            ConversationFormatter()
        )

        train_data = (
            formatter
            .format_dataset(
                split["train"]
            )
        )

        val_data = (
            formatter
            .format_dataset(
                split["test"]
            )
        )

        return {
            "train": train_data,
            "val": val_data
        }