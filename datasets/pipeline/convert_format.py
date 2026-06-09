import json
import csv

def convert_alpaca_to_messages(
    input_file,
    output_file
):
    """
    Alpaca format:
    {
      "instruction": "...",
      "input": "...",
      "output": "..."
    }
    """

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    converted = []
    for item in data:
        prompt = item["instruction"]
        if item.get("input"):
            prompt += (
                "\n\n" +
                item["input"]
            )

        converted.append({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "assistant",
                    "content":
                    item["output"]
                }
            ]
        })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            converted,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Converted {len(converted)} examples"
    )
    
def convert_csv_to_messages(
    input_file,
    output_file
):

    converted = []

    with open(
        input_file,
        newline="",
        encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(
            csvfile
        )

        for row in reader:
            converted.append({
                "messages": [
                    {
                        "role": "user",
                        "content":
                        row["question"]
                    },
                    {
                        "role": "assistant",
                        "content":
                        row["answer"]
                    }
                ]
            })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            converted,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Converted {len(converted)} rows")
    
def convert_jsonl_to_messages(
    input_file,
    output_file
):
    converted = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        for line in f:
            row = json.loads(line)
            converted.append({
                "messages": [
                    {
                        "role": "user",
                        "content":
                        row["question"]
                    },
                    {
                        "role": "assistant",
                        "content":
                        row["answer"]
                    }
                ]
            })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            converted,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Converted {len(converted)} rows")
    
if __name__ == "__main__":
    convert_jsonl_to_messages(
        input_file="datasets/raw/conversations/bootstrap.jsonl",
        output_file="datasets/cleaned/filtered/filtered.json"
    )