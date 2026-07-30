"""
LeetCode 40: Combination Sum II
https://leetcode.com/problems/combination-sum-ii/

Problem: Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.
Each number in candidates may only be used ONCE in the combination. The solution set must
not contain duplicate combinations.

Note: candidates may contain duplicates.

Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30

Examples:
- Input: candidates = [10,1,2,7,6,1,5], target = 8
  Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

- Input: candidates = [2,5,2,1,2], target = 5
  Output: [[1,2,2],[5]]

Approach: Backtracking with sort + same-level dedupe
- Sort candidates so duplicates are adjacent and detectable in O(1)
- Track remaining target, shrinking toward zero; prune when negative
- Same-level dedupe: skip candidates[i] when i > start AND candidates[i] == candidates[i-1]
  - First occurrence at each level creates a valid branch; subsequent identical values would
    produce duplicate combinations → skip
- Single-use constraint: pass i+1 to next backtrack call (unlike LC 39 which passes i)
- Record when remaining == 0 (found a valid combination)

Time: O(n × 2^n) — at most 2^n subsets, each copied in O(n)
Space: O(n) — recursion depth (output list not counted)
"""


def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Return all unique combinations of candidates that sum to target.
    Each number may be used at most once.

    Args:
        candidates: Array of positive integers (may contain duplicates)
        target: Target sum to achieve

    Returns:
        List of unique combinations (each combination is a list of integers)
    """
    candidates.sort()
    ans: list[list[int]] = []

    def backtrack(start: int, remaining: int, sol: list[int]) -> None:
        if remaining == 0:
            ans.append(sol.copy())
            return

        if remaining < 0:
            return  # Prune

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            sol.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i], sol)
            sol.pop()

    backtrack(0, target, [])
    return ans


if __name__ == "__main__":
    # Example 1: Multiple valid combinations
    result = combination_sum2([10, 1, 2, 7, 6, 1, 5], 8)
    expected = [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert sorted(result) == sorted(expected), (
        f"Example 1 failed: got {result}, expected {expected}"
    )

    # Example 2: Candidates with duplicates
    result = combination_sum2([2, 5, 2, 1, 2], 5)
    expected = [[1, 2, 2], [5]]
    assert sorted(result) == sorted(expected), (
        f"Example 2 failed: got {result}, expected {expected}"
    )

    # Edge case: No valid combination
    result = combination_sum2([2], 1)
    expected = []
    assert result == expected, f"Edge case failed: got {result}, expected {expected}"

    print("All tests passed.")
