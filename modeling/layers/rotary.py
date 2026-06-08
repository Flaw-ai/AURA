import torch
import torch.nn as nn

class RotaryEmbedding(nn.Module):
    def __init__(self, dim, base=10000, max_position_embeddings=4096):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float()/ dim))
        self.register_buffer(
            "inv_freq",
            inv_freq
        )
        self.max_position_embeddings = (max_position_embeddings)
        self._build_cache()

    def _build_cache(self):
        t = torch.arange(self.max_position_embeddings)
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat(
            (
                freqs,
                freqs
            ),
            dim=-1
        )
        self.register_buffer(
            "cos_cached",
            emb.cos()
        )
        self.register_buffer(
            "sin_cached",
            emb.sin()
        )

    def forward(self, seq_len):
        return (
            self.cos_cached[:seq_len],
            self.sin_cached[:seq_len]
        )


def rotate_half(x):
    x1 = x[..., :x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2:]

    return torch.cat(
        (-x2, x1),
        dim=-1
    )


def apply_rotary(q, k, cos, sin):
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)

    return (
        q_embed,
        k_embed
    )