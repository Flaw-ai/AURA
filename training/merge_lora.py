from peft import (PeftModel)
from transformers import (AutoModelForCausalLM)


def merge_models(
    base_model,
    adapter_path,
    output_path
):
    model = (
        AutoModelForCausalLM
        .from_pretrained(
            base_model
        )
    )

    model = PeftModel
    .from_pretrained(
        model,
        adapter_path
    )

    merged = (
        model.merge_and_unload()
    )

    merged.save_pretrained(
        output_path
    )


if __name__ == "__main__":
    print(
        "Merge utility ready"
    )