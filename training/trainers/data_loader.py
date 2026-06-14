from datasets import load_dataset

class DatasetLoader:
    def __init__(self, config):
        self.config = config

    def load(self):
        dataset_path = self.config["dataset"]
        dataset = load_dataset(
            "json",
            data_files=dataset_path,
            split="train"
        )

        return dataset