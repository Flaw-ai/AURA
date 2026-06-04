from pathlib import Path
import json
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)

from datasets import Dataset
from trainers.base_trainer import (
    BaseTrainer
)

class SFTTrainer(
    BaseTrainer
):
    def __init__(
        self,
        config
    ):
        super().__init__(config)
        self.model_name = (
            config["model_name"]
        )
        self.dataset_path = (
            config["dataset_path"]
        )
        self.model = None
        self.tokenizer = None

    def load_dataset(self):
        self.logger.info(
            "Loading dataset..."
        )
        with open(
            self.dataset_path,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)
        conversations = []
        for item in data:
            text = ""
            for msg in item[
                "messages"
            ]:
                text += (
                    f"{msg['role']}: "
                    f"{msg['content']}\n"
                )
            conversations.append(
                {"text": text}
            )
        dataset = Dataset.from_list(
            conversations
        )
        self.logger.info(
            f"Loaded "
            f"{len(dataset)} samples"
        )
        return dataset

    def build_model(self):
        self.logger.info(
            "Loading model..."
        )
        self.tokenizer = (
            AutoTokenizer
            .from_pretrained(
                self.model_name
            )
        )
        self.model = (
            AutoModelForCausalLM
            .from_pretrained(
                self.model_name
            )
        )
        self.logger.info(
            "Model loaded."
        )

    def tokenize(
        self,
        dataset
    ):
        def tokenizer_fn(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=self.config.get(
                    "max_length",
                    2048
                )
            )

        return dataset.map(
            tokenizer_fn,
            batched=True
        )

    def train(self):
        dataset = (
            self.load_dataset()
        )
        self.build_model()
        tokenized_dataset = (
            self.tokenize(
                dataset
            )
        )
        args = TrainingArguments(
            output_dir=str(
                self.output_dir
            ),
            num_train_epochs=
            self.config.get(
                "epochs",
                3
            ),
            per_device_train_batch_size=
            self.config.get(
                "batch_size",
                2
            ),
            learning_rate=
            self.config.get(
                "learning_rate",
                2e-5
            ),
            logging_steps=
            self.config.get(
                "logging_steps",
                50
            ),
            save_steps=
            self.config.get(
                "save_steps",
                500
            ),
            report_to="none"
        )

        trainer = Trainer(
            model=self.model,
            args=args,
            train_dataset=
            tokenized_dataset
        )

        self.logger.info(
            "Training started..."
        )

        trainer.train()

        trainer.save_model(
            self.output_dir
        )

        self.logger.info(
            "Training complete."
        )

    def evaluate(self):
        self.logger.info(
            "Evaluation placeholder."
        )
        return {
            "status":
            "not_implemented"
        }