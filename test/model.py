import torch

from modeling.modeling_flaw import (
    FlawConfig,
    FlawForCausalLM
)

config = FlawConfig(
    vocab_size=32000,
    hidden_size=512,
    intermediate_size=1536,
    num_hidden_layers=8,
    num_attention_heads=8,
    num_key_value_heads=4
)

model = FlawForCausalLM(config)

input_ids = torch.randint(
    0,
    32000,
    (2,64)
)

outputs = model(
    input_ids=input_ids
)

print(outputs.logits.shape)

#$env:PYTHONPATH="."
#& ".venv\Scripts\python.exe" "test\model.py"