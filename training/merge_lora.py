import os
import json
import argparse
from peft import PeftModel
from modeling_flaw import (FlawConfig, FlawForCausalLM)

class FlawLoRAMerger:
    def __init__(self, config_path, adapter_path, output_path):
        self.config_path = config_path
        self.adapter_path = adapter_path
        self.output_path = output_path

    def load_config(self):
        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as f:
            config_dict = json.load(f)

        return FlawConfig(**config_dict)

    def build_model(self):
        config = self.load_config()
        model = FlawForCausalLM(config)
        return model

    def load_adapter(self, model):
        if not os.path.exists(
            self.adapter_path
        ):
            raise FileNotFoundError(f"Adapter not found: {self.adapter_path}")

        return PeftModel.from_pretrained(model, self.adapter_path)

    def print_stats(self, model):
        total = sum(
            p.numel()
            for p in model.parameters()
        )
        trainable = sum(
            p.numel()
            for p in model.parameters()
            if p.requires_grad
        )

        print("\nCRAZZZY STATS")
        print(f"Total Parameters     : {total:,}")
        print(f"Trainable Parameters : {trainable:,}")

    def merge(self):
        print("\nLoading FLAW model...")
        model = self.build_model()
        self.print_stats(model)

        print("Loading LoRA adapter...")
        model = self.load_adapter(model)

        print("Merging adapter...")
        merged_model = (model.merge_and_unload())
        os.makedirs(
            self.output_path,
            exist_ok=True
        )
        
        print("Saving merged model...")
    
        merged_model.save_pretrained(self.output_path)
        
        print(f"\nMerged model saved to:\n{self.output_path}")
        
        return merged_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        required=True
    )
    parser.add_argument(
        "--adapter",
        type=str,
        required=True
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True
    )

    return parser.parse_args()


def main():
    args = parse_args()
    merger = FlawLoRAMerger(
        config_path=args.config,
        adapter_path=args.adapter,
        output_path=args.output
    )
    merger.merge()


if __name__ == "__main__":
    main()