---
name: leetcode-quiz
description: Transform a general problem description into a LeetCode-style quiz file
---

# LeetCode Quiz Generator

Transforms a general problem description into a properly formatted quiz file following the project conventions.

## Usage

Invoke with: `/leetcode-quiz` together with a concrete problem description, or by pasting a problem description and asking to create a quiz. This skill requires a specific description to transform — it does not pick problems on its own.

For "next problem" / practice requests where no description is handed in, use the **queue-based default flow** documented in `leetcode/CLAUDE.md` ("Generating Quiz Files"), not this skill.

## What It Does

1. **Parses** the problem description to extract:
   - Problem statement (the "what")
   - Input format and parameters
   - Output format and return type
   - Constraints
   - Example test cases

2. **Generates** a quiz file with:
   - Proper docstring with problem metadata
   - Function signature matching the problem
   - `__main__` block with test cases
   - Placeholders for approach/complexity (filled after solving)

3. **Places** the file in the correct algorithm category directory

## Algorithm Categories

Auto-detects or specify:
- `simulation` - State updates, cellular automaton, multi-step processes
- `graph` - BFS/DFS, shortest path, reachability, connected components
- `two-pointers` - Array traversal with two indices
- `sliding-window` - Fixed/variable window on arrays/strings
- `binary-search` - Search on sorted arrays
- `hash-map` - Frequency counting, lookups
- `dynamic-programming` - Overlapping subproblems, optimal substructure
- `backtracking` - Combinations, permutations, exhaustive search
- `greedy` - Local optimal choices
- `linked-list` - Pointer manipulation
- `tree` - Binary trees, BST, recursion
- `heap` - Priority queue, k-th elements
- `stack` - LIFO operations, monotonic stack
- `misc` - Everything else

## Example Transformations

### Sample 1: Street Lights (Simulation)
**Original:** "Mr.Woods, an electrician for Timberland city, has made some faulty connections on eight street lights..."

**Transformed to:**
```python
"""
Street Lights State After M Days

Problem: Given initial states of street lights, simulate M days of state changes.
A light goes OFF if adjacent lights were both ON or both OFF, else ON.
End lights have one adjacent neighbor (virtual neighbor = 0).

Approach: Simulation
- Iterate M times, each time computing next state from current
- For each position, compare left and right neighbors

Time: O(M * N)   Space: O(N)
"""

def solve(n: int, current_state: list[int], days: int) -> list[int]:
    pass

if __name__ == "__main__":
    test_cases = [
        (8, [1,1,1,0,1,1,1,1], 2, [0,0,0,0,0,1,1,0]),
    ]
    # ... assertions

# solved: YYYY-MM-DD, difficulty, minutes, Street Lights
```

### Sample 2: Social Network Promo (Graph)
**Original:** "On a social networking site, each user can have a group of friends... find the userID to reach maximum walls"

**Transformed to:**
```python
"""
Optimal Promo Starter in Social Network

Problem: Find the starting user ID such that a message reaches the maximum number of users.
Friendship is directed (if A follows B, B may not follow A). A user can only share with friends who haven't received the message yet.

Approach: Graph traversal
- For each node, run BFS/DFS to count reachable nodes
- Return the node with maximum reach

Time: O(N * (V + E))   Space: O(V + E)
"""

def solve(users: int, edges: list[tuple[int, int]]) -> int:
    pass

if __name__ == "__main__":
    test_cases = [
        (4, [(0,1), (1,2), (2,1)], 0),  # Starting from 0 reaches most users
    ]
    # ... assertions

# solved: YYYY-MM-DD, difficulty, minutes, Social Network Promo
```

## Convention Checklist

Generated files follow:
- **File naming:** `{problem_number}_{slug}.py` (problem_number can be sequential in local queue)
- **Directory:** `leetcode/algorithms/<category>/`
- **No hints included** — just the problem description and test cases
- **Placeholder for approach/complexity** — solver fills after solving
- **Solved comment** at end — filled after completion

## Notes

- The skill infers the category from the problem type
- Test cases are extracted from the examples in the description
- Edge cases from constraints are added to test cases when possible
