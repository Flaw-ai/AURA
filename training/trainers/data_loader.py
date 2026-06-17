from datasets import load_dataset

def load_dataset(self):
    self.logger.info("Loading dataset...")
    dataset = load_dataset(
        "json",
        data_files=str(self.dataset_path),
        split="train"
    )

    self.logger.info(f"Loaded {len(dataset)} samples")
    return dataset