![SYNTHETIC HISTORY — Diwali 2026](./assets/diwali-banner.svg)

<p align="center"><a href="https://akhilalladi-code.github.io/diwali-universe/"><strong>🪔 Explore Diwali Universe 2026 · Interactive celebration ↗</strong></a></p>

# GitHub Synthetic History

> **Synthetic test data — not genuine development activity.**

This repository contains a small utility for learning about Git commit timestamps and testing history-processing tools. Generated commits are empty, backdated, and labelled `[SYNTHETIC TEST DATA]`. They must never be presented as evidence of work performed during those dates or used to misrepresent a GitHub contribution record.

## What it does

- Generates a configurable number of empty Git commits for local testing.
- Assigns reproducible, chronologically ordered author and committer timestamps.
- Uses the configured Git identity and rejects obvious placeholder identities.
- Requires an isolated branch whose name starts with `synthetic-test-`.
- Labels every generated commit with `[SYNTHETIC TEST DATA]`.
- Supports a dry run before writing commits.
- Does not push automatically.

## Requirements

- Git 2.30+
- Python 3.9+
- A real Git identity configured locally (`git config user.name` and `git config user.email`). Use an email verified on your GitHub account if you want GitHub to associate the author identity with your account.

## Quick start

Clone this repository:

```bash
git clone https://github.com/akhilalladi-code/github-synthetic-history.git
cd github-synthetic-history
```

Configure your identity (replace the example email with your own verified email):

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

Create an isolated test branch. Do not generate synthetic history on `main`:

```bash
git switch -c synthetic-test-local
```

Preview a small test schedule without creating commits:

```bash
python scripts/generate_history.py --count 10 --start-date 2026-01-01 --end-date 2026-01-10 --dry-run
```

After reviewing the dry-run identity and schedule, you may execute a small local test:

```bash
python scripts/generate_history.py --count 10 --start-date 2026-01-01 --end-date 2026-01-10 --execute
```

Use a disposable clone for larger tests. The generator refuses to run on `main` or any branch not prefixed with `synthetic-test-`.

## Verify local test data

Count labelled synthetic commits:

```bash
git log --format=%s | grep -c '^\[SYNTHETIC TEST DATA\]'
```

Inspect author, committer, timestamps, and subjects:

```bash
git log -5 --format='Author: %an <%ae>%nCommitter: %cn <%ce>%nDate: %aI%nSubject: %s'
```

## Publishing policy

Synthetic history is for testing and demonstrations. Keep it isolated from the default branch. If you publish a test branch, name and describe it clearly as synthetic test data; do not merge it into the default branch or present it as genuine project activity.

GitHub applies its own eligibility rules to contribution activity. Correct author metadata does not make synthetic or backdated commits genuine contributions, and such commits should not be used to imply work that was not performed.

## Safety and scope

- The generator is intended for testing, demonstrations, and learning Git history behavior.
- Generated commits are empty and explicitly labelled as synthetic.
- A fixed seed makes the date schedule reproducible.
- Use a disposable clone; do not run synthetic-history generation in a real project repository.
- The script never pushes automatically.
