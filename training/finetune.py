from peft import LoraConfig

def build_lora():
    config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type=
        "CAUSAL_LM"
    )
    return config


if __name__ == "__main__":
    print(
        build_lora()
    )