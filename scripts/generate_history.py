#!/usr/bin/env python3
"""Create clearly labelled synthetic Git history in this dedicated test repository.

Generated commits are empty and backdated for Git-history testing only. This tool
never pushes, never changes tracked files, and can resume after an interrupted run.
"""
from __future__ import annotations

import argparse
import os
import random
import subprocess
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

PREFIX = "[SYNTHETIC TEST DATA]"


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], text=True, capture_output=True, check=False
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use YYYY-MM-DD dates") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=20_000,
                        help="Total number of synthetic commits desired (default: 20000)")
    parser.add_argument("--start-date", type=parse_day, default=date(2021, 1, 1))
    parser.add_argument("--end-date", type=parse_day, default=date(2026, 11, 5))
    parser.add_argument("--seed", type=int, default=20261105,
                        help="Fixed seed for a repeatable date schedule")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if not 1 <= args.count <= 100_000:
        parser.error("--count must be between 1 and 100000")
    if args.end_date < args.start_date:
        parser.error("--end-date must be on or after --start-date")
    if git("rev-parse", "--is-inside-work-tree", check=False) != "true":
        print("ERROR: Run this inside the dedicated Git repository.", file=sys.stderr)
        return 2

    # Refuse to generate on top of uncommitted edits.
    if git("status", "--porcelain"):
        print("ERROR: Working tree is not clean. Commit or stash changes first.", file=sys.stderr)
        return 2

    history = git("log", "--format=%s").splitlines()
    synthetic_done = sum(1 for subject in history if subject.startswith(PREFIX))
    if synthetic_done > args.count:
        print(
            f"ERROR: Found {synthetic_done} labelled synthetic commits, "
            f"which exceeds requested total {args.count}.",
            file=sys.stderr,
        )
        return 2

    name = git("config", "user.name", check=False)
    email = git("config", "user.email", check=False)
    if not name or not email:
        print("ERROR: Configure git user.name and user.email first.", file=sys.stderr)
        return 2

    start = datetime.combine(args.start_date, time.min, tzinfo=timezone.utc)
    end_exclusive = datetime.combine(
        args.end_date + timedelta(days=1), time.min, tzinfo=timezone.utc
    )
    span = int((end_exclusive - start).total_seconds())
    rng = random.Random(args.seed)
    schedule = sorted(
        start + timedelta(seconds=rng.randrange(span))
        for _ in range(args.count)
    )
    remaining = args.count - synthetic_done

    print("SYNTHETIC TEST DATA — not genuine development activity.")
    print(f"Repository:       {Path.cwd()}")
    print(f"Identity:         {name} <{email}>")
    print(f"Target synthetic: {args.count:,}")
    print(f"Already present:  {synthetic_done:,}")
    print(f"Remaining:        {remaining:,}")
    print(f"Date range (UTC): {args.start_date} through {args.end_date}")
    print(f"Seed:             {args.seed}")

    if args.dry_run:
        print("Dry run only; no commits were created.")
        if remaining:
            print("Next planned date:", schedule[synthetic_done].isoformat())
            print("Last planned date:", schedule[-1].isoformat())
        else:
            print("Target already reached; nothing to do.")
        return 0

    if remaining == 0:
        print("Target already reached; no commits created.")
        return 0

    print("Creating commits. This may take several minutes...")
    for index in range(synthetic_done, args.count):
        stamp = schedule[index]
        iso = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": name,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_COMMITTER_NAME": name,
            "GIT_COMMITTER_EMAIL": email,
            "GIT_AUTHOR_DATE": iso,
            "GIT_COMMITTER_DATE": iso,
        })
        message = f"{PREFIX} Generated history sample {index + 1:05d}/{args.count:05d}"
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            env=env, stdout=subprocess.DEVNULL, check=True,
        )
        completed = index + 1
        if completed % 250 == 0 or completed == args.count:
            print(f"Created {completed:,}/{args.count:,}")

    print("\nGeneration complete.")
    print(f"Verify synthetic commits: git log --format=%s | grep -c '^{PREFIX}'")
    print("Review the disclosure and history before manually pushing.")
    print("This script does not push automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
