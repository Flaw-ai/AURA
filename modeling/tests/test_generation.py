import torch
from modeling.modeling_flaw import (FlawConfig, FlawForCausalLM)
from modeling.generation_flaw import (FlawGenerator)

class DummyTokenizer:
    def __call__(self, text, return_tensors="pt"):
        return {
            "input_ids":
            torch.randint(
                0,
                100,
                (1, 16)
            )
        }

    def decode(self, ids, skip_special_tokens=True):
        return "Test response."


def test_generation():
    config = FlawConfig(
        vocab_size=32000,
        hidden_size=256,
        intermediate_size=512,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_key_value_heads=2
    )

    model = FlawForCausalLM(config)
    tokenizer = DummyTokenizer()
    generator = FlawGenerator(
        model,
        tokenizer
    )
    result = generator.generate("What is AI?")
    print(result)
    assert isinstance(result, str)
    print("Generation test passed.")

if __name__ == "__main__":
    test_generation()