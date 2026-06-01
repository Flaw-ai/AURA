import json

GOOD_PATTERNS = [
    "step-by-step",
    "because",
    "therefore",
    "example",
    "formula"
]

def score_response(text):
    score = 0
    lower = text.lower()
    for pattern in GOOD_PATTERNS:
        if pattern in lower:
            score += 1

    return score

def filter_dataset(
    input_file,
    output_file,
    min_score=2
):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    filtered = []
    for item in data:
        assistant = (
            item["messages"][1]["content"]
        )
        score = score_response(
            assistant
        )

        if score >= min_score:
            filtered.append(item)

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            filtered,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Filtered examples: {len(filtered)}"
    )