# Notes

## Purpose

This file is the running journal for the VC-associate autoresearch loop. Update it after baseline setup and after each meaningful experiment so the final retrospective can be written from this file alone.

## Active Run

### Run
- Tag: `apr21-vc`
- Date: `2026-04-21`
- Objective: Build a venture-capital associate that improves at spotting outlier founders in broad early-stage tech.
- Current best commit: `f3d1f58`
- Current best `val_bpb`: `1.778950`

### Current Founder Rubric
- Core founder signals to test: unusual ability, originality, speed, obsession, earned contrarian insight, execution proof
- Supporting evidence patterns: exceptional achievements, early signs of taste, difficult wins, technical or commercial leverage
- Negative signals: prestige without proof, shallow market understanding, consensus-chasing, weak execution evidence
- Open questions: which prompt and training changes most improve memo quality without degrading runtime; which signals are strongest for early founder prediction

### Latest Experiment
- Hypothesis: letting the depth-3 model use a genuinely smaller width (`HEAD_DIM 64`) might preserve the win while improving efficiency further
- Change made: reduced `HEAD_DIM` from `128` to `64` at `DEPTH = 3`
- Result: `val_bpb 2.174275`, `training_seconds 314.7`, `total_seconds 938.7`, `num_steps 21`
- Keep or discard: discard
- What this taught us about founder prediction: the depth-3 win did not come from blindly shrinking width; on this setup, the current best seems to rely on the larger rounded-up width even at lower depth
- Next move: restore the depth-3 best checkpoint and test optimizer schedule tuning instead of additional width shrinkage

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
