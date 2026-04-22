# Notes

## Purpose

This file is the running journal for the VC-associate autoresearch loop. Update it after baseline setup and after each meaningful experiment so the final retrospective can be written from this file alone.

## Active Run

### Run
- Tag: `apr21-vc`
- Date: `2026-04-21`
- Objective: Build a venture-capital associate that improves at spotting outlier founders in broad early-stage tech.
- Current best commit: `df3e588`
- Current best `val_bpb`: `2.095573`

### Current Founder Rubric
- Core founder signals to test: unusual ability, originality, speed, obsession, earned contrarian insight, execution proof
- Supporting evidence patterns: exceptional achievements, early signs of taste, difficult wins, technical or commercial leverage
- Negative signals: prestige without proof, shallow market understanding, consensus-chasing, weak execution evidence
- Open questions: which prompt and training changes most improve memo quality without degrading runtime; which signals are strongest for early founder prediction

### Latest Experiment
- Hypothesis: removing one accumulation step would improve experiments per hour enough to justify the change
- Change made: reduced `TOTAL_BATCH_SIZE` from `2**16` to `2**15`, dropping gradient accumulation from 2 to 1
- Result: `val_bpb 2.152058`, `training_seconds 323.9`, `total_seconds 832.2`, `num_steps 24`
- Keep or discard: discard
- What this taught us about founder prediction: throughput improved materially, but not enough to offset the quality regression; handoff notes need to track both search speed and model quality so a future agent does not keep a faster but weaker baseline
- Next move: revert to the best commit, then test a lower-complexity architecture change that cuts wall-clock without cutting effective batch size

## Driver Run: 2026-04-21T16:17:00
- Commit: `374a6ec`
- Experiment: reduce total batch size to `2**15`
- Status: discard
- val_bpb: `2.152058`
- training_seconds: `323.9`
- total_seconds: `832.2`
- memory_gb: `0.0`
- Handoff note: faster wall-clock than baseline (`832.2s` vs `1233.9s`) but worse objective; do not keep this as the branch baseline

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
