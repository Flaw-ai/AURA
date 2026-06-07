from __future__ import annotations
import math
from typing import List, Optional, Tuple, Union
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithPast, BaseModelOutputWithPast

class FlawRMSNorm(nn.Module):
    def __init__(self, hidden_size: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = eps
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x = x.float()
        rms = x.pow(2).mean(-1, keepdim=True)
        x = x * torch.rsqrt(rms + self.eps)
        return (self.weight * x).to(dtype)

class FlawRotaryEmbedding(nn.Module):
    def __init__(
        self,
        dim: int,
        max_position_embeddings: int = 4096,
        base: float = 10_000.0,
        device=None,
    ):
        super().__init__()
        self.dim = dim
        self.max_position_embeddings = max_position_embeddings
        self.base = base

        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2, dtype=torch.float32, device=device) / dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)
        self._build_cache(max_position_embeddings, device=device, dtype=torch.float32)

    def _build_cache(self, seq_len: int, device, dtype):
        self.max_seq_len_cached = seq_len
        t = torch.arange(seq_len, device=device, dtype=torch.float32)
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos().to(dtype), persistent=False)
        self.register_buffer("sin_cached", emb.sin().to(dtype), persistent=False)

    def forward(self, x: torch.Tensor, seq_len: int):
        if seq_len > self.max_seq_len_cached:
            self._build_cache(seq_len, device=x.device, dtype=x.dtype)
        return (
            self.cos_cached[:seq_len].to(x.dtype),
            self.sin_cached[:seq_len].to(x.dtype),
        )


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1, x2 = x[..., : x.shape[-1] // 2], x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def _apply_rope(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    position_ids: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    cos = cos[position_ids].unsqueeze(1)
    sin = sin[position_ids].unsqueeze(1)
    q_rot = q * cos + _rotate_half(q) * sin
    k_rot = k * cos + _rotate_half(k) * sin
    return q_rot, k_rot


def _repeat_kv(x: torch.Tensor, n_rep: int) -> torch.Tensor:
    if n_rep == 1:
        return x
    B, H, S, D = x.shape
    return (
        x[:, :, None, :, :]
        .expand(B, H, n_rep, S, D)
        .reshape(B, H * n_rep, S, D)
    )

class FlawAttention(nn.Module):

    def __init__(self, config: FlawConfig, layer_idx: int):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        self.num_kv_heads = config.num_key_value_heads
        self.num_kv_groups = self.num_heads // self.num_kv_heads
        self.max_pos = config.max_position_embeddings
        self.attn_dropout = config.attention_dropout
        self.scale = self.head_dim ** -0.5

        assert self.head_dim * self.num_heads == self.hidden_size, (
            "hidden_size must be divisible by num_attention_heads"
        )
        assert self.num_heads % self.num_kv_heads == 0, (
            "num_attention_heads must be divisible by num_key_value_heads"
        )

        self.q_proj = nn.Linear(self.hidden_size, self.num_heads    * self.head_dim, bias=False)
        self.k_proj = nn.Linear(self.hidden_size, self.num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(self.hidden_size, self.num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(self.hidden_size, self.hidden_size,                  bias=False)

        self.rotary_emb = FlawRotaryEmbedding(
            dim=self.head_dim,
            max_position_embeddings=self.max_pos,
            base=config.rope_theta,
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple]]:

        B, S, _ = hidden_states.shape

        q = self.q_proj(hidden_states).view(B, S, self.num_heads,    self.head_dim).transpose(1, 2)
        k = self.k_proj(hidden_states).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(hidden_states).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)

        kv_seq_len = k.shape[-2]
        if past_key_value is not None:
            kv_seq_len += past_key_value[0].shape[-2]

        cos, sin = self.rotary_emb(v, seq_len=kv_seq_len)
        q, k = _apply_rope(q, k, cos, sin, position_ids)

        if past_key_value is not None:
            k = torch.cat([past_key_value[0], k], dim=2)
            v = torch.cat([past_key_value[1], v], dim=2)

        present = (k, v) if use_cache else None

        k = _repeat_kv(k, self.num_kv_groups)
        v = _repeat_kv(v, self.num_kv_groups)

        attn = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        if attention_mask is not None:
            attn = attn + attention_mask

        attn = F.softmax(attn, dim=-1, dtype=torch.float32).to(q.dtype)
        attn = F.dropout(attn, p=self.attn_dropout, training=self.training)

        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(B, S, self.hidden_size)
        out = self.o_proj(out)

        return out, (attn if output_attentions else None), present

class FlawMLP(nn.Module):
    def __init__(self, config: FlawConfig):
        super().__init__()
        self.gate_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.up_proj   = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.down_proj = nn.Linear(config.intermediate_size, config.hidden_size, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))

class FlawDecoderLayer(nn.Module):
    def __init__(self, config: FlawConfig, layer_idx: int):
        super().__init__()
        self.self_attn            = FlawAttention(config, layer_idx)
        self.mlp                  = FlawMLP(config)
        self.input_layernorm      = FlawRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = FlawRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.hidden_dropout       = config.hidden_dropout

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        past_key_value: Optional[Tuple] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
    ) -> Tuple:
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        hidden_states, attn_weights, present = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            use_cache=use_cache,
        )
        hidden_states = F.dropout(hidden_states, p=self.hidden_dropout, training=self.training)
        hidden_states = residual + hidden_states

        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = F.dropout(hidden_states, p=self.hidden_dropout, training=self.training)
        hidden_states = residual + hidden_states

        return hidden_states, attn_weights, present

class FlawModel(PreTrainedModel):
    config_class = FlawConfig
    base_model_prefix = "model"
    supports_gradient_checkpointing = True

    def __init__(self, config: FlawConfig):
        super().__init__(config)
        self.embed_tokens = nn.Embedding(
            config.vocab_size, config.hidden_size,
            padding_idx=config.pad_token_id,
        )
        self.layers = nn.ModuleList(
            [FlawDecoderLayer(config, i) for i in range(config.num_hidden_layers)]
        )
        self.norm = FlawRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.gradient_checkpointing = False
        self.post_init()

    def _init_weights(self, module: nn.Module):
        std = self.config.initializer_range
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=std)
        if isinstance(module, nn.Linear) and module.bias is not None:
            nn.init.zeros_(module.bias)

    def _make_causal_mask(
        self,
        bsz: int,
        seq_len: int,
        device: torch.device,
        dtype: torch.dtype,
        past_kv_len: int = 0,
    ) -> torch.Tensor:
        total = seq_len + past_kv_len
        mask = torch.full((seq_len, total), torch.finfo(dtype).min, device=device)
        cond = torch.arange(total, device=device)
        mask.masked_fill_(
            cond[None, :] <= (torch.arange(seq_len, device=device) + past_kv_len)[:, None],
            0,
        )
        return mask.to(dtype).view(1, 1, seq_len, total).expand(bsz, 1, seq_len, total)

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[Tuple]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:

        use_cache = use_cache if use_cache is not None else self.config.use_cache
        output_attentions = output_attentions or False
        output_hidden_states = output_hidden_states or False
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("Supply exactly one of input_ids or inputs_embeds")
        if input_ids is not None:
            B, S = input_ids.shape
        else:
            B, S, _ = inputs_embeds.shape

        past_kv_len = past_key_values[0][0].shape[-2] if past_key_values else 0

        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(
                past_kv_len, S + past_kv_len, dtype=torch.long, device=device
            ).unsqueeze(0)

        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        causal_mask = self._make_causal_mask(
            B, S, inputs_embeds.device, inputs_embeds.dtype, past_kv_len=past_kv_len
        )

        hidden_states = inputs_embeds
        all_hidden, all_attns, next_cache = (), (), ()

        for idx, layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden += (hidden_states,)

            past_kv = past_key_values[idx] if past_key_values is not None else None

            if self.gradient_checkpointing and self.training:
                def _ckpt(*args):
                    return layer(*args, output_attentions=output_attentions, use_cache=False)
                layer_out = torch.utils.checkpoint.checkpoint(
                    _ckpt, hidden_states, causal_mask, position_ids, None
                )
            else:
                layer_out = layer(
                    hidden_states,
                    attention_mask=causal_mask,
                    position_ids=position_ids,
                    past_key_value=past_kv,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                )

            hidden_states = layer_out[0]
            if use_cache:
                next_cache += (layer_out[2],)
            if output_attentions:
                all_attns += (layer_out[1],)

        hidden_states = self.norm(hidden_states)

        if output_hidden_states:
            all_hidden += (hidden_states,)

        if not return_dict:
            return tuple(
                v for v in [hidden_states, next_cache or None, all_hidden or None, all_attns or None]
                if v is not None
            )

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache or None,
            hidden_states=all_hidden or None,
            attentions=all_attns or None,
        )

class FlawForCausalLM(PreTrainedModel):
    config_class = FlawConfig
    base_model_prefix = "model"
    _tied_weights_keys = ["lm_head.weight"]

    def __init__(self, config: FlawConfig):
        super().__init__(config)
        self.model   = FlawModel(config)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.post_init()

    def get_input_embeddings(self):  return self.model.embed_tokens
    def set_input_embeddings(self, v): self.model.embed_tokens = v
    def get_output_embeddings(self): return self.lm_head
    def set_output_embeddings(self, v): self.lm_head = v

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[Tuple]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:

        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        out = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        hidden_states = out[0] if not return_dict else out.last_hidden_state
        logits = self.lm_head(hidden_states).float()

        loss = None
        if labels is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = F.cross_entropy(
                shift_logits.view(-1, self.config.vocab_size),
                shift_labels.view(-1),
                ignore_index=-100,
            )

        if not return_dict:
            output = (logits,) + out[1:]
            return (loss,) + output if loss is not None else output

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=out.past_key_values,
            hidden_states=out.hidden_states,
            attentions=out.attentions,
        )

    def prepare_inputs_for_generation(
        self,
        input_ids,
        past_key_values=None,
        attention_mask=None,
        inputs_embeds=None,
        **kwargs,
    ):
        if past_key_values:
            input_ids = input_ids[:, -1:]

        position_ids = kwargs.get("position_ids", None)
        if attention_mask is not None and position_ids is None:
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)
            if past_key_values:
                position_ids = position_ids[:, -1:]

        if inputs_embeds is not None and past_key_values is None:
            model_inputs = {"inputs_embeds": inputs_embeds}
        else:
            model_inputs = {"input_ids": input_ids}

        model_inputs.update({
            "position_ids":  position_ids,
            "past_key_values": past_key_values,
            "use_cache":     kwargs.get("use_cache"),
            "attention_mask": attention_mask,
        })
        return model_inputs

    @staticmethod
    def _reorder_cache(past_key_values, beam_idx):
        return tuple(
            (layer[0].index_select(0, beam_idx), layer[1].index_select(0, beam_idx))
            for layer in past_key_values
        )

    @property
    def num_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    @property
    def num_trainable_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def model_size_mb(self) -> float:
        return self.num_parameters * 4 / 1024 ** 2

    def __repr__(self):
        cfg = self.config
        return (
            f"FlawForCausalLM("
            f"vocab={cfg.vocab_size}, "
            f"hidden={cfg.hidden_size}, "
            f"layers={cfg.num_hidden_layers}, "
            f"heads={cfg.num_attention_heads}q/{cfg.num_key_value_heads}kv, "
            f"params={self.num_parameters:,})"
        )
