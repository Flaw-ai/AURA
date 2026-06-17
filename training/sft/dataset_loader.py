import json
from pathlib import Path
from datasets import Dataset

class DatasetLoader:
    def __init__(self, train_path, val_path=None, test_path=None):
        self.train_path = Path(train_path)
        self.val_path = (Path(val_path) if val_path else None)
        self.test_path = (Path(test_path) if test_path else None)

    def _load_jsonl(self, path):
        cleaned = []
        
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    sample = json.loads(line)
                except Exception:
                    continue

                if ("messages" not in sample):
                    continue

                if (len(sample["messages"]) < 2):
                    continue

                cleaned.append(sample)
        return Dataset.from_list(cleaned)

    def load(self):
        datasets = {
            "train": self._load_jsonl(self.train_path)
        }

        if self.val_path:
            datasets["val"] = (
                self._load_jsonl(self.val_path)
            )

        if self.test_path:
            datasets["test"] = (
                self._load_jsonl(self.test_path)
            )
        return datasets

    def statistics(self, dataset):
        total = len(dataset)
        avg_turns = (
            sum(len(x["messages"]) for x in dataset) / total
        )

        return {
            "samples": total,
            "avg_turns":
            round(avg_turns, 2)
        }

    def print_stats(self, datasets):
        print("\nDATASET STATS\n")

        for name, ds in datasets.items():
            stats = self.statistics(ds)
            print(
                f"{name.upper()}: "
                f"{stats['samples']:,} samples | "
                f"avg turns = "
                f"{stats['avg_turns']}"
            )