#!/bin/bash

set -e
echo "FLAW DATA PREPROCESSING"
echo ""
echo "[1/6] Cleaning datasets..."
python datasets/pipeline/clean_dataset.py
echo ""
echo "[2/6] Removing duplicates..."
python datasets/pipeline/deduplicate.py
echo ""
echo "[3/6] Applying quality filters..."
python datasets/pipeline/quality_filter.py
echo ""
echo "[4/6] Ranking responses..."
python datasets/pipeline/ranking_pipeline.py
echo ""
echo "[5/6] Converting dataset format..."
python datasets/pipeline/convert_format.py
echo ""
echo "[6/6] Dataset statistics..."
python datasets/pipeline/merge_datasets.py
echo ""
echo "PREPROCESSING COMPLETE"