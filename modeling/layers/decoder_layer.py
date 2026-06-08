import torch
import torch.nn as nn
import torch.nn.functional as F
from .attention import FlawAttention
from .mlp import FlawMLP
from .rmsnorm import RMSNorm

class FlawDecoderLayer(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.layer_idx = layer_idx
        self.self_attn = FlawAttention(config)
        self.mlp = FlawMLP(config)
        self.input_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps
        )
        self.post_attention_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps
        )
        self.hidden_dropout = getattr(
            config,
            "hidden_dropout",
            0.0
        )

    def forward(self, hidden_states, attention_mask=None, output_attentions=False):
        residual = hidden_states
        hidden_states = (self.input_layernorm(hidden_states))
        attn_output = (self.self_attn(
                hidden_states,
                attention_mask
            )
        )
        attn_output = F.dropout(
            attn_output,
            p=self.hidden_dropout,
            training=self.training
        )
        hidden_states = (residual + attn_output)

        residual = hidden_states
        hidden_states = (self.post_attention_layernorm(hidden_states))
        mlp_output = self.mlp(hidden_states)
        mlp_output = F.dropout(
            mlp_output,
            p=self.hidden_dropout,
            training=self.training
        )
        hidden_states = (residual + mlp_output)

        outputs = (hidden_states)

        if output_attentions:
            outputs += (None)

        return outputs