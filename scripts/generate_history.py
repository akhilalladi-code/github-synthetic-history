#!/usr/bin/env python3
"""Generate clearly labelled empty, backdated commits in this dedicated test repository.

This utility does not push. It permits one initial disclosure commit and refuses
to run in a repository with a longer history.
"""
from __future__ import annotations

import argparse
import os
import random
import subprocess
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
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
    parser.add_argument("--count", type=int, default=20_000)
    parser.add_argument("--start-date", type=parse_day, default=date(2021, 1, 1))
    parser.add_argument("--end-date", type=parse_day, default=date(2026, 11, 5))
    parser.add_argument("--seed", type=int, default=20261105)
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

    count_text = git("rev-list", "--count", "HEAD", check=False)
    existing_count = int(count_text) if count_text.isdigit() else 0
    if existing_count > 1:
        print("ERROR: More than the initial disclosure commit exists. Refusing to rewrite history.", file=sys.stderr)
        return 2

    name = git("config", "user.name", check=False)
    email = git("config", "user.email", check=False)
    if not name or not email:
        print("ERROR: Configure git user.name and user.email first.", file=sys.stderr)
        return 2

    start = datetime.combine(args.start_date, time.min, tzinfo=timezone.utc)
    end_exclusive = datetime.combine(args.end_date + timedelta(days=1), time.min, tzinfo=timezone.utc)
    span = int((end_exclusive - start).total_seconds())
    rng = random.Random(args.seed)
    schedule = sorted(start + timedelta(seconds=rng.randrange(span)) for _ in range(args.count))

    print("SYNTHETIC TEST DATA — not genuine development activity.")
    print(f"Repository: {Path.cwd()}")
    print(f"Identity:   {name} <{email}>")
    print(f"Count:      {args.count:,}")
    print(f"Date range: {args.start_date} through {args.end_date} (UTC)")
    print(f"Seed:       {args.seed}")
    if args.dry_run:
        print("Dry run only; no commits were created.")
        print("First planned date:", schedule[0].isoformat())
        print("Last planned date: ", schedule[-1].isoformat())
        return 0

    print("Creating commits. This may take several minutes...")
    for index, stamp in enumerate(schedule, start=1):
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
        message = f"[SYNTHETIC TEST DATA] Generated history sample {index:05d}/{args.count:05d}"
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            env=env, stdout=subprocess.DEVNULL, check=True
        )
        if index % 500 == 0 or index == args.count:
            print(f"Created {index:,}/{args.count:,}")

    print("\nComplete. Verify with: git rev-list --count HEAD")
    print("Review the history and disclosure before manually pushing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
