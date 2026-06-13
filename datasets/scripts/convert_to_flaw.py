from datasets import load_from_disk
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT = BASE_DIR / "raw_public_datasets"
OUTPUT = "merged.jsonl"
count = 0


def write_example(prompt, answer, file):
    record = {
        "messages": [
            {
                "role": "user",
                "content": str(prompt)
            },
            {
                "role": "assistant",
                "content": str(answer)
            }
        ]
    }

    file.write(json.dumps(record, ensure_ascii=False) + "\n")


with open(OUTPUT, "w", encoding="utf-8") as out:
    print("Processing Dolly")
    dolly = load_from_disk(ROOT / "dolly")
    
    for row in dolly["train"]:
        prompt = row["instruction"]
        if row["context"]:
            prompt += "\n\n" + row["context"]
        answer = row["response"]
        write_example(prompt, answer, out)
        count += 1

    print("Processing GSM8K")
    gsm = load_from_disk(ROOT / "gsm8k")

    for split in gsm.keys():
        for row in gsm[split]:
            write_example(
                row["question"],
                row["answer"],
                out
            )
            count += 1

    print("Processing OpenAssistant")
    oasst = load_from_disk(ROOT / "openassistant")

    for split in oasst.keys():
        for row in oasst[split]:
            if (
                "text" in row
                and row["text"]
            ):
                write_example(
                    "Continue conversation",
                    row["text"],
                    out
                )
                count += 1

    print("Processing UltraChat")
    ultra = load_from_disk(ROOT / "ultrachat")

    for split in ultra.keys():
        for row in ultra[split]:
            msgs = row["messages"]
            if len(msgs) < 2:
                continue
            for i in range(len(msgs) - 1):
                if (
                    msgs[i]["role"] == "user"
                    and msgs[i + 1]["role"] == "assistant"
                ):
                    write_example(
                        msgs[i]["content"],
                        msgs[i + 1]["content"],
                        out
                    )
                    count += 1

print()
print("DONE")
print("Examples:", count)
print("Output:", OUTPUT)