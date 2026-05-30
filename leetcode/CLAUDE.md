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

## Problem Queue

Work through in order. Check off as completed.

| # | LC | Problem | Diff | Pattern |
|---|-----|---------|------|---------|
| 1 | 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | E | Hash map complement |
| 2 | 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | E | One pass, running min |
| 3 | 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | E | Set membership |
| 4 | 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | E | Frequency map / Counter |
| 5 | 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | M | Hash key from sorted tuple |
| 6 | 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | M | Prefix/suffix |
| 7 | 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | E | Two pointers |
| 8 | 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | E | Read/write two pointers |
| 9 | 15 | [3Sum](https://leetcode.com/problems/3sum/) | M | Sort + two pointers + dedupe |
| 10 | 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | E | Stack matching |
| 11 | 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | E | Bisect template |
| 12 | 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | M | Modified binary search |
| 13 | 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | E | Iterative pointer flip |
| 14 | 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | E | Dummy head merge |
| 15 | 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | E | Floyd slow/fast |
| 16 | 104 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | E | Recursive DFS |
| 17 | 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | M | BFS with deque |
| 18 | 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | E | DFS swap children |
| 19 | 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | M | Grid flood fill |
| 20 | 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | M | Graph cycle / topo BFS |
| 21 | 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | M | Sliding window |
| 22 | 567 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | M | Fixed-size sliding window |
| 23 | 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | M | Monotonic stack |
| 24 | 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | M | heapq size-k |
| 25 | 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | M | Kadane |
| 26 | 198 | [House Robber](https://leetcode.com/problems/house-robber/) | M | 1D DP take/skip |
| 27 | 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | E | Fibonacci-style DP |
| 28 | 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | M | Unbounded knapsack DP |
| 29 | 133 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | M | BFS/DFS + clone map |
| 30 | 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | M | Counter + heap/bucket |

**Hard (after queue 1–30):** 42, 23, 76, 295, 124, 127 — only when the parent pattern is solid.

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
# solved: 2026-05-18, easy, 25min, Two Sum
# solved: 2026-05-18, easy, 25min, Best Time
# solved: 2026-05-19, easy, 15min, Contains Dup
# solved: 2026-05-19, easy, 15min, Valid Anagram
# solved: 2026-05-19, medium, 30min, Group Anagrams
# solved: 2026-05-20, medium, 45min, Product of Array Expect Self
# solved: 2026-05-20, easy, 15min, Valid Palindrome
# solved: 2026-05-20, easy, 15min, Move Zeros
# solved: 2026-05-22, medium, 30min, 3Sum
# solved: 2026-05-22, easy, 15min, Valid Parentheses
# solved: 2026-05-22, easy, 30min, Binary Search
# solved: 2026-05-22, medium, 45min, Search in Rotated Sorted Array
# solved: 2026-05-23, easy, 30min, Reverse Linkied List
# sloved: 2026-05-23, easy, 25min, Merge Two Sorted Lists
# sloved: 2026-05-23, easy, 25min, Linked List Cycle
# solved: 2026-05-24, easy, 60min, Maximum Depth of Binary Tree
# solved: 2026-05-24, medium, 60min, Binary Tree Level Order Traversal
# solved: 2026-05-24, easy, 15min, Invert Binary Tree
# solved: 2026-05-24, medium, 40min, Number of Islands
# solved: 2026-05-25, medium, 60min, Course Schedule
# solved: 2026-05-25, medium, 40min, Longest Substring Without Repeating Characters
# solved: 2026-05-25, medium, 60min, Permutation in String
# solved: 2026-05-26, medium, 30min, Daily Temperatures
# solved: 2026-05-26, medium, 30min, Kth Largest Element in an Array
# solved: 2026-05-29, medium, 30min, Maximum Subarray
# solved: 2026-05-29, medium, 30min, House Robber
# solved: 2026-05-29, medium, 30min, Climbing Stairs
# solved: 2026-05-29, medium, 60min, Coin Change
```

Update the queue table above by marking completed rows (e.g. prefix with `x` in the # column).
