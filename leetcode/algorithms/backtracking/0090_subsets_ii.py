"""
LeetCode 90: Subsets II
https://leetcode.com/problems/subsets-ii/

Problem: Given an integer array nums that may contain duplicates, return all possible
subsets (the power set). The solution set must not contain duplicate subsets. You may
return the answer in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10

Examples:
- Input: nums = [1,2,2]
  Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
- Input: nums = [0]
  Output: [[],[0]]

Approach: Backtracking with sort + same-level dedupe
- Sort nums first so duplicates are adjacent and detectable in O(1)
- Same backtracking structure as Subsets (LC 78): start index, choose/explore/unchoose
- Dedupe rule: skip nums[i] when i > start AND nums[i] == nums[i-1]
  - The first occurrence at each level creates a valid branch
  - Subsequent identical values at the same level would produce duplicate subsets → skip
  - When recursing deeper (start = i+1), the first duplicate at that level is again valid
- Record every partial path — each node in the decision tree is a valid subset
- No visited array needed — the start index already prevents reusing elements

Time: O(n × 2^n) — 2^n subsets in worst case, each copied in O(n)
Space: O(n) — recursion depth (output list not counted)
"""


def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Return all possible unique subsets of nums (may contain duplicates).

    Args:
        nums: Array of integers (may contain duplicates)

    Returns:
        List of all unique subsets (any order)
    """
    nums.sort()
    ans: list[list[int]] = []

    def backtrack(start: int, sol: list[int]) -> None:
        ans.append(sol.copy())

        for i in range(start, len(nums)):
            # Skip duplicate at this level: if same as previous and previous
            # wasn't picked at this level (i > start means it's a sibling, not the first pick)
            if i > start and nums[i] == nums[i - 1]:
                continue

            sol.append(nums[i])
            backtrack(i + 1, sol)
            sol.pop()

    backtrack(0, [])
    return ans


if __name__ == "__main__":
    # Example 1: Contains duplicates
    result = subsets_with_dup([1, 2, 2])
    expected = [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    assert sorted(result) == sorted(expected), (
        f"Example 1 failed: got {result}, expected {expected}"
    )

    # Example 2: Single element
    result = subsets_with_dup([0])
    expected = [[], [0]]
    assert sorted(result) == sorted(expected), (
        f"Example 2 failed: got {result}, expected {expected}"
    )

    # Edge case: All duplicates
    result = subsets_with_dup([1, 1, 1])
    expected = [[], [1], [1, 1], [1, 1, 1]]
    assert sorted(result) == sorted(expected), (
        f"All duplicates failed: got {result}, expected {expected}"
    )

    print("All tests passed.")
