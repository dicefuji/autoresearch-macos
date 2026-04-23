# Autoresearch Run: apr21-vc — Lessons Learned

**Run dates:** 2026-04-21 – 2026-04-23  
**Branch:** `autoresearch/apr21-vc`  
**Total experiments:** 63  
**Keeps:** 16  
**val_bpb journey:** 2.095 → 1.779 → 1.639 → 1.621 → 1.583 → 1.541 → 1.521 → **1.473**  
**Total improvement:** −0.622 bits/byte (−30%)

---

## Final Best Configuration

```
DEPTH = 2
ASPECT_RATIO = 96          # model_dim = 256
HEAD_DIM = 128             # num_heads = 2
TOTAL_BATCH_SIZE = 2**15   # 32K tokens per step
EMBEDDING_LR = 0.45
UNEMBEDDING_LR = 0.005
MATRIX_LR = 0.040          # Muon
SCALAR_LR = 0.15           # per-layer scalars
WEIGHT_DECAY = 0.2
WARMUP_RATIO = 0.0
WARMDOWN_RATIO = 0.35
MLP expansion: 3x
Activation: ReLU²
```

---

## Core Finding: Step Count Dominates Capacity in Fixed-Time Budgets

Every major improvement came from getting more optimizer steps in the 5-minute wall-clock budget. The "right" model for a fixed-time run is not the most expressive model — it's the model that trains fastest while retaining enough capacity to make each step useful.

This played out in three successive waves:

| Change | val_bpb | Steps gained |
|---|---|---|
| Depth 4 → 3 | 2.095 → 1.779 | ~33% more steps |
| Depth 3 → 2 | 1.621 → 1.583 | ~50% more steps |
| Batch 2^16 → 2^15 | 1.521 → 1.479 | ~2x more steps |

Depth=1 was tried (val_bpb 1.569) and was worse than depth=2 (1.521 at the time) — the capacity floor was hit. So the sweet spot was 2 layers for this model size and budget.

---

## HP Optima Shift Completely When Architecture Changes

All hyperparameters needed re-tuning after each architectural change. What was optimal for depth=3 was sub-optimal or actively harmful for depth=2:

| Parameter | Depth-3 optimum | Depth-2 optimum |
|---|---|---|
| SCALAR_LR | 0.25 | 0.15 |
| MATRIX_LR | 0.03 | 0.04 |
| WARMDOWN_RATIO | 0.30 | 0.35 |
| TOTAL_BATCH_SIZE | 2^16 | 2^15 |

The direction of the shift makes sense: more frequent updates (depth=2 + smaller batch) means you can afford slightly larger MATRIX_LR per step but need calmer SCALAR_LR to prevent oscillation.

---

## Warmdown Ratio Has a Sharp Cliff

The LR warmdown schedule is the most sensitive parameter we found:

- **Depth-3:** 0.5 → 0.4 → 0.30 each improved; **0.25 catastrophically worse (2.062)**
- **Depth-2:** 0.30 was OK, 0.35 slightly better; 0.40 slightly worse

The collapse at 0.25 for depth=3 (from 1.621 to 2.062) was striking — too little cooldown causes the model to end training at a high LR without converging. The cliff is sharp and one-sided: too long is gently bad, too short is catastrophically bad.

No warmup (WARMUP_RATIO=0.0) was always optimal. A 15% warmup added during early experiments cost ~0.07 val_bpb.

---

## SCALAR_LR: Consistently Too High at Default Values

The per-layer scalar parameters (resid_lambdas, x0_lambdas) are updated with Adam at a rate that was consistently too high. Every decrease helped until hitting the floor:

`0.35 → 0.25 → 0.20 → 0.15` — all four steps improved.  
`0.10` was worse again (non-monotonic, likely MPS timing noise).

The pattern makes sense: these scalars are applied at every layer every step. With hundreds of steps in a 5-minute run, a high LR causes them to overshoot repeatedly.

---

## Batch Size Context-Dependence: Order Matters

`TOTAL_BATCH_SIZE = 2^15` was the **very first thing tried** (experiment 2) and gave **2.152** — worse than the 2.096 baseline. It was marked as a dead end.

Much later, the same change on the fully tuned depth=2, 3x MLP checkpoint gave **1.479** — a large improvement. The difference: a small noisy batch wastes optimizer steps on bad gradients; once the model and schedule are well-tuned, those extra steps are useful rather than harmful.

**Lesson:** Don't permanently discard experiments that fail early. The result depends on what the base model is doing.

---

## Architecture Negatives: What Didn't Help

All of the following were tried and clearly worse:

- **Sliding window attention (LS pattern):** +0.25 val_bpb — attention capacity is needed for this task
- **Wider model (ASPECT_RATIO 80 → model_dim 384):** +0.32 — slower with no benefit  
- **Larger batch (2^17):** +0.45 — far fewer steps, devastating
- **HEAD_DIM=64 (3 heads, model_dim 192):** +0.066 — smaller model worse
- **GELU vs ReLU²:** +0.036 — ReLU² is genuinely better here
- **MQA (n_kv_head=1):** +0.027 — full per-head KV needed
- **Gradient clipping at 1.0:** +0.011 — model is stable without it
- **ns_steps=6 (Muon):** +0.16 — 5 Newton-Schulz steps is enough
- **2x MLP expansion:** +0.053 — too little capacity
- **5x or 6x MLP:** ~+0.067 — slower with no gain
- **Cosine LR cooldown:** +0.14 — linear decay is better here
- **Non-zero FINAL_LR_FRAC:** +0.16 — decaying to zero is correct
- **Adam beta1 0.85 or 0.90:** +0.13 — low beta1 (0.8) is better for short runs
- **Muon momentum warmup compression:** +0.44 (catastrophic) — the slow 300-step warmup is intentional; don't compress it for short runs

---

## The Muon Momentum Warmup Mismatch (and Why It Doesn't Matter)

`get_muon_momentum` warms from 0.85 to 0.95 over 300 steps, but our 5-minute runs only produce ~110–300 steps. Momentum never reaches 0.95 — it peaks around 0.88–0.92.

This looked like a bug to fix. Compressing the warmup to 80 steps so momentum reaches 0.95 earlier gave **2.058** — catastrophically worse. The slow warmup is deliberate: it keeps Muon highly responsive (low momentum = more forgetful) during early training when gradients change rapidly, and gradually stabilizes it. The 300-step target was chosen for multi-thousand-step runs and happens to work fine scaled down.

---

## Robust Parameters (Change Doesn't Help)

These were stable across all experiments:

- **EMBEDDING_LR = 0.45** — tried 0.38, 0.40, 0.42; all worse  
- **UNEMBEDDING_LR = 0.005** — 0.004 slightly worse, 0.006 catastrophic (+0.36)  
- **WEIGHT_DECAY = 0.2** — tried 0.1, 0.15, 0.25; all worse  
- **Adam beta2 = 0.95** — tried 0.99; worse  
- **Muon beta2 = 0.95** — tried 0.98; worse  
- **WINDOW_PATTERN = "L"** — full attention throughout is better than any mixed pattern  
- **RoPE base = 10000** — tried 2000; slightly worse  
- **HEAD_DIM = 128** — tried 64; worse (also shrinks model_dim)

---

## MPS-Specific Observations

Running on Apple M1 Pro MPS introduces significant timing variability: individual training steps sometimes take 3–15× longer than normal (likely due to memory pressure or thermal throttling). This adds noise to val_bpb results at the level of ±0.002–0.005.

Practical effects seen:
- `DEVICE_BATCH_SIZE=32` hung for 30 minutes and timed out (not OOM — MPS just stalled)
- `SCALAR_LR=0.12` gave 1.702, mysteriously worse than both 0.10 (1.575) and 0.15 (1.522) — almost certainly a bad-luck run with timing spikes early in training
- Experiments within ~0.003 of each other should be treated as tied

The `peak_vram_mb` metric reported as 0.0 throughout — MPS doesn't expose this via PyTorch's memory API.

---

## Operational Lessons

1. **Run the queue driver, not manual experiments.** The driver's keep/revert logic is critical — it ensures each experiment starts from the current best rather than a stale base.

2. **Re-explore after big architectural changes.** After going depth 3→2, we ran another full sweep of all previously tuned parameters. About half the "confirmed" optima had shifted.

3. **Path dependence is real.** An experiment that fails at one base may succeed later. Track the base commit alongside the result, not just the delta.

4. **Watch for replacement string staleness.** When an experiment is kept, subsequent experiments that reference the old value will fail with "Replacement failed." Always check that the queue strings match the current `train.py` values before launching.

5. **10–12 minutes per experiment (5 min training + ~6 min evaluation).** Plan queue sizes accordingly. 6-experiment batches take ~70 minutes. For overnight runs, queue 20–30 experiments with a multi-hour time budget.
