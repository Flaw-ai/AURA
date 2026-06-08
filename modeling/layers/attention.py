import torch
import torch.nn as nn
import torch.nn.functional as F
from .rotary import (RotaryEmbedding, apply_rotary)

class FlawAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.hidden_size = (config.hidden_size)
        self.num_heads = (config.num_attention_heads)
        self.num_kv_heads = (config.num_key_value_heads)
        self.head_dim = (self.hidden_size // self.num_heads)
        self.num_groups = (self.num_heads // self.num_kv_heads)
        self.scale = (self.head_dim ** -0.5)
        self.q_proj = nn.Linear(
            self.hidden_size,
            self.hidden_size,
            bias=False
        )
        self.k_proj = nn.Linear(
            self.hidden_size,
            self.num_kv_heads *
            self.head_dim,
            bias=False
        )
        self.v_proj = nn.Linear(
            self.hidden_size,
            self.num_kv_heads *
            self.head_dim,
            bias=False
        )
        self.o_proj = nn.Linear(
            self.hidden_size,
            self.hidden_size,
            bias=False
        )
        self.rotary = RotaryEmbedding(
            self.head_dim
        )

    def repeat_kv(self, x):
        b, h, s, d = x.shape
        x = (
            x[:, :, None]
            .expand(
                b,
                h,
                self.num_groups,
                s,
                d
            )
            .reshape(
                b,
                h *
                self.num_groups,
                s,
                d
            )
        )

        return x

    def forward(self, hidden_states, attention_mask=None):
        bsz, seq_len, _ = (hidden_states.shape)
        q = (
            self.q_proj(
                hidden_states
            )
            .view(
                bsz,
                seq_len,
                self.num_heads,
                self.head_dim
            )
            .transpose(1, 2)
        )
        k = (
            self.k_proj(
                hidden_states
            )
            .view(
                bsz,
                seq_len,
                self.num_kv_heads,
                self.head_dim
            )
            .transpose(1, 2)
        )
        v = (
            self.v_proj(
                hidden_states
            )
            .view(
                bsz,
                seq_len,
                self.num_kv_heads,
                self.head_dim
            )
            .transpose(1, 2)
        )
        cos, sin = (self.rotary(seq_len))
        cos = ( cos.to(q.device).unsqueeze(0).unsqueeze(0))
        sin = (sin.to(q.device).unsqueeze(0).unsqueeze(0))

        q, k = apply_rotary(
            q,
            k,
            cos,
            sin
        )
        k = self.repeat_kv(k)
        v = self.repeat_kv(v)
        scores = (torch.matmul(q, k.transpose(-2, -1)) * self.scale)

        if attention_mask is not None:
            scores += attention_mask

        probs = F.softmax(
            scores,
            dim=-1
        )
        out = torch.matmul(
            probs,
            v
        )
        out = (
            out.transpose(
                1,
                2
            )
            .contiguous()
            .view(
                bsz,
                seq_len,
                self.hidden_size
            )
        )

        return self.o_proj(out)