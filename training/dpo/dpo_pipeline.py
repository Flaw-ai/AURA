import json
from pathlib import Path
from .preference_dataset import (PreferenceDataset)
from .pair_generator import (PairGenerator)
from .reward_formatter import (RewardFormatter)

class DPOPipeline:
    def __init__(self, dataset_path: str, output_dir: str = "output"):
        self.dataset_path = (dataset_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dataset = (PreferenceDataset(dataset_path))
        self.generator = (PairGenerator())
        self.rewarder = (RewardFormatter())

    def load_data(self):
        raw = self.dataset.load()
        cleaned = (self.dataset.clean(raw))
        return cleaned["dataset"]

    def score_pair(self, pair):
        chosen_score = (self.rewarder.total_reward(pair["chosen"]))
        rejected_score = (self.rewarder.total_reward(pair["rejected"]))
        pair["chosen_reward"] = (chosen_score)
        pair["rejected_reward"] = (rejected_score)
        pair["reward_gap"] = round(chosen_score["reward"] - rejected_score["reward"], 4)

        return pair

    def process(self):
        dataset = (self.load_data())

        processed = []

        for pair in dataset:
            scored = (self.score_pair(pair))
            processed.append(scored)

        return processed

    def save(self, processed):
        output_file = (self.output_dir/"dpo_dataset.json")
        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                processed,
                f,
                indent=4,
                ensure_ascii=False
            )

        return output_file

    def run(self):
        print("\n=== DPO PIPELINE ===")
        processed = (self.process())
        output = self.save(processed)
        print(f"Saved: {output}")
        print(f"Samples: " f"{len(processed)}")

        return processed


if __name__ == "__main__":
    pipeline = DPOPipeline("preferences.json")
    pipeline.run()