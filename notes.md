# Notes

## Purpose

This file is the running journal for the VC-associate autoresearch loop. It is append-only from this point forward: do not rewrite prior run entries. Add a new dated block for every completed experiment so another agent can reconstruct what worked, what failed, and what the current best checkpoint is.

## Active Run

### Run
- Tag: `apr21-vc`
- Date: `2026-04-21`
- Objective: Build a venture-capital associate that improves at spotting outlier founders in broad early-stage tech.
- Current best commit: `1ace239`
- Current best `val_bpb`: `1.639182`

### Current Founder Rubric
- Core founder signals to test: unusual ability, originality, speed, obsession, earned contrarian insight, execution proof
- Supporting evidence patterns: exceptional achievements, early signs of taste, difficult wins, technical or commercial leverage
- Negative signals: prestige without proof, shallow market understanding, consensus-chasing, weak execution evidence
- Open questions: which prompt and training changes most improve memo quality without degrading runtime; which signals are strongest for early founder prediction

### Latest Experiment
- Status: historical section retained for compatibility; use appended `## Driver Run:` entries below as the source of truth.

## Driver Run: 2026-04-21T16:17:00
- Commit: `374a6ec`
- Experiment: reduce total batch size to `2**15`
- Status: discard
- val_bpb: `2.152058`
- training_seconds: `323.9`
- total_seconds: `832.2`
- memory_gb: `0.0`
- Handoff note: faster wall-clock than baseline (`832.2s` vs `1233.9s`) but worse objective; do not keep this as the branch baseline

## Driver Run: 2026-04-21T16:28:00
- Commit: `f3d1f58`
- Experiment: reduce depth from `4` to `3`
- Status: keep
- val_bpb: `1.778950`
- training_seconds: `338.8`
- total_seconds: `665.6`
- memory_gb: `0.0`
- Handoff note: clear win on both objective and wall-clock; this is the new branch baseline

## Driver Run: 2026-04-21T16:41:00
- Commit: `9ff8709`
- Experiment: reduce head dimension from `128` to `64` at `DEPTH = 3`
- Status: discard
- val_bpb: `2.174275`
- training_seconds: `314.7`
- total_seconds: `938.7`
- memory_gb: `0.0`
- Handoff note: strong regression versus the depth-3 best; restore `HEAD_DIM = 128` before the next run

## Driver Run: 2026-04-21T16:58:00
- Commit: `1ace239`
- Experiment: lower `EMBEDDING_LR`, `MATRIX_LR`, and `SCALAR_LR` on the depth-3 checkpoint
- Status: keep
- val_bpb: `1.639182`
- training_seconds: `301.0`
- total_seconds: `574.9`
- memory_gb: `0.0`
- Handoff note: clear win on both objective and total wall-clock; this is the new branch baseline

## Driver Run: 2026-04-21T17:11:00
- Commit: `01726fa`
- Experiment: add a small warmup and a less aggressive cooldown on the lower-LR checkpoint
- Status: discard
- val_bpb: `1.696098`
- training_seconds: `301.0`
- total_seconds: `595.5`
- memory_gb: `0.0`
- Handoff note: final metrics did flush after an initial watcher miss; result is worse than the current best `1.639182`, so keep the lower-LR baseline

## Driver Run: 2026-04-22T00:02:00
- Commit: `564dc82`
- Experiment: use `WINDOW_PATTERN = "SLL"` on the lower-LR depth-3 checkpoint
- Status: discard
- val_bpb: `1.647455`
- training_seconds: `300.4`
- total_seconds: `572.9`
- memory_gb: `0.0`
- Handoff note: close to the current best but still worse; restore full-context attention before the next run

## Driver Run: 2026-04-22T00:16:00
- Commit: `b4c3428`
- Experiment: lower `WEIGHT_DECAY` from `0.2` to `0.1` on the lower-LR depth-3 checkpoint
- Status: discard
- val_bpb: `1.681401`
- training_seconds: `300.3`
- total_seconds: `588.2`
- memory_gb: `0.0`
- Handoff note: lower regularization hurt quality and reduced useful steps (`116` vs `147` on the best run); keep the original `WEIGHT_DECAY = 0.2`

## Driver Run: 2026-04-22T00:27:00
- Commit: `2d5d6f6`
- Experiment: lower `EMBEDDING_LR` from `0.45` to `0.40` on the best checkpoint
- Status: discard
- val_bpb: `1.641244`
- training_seconds: `300.0`
- total_seconds: `562.7`
- memory_gb: `0.0`
- Handoff note: very close to the current best but still worse by `0.002062`; restore `EMBEDDING_LR = 0.45` before overnight search

## Active Run Template

### Run
- Tag:
- Date:
- Objective:
- Current best commit:
- Current best `val_bpb`:

### Current Founder Rubric
- Core founder signals to test:
- Supporting evidence patterns:
- Negative signals:
- Open questions:

### Latest Experiment
- Hypothesis:
- Change made:
- Result:
- Keep or discard:
- What this taught us about founder prediction:
- Next move:

## Memo Snippet Template

### Candidate: <name / company>
- Founder score:
- Market score:
- Contrarian insight score:
- Execution score:
- Overall conviction:
- Core founder signal:
- Supporting evidence:
- Market context:
- Risks:
- Decision:

## Retrospective Prompts

- Which founder signals became more predictive over time?
- Which obvious prestige markers turned out to be weak shortcuts?
- What kinds of contrarian thinking appeared repeatedly among strong candidates?
- What changes to prompts or training produced the biggest jump in memo quality?
- What should the next run test?

## Driver Run: 2026-04-22T01:06:06
- Commit: `57dccfc`
- Experiment: lower MATRIX_LR from 0.03 to 0.028 on the current best checkpoint
- Status: discard
- Log: `001-57dccfc.log`
- val_bpb: `1.867773`
- training_seconds: `325.9`
- total_seconds: `621.9`
- memory_gb: `0.0`
- Hypothesis: a slightly gentler Muon step may improve stability without losing useful progress
- Next move: if this is close but worse, try a slightly lower scalar LR instead

## Driver Run: 2026-04-22T01:18:37
- Commit: `51a945d`
- Experiment: lower MATRIX_LR from 0.03 to 0.025 on the current best checkpoint
- Status: discard
- Log: `001-51a945d.log`
- val_bpb: `1.650867`
- training_seconds: `301.5`
- total_seconds: `572.0`
- memory_gb: `0.0`
- Hypothesis: the depth-3 model may still be slightly overstepping in the matrix group
- Next move: if this degrades sharply, matrix LR is probably already near the sweet spot

## Driver Run: 2026-04-22T01:28:07
- Commit: `69a7274`
- Experiment: lower SCALAR_LR from 0.35 to 0.30 on the current best checkpoint
- Status: discard
- Log: `002-69a7274.log`
- val_bpb: `1.641866`
- training_seconds: `300.6`
- total_seconds: `561.6`
- memory_gb: `0.0`
- Hypothesis: per-layer scalars may still be moving too aggressively early in the run
- Next move: if this helps, try a more conservative scalar LR after restoring the best run

## Driver Run: 2026-04-22T01:37:42
- Commit: `36e1830`
- Experiment: lower SCALAR_LR from 0.35 to 0.25 on the current best checkpoint
- Status: keep
- Log: `003-36e1830.log`
- val_bpb: `1.637168`
- training_seconds: `300.2`
- total_seconds: `568.2`
- memory_gb: `0.0`
- Hypothesis: the best run may benefit from much calmer scalar updates under the fixed budget
- Next move: if this is too slow, keep the original scalar LR

## Driver Run: 2026-04-22T01:47:07
- Commit: `cfc7f96`
- Experiment: lower UNEMBEDDING_LR from 0.004 to 0.003 on the current best checkpoint
- Status: discard
- Log: `004-cfc7f96.log`
- val_bpb: `1.639387`
- training_seconds: `300.8`
- total_seconds: `558.0`
- memory_gb: `0.0`
- Hypothesis: the lm_head may converge better with a slightly smaller Adam step
- Next move: if there is no movement, unembedding LR is probably not the main bottleneck
