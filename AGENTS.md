# Repository Guidelines

## Project Structure & Module Organization
This repository is intentionally flat. The core files are `train.py` (model, optimizer, training loop, and the main experimentation surface), `prepare.py` (data download, tokenizer training, and runtime utilities), and `program.md` (the instructions agents read). Supporting materials live in `README.md`, `analysis.ipynb`, and `progress.png`. There is no `src/` or `tests/` package today.

## Build, Test, and Development Commands
Use `uv` for all local workflows:

- `uv sync`: install Python dependencies from `pyproject.toml` and `uv.lock`.
- `uv run prepare.py`: download data shards and train the tokenizer into `~/.cache/autoresearch/`.
- `uv run prepare.py --num-shards 8`: quick prep path for limited testing.
- `uv run train.py`: run one fixed-budget training experiment.

This project targets Python 3.10+ and currently assumes macOS with Apple Silicon MPS support in both `prepare.py` and `train.py`.

## Coding Style & Naming Conventions
Follow the existing Python style: 4-space indentation, `snake_case` for functions and variables, `PascalCase` for classes, and short module-level docstrings where useful. Keep changes focused and local; the project is designed so most experimentation happens in `train.py`. Avoid introducing extra modules unless the change clearly improves maintainability.

No formatter or linter is configured in the repo. Match surrounding style and keep imports, comments, and helper functions minimal and readable.

## Testing Guidelines
There is no formal automated test suite yet. Treat the runnable checks as:

- `uv run prepare.py` for data/tokenizer setup validation.
- `uv run train.py` for end-to-end training smoke tests.

If you add tests, prefer lightweight `pytest` files under a new `tests/` directory and name them `test_<feature>.py`.

## Commit & Pull Request Guidelines
Recent commits use short, imperative subjects such as `Adapt autoresearch for macOS / MPS` and `Tune hyperparameters for macOS MPS efficiency`. Keep commit titles concise, action-first, and specific.

Contributors and agents should commit frequently. Prefer small, reviewable commits over large batches, and push to `origin` as often as practical when credentials and network access allow. The default operating mode is: commit at each stable milestone, and push after each accepted improvement when possible.

Pull requests should explain the experiment or fix, note any platform assumptions, list the commands you ran, and include before/after metrics when changing training behavior. Link related issues when applicable, and attach screenshots only for documentation or notebook output changes.

## Agent-Specific Notes
Preserve the repo’s workflow split: humans iterate on `program.md`, while agents typically modify `train.py`. Treat `prepare.py` as infrastructure and only change it when fixing platform support or data pipeline issues.
