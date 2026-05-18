# LeetCode Practice

## Language
Python 3. Solutions must be self-contained and runnable.

## File Naming
`{problem_number}_{slug}.py` — e.g., `0001_two_sum.py`

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
After solving, add a one-line entry to the `solved` section so Claude can track progress:

```python
# solved: 2024-XX-XX, medium, 25min, two-pointer
```
