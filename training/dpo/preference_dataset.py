import json
from pathlib import Path

class PreferenceDataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def load(self):
        with open(
            self.dataset_path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    def validate_sample(self, sample):
        required = [
            "prompt",
            "chosen",
            "rejected"
        ]

        return all(
            field in sample
            for field in required
        )

    def clean(self, dataset):
        cleaned = []
        rejected = 0

        for sample in dataset:
            if self.validate_sample(sample):
                cleaned.append(sample)
            else:
                rejected += 1

        return {
            "dataset": cleaned,
            "rejected": rejected
        }

    def statistics(self, dataset):
        return {
            "samples": len(dataset),
            "avg_prompt_chars": round(sum(len(x["prompt"]) for x in dataset)/ max(len(dataset), 1), 2)
        }