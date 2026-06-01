import json
import re

MIN_LENGTH = 20

def clean_text(text):
    text = text.strip()
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    text = re.sub(
        r"http\S+",
        "",
        text
    )
    return text

def is_valid(example):
    if len(example) < MIN_LENGTH:
        return False
    banned_patterns = [
        "lorem ipsum",
        "click here",
        "subscribe"
    ]
    lower = example.lower()
    for pattern in banned_patterns:
        if pattern in lower:
            return False
    return True

def clean_dataset(
    input_file,
    output_file
):
    cleaned = []
    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    for item in data:
        user = clean_text(
            item["messages"][0]["content"]
        )
        assistant = clean_text(
            item["messages"][1]["content"]
        )
        if (
            is_valid(user)
            and
            is_valid(assistant)
        ):
            cleaned.append({
                "messages": [
                    {
                        "role": "user",
                        "content": user
                    },
                    {
                        "role": "assistant",
                        "content": assistant
                    }
                ]
            })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Saved {len(cleaned)} examples"
    )