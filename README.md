# SNU AI Challenge 2026

This repository contains my experiments for the SNU AI Challenge 2026.

## Task

Given a sentence and 4 shuffled video frames, the goal is to predict the correct chronological order of the images.

Each sample contains:

- one sentence describing an event
- four shuffled image frames
- the target ordering for training data

The final output is a `submission.csv` file for Kaggle.

## Current Approaches

### 1. CLIP baseline

The initial baseline uses a CLIP image/text encoder and trains a 24-class ordering classifier.

- CLIP image/text encoder
- 24 possible image order classes
- Validation split from `train.csv`
- Submission generation for Kaggle

### 2. Qwen3-VL prompt-based inference

The second approach uses a vision-language model to directly infer the chronological order from the sentence and four images.

- Model: `Qwen/Qwen3-VL-4B-Instruct`
- Prompt-based inference without fine-tuning
- The model receives 4 labeled frames and the sentence
- The predicted chronological order is converted into the competition submission format
- Submission files are saved under `outputs/`

## Current Results

| Date | Model | Method | Valid Accuracy | Validation Loss | Notes |
|---|---|---|---:|---:|---|
| 2026-07-17 | CLIP-ViT-B-32 | 24-class ordering classifier | 0.05125 | 3.13687 | Initial baseline result |
| 2026-07-20 | Qwen3-VL-4B-Instruct | Enhanced prompt inference | 0.11 | - | Better than baseline, but identity-order prediction ratio was high |


## Experiment Notes

The initial CLIP baseline showed low validation accuracy, around 5.1%.

After that, I tested `Qwen/Qwen3-VL-4B-Instruct` with prompt-based inference. The enhanced prompt improved validation accuracy to about 11%, but the model often predicted the original input order `[1, 2, 3, 4]`.

The 24-candidate prompt approach performed worse than the enhanced prompt, so it is not used as the current main approach.

Next steps:

- Image quality preprocessing
  - Improve image clarity before model input
  - Test resizing, sharpening, contrast adjustment, and noise reduction

- Smarter validation split
  - Create a validation set that better matches the Kaggle test distribution
  - Check whether sentence types, answer patterns, and scene categories are balanced

- QLoRA fine-tuning
  - Move from prompt-only inference to supervised fine-tuning
  - Use QLoRA to train the model efficiently under limited GPU memory

- Input image order TTA
  - Run inference with multiple permutations of the four input images
  - Aggregate the predictions to reduce bias toward the original input order

## Repository Structure

```text
SNU_2026/
├─ notebooks/
│  ├─ SNU_AI_Challenge_Baseline_Code.ipynb
│  └─ Qwen3-VL-4B-Instruct.ipynb
├─ src/
├─ README.md
└─ .gitignore