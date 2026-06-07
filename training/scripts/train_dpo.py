import yaml
from training.dpo.dpo_pipeline import (DPOPipeline)

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config("training/configs/dpo.yaml")
    pipeline = DPOPipeline(dataset_path=cfg.get("dataset_path"," datasets/dpo.json"))
    pipeline.run()


if __name__ == "__main__":
    main()