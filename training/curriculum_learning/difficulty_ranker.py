from __future__ import annotations
import math
import re
from typing import Dict, List, Optional, Tuple
import numpy as np

_REASONING_PATTERNS: List[str] = [
    r"\blet'?s\b",
    r"\bstep\s*\d*\b",
    r"\bfirst(?:ly)?\b",
    r"\bsecond(?:ly)?\b",
    r"\bthird(?:ly)?\b",
    r"\btherefore\b",
    r"\bthus\b",
    r"\bhence\b",
    r"\bconsequently\b",
    r"\bbecause\b",
    r"\bsince\b",
    r"\bgiven\s+that\b",
    r"\bprove\b",
    r"\bderive\b",
    r"\bsuppose\b",
    r"\bassume\b",
    r"\bconsider\b",
    r"\banalyze\b",
    r"\bevaluate\b",
    r"\bcompare\b",
    r"\bcontrast\b",
    r"\bconclude\b",
    r"\bimplies?\b",
    r"\bit\s+follows\b",
    r"\bwe\s+can\s+see\b",
    r"\bthis\s+means\b",
    r"\bin\s+other\s+words\b",
]

_CONSTRAINT_KEYWORDS: frozenset = frozenset({
    "only", "must", "never", "always", "exactly", "no more than",
    "at least", "without", "using", "in the style of", "do not",
    "avoid", "ensure", "require", "limit", "strictly", "exclusively",
    "forbidden", "mandatory", "prohibited", "constraint", "rule",
    "format", "structure", "schema", "json", "xml", "yaml",
})

_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)

_STAGE_BINS: Dict[str, Tuple[float, float]] = {
    "warmup": (0.00, 0.20),
    "easy":   (0.20, 0.40),
    "medium": (0.40, 0.62),
    "hard":   (0.62, 0.82),
    "exam":   (0.82, 1.01),
}

_WEIGHTS: Dict[str, float] = {
    "length":      0.25,
    "vocab":       0.15,
    "reasoning":   0.25,
    "code":        0.15,
    "turns":       0.10,
    "constraints": 0.10,
}

assert abs(sum(_WEIGHTS.values()) - 1.0) < 1e-9, "Weights must sum to 1.0"

class DifficultyRanker:
    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        stage_bins: Optional[Dict[str, Tuple[float, float]]] = None,
    ):
        self.weights    = weights    or _WEIGHTS
        self.stage_bins = stage_bins or _STAGE_BINS

        self._reasoning_re: List[re.Pattern] = [
            re.compile(p, re.IGNORECASE) for p in _REASONING_PATTERNS
        ]

    def _signal_length(self, text: str) -> float:
        n = len(text.split())
        return float(1.0 - math.exp(-n / 400.0))

    def _signal_vocab(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text.lower())
        if len(words) < 10:
            return 0.0
        ttr = len(set(words)) / len(words)
        return float(np.clip((ttr - 0.30) / 0.60, 0.0, 1.0))

    def _signal_reasoning(self, text: str) -> float:
        sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
        if not sentences:
            return 0.0
        hits = sum(
            1 for s in sentences
            if any(p.search(s) for p in self._reasoning_re)
        )
        return float(np.clip(hits / len(sentences) * 2.0, 0.0, 1.0))

    def _signal_code(self, text: str) -> float:
        blocks = _CODE_BLOCK_RE.findall(text)
        if not blocks:
            return 0.0
        total_lines = sum(len(b.split("\n")) for b in blocks)
        return float(1.0 - math.exp(-total_lines / 35.0))

    def _signal_turns(self, messages: List[Dict]) -> float:
        n = max(len(messages) - 1, 0)
        return float(1.0 - math.exp(-n / 7.0))

    def _signal_constraints(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        hits = sum(1 for w in words if w in _CONSTRAINT_KEYWORDS)
        return float(np.clip(hits / max(len(words), 1) * 15.0, 0.0, 1.0))

    def _extract_texts(self, sample: Dict) -> Tuple[str, str, str]:
        messages = sample.get("messages", [])
        asst = " ".join(
            m.get("content", "") for m in messages if m.get("role") == "assistant"
        )
        user = " ".join(
            m.get("content", "") for m in messages if m.get("role") == "user"
        )
        full = " ".join(m.get("content", "") for m in messages)
        return asst, user, full

    def _compute_signals(self, sample: Dict) -> Dict[str, float]:
        messages = sample.get("messages", [])
        asst, user, full = self._extract_texts(sample)
        return {
            "length":      self._signal_length(asst),
            "vocab":       self._signal_vocab(asst),
            "reasoning":   self._signal_reasoning(full),
            "code":        self._signal_code(full),
            "turns":       self._signal_turns(messages),
            "constraints": self._signal_constraints(user),
        }

    def score(self, sample: Dict) -> float:
        signals = self._compute_signals(sample)
        raw = sum(self.weights[k] * v for k, v in signals.items())
        return round(float(np.clip(raw, 0.0, 1.0)), 4)

    def classify(self, sample: Dict) -> str:
        s = self.score(sample)
        for stage, (lo, hi) in self.stage_bins.items():
            if lo <= s < hi:
                return stage
        return "exam"

    def score_batch(self, samples: List[Dict]) -> List[float]:
        return [self.score(s) for s in samples]

    def classify_batch(self, samples: List[Dict]) -> List[str]:
        return [self.classify(s) for s in samples]

    def signal_breakdown(self, sample: Dict) -> Dict:
        """
        Returns full per-signal diagnostics — useful for debugging
        why a sample was assigned to a particular stage.

        Example output::

            {
              "stage": "medium",
              "total_score": 0.4821,
              "raw_signals": {"length": 0.72, "vocab": 0.44, ...},
              "weighted":    {"length": 0.18, "vocab": 0.07, ...},
            }
        """
        signals = self._compute_signals(sample)
        weighted = {k: round(self.weights[k] * v, 4) for k, v in signals.items()}
        total = round(sum(weighted.values()), 4)

        return {
            "stage":        self.classify(sample),
            "total_score":  total,
            "raw_signals":  {k: round(v, 4) for k, v in signals.items()},
            "weighted":     weighted,
        }

    def dataset_stats(self, samples: List[Dict]) -> Dict:
        scores = np.array(self.score_batch(samples))
        stages = self.classify_batch(samples)

        distribution: Dict[str, int] = {s: 0 for s in self.stage_bins}
        for stage in stages:
            distribution[stage] = distribution.get(stage, 0) + 1

        all_signals: Dict[str, List[float]] = {k: [] for k in self.weights}
        for sample in samples:
            s = self._compute_signals(sample)
            for k, v in s.items():
                all_signals[k].append(v)

        mean_signals = {k: round(float(np.mean(v)), 4) for k, v in all_signals.items()}

        return {
            "n_samples": len(samples),
            "distribution": distribution,
            "score_percentiles": {
                "p10":  round(float(np.percentile(scores, 10)),  4),
                "p25":  round(float(np.percentile(scores, 25)),  4),
                "p50":  round(float(np.percentile(scores, 50)),  4),
                "p75":  round(float(np.percentile(scores, 75)),  4),
                "p90":  round(float(np.percentile(scores, 90)),  4),
                "mean": round(float(scores.mean()),               4),
                "std":  round(float(scores.std()),                4),
            },
            "mean_signals": mean_signals,
        }

    def reweight(self, **kwargs: float) -> "DifficultyRanker":
        new_weights = {**self.weights, **kwargs}
        total = sum(new_weights.values())
        normalised = {k: v / total for k, v in new_weights.items()}
        return DifficultyRanker(weights=normalised, stage_bins=self.stage_bins)

    def __repr__(self) -> str:
        w = ", ".join(f"{k}={v}" for k, v in self.weights.items())
        return f"DifficultyRanker(weights=[{w}])"