import json


def rank_response(
    educational_score,
    clarity_score,
    safety_score
):
    return round(
        educational_score * 0.5 +
        clarity_score * 0.3 +
        safety_score * 0.2,
        2
    )


def rank_dataset(
    input_file,
    output_file
):
    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    ranked = []

    for item in data:

        response = (
            item["messages"][1]["content"]
        )

        educational = 1.0
        clarity = 1.0
        safety = 1.0

        score = rank_response(
            educational,
            clarity,
            safety
        )

        item["rank_score"] = score

        ranked.append(item)

    ranked.sort(
        key=lambda x:
        x["rank_score"],
        reverse=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            ranked,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Ranked {len(ranked)} examples"
    )


if __name__ == "__main__":
    rank_dataset(
        "datasets/cleaned/filtered/filtered.json",
        "datasets/cleaned/ranked/ranked.json"
    )