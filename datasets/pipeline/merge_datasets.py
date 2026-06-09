import json
from pathlib import Path


def load_file(path):

    path = Path(path)

    if not path.exists():
        print(f"Skipping missing file: {path}")
        return []

    if path.suffix == ".jsonl":

        data = []

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                line = line.strip()

                if line:
                    data.append(
                        json.loads(line)
                    )

        return data

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def deduplicate(dataset):

    seen = set()

    unique = []

    for item in dataset:

        key = json.dumps(
            item,
            sort_keys=True,
            ensure_ascii=False
        )

        if key not in seen:

            seen.add(key)

            unique.append(item)

    return unique


def merge_datasets(
    input_files,
    output_file
):

    merged = []

    for file in input_files:

        data = load_file(file)

        print(
            f"Loaded {len(data)} examples from {file}"
        )

        merged.extend(data)

    before = len(merged)

    merged = deduplicate(merged)

    after = len(merged)

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
            merged,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("=" * 60)
    print(f"Before deduplication : {before}")
    print(f"After deduplication  : {after}")
    print(f"Saved dataset        : {output_file}")
    print("=" * 60)


if __name__ == "__main__":

    input_files = [

        # cleaned datasets
        "datasets/cleaned/filtered/filtered.json",

        "datasets/cleaned/reasoning/reasoning.json",

        "datasets/cleaned/exam_qa/exam_qa.json",

        # synthetic data
        "datasets/synthetic/generated/flaw_dataset.jsonl"
    ]

    output_file = (
        "datasets/cleaned/tutoring/train.json"
    )

    merge_datasets(
        input_files,
        output_file
    )