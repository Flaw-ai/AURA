import yaml
from trainers.sft_trainer import (SFTTrainer)
from trainers.dpo_trainer import (DPOTrainer)
from trainers.curriculum_trainer import (CurriculumTrainer)

def main():
    with open(
        "configs/train.yaml",
        "r"
    ) as f:
        config = yaml.safe_load(f)

    trainer_type = config.get(
        "trainer",
        "sft"
    )

    if trainer_type == "sft":
        trainer = SFTTrainer(
            config
        )

    elif trainer_type == "dpo":
        trainer = DPOTrainer(
            config
        )

    elif trainer_type == "curriculum":
        trainer = CurriculumTrainer(
            config
        )

    else:
        raise ValueError(
            "Unknown trainer"
        )
    trainer.train()

if __name__ == "__main__":
    main()