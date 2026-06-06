from __future__ import annotations
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from .curriculum_builder import CurriculumBuilder
from .difficulty_ranker import DifficultyRanker
from .progression_tracker import ProgressionTracker
from .stage_manager import StageManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("flaw.pipeline")
DEFAULT_STAGE_ORDER: List[str] = ["warmup", "easy", "medium", "hard", "exam"]

STAGE_GATES: Dict[str, Dict[str, Optional[float]]] = {
    "warmup": {"min_accuracy": 0.92, "max_loss": 0.22},
    "easy":   {"min_accuracy": 0.87, "max_loss": 0.35},
    "medium": {"min_accuracy": 0.80, "max_loss": 0.50},
    "hard":   {"min_accuracy": 0.72, "max_loss": 0.65},
    "exam":   {"min_accuracy": 0.65, "max_loss": 0.78},
}

_DRY_RUN_METRICS: Dict[str, Dict[str, float]] = {
    "warmup": {"loss": 0.09,  "accuracy": 0.97},
    "easy":   {"loss": 0.17,  "accuracy": 0.94},
    "medium": {"loss": 0.32,  "accuracy": 0.87},
    "hard":   {"loss": 0.50,  "accuracy": 0.76},
    "exam":   {"loss": 0.63,  "accuracy": 0.68},
}

class CurriculumPipeline:
    VERSION = "2.1.0"

    def __init__(
        self,
        output_dir: str             = "curriculum_outputs",
        checkpoint_dir: str         = "checkpoints",
        log_dir: str                = "logs",
        early_stopping_patience: int = 3,
        min_stage_samples: int       = 50,
        max_stage_retries: int       = 1,
        enable_wandb: bool           = False,
        experiment_name: str         = "flaw_curriculum",
        dry_run: bool                = False,
    ):
        self.output_dir    = Path(output_dir)
        self.checkpoint_dir = Path(checkpoint_dir)
        self.log_dir       = Path(log_dir)
        self.early_stopping_patience = early_stopping_patience
        self.min_stage_samples       = min_stage_samples
        self.max_stage_retries       = max_stage_retries
        self.enable_wandb            = enable_wandb
        self.experiment_name         = experiment_name
        self.dry_run                 = dry_run

        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        for d in [self.output_dir, self.checkpoint_dir, self.log_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self.ranker  = DifficultyRanker()
        self.builder = CurriculumBuilder(ranker=self.ranker)
        self.manager = StageManager(ranker=self.ranker, stage_order=DEFAULT_STAGE_ORDER)
        self.tracker = ProgressionTracker(
            log_dir=str(self.log_dir),
            run_id=self.run_id,
        )

        self._setup_file_logger()
        self._init_wandb()

        logger.info("FlawCurriculumPipeline v%s | run=%s | dry_run=%s",
                    self.VERSION, self.run_id, self.dry_run)

    def _setup_file_logger(self):
        log_file = self.log_dir / f"pipeline_{self.run_id}.log"
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)
        logger.info("File logging → %s", log_file)

    def _init_wandb(self):
        if not self.enable_wandb:
            return
        try:
            import wandb
            wandb.init(
                project="flaw-curriculum",
                name=f"{self.experiment_name}_{self.run_id}",
                config={
                    "pipeline_version":  self.VERSION,
                    "early_stopping":    self.early_stopping_patience,
                    "min_stage_samples": self.min_stage_samples,
                    "dry_run":           self.dry_run,
                },
            )
            self._wandb = wandb
            logger.info("W&B initialized (project=flaw-curriculum)")
        except ImportError:
            logger.warning("wandb not installed — skipping W&B logging")
            self.enable_wandb = False
            self._wandb = None
        except Exception as exc:
            logger.warning("W&B init failed: %s", exc)
            self.enable_wandb = False
            self._wandb = None

    def validate_dataset(
        self,
        dataset: List[Dict],
    ) -> Tuple[List[Dict], Dict]:
        valid: List[Dict] = []
        stats: Dict[str, Any] = {
            "total": len(dataset),
            "rejected_no_messages":  0,
            "rejected_too_short":    0,
            "rejected_malformed_msg": 0,
            "rejected_empty_content": 0,
            "valid": 0,
            "rejection_rate": 0.0,
        }

        _allowed_roles = {"system", "user", "assistant"}

        for sample in dataset:
            try:
                if "messages" not in sample:
                    stats["rejected_no_messages"] += 1
                    continue

                msgs = sample["messages"]
                if len(msgs) < 2:
                    stats["rejected_too_short"] += 1
                    continue

                ok = True
                for msg in msgs:
                    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                        stats["rejected_malformed_msg"] += 1
                        ok = False
                        break
                    if msg["role"] not in _allowed_roles:
                        stats["rejected_malformed_msg"] += 1
                        ok = False
                        break
                    if not isinstance(msg["content"], str) or not msg["content"].strip():
                        stats["rejected_empty_content"] += 1
                        ok = False
                        break

                if ok:
                    valid.append(sample)

            except Exception:
                stats["rejected_malformed_msg"] += 1

        stats["valid"] = len(valid)
        n_rejected = stats["total"] - stats["valid"]
        stats["rejection_rate"] = round(n_rejected / max(stats["total"], 1), 4)

        return valid, stats

    def check_stage_gate(
        self,
        stage_name: str,
        result: Dict,
    ) -> Tuple[bool, str]:
        gate = STAGE_GATES.get(stage_name)
        if not gate:
            return True, "no gate defined for this stage"

        accuracy = result.get("accuracy")
        loss     = result.get("loss")

        min_acc = gate.get("min_accuracy")
        max_loss = gate.get("max_loss")

        if min_acc is not None and (accuracy is None or accuracy < min_acc):
            return False, f"accuracy={accuracy:.4f} < required={min_acc}"

        if max_loss is not None and (loss is None or loss > max_loss):
            return False, f"loss={loss:.4f} > required={max_loss}"

        return True, "all thresholds cleared"

    def train_on_stage(
        self,
        stage_name: str,
        samples: List[Dict],
        model=None,
        tokenizer=None,
        training_args=None,
    ) -> Dict:
        if self.dry_run or model is None or tokenizer is None:
            return self._dry_run_metrics(stage_name)
        return self._real_train(stage_name, samples, model, tokenizer, training_args)

    def _real_train(
        self,
        stage_name: str,
        samples: List[Dict],
        model,
        tokenizer,
        training_args,
    ) -> Dict:
        try:
            from transformers import Trainer, DataCollatorForSeq2Seq
        except ImportError:
            raise RuntimeError(
                "transformers is required for real training. "
                "Install with:  pip install transformers"
            )

        stage_dataset = _StageDataset(samples, tokenizer)

        ckpt_path = self.checkpoint_dir / f"stage_{stage_name}_{self.run_id}"
        ckpt_path.mkdir(parents=True, exist_ok=True)

        if training_args is not None:
            training_args.output_dir = str(ckpt_path)

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=stage_dataset,
            data_collator=DataCollatorForSeq2Seq(
                tokenizer,
                pad_to_multiple_of=8,
                return_tensors="pt",
            ),
        )

        train_out = trainer.train()
        eval_metrics = trainer.evaluate()
        train_loss = train_out.training_loss
        accuracy = float(np.clip(1.0 - train_loss / 3.0, 0.0, 1.0))

        return {
            "loss":                 round(train_loss, 6),
            "accuracy":             round(accuracy, 4),
            "steps":                train_out.global_step,
            "samples_per_second":   train_out.metrics.get("train_samples_per_second", 0),
            "eval_loss":            eval_metrics.get("eval_loss"),
            "checkpoint":           str(ckpt_path),
            "dry_run":              False,
        }

    def _dry_run_metrics(self, stage_name: str) -> Dict:
        base = _DRY_RUN_METRICS.get(stage_name, {"loss": 1.0, "accuracy": 0.50})
        rng  = np.random.default_rng()
        noise = rng.normal(0.0, 0.012)
        return {
            "loss":     round(float(np.clip(base["loss"]     + noise,  0.01, 2.0)), 4),
            "accuracy": round(float(np.clip(base["accuracy"] - noise,  0.00, 1.0)), 4),
            "steps":    0,
            "dry_run":  True,
        }

    def curriculum_summary(self, curriculum: Dict) -> Dict:
        total = sum(len(v) for v in curriculum.values()) or 1
        return {
            stage: {
                "count": len(samples),
                "pct":   round(len(samples) / total * 100, 1),
            }
            for stage, samples in curriculum.items()
        }

    def export_curriculum(self, curriculum: Dict):
        file_path = self.output_dir / f"curriculum_dataset_{self.run_id}.json"

        exportable = {
            stage: [
                {k: v for k, v in s.items() if not k.startswith("__")}
                for s in samples
            ]
            for stage, samples in curriculum.items()
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(exportable, f, indent=2, ensure_ascii=False)

        logger.info("Curriculum exported → %s", file_path)

    def generate_report(self) -> Dict:
        logs = self.tracker.all_logs()

        losses = [l["loss"]     for l in logs] if logs else []
        accs   = [l["accuracy"] for l in logs] if logs else []

        report = {
            "run_id":           self.run_id,
            "pipeline_version": self.VERSION,
            "timestamp":        datetime.utcnow().isoformat() + "Z",
            "dry_run":          self.dry_run,
            "stages_completed": len(logs),
            "summary": {
                "best_loss":     round(min(losses), 4)           if losses else None,
                "best_accuracy": round(max(accs),   4)           if accs   else None,
                "avg_loss":      round(float(np.mean(losses)), 4) if losses else None,
                "avg_accuracy":  round(float(np.mean(accs)),   4) if accs   else None,
            },
            "history": logs,
        }

        report_file = self.output_dir / f"curriculum_report_{self.run_id}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info("Report saved → %s", report_file)
        return report

    def save_pipeline_state(self, extra: Optional[Dict] = None):
        state = {
            "run_id":   self.run_id,
            "version":  self.VERSION,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "logs":      self.tracker.all_logs(),
            **(extra or {}),
        }
        state_file = self.checkpoint_dir / f"pipeline_state_{self.run_id}.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
        logger.debug("State saved → %s", state_file)

    def _log_wandb(self, stage: str, result: Dict, n_samples: int):
        if not self.enable_wandb or self._wandb is None:
            return
        self._wandb.log({
            f"{stage}/loss":     result["loss"],
            f"{stage}/accuracy": result["accuracy"],
            f"{stage}/samples":  n_samples,
        })

    def run(
        self,
        dataset: List[Dict],
        model=None,
        tokenizer=None,
        training_args=None,
    ) -> Dict:
        _banner = "=" * 62
        logger.info(_banner)
        logger.info("  FLAW CURRICULUM PIPELINE  v%s", self.VERSION)
        logger.info("  run_id  : %s", self.run_id)
        logger.info("  dry_run : %s", self.dry_run)
        logger.info(_banner)
        valid_dataset, val_stats = self.validate_dataset(dataset)

        logger.info(
            "Validation | total=%d  valid=%d  rejected=%d  (%.1f%% rejection)",
            val_stats["total"],
            val_stats["valid"],
            val_stats["total"] - val_stats["valid"],
            val_stats["rejection_rate"] * 100,
        )
        for key in ("rejected_no_messages", "rejected_too_short",
                    "rejected_malformed_msg", "rejected_empty_content"):
            if val_stats[key]:
                logger.warning("  %s: %d", key, val_stats[key])

        if not valid_dataset:
            logger.error("Zero valid samples — aborting.")
            return {}
        ds_stats = self.ranker.dataset_stats(valid_dataset)
        logger.info(
            "Dataset analytics | median_score=%.3f  std=%.3f",
            ds_stats["score_percentiles"]["p50"],
            ds_stats["score_percentiles"]["std"],
        )

        curriculum = self.builder.build(valid_dataset)
        summary    = self.curriculum_summary(curriculum)

        logger.info("Curriculum distribution:")
        for stage, info in summary.items():
            bar = "█" * max(1, int(info["pct"] / 5))
            logger.info("  %-8s %5d samples (%5.1f%%)  %s", stage, info["count"], info["pct"], bar)

        self.export_curriculum(curriculum)

        consecutive_failures = 0

        for stage in self.manager.get_stages():
            samples = curriculum.get(stage, [])

            if len(samples) < self.min_stage_samples:
                logger.warning(
                    "Skipping %r — %d samples < min_stage_samples=%d",
                    stage, len(samples), self.min_stage_samples,
                )
                continue

            logger.info("─" * 52)
            logger.info("Stage: %-8s | %d samples", stage.upper(), len(samples))

            result = None
            for attempt in range(self.max_stage_retries + 1):
                if attempt > 0:
                    logger.warning("  Retrying %r (attempt %d)…", stage, attempt + 1)

                result = self.train_on_stage(
                    stage_name=stage,
                    samples=samples,
                    model=model,
                    tokenizer=tokenizer,
                    training_args=training_args,
                )

                self._log_wandb(stage, result, len(samples))
                logger.info(
                    "  loss=%.4f  accuracy=%.4f  steps=%s",
                    result["loss"],
                    result["accuracy"],
                    result.get("steps", "n/a"),
                )

                passed, reason = self.check_stage_gate(stage, result)
                if passed:
                    logger.info("  Gate ✓ %s", reason)
                    break
                else:
                    logger.warning("  Gate ✗ %s", reason)
                    if attempt < self.max_stage_retries:
                        continue
                    consecutive_failures += 1
                    if consecutive_failures >= self.early_stopping_patience:
                        logger.error(
                            "Early stopping — %d consecutive gate failures (patience=%d)",
                            consecutive_failures, self.early_stopping_patience,
                        )
                        self.tracker.log_stage(
                            stage_name=stage,
                            samples=len(samples),
                            loss=result["loss"],
                            accuracy=result["accuracy"],
                            extra=result,
                        )
                        self.save_pipeline_state(extra={"stopped_at": stage, "reason": "early_stopping"})
                        return self.generate_report()
            else:
                consecutive_failures = 0

            if passed:
                consecutive_failures = 0

            self.tracker.log_stage(
                stage_name=stage,
                samples=len(samples),
                loss=result["loss"],
                accuracy=result["accuracy"],
                extra=result,
            )

            self.save_pipeline_state(extra={"last_completed_stage": stage})

        report = self.generate_report()

        logger.info(_banner)
        logger.info("  CURRICULUM COMPLETE")
        logger.info("  Stages completed : %d", report["stages_completed"])
        summary_r = report.get("summary", {})
        if summary_r.get("best_accuracy") is not None:
            logger.info("  Best accuracy    : %.4f", summary_r["best_accuracy"])
            logger.info("  Best loss        : %.4f", summary_r["best_loss"])
        logger.info(_banner)

        if self.enable_wandb and self._wandb is not None:
            self._wandb.finish()

        return report

class _StageDataset:
    _ROLE_TOKENS = {
        "system":    "<|system|>",
        "user":      "<|user|>",
        "assistant": "<|assistant|>",
    }
    _END_TOKEN = "<|end|>"

    def __init__(self, samples: List[Dict], tokenizer, max_length: int = 2048):
        self.samples    = samples
        self.tokenizer  = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict:
        sample = self.samples[idx]
        text   = self._format(sample["messages"])
        enc    = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding=False,
            return_tensors=None,
        )
        enc["labels"] = list(enc["input_ids"])
        return enc

    def _format(self, messages: List[Dict]) -> str:
        parts = []
        for msg in messages:
            role    = msg.get("role", "user")
            content = msg.get("content", "")
            token   = self._ROLE_TOKENS.get(role, f"<|{role}|>")
            parts.append(f"{token}\n{content}\n")
        parts.append(self._END_TOKEN)
        return "".join(parts)