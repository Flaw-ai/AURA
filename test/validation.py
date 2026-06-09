from modeling.configuration_flaw import FlawConfig
from modeling.modeling_flaw import FlawForCausalLM

config = FlawConfig(
    vocab_size=32000,
    hidden_size=512,
    intermediate_size=1536,
    num_hidden_layers=8,
    num_attention_heads=8,
    num_key_value_heads=4
)

model = FlawForCausalLM(config)

print(model)
print(model.num_parameters)

#Set-Location "c:\Users\rudra\OneDrive\Documents\VS_Code\just_study\ai"
#>> $env:PYTHONPATH="."
#>> & "c:\Users\rudra\OneDrive\Documents\VS_Code\.venv\Scripts\python.exe" "test\validation.py"