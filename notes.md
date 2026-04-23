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

## Driver Run: 2026-04-22T01:56:30
- Commit: `ee20bf0`
- Experiment: raise UNEMBEDDING_LR from 0.004 to 0.005 on the current best checkpoint
- Status: keep
- Log: `005-ee20bf0.log`
- val_bpb: `1.626630`
- training_seconds: `300.3`
- total_seconds: `556.0`
- memory_gb: `0.0`
- Hypothesis: the lm_head may be under-updating relative to the lower embedding and matrix learning rates
- Next move: if this hurts, keep the original unembedding LR

## Driver Run: 2026-04-22T02:05:55
- Commit: `0f032e7`
- Experiment: lower WEIGHT_DECAY from 0.2 to 0.15 on the current best checkpoint
- Status: discard
- Log: `006-0f032e7.log`
- val_bpb: `1.631628`
- training_seconds: `301.6`
- total_seconds: `557.4`
- memory_gb: `0.0`
- Hypothesis: 0.1 was too weak, but 0.15 may preserve regularization while avoiding under-training
- Next move: if this is still worse, the original weight decay is likely correct

## Driver Run: 2026-04-22T02:15:15
- Commit: `824597a`
- Experiment: set WARMDOWN_RATIO from 0.5 to 0.4 while keeping no warmup and zero final LR
- Status: keep
- Log: `007-824597a.log`
- val_bpb: `1.621708`
- training_seconds: `300.3`
- total_seconds: `553.3`
- memory_gb: `0.0`
- Hypothesis: the best checkpoint may benefit from spending less of the fixed budget in cooldown without adding the warmup that hurt before
- Next move: if this regresses, keep the original schedule shape

## Driver Run: 2026-04-22T10:15:41
- Commit: `cce4abe`
- Experiment: set WARMDOWN_RATIO from 0.4 to 0.35 — more steps at peak LR
- Status: discard
- Log: `001-cce4abe.log`
- val_bpb: `1.623379`
- training_seconds: `301.7`
- total_seconds: `562.0`
- memory_gb: `0.0`
- Hypothesis: 0.4 helped; 0.35 gives even more peak-LR time in the 5-min budget
- Next move: if better, try 0.3; if worse, 0.4 is the sweet spot

## Driver Run: 2026-04-22T10:25:03
- Commit: `e696d53`
- Experiment: set WARMDOWN_RATIO from 0.4 to 0.30
- Status: keep
- Log: `002-e696d53.log`
- val_bpb: `1.621203`
- training_seconds: `300.4`
- total_seconds: `555.6`
- memory_gb: `0.0`
- Hypothesis: model may benefit from spending even less time in cooldown
- Next move: if worse than 0.35 experiment, stop here

## Driver Run: 2026-04-22T10:35:08
- Commit: `21860c4`
- Experiment: lower SCALAR_LR from 0.25 to 0.20
- Status: discard
- Log: `003-21860c4.log`
- val_bpb: `1.716475`
- training_seconds: `315.6`
- total_seconds: `598.2`
- memory_gb: `0.0`
- Hypothesis: the downward trend in scalar LR may continue to help
- Next move: if worse, 0.25 is the sweet spot

## Driver Run: 2026-04-22T10:44:51
- Commit: `26f6e31`
- Experiment: lower EMBEDDING_LR from 0.45 to 0.42
- Status: discard
- Log: `004-26f6e31.log`
- val_bpb: `1.675572`
- training_seconds: `300.3`
- total_seconds: `575.8`
- memory_gb: `0.0`
- Hypothesis: like SCALAR_LR, embeddings may converge better with a slightly gentler Adam step
- Next move: if better, try 0.40; if worse, keep 0.45

## Driver Run: 2026-04-22T10:54:57
- Commit: `6f4b9a5`
- Experiment: lower EMBEDDING_LR from 0.45 to 0.40
- Status: discard
- Log: `005-6f4b9a5.log`
- val_bpb: `1.651349`
- training_seconds: `300.6`
- total_seconds: `597.7`
- memory_gb: `0.0`
- Hypothesis: a more aggressive embedding LR reduction may help after scalar and warmdown tuning
- Next move: if worse than 0.42 experiment, use 0.42 as the new floor

## Driver Run: 2026-04-22T11:04:37
- Commit: `eb2bbb9`
- Experiment: raise UNEMBEDDING_LR from 0.005 to 0.006
- Status: discard
- Log: `006-eb2bbb9.log`
- val_bpb: `1.878980`
- training_seconds: `305.0`
- total_seconds: `572.6`
- memory_gb: `0.0`
- Hypothesis: 0.005 helped vs 0.004; lm_head may still benefit from a slightly larger Adam step
- Next move: if worse, 0.005 is the sweet spot for unembedding

## Driver Run: 2026-04-22T11:14:10
- Commit: `a2063d0`
- Experiment: raise MATRIX_LR from 0.03 to 0.032
- Status: discard
- Log: `007-a2063d0.log`
- val_bpb: `1.625393`
- training_seconds: `300.3`
- total_seconds: `565.5`
- memory_gb: `0.0`
- Hypothesis: with calmer scalar/embedding/warmdown, Muon may benefit from a slightly larger step to match the new regime
- Next move: if worse, keep 0.03; lowering was clearly bad so up is worth a try

## Driver Run: 2026-04-22T11:23:42
- Commit: `7f4c7f4`
- Experiment: lower WEIGHT_DECAY from 0.2 to 0.15 on the updated best checkpoint
- Status: discard
- Log: `008-7f4c7f4.log`
- val_bpb: `1.677571`
- training_seconds: `301.3`
- total_seconds: `564.6`
- memory_gb: `0.0`
- Hypothesis: the previous WD test was discarded, but the new LR/warmdown regime may be more tolerant of lighter regularization
- Next move: if still worse, keep 0.2

## Driver Run: 2026-04-22T14:19:52
- Commit: `c8cca1b`
- Experiment: set WARMDOWN_RATIO from 0.30 to 0.25
- Status: discard
- Log: `001-c8cca1b.log`
- val_bpb: `2.062247`
- training_seconds: `335.1`
- total_seconds: `1011.7`
- memory_gb: `0.0`
- Hypothesis: 0.5->0.4->0.30 all improved; continuing the trend may still help
- Next move: if better, try 0.20; if worse, 0.30 is the sweet spot

## Driver Run: 2026-04-22T14:39:25
- Commit: `6a5edd3`
- Experiment: set WARMDOWN_RATIO from 0.30 to 0.20
- Status: discard
- Log: `002-6a5edd3.log`
- val_bpb: `1.809597`
- training_seconds: `301.7`
- total_seconds: `1165.8`
- memory_gb: `0.0`
- Hypothesis: more time at peak LR may still improve val_bpb if the model is not yet overfitting
- Next move: if worse than 0.25 but better than 0.30, settle at 0.25

## Driver Run: 2026-04-22T14:49:45
- Commit: `b29ad6b`
- Experiment: raise ADAM_BETAS beta1 from 0.8 to 0.85
- Status: discard
- Log: `003-b29ad6b.log`
- val_bpb: `1.647907`
- training_seconds: `301.3`
- total_seconds: `611.9`
- memory_gb: `0.0`
- Hypothesis: more momentum in Adam may help embedding/unembedding convergence in the fixed budget
- Next move: if better, try 0.90; if worse, 0.8 is correct

## Driver Run: 2026-04-22T14:59:14
- Commit: `2d84116`
- Experiment: raise ADAM_BETAS beta1 from 0.8 to 0.90
- Status: discard
- Log: `004-2d84116.log`
- val_bpb: `1.650593`
- training_seconds: `300.6`
- total_seconds: `561.9`
- memory_gb: `0.0`
- Hypothesis: standard Adam beta1=0.9 may outperform the non-standard 0.8
- Next move: if worse, the low beta1 is intentional for the fixed short budget

## Driver Run: 2026-04-22T15:12:27
- Commit: `250cc30`
- Experiment: raise TOTAL_BATCH_SIZE from 2**16 to 2**17
- Status: discard
- Log: `005-250cc30.log`
- val_bpb: `1.972390`
- training_seconds: `315.2`
- total_seconds: `786.0`
- memory_gb: `0.0`
- Hypothesis: larger effective batch may give more stable gradient estimates and better val_bpb per optimizer step
- Next move: if worse, the current batch size is well-tuned; if better, consider 2^18

## Driver Run: 2026-04-22T15:22:30
- Commit: `832c907`
- Experiment: set WINDOW_PATTERN from 'L' to 'LS' — full attention in layer 0, half-context in layer 1, full in layer 2
- Status: discard
- Log: `006-832c907.log`
- val_bpb: `1.871419`
- training_seconds: `300.8`
- total_seconds: `595.1`
- memory_gb: `0.0`
- Hypothesis: pure-L gave worse results before, but with the current better-tuned schedule the small efficiency gain may make up the difference
- Next move: if worse, keep all-L; the previous experiment showed this costs ~0.005 val_bpb

## Driver Run: 2026-04-22T15:32:23
- Commit: `68833d1`
- Experiment: raise ASPECT_RATIO from 64 to 80; model_dim goes from 256 to 384
- Status: discard
- Log: `007-68833d1.log`
- val_bpb: `1.940620`
- training_seconds: `305.2`
- total_seconds: `585.3`
- memory_gb: `0.0`
- Hypothesis: a slightly wider model under the 5-min budget may have more capacity and better val_bpb
- Next move: if slower and worse, the current size is right; if better but slower the capacity gain is worth it

## Driver Run: 2026-04-22T15:42:03
- Commit: `9c2c026`
- Experiment: increase ns_steps from 5 to 6 in the MuonAdamW optimizer call
- Status: discard
- Log: `008-9c2c026.log`
- val_bpb: `1.684874`
- training_seconds: `302.5`
- total_seconds: `572.7`
- memory_gb: `0.0`
- Hypothesis: one more Newton-Schulz step gives a more accurate polar factor; marginal cost on MPS
- Next move: if no improvement, ns_steps=5 is sufficient

## Driver Run: 2026-04-22T15:59:16
- Commit: `9d88d86`
- Experiment: change get_muon_momentum warmup from 300 steps to 80 steps so momentum reaches 0.95 before cooldown
- Status: discard
- Log: `001-9d88d86.log`
- val_bpb: `2.058078`
- training_seconds: `342.6`
- total_seconds: `782.6`
- memory_gb: `0.0`
- Hypothesis: we do ~110 steps per run; the 300-step warmup means momentum never exceeds ~0.89, effectively training with sub-optimal Muon momentum the whole time
- Next move: if better, also try starting momentum at 0.90 instead of 0.85

## Driver Run: 2026-04-22T16:09:06
- Commit: `d54a1d8`
- Experiment: change get_muon_momentum to warm from 0.90 to 0.95 over 80 steps instead of 0.85 to 0.95 over 300
- Status: discard
- Log: `002-d54a1d8.log`
- val_bpb: `1.684748`
- training_seconds: `300.6`
- total_seconds: `582.3`
- memory_gb: `0.0`
- Hypothesis: higher starting momentum may help even in early steps; combined with faster warmup
- Next move: if worse than the 80-step warmup alone, the 0.85 start is intentional

## Driver Run: 2026-04-22T16:18:51
- Commit: `cbafe4f`
- Experiment: raise FINAL_LR_FRAC from 0.0 to 0.1 so LR decays to 10% of peak rather than 0
- Status: discard
- Log: `003-cbafe4f.log`
- val_bpb: `1.680585`
- training_seconds: `308.3`
- total_seconds: `578.1`
- memory_gb: `0.0`
- Hypothesis: fully zeroing the LR at the end of the 5-min budget may cause abrupt loss of progress; ending at 10% may smooth convergence
- Next move: if better, try 0.05; if worse, 0.0 is correct for this budget

## Driver Run: 2026-04-22T16:29:06
- Commit: `1b9e0da`
- Experiment: replace linear cooldown with cooldown**2 for a convex decay curve
- Status: discard
- Log: `004-1b9e0da.log`
- val_bpb: `1.661176`
- training_seconds: `311.4`
- total_seconds: `607.8`
- memory_gb: `0.0`
- Hypothesis: linear decay may cut LR too fast early in cooldown; a squared schedule keeps more LR budget until near the end
- Next move: if worse, linear is fine; if better, try cooldown**1.5 for a middle ground

## Driver Run: 2026-04-22T16:39:18
- Commit: `a13c37e`
- Experiment: raise Muon beta2 from 0.95 to 0.98 for slower variance adaptation
- Status: discard
- Log: `005-a13c37e.log`
- val_bpb: `1.686451`
- training_seconds: `324.9`
- total_seconds: `604.2`
- memory_gb: `0.0`
- Hypothesis: 0.95 adapts step sizes very quickly; 0.98 gives a more stable estimate over the ~110 training steps
- Next move: if worse, fast variance adaptation is beneficial for this short budget

## Driver Run: 2026-04-22T16:47:58
- Commit: `14e3392`
- Experiment: set DEPTH=2 and ASPECT_RATIO=96 (model_dim stays 256, 2 layers instead of 3, ~50% more optimizer steps)
- Status: keep
- Log: `006-14e3392.log`
- val_bpb: `1.582612`
- training_seconds: `300.3`
- total_seconds: `512.3`
- memory_gb: `0.0`
- Hypothesis: depth=3 beat depth=4 largely due to more steps in the fixed budget; depth=2 gets even more steps — capacity vs. iteration count tradeoff
- Next move: if clearly worse, depth=3 has the right capacity; if competitive, try depth=2 with tuned LRs

## Driver Run: 2026-04-22T17:05:49
- Commit: `cfcd4d0`
- Experiment: retry WARMDOWN_RATIO=0.25 on the depth-2 checkpoint (was catastrophic for depth-3 but depth-2 has ~50% more steps)
- Status: discard
- Log: `001-cfcd4d0.log`
- val_bpb: `1.683845`
- training_seconds: `305.4`
- total_seconds: `539.6`
- memory_gb: `0.0`
- Hypothesis: depth-2 gets ~170 steps; 0.25 warmdown means ~43 steps of cooldown which may be adequate unlike for depth-3
- Next move: if still terrible, 0.30 is the floor regardless of depth; if better, try 0.20

## Driver Run: 2026-04-22T17:14:28
- Commit: `da48886`
- Experiment: try WARMDOWN_RATIO=0.35 on depth-2 — slightly more cooldown
- Status: keep
- Log: `002-da48886.log`
- val_bpb: `1.561836`
- training_seconds: `301.2`
- total_seconds: `512.5`
- memory_gb: `0.0`
- Hypothesis: depth-2 with more steps may benefit from a slightly longer cooldown that gives smoother final convergence
- Next move: if worse, 0.30 is optimal; if better, try 0.40

## Driver Run: 2026-04-22T17:23:05
- Commit: `0053eca`
- Experiment: retry MATRIX_LR=0.025 on depth-2 (was worse for depth-3 but depth-2 has different gradient dynamics)
- Status: discard
- Log: `003-0053eca.log`
- val_bpb: `1.580155`
- training_seconds: `301.4`
- total_seconds: `509.2`
- memory_gb: `0.0`
- Hypothesis: with 2 layers the Muon updates are applied more frequently per token; a gentler step may work better
- Next move: if worse, 0.03 is correct for depth-2 as well

## Driver Run: 2026-04-22T17:31:40
- Commit: `e59235e`
- Experiment: try MATRIX_LR=0.035 on depth-2 — slightly more aggressive Muon
- Status: keep
- Log: `004-e59235e.log`
- val_bpb: `1.555866`
- training_seconds: `300.8`
- total_seconds: `507.5`
- memory_gb: `0.0`
- Hypothesis: depth-2 with more gradient steps may tolerate a slightly higher Muon LR; we only tried 0.03 and 0.032 before on depth-3
- Next move: if better, try 0.04; if worse, 0.03 is correct

## Driver Run: 2026-04-22T17:40:21
- Commit: `35e3679`
- Experiment: retry SCALAR_LR=0.20 on depth-2 (was much worse for depth-3 but depth-2 has different convergence speed)
- Status: keep
- Log: `005-35e3679.log`
- val_bpb: `1.541022`
- training_seconds: `302.5`
- total_seconds: `513.0`
- memory_gb: `0.0`
- Hypothesis: with ~170 steps, per-layer scalars may converge fine with a gentler 0.20 update rate
- Next move: if worse, 0.25 is correct; if better, try 0.15

## Driver Run: 2026-04-22T17:48:03
- Commit: `84824c1`
- Experiment: set DEPTH=1 and ASPECT_RATIO=192 (model_dim=256, 1 layer, potentially 3x more steps than depth-3)
- Status: discard
- Log: `006-84824c1.log`
- val_bpb: `1.568834`
- training_seconds: `300.1`
- total_seconds: `455.0`
- memory_gb: `0.0`
- Hypothesis: if the depth-3→depth-2 improvement comes purely from more gradient steps, depth-1 should win; tests the capacity floor
- Next move: if competitive, tune LRs for depth-1; if badly worse, depth-2 is the sweet spot for capacity vs. steps

## Driver Run: 2026-04-22T23:41:09
- Commit: `3c3f680`
- Experiment: lower SCALAR_LR from 0.20 to 0.15 — continuing the downward trend that worked for depth-2
- Status: keep
- Log: `001-3c3f680.log`
- val_bpb: `1.521804`
- training_seconds: `301.2`
- total_seconds: `505.8`
- memory_gb: `0.0`
- Hypothesis: 0.25→0.20 helped for depth-2; 0.15 may help further given more gradient steps
- Next move: if worse, 0.20 is the floor; if better, try 0.10

## Driver Run: 2026-04-22T23:49:40
- Commit: `e42e37e`
- Experiment: raise MATRIX_LR from 0.035 to 0.04 — continuing the upward trend for Muon in depth-2
- Status: discard
- Log: `002-e42e37e.log`
- val_bpb: `1.529672`
- training_seconds: `300.4`
- total_seconds: `504.7`
- memory_gb: `0.0`
- Hypothesis: 0.03→0.035 helped; 0.04 may help further given more gradient steps available
- Next move: if worse, 0.035 is the ceiling; if better, try 0.045

## Driver Run: 2026-04-22T23:58:12
- Commit: `2d94c45`
- Experiment: raise WARMDOWN_RATIO from 0.35 to 0.40 — continuing the trend toward more cooldown in depth-2
- Status: discard
- Log: `003-2d94c45.log`
- val_bpb: `1.526849`
- training_seconds: `301.1`
- total_seconds: `505.3`
- memory_gb: `0.0`
- Hypothesis: 0.30→0.35 improved; the depth-2 model with more steps may benefit from even more gradual cooldown
- Next move: if worse, 0.35 is optimal for depth-2

## Driver Run: 2026-04-23T00:06:44
- Commit: `4769123`
- Experiment: lower EMBEDDING_LR from 0.45 to 0.40 — was worse for depth-3 but depth-2 LRs are generally lower
- Status: discard
- Log: `004-4769123.log`
- val_bpb: `1.531466`
- training_seconds: `301.0`
- total_seconds: `504.7`
- memory_gb: `0.0`
- Hypothesis: SCALAR_LR and MATRIX_LR both shifted for depth-2; embedding LR may also want to move
- Next move: if worse, 0.45 is correct; if better, try 0.35
