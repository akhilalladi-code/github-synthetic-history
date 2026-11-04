# GitHub Synthetic History

> **Synthetic test data — not genuine development activity.**

This repository demonstrates Git commit-history and date handling. Generated commits are intentionally empty, backdated, and labelled as synthetic. They must not be represented as evidence of work performed during those dates.

## What it does

- Generates a configurable number of empty Git commits.
- Assigns reproducible, chronologically ordered author and committer timestamps.
- Labels every generated commit with `[SYNTHETIC TEST DATA]`.
- Operates only in this dedicated repository.
- Supports a dry run before writing commits.
- Does not push automatically.

## Requirements

- Git 2.30+
- Python 3.9+
- A Git identity configured locally (`git config user.name` and `git config user.email`).
- Use an email address verified on your GitHub account if you want commits attributed to that account.

## Quick start

Clone this repository:

```bash
git clone https://github.com/akhilalladi-code/github-synthetic-history.git
cd github-synthetic-history
```

Preview the requested 20,000-commit schedule (no commits are created):

```bash
python scripts/generate_history.py --count 20000 \
  --start-date 2021-01-01 --end-date 2026-11-05 --dry-run
```

Generate the synthetic commits locally:

```bash
python scripts/generate_history.py --count 20000 \
  --start-date 2021-01-01 --end-date 2026-11-05 --execute
```

The generator permits this repository's one initial disclosure commit and refuses to run if it already contains more than one commit. It never modifies other repositories.

## Verify before publishing generated history

```bash
git rev-list --count HEAD
git log --oneline --decorate -5
```

The expected total after generation is 20,001 commits: one disclosure commit plus 20,000 labelled synthetic commits.

The generated history remains local until you explicitly run:

```bash
git push origin main
```

Review the output and disclosure before pushing.

## GitHub contribution graph

GitHub applies its own eligibility rules to contribution activity, including author email association, repository visibility/settings, and the default branch. Backdated commits do not guarantee contribution-graph entries. Synthetic history is not a substitute for genuine contributions and must not be represented as such.

## Safety and scope

- No existing repository is modified.
- Generated commits do not change tracked files.
- Every generated commit message is visibly labelled synthetic.
- A fixed seed makes the date schedule reproducible.
- Intended for testing, demonstrations, and learning Git history behavior.
