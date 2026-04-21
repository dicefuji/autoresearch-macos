#!/usr/bin/env python3
"""Queue-driven unattended experiment runner for autoresearch.

This script automates the mechanical loop:
- apply one queued train.py edit
- commit and optionally push it
- run training with timeout and log capture
- parse metrics from run.log
- append results.tsv
- keep or revert based on val_bpb
- append a short notes.md journal entry

It does not invent experiments on its own. The "brain" still comes from a
prepared queue or a live coding agent. This script makes unattended execution
explicit and repeatable.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TRAIN_PATH = ROOT / "train.py"
RESULTS_PATH = ROOT / "results.tsv"
NOTES_PATH = ROOT / "notes.md"
RUN_LOG_PATH = ROOT / "run.log"
RUNS_DIR = ROOT / "runs"
DEFAULT_QUEUE = ROOT / "queue" / "experiments.json"
METRICS_RE = re.compile(
    r"^val_bpb:\s+(?P<val_bpb>[0-9.]+)\n"
    r"training_seconds:\s+(?P<training_seconds>[0-9.]+)\n"
    r"total_seconds:\s+(?P<total_seconds>[0-9.]+)\n"
    r"peak_vram_mb:\s+(?P<peak_vram_mb>[0-9.]+)",
    re.MULTILINE,
)


@dataclass
class Metrics:
    val_bpb: float
    training_seconds: float
    total_seconds: float
    peak_vram_mb: float

    @property
    def memory_gb(self) -> float:
        return self.peak_vram_mb / 1024.0 if self.peak_vram_mb else 0.0


def run(cmd: list[str], *, check: bool = True, capture: bool = True, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=capture,
    )


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], check=check)


def load_queue(path: Path) -> list[dict]:
    with path.open() as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list of experiments")
    return payload


def apply_replacements(replacements: list[dict]) -> None:
    text = TRAIN_PATH.read_text()
    updated = text
    for repl in replacements:
        old = repl["old"]
        new = repl["new"]
        count = repl.get("count", 1)
        updated, n = re.subn(re.escape(old), new, updated, count=count)
        if n != count:
            raise ValueError(f"Replacement failed for snippet: {old!r}")
    TRAIN_PATH.write_text(updated)


def parse_metrics(log_text: str) -> Metrics:
    match = METRICS_RE.search(log_text)
    if not match:
        raise ValueError("Could not parse final metrics from run.log")
    return Metrics(
        val_bpb=float(match.group("val_bpb")),
        training_seconds=float(match.group("training_seconds")),
        total_seconds=float(match.group("total_seconds")),
        peak_vram_mb=float(match.group("peak_vram_mb")),
    )


def get_current_branch() -> str:
    return git("branch", "--show-current").stdout.strip()


def get_head_short() -> str:
    return git("rev-parse", "--short", "HEAD").stdout.strip()


def ensure_clean_worktree() -> None:
    status = git("status", "--short").stdout.strip()
    if status:
        raise RuntimeError("Worktree is not clean. Commit or clean changes before starting the driver.")


def current_best_val_bpb() -> float | None:
    if not RESULTS_PATH.exists():
        return None
    rows = RESULTS_PATH.read_text().strip().splitlines()[1:]
    vals = []
    for row in rows:
        parts = row.split("\t")
        if len(parts) >= 4 and parts[3] == "keep":
            try:
                vals.append(float(parts[1]))
            except ValueError:
                pass
    return min(vals) if vals else None


def append_results(commit: str, metrics: Metrics | None, status: str, description: str) -> None:
    if not RESULTS_PATH.exists():
        RESULTS_PATH.write_text("commit\tval_bpb\tmemory_gb\tstatus\tdescription\n")
    val_bpb = f"{metrics.val_bpb:.6f}" if metrics else "0.000000"
    memory_gb = f"{metrics.memory_gb:.1f}" if metrics else "0.0"
    with RESULTS_PATH.open("a") as f:
        f.write(f"{commit}\t{val_bpb}\t{memory_gb}\t{status}\t{description}\n")


def append_note(experiment: dict, commit: str, status: str, metrics: Metrics | None, log_name: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    lines = [
        "",
        f"## Driver Run: {timestamp}",
        f"- Commit: `{commit}`",
        f"- Experiment: {experiment['description']}",
        f"- Status: {status}",
        f"- Log: `{log_name}`",
    ]
    if metrics:
        lines.extend(
            [
                f"- val_bpb: `{metrics.val_bpb:.6f}`",
                f"- training_seconds: `{metrics.training_seconds:.1f}`",
                f"- total_seconds: `{metrics.total_seconds:.1f}`",
                f"- memory_gb: `{metrics.memory_gb:.1f}`",
            ]
        )
    if experiment.get("hypothesis"):
        lines.append(f"- Hypothesis: {experiment['hypothesis']}")
    if experiment.get("next_move"):
        lines.append(f"- Next move: {experiment['next_move']}")
    with NOTES_PATH.open("a") as f:
        f.write("\n".join(lines) + "\n")


def train(timeout_seconds: int, log_path: Path) -> Metrics:
    with log_path.open("w") as f:
        proc = subprocess.run(
            ["./.venv/bin/python", "train.py"],
            cwd=ROOT,
            text=True,
            stdout=f,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    shutil.copyfile(log_path, RUN_LOG_PATH)
    if proc.returncode != 0:
        raise RuntimeError(f"Training exited with status {proc.returncode}")
    return parse_metrics(log_path.read_text())


def restore_train_from(commit: str) -> None:
    git("checkout", commit, "--", "train.py")


def push_head() -> None:
    git("push", "origin", get_current_branch())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run unattended autoresearch experiments from a queue.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE, help="Path to JSON experiment queue.")
    parser.add_argument("--hours", type=float, default=4.0, help="Wall-clock budget for the driver.")
    parser.add_argument("--timeout-minutes", type=int, default=30, help="Per-run timeout.")
    parser.add_argument("--max-runs", type=int, default=0, help="Optional cap on number of experiments.")
    parser.add_argument("--push", action="store_true", help="Push commits after commit and after accepted runs.")
    args = parser.parse_args()

    if get_current_branch() == "master":
        raise RuntimeError("Run this driver from a dedicated autoresearch/* branch, not master.")
    ensure_clean_worktree()
    queue = load_queue(args.queue)
    RUNS_DIR.mkdir(exist_ok=True)
    start = time.time()
    runs_completed = 0

    for idx, experiment in enumerate(queue, start=1):
        if args.max_runs and runs_completed >= args.max_runs:
            break
        if time.time() - start >= args.hours * 3600:
            break

        base_commit = get_head_short()
        apply_replacements(experiment["replacements"])
        git("add", "train.py")
        git("commit", "-m", experiment["commit_message"])
        commit = get_head_short()
        if args.push:
            push_head()

        log_path = RUNS_DIR / f"{idx:03d}-{commit}.log"
        metrics = None
        status = "crash"
        try:
            metrics = train(args.timeout_minutes * 60, log_path)
            best_before = current_best_val_bpb()
            status = "keep" if best_before is None or metrics.val_bpb < best_before else "discard"
        except subprocess.TimeoutExpired:
            log_path.write_text(f"Timed out after {args.timeout_minutes} minutes\n")
            shutil.copyfile(log_path, RUN_LOG_PATH)
            status = "crash"
        except Exception as exc:
            with log_path.open("a") as f:
                f.write(f"\nDriver error: {exc}\n")
            shutil.copyfile(log_path, RUN_LOG_PATH)
            status = "crash"

        append_results(commit, metrics, status, experiment["description"])
        append_note(experiment, commit, status, metrics, log_path.name)
        git("add", "results.tsv", "notes.md", "run.log", str(log_path.relative_to(ROOT)))

        if status == "keep":
            git("commit", "-m", f"Keep experiment: {experiment['description']}")
            if args.push:
                push_head()
        else:
            restore_train_from(base_commit)
            git("add", "train.py", "results.tsv", "notes.md", "run.log", str(log_path.relative_to(ROOT)))
            git("commit", "-m", f"Log failed experiment: {experiment['description']}")
            if args.push:
                push_head()

        runs_completed += 1

    print(f"Driver finished after {runs_completed} queued experiments.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
