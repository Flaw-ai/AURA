import yaml
from training.sft.training_pipeline import (SFTTrainingPipeline)

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    train_cfg = load_config("training/configs/train.yaml")
    sft_cfg = load_config("training/configs/sft.yaml")
    pipeline = SFTTrainingPipeline(train_cfg=train_cfg, sft_cfg=sft_cfg)
    pipeline.train()


if __name__ == "__main__":
    main()