# GitHub Synthetic History

> **Synthetic test data — not genuine development activity.**

This repository contains a small utility for learning about Git commit timestamps and testing history-processing tools. Generated commits are empty, backdated, and labelled `[SYNTHETIC TEST DATA]`. They must never be presented as evidence of work performed during those dates or used to misrepresent a GitHub contribution record.

## What it does

- Generates a configurable number of empty Git commits for local testing.
- Assigns reproducible, chronologically ordered author and committer timestamps.
- Labels every generated commit with `[SYNTHETIC TEST DATA]`.
- Supports a dry run before writing commits.
- Does not push automatically.

## Requirements

- Git 2.30+
- Python 3.9+
- A Git identity configured locally (`git config user.name` and `git config user.email`).

## Quick start

Clone this repository:

```bash
git clone https://github.com/akhilalladi-code/github-synthetic-history.git
cd github-synthetic-history
```

Preview a small test schedule without creating commits:

```bash
python scripts/generate_history.py --count 10 --start-date 2026-01-01 --end-date 2026-01-10 --dry-run
```

For a local-only test, use a small count and a disposable clone. Review the script's options before executing it.

## Verify local test data

Count labelled synthetic commits:

```bash
git log --format=%s | grep -c '^\[SYNTHETIC TEST DATA\]'
```

Inspect the author and timestamps:

```bash
git log -5 --format='Author: %an <%ae>%nDate: %aI%nSubject: %s'
```

## Publishing policy

**Do not push generated synthetic history to the public repository's default branch.** Keep generated test commits in a disposable local clone or a clearly isolated test branch that is not used to represent genuine project activity. The public default branch is intended to contain the generator, documentation, and genuine project changes only.

GitHub applies its own eligibility rules to contribution activity. Synthetic or backdated commits are not genuine contributions and must not be used to imply work that was not performed.

## Safety and scope

- The generator is intended for testing, demonstrations, and learning Git history behavior.
- Generated commits are empty and explicitly labelled as synthetic.
- A fixed seed makes the date schedule reproducible.
- Use a disposable clone; do not run synthetic-history generation in a real project repository.
