import json
import random
from pathlib import Path


class SyntheticGenerator:

    def __init__(self, seed=42):
        random.seed(seed)

    def sample(self, prompt, answer, category):

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
            "category": category,
            "source": "synthetic"
        }

    # --------------------------------------------------
    # Math
    # --------------------------------------------------

    def generate_math(self, count):

        dataset = []

        for _ in range(count):

            a = random.randint(1, 500)
            b = random.randint(1, 500)

            dataset.append(
                self.sample(
                    f"What is {a} + {b}?",
                    f"{a+b}",
                    "math"
                )
            )

            dataset.append(
                self.sample(
                    f"What is {a} × {b}?",
                    f"{a*b}",
                    "math"
                )
            )

        return dataset

    # --------------------------------------------------
    # Science
    # --------------------------------------------------

    def generate_science(self, count):

        topics = [
            (
                "What is photosynthesis?",
                "Photosynthesis is the process by which plants convert sunlight into chemical energy."
            ),
            (
                "What is gravity?",
                "Gravity is the force that attracts objects toward one another."
            ),
            (
                "What is an atom?",
                "An atom is the smallest unit of ordinary matter."
            ),
            (
                "Why do plants need sunlight?",
                "Plants use sunlight to produce food through photosynthesis."
            )
        ]

        dataset = []

        for _ in range(count):

            q, a = random.choice(topics)

            dataset.append(
                self.sample(
                    q,
                    a,
                    "science"
                )
            )

        return dataset

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    def generate_reasoning(self, count):

        dataset = []

        for _ in range(count):

            apples = random.randint(5, 50)
            given = random.randint(1, apples)

            answer = (
                f"Start with {apples}. "
                f"Give away {given}. "
                f"{apples-given} remain."
            )

            dataset.append(
                self.sample(
                    f"I have {apples} apples and give away {given}. How many remain?",
                    answer,
                    "reasoning"
                )
            )

        return dataset

    # --------------------------------------------------
    # Tutoring
    # --------------------------------------------------

    def generate_tutoring(self, count):

        topics = [
            "fractions",
            "electricity",
            "photosynthesis",
            "force",
            "algebra",
            "atoms",
            "ecosystems",
            "programming"
        ]

        dataset = []

        for _ in range(count):

            topic = random.choice(topics)

            dataset.append(
                self.sample(
                    f"Teach me about {topic}.",
                    (
                        f"{topic.capitalize()} is an important concept. "
                        f"Let's learn it step-by-step with examples and explanations."
                    ),
                    "tutoring"
                )
            )

        return dataset

    # --------------------------------------------------
    # Exam
    # --------------------------------------------------

    def generate_exam(self, count):

        dataset = []

        for _ in range(count):

            a = random.randint(1, 100)
            b = random.randint(1, 100)

            dataset.append(
                self.sample(
                    f"Solve {a}+{b}. Show steps.",
                    (
                        f"Step 1: Add {a} and {b}\n"
                        f"Step 2: Result = {a+b}\n"
                        f"Final Answer: {a+b}"
                    ),
                    "exam"
                )
            )

        return dataset

    # --------------------------------------------------
    # Hinglish
    # --------------------------------------------------

    def generate_hinglish(self, count):

        dataset = []

        prompts = [
            "Gravity kya hoti hai?",
            "Photosynthesis explain karo",
            "Atom kya hai?",
            "Electricity kaise kaam karti hai?"
        ]

        answers = [
            "Gravity ek force hai jo objects ko attract karti hai.",
            "Photosynthesis mein plants sunlight se food banate hain.",
            "Atom matter ka smallest unit hota hai.",
            "Electricity electrons ke flow se kaam karti hai."
        ]

        for _ in range(count):

            idx = random.randint(
                0,
                len(prompts)-1
            )

            dataset.append(
                self.sample(
                    prompts[idx],
                    answers[idx],
                    "hinglish"
                )
            )

        return dataset

    # --------------------------------------------------
    # Master Generator
    # --------------------------------------------------

    def generate_dataset(self):

        dataset = []

        dataset.extend(
            self.generate_math(10000)
        )

        dataset.extend(
            self.generate_science(10000)
        )

        dataset.extend(
            self.generate_reasoning(10000)
        )

        dataset.extend(
            self.generate_tutoring(10000)
        )

        dataset.extend(
            self.generate_exam(10000)
        )

        dataset.extend(
            self.generate_hinglish(5000)
        )

        random.shuffle(dataset)

        return dataset

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save_jsonl(
        self,
        dataset,
        output_file
    ):

        Path(
            output_file
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            for row in dataset:

                f.write(
                    json.dumps(
                        row,
                        ensure_ascii=False
                    )
                    + "\n"
                )

        print(
            f"Saved {len(dataset)} examples"
        )


if __name__ == "__main__":

    generator = SyntheticGenerator()

    dataset = generator.generate_dataset()

    generator.save_jsonl(
        dataset,
        "datasets/synthetic/generated/flaw_dataset.jsonl"
    )

    print(
        f"Total examples: {len(dataset)}"
    )