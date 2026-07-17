"""
LeetCode 78: Subsets
https://leetcode.com/problems/subsets/

Problem: Given an integer array nums of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets. You may return
the solution in any order.

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All elements of nums are unique

Examples:
- Input: nums = [1,2,3]
  Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
- Input: nums = [0]
  Output: [[],[0]]

Approach: Backtracking
- At each position, decide to include or exclude the current element
- Only look forward (start index) to avoid duplicate subsets
- Record every partial path — even incomplete ones are valid subsets

Time: O(2^n × n) — 2^n subsets, each copied in O(n)   Space: O(n) recursion depth
"""


def subsets(nums: list[int]) -> list[list[int]]:
    """
    Return all possible subsets (power set) of the given unique integers.

    Args:
        nums: Array of unique integers

    Returns:
        List of all subsets (any order, no duplicates)
    """
    ans = []

    def backtrack(start: int, sol: list[int]):
        ans.append(sol.copy())

        for i in range(start, len(nums)):
            # Choose
            sol.append(nums[i])

            # Explore
            backtrack(i + 1, sol)

            # Unchoose (backtrack)
            sol.pop()

    backtrack(0, [])
    return ans


if __name__ == "__main__":
    # Example 1: Three elements
    result = subsets([1, 2, 3])
    expected = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    assert sorted(result) == sorted(expected), (
        f"Example 1 failed: got {result}, expected {expected}"
    )

    # Example 2: Single element
    result = subsets([0])
    expected = [[], [0]]
    assert sorted(result) == sorted(expected), (
        f"Example 2 failed: got {result}, expected {expected}"
    )

    print("All tests passed.")
