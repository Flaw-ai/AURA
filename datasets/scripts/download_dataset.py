from datasets import load_dataset

datasets_to_download = {
    "dolly": ("databricks/databricks-dolly-15k", None),
    "openassistant": ("OpenAssistant/oasst1", None),
    "gsm8k": ("openai/gsm8k", "main"),
    "ultrachat": ("HuggingFaceH4/ultrachat_200k", None),
}

for name, (path, config) in datasets_to_download.items():
    print(f"Downloading {name}")
    if config:
        ds = load_dataset(path, config)
    else:
        ds = load_dataset(path)
    ds.save_to_disk(f"datasets/raw/{name}")

print("Done")