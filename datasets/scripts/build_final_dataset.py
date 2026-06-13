import shutil

shutil.copy(
    "raw_public_datasets/clean.jsonl",
    "cleaned/external/flaw_dataset.jsonl"
)

print("Final dataset ready")