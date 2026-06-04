import json
from pathlib import Path
from datasets import Dataset

class DatasetLoader:
    
    def __init__(self, dataset_path):
        self.dataset_path = Path(
            dataset_path
        )

    def load(self):
        with open(
            self.dataset_path,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        cleaned = []

        for sample in data:
            if ("messages" not in sample):
                continue
            if (
                len(sample["messages"])
                < 2
            ):
                continue

            cleaned.append(sample)

        return Dataset.from_list(cleaned)

    def train_val_split(self, dataset, test_size=0.1):

        return dataset.train_test_split(
            test_size=test_size,
            seed=42
        )

    def statistics(self, dataset):

        total = len(dataset)
        avg_turns = sum(
            len(x["messages"])
            for x in dataset
        ) / total

        return {
            "samples": total,
            "avg_turns":
            round(avg_turns, 2)
        }