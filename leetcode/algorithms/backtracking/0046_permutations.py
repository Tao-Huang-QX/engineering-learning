"""
LeetCode 46: Permutations
https://leetcode.com/problems/permutations/

Problem: Given an array nums of distinct integers, return all possible permutations.
You can return the answer in any order.

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All elements of nums are distinct

Examples:
- Input: nums = [1,2,3]
  Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
- Input: nums = [0,1]
  Output: [[0,1],[1,0]]
- Input: nums = [1]
  Output: [[1]]

Approach: Backtracking
- Build permutations by choosing one unused element at a time
- Track used elements to avoid duplicates in current solution
- When solution length equals input length, record the permutation
- Backtrack by undoing the choice (pop + unmark) to try next option

Time: O(n × n!) — n! permutations, each requires O(n) to copy into result
Space: O(n) — recursion depth n + used array (output list not counted)
"""


def permute(nums: list[int]) -> list[list[int]]:
    """
    Return all possible permutations of the given distinct integers.

    Args:
        nums: Array of distinct integers

    Returns:
        List of all permutations (any order)
    """
    if len(nums) == 1:
        return [nums.copy()]

    ans = []
    used = [False] * len(nums)

    def backtrack(sol: list[int]):
        # Base case: path is complete when it has all elements
        if len(sol) == len(nums):
            ans.append(sol.copy())
            return

        for i in range(len(nums)):
            if not used[i]:
                # Choose
                used[i] = True
                sol.append(nums[i])

                # Explore
                backtrack(sol)

                # Unchoose (backtrack)
                sol.pop()
                used[i] = False

    backtrack([])
    return ans


if __name__ == "__main__":
    # Example 1: Three distinct numbers
    ans = permute([1, 2, 3])
    expected = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert sorted(ans) == sorted(expected), f"Example 1 failed: got {ans}, expected {expected}"

    # Example 2: Two elements
    ans = permute([0, 1])
    expected = [[0, 1], [1, 0]]
    assert sorted(ans) == sorted(expected), f"Example 2 failed: got {ans}, expected {expected}"

    # Example 3: Single element
    ans = permute([1])
    expected = [[1]]
    assert ans == expected, f"Example 3 failed: got {ans}, expected {expected}"

    print("All tests passed.")
