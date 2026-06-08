import torch
from modeling.modeling_flaw import (FlawConfig, FlawForCausalLM)

def test_forward():
    config = FlawConfig(
        vocab_size=32000,
        hidden_size=256,
        intermediate_size=512,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_key_value_heads=2
    )
    model = FlawForCausalLM(config)
    input_ids = torch.randint(
        0,
        config.vocab_size,
        (2, 32)
    )
    outputs = model(
        input_ids=input_ids,
        labels=input_ids
    )
    assert outputs.logits.shape == (
        2,
        32,
        config.vocab_size
    )
    assert outputs.loss is not None
    print("Forward test passed.")


if __name__ == "__main__":
    test_forward()