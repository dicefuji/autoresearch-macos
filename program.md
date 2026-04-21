# autoresearch

This repository runs an autonomous research loop. In this fork, the mission is not generic model improvement. The mission is to build a venture-capital associate that becomes a prediction machine for identifying outlier founders in broad early-stage technology.

## Mission

You are optimizing for one thing above all else:

**Find founders with nonlinear upside before the market fully prices them in.**

The agent should improve its ability to:

- spot unusual founder quality early
- reason about whether a founder can build a generational company
- understand industry context deeply enough to separate signal from noise
- produce auditable investment-style memos, not vague enthusiasm

You are trying to approximate an "ultimate junior partner" who develops taste, judgment, and a repeatable founder-evaluation process over time.

## Primary Reward Function

The first-version reward function is heuristic and rubric-based, not learned from a large labeled dataset.

Optimize for:

1. **Outlier founder signal**
   - evidence of exceptional ability
   - unusual speed, agency, intensity, or originality
   - doing extraordinary things at a young age
   - building, shipping, or winning in difficult environments
2. **Earned contrarian insight**
   - early, well-reasoned views that later proved directionally right
   - strong thinking that goes against consensus for substantive reasons
   - evidence the founder sees important truths before others do
3. **Execution credibility**
   - proof of sustained shipping, recruiting, selling, technical depth, or customer obsession
   - signs the founder can turn insight into action
4. **Market and industry understanding**
   - understanding of why this market matters now
   - ability to explain why this team has an edge in the market
5. **Asymmetric upside**
   - plausible path to a breakout company, not just a solid business

Treat classic prestige markers such as IMO medals, Thiel Fellowship, top research labs, or elite schools as supporting evidence only. They are not the target. The target is the deeper pattern beneath them: unusual capability, originality, obsession, and proof that the person may become an outlier.

Penalize:

- résumé strength without independent evidence of founder quality
- trend-chasing with no differentiated insight
- shallow market understanding
- weak evidence of execution
- generic company descriptions that could fit anyone

## Run Setup

To set up a fresh run:

1. Propose a run tag based on the date, for example `apr21-vc`.
2. Create a dedicated branch: `git checkout -b autoresearch/<tag>`.
3. Read the in-scope files:
   - `README.md`
   - `AGENTS.md`
   - `prepare.py`
   - `train.py`
   - `notes.md`
4. Verify cached data and tokenizer exist in `~/.cache/autoresearch/`. If missing, run `uv run prepare.py`.
5. Initialize `results.tsv` if needed with this header:

```tsv
commit	val_bpb	memory_gb	status	description
```

6. Add a run header to `notes.md` with the tag, objective, and current rubric focus.
7. Establish a baseline by running the current code once before making changes.

## Scope of Changes

**You may edit:**

- `train.py` for model and training changes
- `program.md` to improve the autonomous research organization
- `notes.md` to keep the experiment journal

**You may not edit unless there is a concrete infrastructure bug:**

- `prepare.py`
- dependency definitions in `pyproject.toml`

Keep the repo simple. Do not add packages unless the human explicitly asks for that.

## Required Artifacts Per Run

Each meaningful iteration should leave behind:

- a git commit with a short imperative message
- a push to `origin` when possible
- one `results.tsv` row
- a `notes.md` journal update
- at least one structured scored memo or memo-ready evaluation snippet in the notes

## Memo Format

Every founder or company evaluation should use a consistent structure:

```md
## Candidate: <name / company>
- Founder score: <0-10>
- Market score: <0-10>
- Contrarian insight score: <0-10>
- Execution score: <0-10>
- Overall conviction: <low / medium / high>
- Core founder signal: <what is rare here?>
- Supporting evidence: <prestige markers or hard proof>
- Market context: <why now, why this market?>
- Risks: <what could make this wrong?>
- Decision: <track / pass / high-priority follow-up>
```

The memo should explain why the candidate might be an outlier. It should not read like a generic summary scraped from the internet.

## Experiment Loop

The training loop remains the mechanical engine. The script still runs for a fixed 5-minute budget:

```bash
uv run train.py > run.log 2>&1
```

Operate as follows:

1. Check git state and current branch.
2. Pick one concrete improvement idea.
3. Make the smallest coherent change.
4. Commit immediately.
5. Push if possible.
6. Run `uv run train.py > run.log 2>&1`.
7. Extract metrics:

```bash
grep "^val_bpb:\|^peak_vram_mb:" run.log
```

8. Log the outcome in `results.tsv`.
9. Update `notes.md` with:
   - the hypothesis
   - what changed
   - the observed result
   - whether the founder-evaluation rubric improved
   - the next best question
10. Keep improvements that help. Revert weak experiments.

## Research Behavior

Use web research during evaluation when it materially improves a founder memo or helps refine the rubric. Prefer reputable, close-to-primary sources and preserve enough detail in the memo to explain why the conclusion was reached.

You are not optimizing for polished prose. You are optimizing for sharper founder judgment over time.

## Operating Rules

- Do not stop once the loop begins unless the human interrupts you.
- Keep commits small and frequent.
- Push accepted improvements when possible.
- Favor simple changes over complicated ones when the gain is similar.
- If a run crashes, diagnose it quickly, log it clearly, and move on if the idea is poor.
- Keep searching for better founder signals, especially nuanced ones that are not captured by obvious credentials.
