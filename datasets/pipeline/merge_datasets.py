import json

def merge_datasets(
    input_files,
    output_file
):

    merged = []

    for file in input_files:
        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)
            merged.extend(data)

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

    print(
        f"Merged {len(merged)} examples"
    )