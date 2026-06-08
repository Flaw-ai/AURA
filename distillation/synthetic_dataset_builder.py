import json
from pathlib import Path

class SyntheticDatasetBuilder:
    def __init__(self):
        pass

    def create_sample(self, prompt, answer, category="general"):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ],
            "category": category
        }

    def build(self, prompts, answers, category="general"):
        dataset = []
        for p, a in zip(prompts, answers):
            dataset.append(
                self.create_sample(
                    p,
                    a,
                    category
                )
            )
        return dataset

    def save(self, dataset, output_file):
        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                dataset,
                f,
                indent=2,
                ensure_ascii=False
            )

    def load(self, file_path):
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)