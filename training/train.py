import yaml
from trainers.sft_trainer import SFTTrainer
from trainers.dpo_trainer import DPOTrainer
from trainers.curriculum_trainer import CurriculumTrainer


def load_config():
    with open(
        "training/configs/train.yaml",
        "r"
    ) as f:
        return yaml.safe_load(f)


def build_trainer(config):
    trainer_type = config.get(
        "trainer",
        "sft"
    )

    mapping = {
        "sft": SFTTrainer,
        "dpo": DPOTrainer,
        "curriculum": CurriculumTrainer
    }

    if trainer_type not in mapping:
        raise ValueError(f"Unknown trainer: {trainer_type}")

    return mapping[trainer_type](config)


def main():
    config = load_config()
    trainer = build_trainer(config)
    trainer.train()


if __name__ == "__main__":
    main()