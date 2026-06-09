from pathlib import Path
import json


def collect_data():
    Path("datasets/raw/conversations").mkdir(
        parents=True,
        exist_ok=True
    )

    dataset = [
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is gravity?"
                },
                {
                    "role": "assistant",
                    "content": "Gravity is the force that attracts objects toward each other."
                }
            ]
        },
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is photosynthesis?"
                },
                {
                    "role": "assistant",
                    "content": "Photosynthesis is how plants make food."
                }
            ]
        }
    ]

    with open(
        "datasets/raw/conversations/bootstrap.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            dataset,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Bootstrap dataset created.")

if __name__ == "__main__":
    collect_data()