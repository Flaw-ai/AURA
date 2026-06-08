import torch
from modeling.modeling_flaw import (FlawConfig)
from modeling.layers.attention import (FlawAttention)

def test_attention():
    config = FlawConfig(
        hidden_size=256,
        num_attention_heads=8,
        num_key_value_heads=4
    )
    attention = FlawAttention(config)
    hidden_states = torch.randn(
        2,
        64,
        256
    )
    output = attention(hidden_states)
    assert output.shape == (
        2,
        64,
        256
    )
    print("Attention test passed.")


if __name__ == "__main__":
    test_attention()