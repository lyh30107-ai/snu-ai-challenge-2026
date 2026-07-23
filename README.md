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

### 3. SigLIP2 Pairwise Ranker

The current main approach uses frozen SigLIP2 image/text features and trains a lightweight pairwise temporal ranker.

- Model: `google/siglip2-so400m-patch16-384`
- Cached image/text feature extraction
- Pairwise before/after prediction between image pairs
- Position prediction auxiliary loss
- No-ordering calibration
- Full permutation TTA
- Greedy TTA selection based on validation accuracy

This approach is faster than full VLM fine-tuning because the SigLIP2 backbone is frozen and only the ranking head is trained.

## Current Results

| Date | Model | Method | Valid Accuracy | Validation Loss | Notes |
|---|---|---|---:|---:|---|
| 2026-07-17 | CLIP-ViT-B-32 | 24-class ordering classifier | 0.05125 | 3.13687 | Initial baseline result |
| 2026-07-20 | Qwen3-VL-4B-Instruct | Enhanced prompt inference | 0.11 | - | Better than baseline, but identity-order prediction ratio was high |
| 2026-07-21 | Qwen3-VL-4B | Prompt + TTA | 0.16 | - | Reduced identity-order bias |
| 2026-07-21 | Qwen3-VL-4B QLoRA | Small QLoRA fine-tuning | 0.20 | - | High identity ratio |
| 2026-07-22 | SigLIP-Base | 24-class classifier | ~0.07-0.10 | - | Low accuracy with frozen features |
| 2026-07-22 | CLIP-B/32 LoRA | Permutation scoring | 0.2725 | - | Overfitting observed |
| 2026-07-23 | SigLIP2-SO400M | Cached features + pairwise ranker | 0.3901 | - | Best single-checkpoint validation before TTA |
| 2026-07-23 | SigLIP2-SO400M | Pairwise ranker + full TTA | 0.4242 | - | TTA improved validation accuracy; identity ratio 0.3026 |
| 2026-07-23 | SigLIP2-SO400M | Pairwise ranker + greedy TTA | 0.4284 | - | Best local validation result so far among rule-safe single-model pipelines |


## Experiment Notes

The initial CLIP baseline showed low validation accuracy, around 5.1%.

After that, I tested `Qwen/Qwen3-VL-4B-Instruct` with prompt-based inference. The enhanced prompt improved validation accuracy to about 11%, but the model often predicted the original input order `[1, 2, 3, 4]`.

The 24-candidate prompt approach performed worse than the enhanced prompt, so it is not used as the current main approach.

The strongest rule-safe pipeline so far is the SigLIP2-SO400M cached feature pipeline with a pairwise temporal ranker. Instead of directly predicting one of 24 order classes, the model learns pairwise before/after relationships between frames and decodes them into a full ordering.

Full TTA improved local validation accuracy from about 0.3901 to 0.4242. Greedy TTA selection further improved the best local validation accuracy to about 0.4284.

The model still shows a gap between training accuracy and validation accuracy, suggesting that the frozen SigLIP2 feature representation has limited ability to capture fine-grained temporal changes. Future work should focus on backbone fine-tuning, LoRA adaptation, or stronger temporal ranking objectives rather than simply increasing the number of epochs.


## Repository Structure

```text
SNU_2026/
├─ notebooks/
│  ├─ SNU_AI_Challenge_Baseline_Code.ipynb
│  ├─ Qwen3-VL-4B-Instruct.ipynb
│  └─ snu-ai-challenge-siglip2-pairwise-tta.ipynb
├─ src/
├─ outputs/
├─ README.md
└─ .gitignore