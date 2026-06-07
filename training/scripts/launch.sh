#!/bin/bash

set -e
echo "FLAW TRAINING PIPELINE"
echo ""
echo "[1/5] Activating environment..."
source venv/bin/activate
echo ""
echo "[2/5] Starting SFT training..."
python training/scripts/train_sft.py
echo ""
echo "[3/5] Starting DPO training..."
python training/scripts/train_dpo.py
echo ""
echo "[4/5] Merging LoRA weights..."
python training/merge_lora.py
echo ""
echo "[5/5] Running evaluation..."
python training/scripts/evaluate.py
echo ""
echo "TRAINING COMPLETE"