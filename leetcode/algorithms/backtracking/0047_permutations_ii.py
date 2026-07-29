"""
LeetCode 47: Permutations II
https://leetcode.com/problems/permutations-ii/

Problem: Given a collection of numbers nums that might contain duplicates,
return all possible unique permutations. You can return the answer in any order.

Constraints:
- 1 <= nums.length <= 8
- -10 <= nums[i] <= 10

Examples:
- Input: nums = [1,1,2]
  Output: [[1,1,2],[1,2,1],[2,1,1]]
- Input: nums = [1,2,3]
  Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Approach: Backtracking with sort + dedupe
- Sort nums first so duplicates are adjacent and detectable in O(1)
- Same backtracking structure as Permutations (LC 46): used[] array, choose/explore/unchoose
- Dedupe rule: skip nums[i] when nums[i] == nums[i-1] AND used[i-1] is False
  - If used[i-1] is True, we're deeper in a branch that already committed to that value → valid
  - If used[i-1] is False, picking the current duplicate would create an identical branch → skip
- Base case: when solution length equals input length, record the permutation

Time: O(n × n!) — n! permutations, each copied in O(n)
Space: O(n) — recursion depth + used array (output list not counted)
"""


def permute_unique(nums: list[int]) -> list[list[int]]:
    """
    Return all possible unique permutations of nums (may contain duplicates).

    Args:
        nums: Array of integers (may contain duplicates)

    Returns:
        List of all unique permutations (any order)
    """
    if len(nums) == 1:
        return [nums.copy()]

    nums.sort()
    ans: list[list[int]] = []
    used = [False] * len(nums)

    def backtrack(sol: list[int]) -> None:
        if len(sol) == len(nums):
            ans.append(sol.copy())
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # Skip: if same as previous and previous wasn't chosen at this level
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            used[i] = True
            sol.append(nums[i])
            backtrack(sol)
            sol.pop()
            used[i] = False

    backtrack([])
    return ans


if __name__ == "__main__":
    # Example 1: Contains duplicates
    ans = permute_unique([1, 1, 2])
    expected = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    assert sorted(ans) == sorted(expected), f"Example 1 failed: got {ans}, expected {expected}"

    # Example 2: All distinct (should match regular permutations)
    ans = permute_unique([1, 2, 3])
    expected = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert sorted(ans) == sorted(expected), f"Example 2 failed: got {ans}, expected {expected}"

    # Edge case: Single element
    ans = permute_unique([1])
    expected = [[1]]
    assert ans == expected, f"Single element failed: got {ans}, expected {expected}"

    print("All tests passed.")
