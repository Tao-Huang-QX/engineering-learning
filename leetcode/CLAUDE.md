# LeetCode Practice

## Environment

Activate the project virtualenv at the start of every session:

```bash
pyenv activate engineering-learning
```

## Python Tooling

- **Linting/Formatting:** `ruff` (replaces flake8/black/pylint)
- Run lint: `ruff check .`
- Auto-format: `ruff format .`
- Config: `pyproject.toml` in project root

Run solutions from this directory, e.g. `python algorithms/hash-map/0001_two_sum.py`.

## Language

Python 3. Solutions must be self-contained and runnable.

## Learning Approach

Accelerated, pattern-first practice — not a phased data-structure syllabus.

- **Difficulty:** Easy + Medium mixed from the start; add Hard after ~25–30 core problems (only when the pattern is already familiar).
- **Session loop:** read problem → name the pattern → attempt (15–25 min Easy, 25–40 min Medium) → review → one-line takeaway ("when I see X, try Y").
- **Placement:** file by **primary technique/pattern**, not by data-structure topic.
- **Pace target:** 4–6 problems per week with review.

## Learning Roadmap Reference

Following [labuladong's algorithm roadmap](https://labuladong.online/zh/roadmap/algo/) for systematic pattern-based learning:

**Core Philosophy:**
- Framework thinking — Learn patterns, not just individual problems
- Two fundamental storage: Array (sequential) and Linked List (chained)
- All other structures are combinations or abstractions of these two

**Resources:**
- [labuladong 网站题目列表](https://leetcode.cn/problem-list/59jEaTgw/) — Official LeetCode problem list
- [labuladong/fucking-algorithm GitHub](https://github.com/labuladong/fucking-algorithm) — 60+ articles, framework-based approach

## Problem Queue

See [QUEUE.md](QUEUE.md) for the full 96-problem roadmap following labuladong's pattern-based learning.

## Progress Tracking

See [PROGRESS.md](PROGRESS.md) for completion history and stats.

## File Naming

`{problem_number}_{slug}.py` — e.g., `0001_two_sum.py`

## Auto-Generate Problem Files

**Convention:** When starting a new quiz, Claude automatically generates the problem file.

**Template structure:**
- Docstring with problem metadata (number, title, URL, description)
- Empty `solve()` function matching LeetCode signature
- `__main__` block with all test cases from problem description
- Approach/complexity sections left as placeholders (fill after solving)

**Example:**
```python
def solve(nums: list[int], target: int) -> list[int]:
    """Return indices of the two numbers that add up to target."""
    pass
```

This removes setup friction and lets you focus on solving.

## Claude's Role: Quiz Workflow

**Strict problem-first approach:**

1. **New quiz:** Create problem file + provide problem description only
2. **NO hints or solutions** unless explicitly asked
3. **Wait for user to:**
   - Attempt the problem independently
   - Ask for a hint → Provide a small hint
   - Ask for solution → Explain approach
   - Submit code for review → Review their code

**Important:** Don't jump into teaching mode or provide unsolicited hints. Let the user attempt first.

## Directory Placement

- Technique-based problems → `algorithms/<technique>/`
- Data structure implementations → `data-structures/<structure>/`
- If a problem fits multiple categories, pick the primary technique and add a cross-reference comment at the top

## Solution Template

Every file starts with this docstring:

```python
"""
LeetCode {number}: {title}
https://leetcode.com/problems/{slug}/

Problem: {one-line description}

Approach: {technique name}
- {key insight 1}
- {key insight 2}

Time: O(...)   Space: O(...)
"""
```

Include a `__main__` block with test cases or use the standard test runner from `templates/python/`.

## Review Checklist

- [ ] Edge cases covered (empty input, single element, duplicates, extremes)
- [ ] Time and space complexity stated and correct
- [ ] Variable names are descriptive (no `i`, `j` unless they're trivial loop indices)
- [ ] No unnecessary optimizations — correct first, fast second
- [ ] Pattern matches the directory it's placed in

## Problem Tracking

After solving, add a one-line entry at the bottom of the solution file:

```python
# solved: YYYY-MM-DD, difficulty, minutes, Problem Name
```

Update [PROGRESS.md](PROGRESS.md) with the completion.
