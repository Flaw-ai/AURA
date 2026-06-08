import json
import random
from pathlib import Path

class SyntheticGenerator:
    def __init__(self, category="general"):
        self.category = category

    def create_sample(self, prompt, answer, source="synthetic", difficulty="medium", language="english"):
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
            "category": self.category,
            "source": source,
            "difficulty": difficulty,
            "language": language
        }

    def generate_from_pairs(self, prompts, answers, difficulty="medium", language="english"):
        dataset = []

        for prompt, answer in zip(prompts, answers):
            dataset.append(
                self.create_sample(
                    prompt=prompt,
                    answer=answer,
                    difficulty=difficulty,
                    language=language
                )
            )
        return dataset

    def augment_prompt(self, prompt):
        prefixes = [
            "Explain clearly:",
            "Teach a student:",
            "Answer step by step:",
            "Provide a detailed explanation:",
            "Solve the following:"
        ]

        return (random.choice(prefixes) + "\n\n" + prompt)

    def create_augmented_dataset(self, prompts, answers):
        dataset = []
        for prompt, answer in zip(prompts, answers):
            dataset.append(
                self.create_sample(
                    prompt=self.augment_prompt(prompt),
                    answer=answer
                )
            )
        return dataset

    def balance_categories(self, datasets):
        min_size = min(
            len(d)
            for d in datasets
        )
        balanced = []

        for dataset in datasets:
            balanced.extend(
                random.sample(dataset, min_size))

        random.shuffle(balanced)
        return balanced

    def save_json(self, dataset, output_path):
        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                dataset,
                f,
                indent=2,
                ensure_ascii=False
            )

    def save_jsonl(self, dataset, output_path):
        Path(
            output_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:
            for sample in dataset:
                f.write(
                    json.dumps(
                        sample,
                        ensure_ascii=False
                    ) + "\n")

    def load_json(self, path):
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    def statistics(self, dataset):
        categories = {}
        difficulties = {}

        for sample in dataset:
            category = sample.get(
                "category",
                "unknown"
            )
            difficulty = sample.get(
                "difficulty",
                "unknown"
            )
            categories[category] = (categories.get(category, 0) + 1)
            difficulties[difficulty] = (difficulties.get(difficulty, 0) + 1)

        return {
            "samples": len(dataset),
            "categories": categories,
            "difficulty": difficulties
        }


if __name__ == "__main__":
    generator = SyntheticGenerator()
    dataset = generator.generate_from_pairs(
        ["What is photosynthesis?"],
        ["Photosynthesis is the process by which plants convert sunlight into energy."]
    )
    print(generator.statistics(dataset))