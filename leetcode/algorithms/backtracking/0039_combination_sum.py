"""
LeetCode 39: Combination Sum
https://leetcode.com/problems/combination-sum/

Problem: Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen numbers sum
to target. You may return the combinations in any order. The same number may be chosen
from candidates an unlimited number of times.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40

Examples:
- Input: candidates = [2,3,6,7], target = 7
  Output: [[2,2,3],[7]]
- Input: candidates = [2,3,5], target = 8
  Output: [[2,2,2,2],[2,3,3],[3,5]]
- Input: candidates = [2], target = 1
  Output: []

Approach: Backtracking
- Track remaining target, shrinking toward zero
- Pass same index i to allow unlimited reuse of current candidate
- Move forward via start index to avoid duplicate combinations
- Prune branches when remaining goes negative

Time: O(N^(Target/min)) — N candidates, depth bounded by Target/min(candidate), exponential worst case
Space: O(Target/min) — recursion depth when using smallest candidate repeatedly
"""


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Return all unique combinations of candidates that sum to target.
    Each number may be used unlimited times.

    Args:
        candidates: Array of distinct positive integers
        target: Target sum to achieve

    Returns:
        List of unique combinations (each combination is a list of integers)
    """
    ans = []

    def backtrack(start: int, remaining: int, sol: list[int]):
        if remaining == 0:
            ans.append(sol.copy())
            return
        if remaining < 0:
            return  # Prune

        for i in range(start, len(candidates)):
            # Choose
            sol.append(candidates[i])

            # Explore
            backtrack(i, remaining - candidates[i], sol)

            # Unchoose (backtrack)
            sol.pop()

    backtrack(0, target, [])
    return ans


if __name__ == "__main__":
    # Example 1: Standard case with multiple combinations
    result = combination_sum([2, 3, 6, 7], 7)
    expected = [[2, 2, 3], [7]]
    assert sorted(result) == sorted(expected), (
        f"Example 1 failed: got {result}, expected {expected}"
    )

    # Example 2: Multiple ways to reach target
    result = combination_sum([2, 3, 5], 8)
    expected = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert sorted(result) == sorted(expected), (
        f"Example 2 failed: got {result}, expected {expected}"
    )

    # Example 3: No valid combination
    result = combination_sum([2], 1)
    expected = []
    assert result == expected, f"Example 3 failed: got {result}, expected {expected}"

    print("All tests passed.")
