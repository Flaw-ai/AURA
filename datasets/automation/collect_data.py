from pathlib import Path
import json


def collect_data():
    Path("datasets/raw/conversations").mkdir(
        parents=True,
        exist_ok=True
    )

    sample = {
        "messages": [
            {
                "role": "user",
                "content":
                "What is gravity?"
            },
            {
                "role": "assistant",
                "content":
                "Gravity is the force that attracts objects toward each other."
            }
        ]
    }

    output = (
        "datasets/raw/conversations/"
        "bootstrap.jsonl"
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(sample)
            + "\n"
        )

    print("Bootstrap dataset created.")

if __name__ == "__main__":
    collect_data()