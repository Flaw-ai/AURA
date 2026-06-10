from pathlib import Path
import json
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from modeling.modeling_flaw import (
    FlawConfig,
    FlawForCausalLM
)
from trainers.base_trainer import (
    BaseTrainer
)

class SFTTrainer(BaseTrainer):
    def __init__(self, config):
        super().__init__(config)
        self.dataset_path = config["dataset_path"]
        self.config_path = config["config_path"]
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

            for msg in item["messages"]:
                role = msg["role"]
                content = msg["content"]
                text += (
                    f"<|{role}|>\n"
                    f"{content}\n"
                )
            conversations.append(
                {"text": text}
            )

        dataset = Dataset.from_list(conversations)
        self.logger.info(f"Loaded {len(dataset)} samples")
        return dataset

    def build_model(self):
        self.logger.info(
            "Building Flaw model..."
        )
        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as f:
            cfg = json.load(f)

        flaw_config = FlawConfig(
            **cfg
        )
        self.model = (
            FlawForCausalLM(flaw_config)
        )
        self.tokenizer = (
            AutoTokenizer.from_pretrained("models/flaw")
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = (self.tokenizer.eos_token)

        self.logger.info(
            f"Parameters: "
            f"{self.model.num_parameters:,}"
        )

    def tokenize(self, dataset):
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
            batched=True,
            remove_columns=["text"]
        )

    def build_collator(self):
        return (
            DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            )
        )

    def train(self):
        dataset = (self.load_dataset())
        self.build_model()
        tokenized_dataset = (
            self.tokenize(dataset)
        )

        training_args = (
            TrainingArguments(
                output_dir=str(
                    self.output_dir
                ),
                num_train_epochs=
                self.config.get(
                    "epochs",
                    5
                ),
                per_device_train_batch_size=
                self.config.get(
                    "batch_size",
                    8
                ),
                gradient_accumulation_steps=
                self.config.get(
                    "gradient_accumulation_steps",
                    4
                ),
                learning_rate=float(
                    self.config.get(
                        "learning_rate",
                        3e-4
                    )
                ),
                weight_decay=float(
                    self.config.get(
                        "weight_decay",
                        0.1
                    )
                ),
                warmup_ratio=float(
                    self.config.get(
                        "warmup_ratio",
                        0.05
                    )
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
                eval_strategy="no",
                bf16=self.config.get(
                    "mixed_precision",
                    "bf16"
                ) == "bf16",
                gradient_checkpointing=
                self.config.get(
                    "gradient_checkpointing",
                    True
                ),
                report_to="none"
            )
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=
            self.build_collator()
        )
        self.logger.info("Training started...")
        trainer.train()
        trainer.save_model(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        self.logger.info("Training complete.")

    def evaluate(self):
        return {"status": "not_implemented"}