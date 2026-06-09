import json
import hashlib

def hash_text(text):
    return hashlib.md5(
        text.encode()
    ).hexdigest()

def deduplicate_dataset(
    input_file,
    output_file
):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    seen = set()
    unique = []

    for item in data:
        combined = (
            item["messages"][0]["content"]
            +
            item["messages"][1]["content"]
        )
        hashed = hash_text(combined)
        if hashed not in seen:
            seen.add(hashed)
            unique.append(item)

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            unique,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Unique examples: {len(unique)}"
    )
    
if __name__ == "__main__":
    deduplicate_dataset(
        "datasets/cleaned/filtered/filtered.json",
        "datasets/cleaned/reasoning/reasoning.json"
    )