"""
LeetCode 494: Target Sum
https://leetcode.com/problems/target-sum/

Problem: You are given an integer array nums and an integer target. You want to
build an expression out of nums by adding one of the symbols '+' and '-' before
each integer in nums and then concatenate all the integers. Return the number of
different expressions that evaluate to target.

Constraints:
- 1 <= nums.length <= 20
- 0 <= nums[i] <= 1000
- 0 <= sum(nums[i]) <= 1000
- -1000 <= target <= 1000

Examples:
- Input: nums = [1,1,1,1,1], target = 3
  Output: 5
  Explanation: -1+1+1+1+1 = 3, +1-1+1+1+1 = 3, +1+1-1+1+1 = 3,
               +1+1+1-1+1 = 3, +1+1+1+1-1 = 3

- Input: nums = [1], target = 1
  Output: 1

Approach: Subset sum DP (reduce from +/- to subset selection)
- Derivation: S_pos + S_neg = total, S_pos - S_neg = target → S_pos = (total + target) / 2
- Guard: |target| > total impossible; odd parity makes S_pos non-integer
- dp[j] = number of subsets that sum to j (0/1 knapsack counting)
- For each num, iterate j backwards: dp[j] = dp[j] + dp[j - num] (skip + take)

Time: O(n * S_pos) — worst case S_pos = total ≤ 1000
Space: O(S_pos) — 1D DP array
"""


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    Return the number of ways to assign + and - to reach target.

    Args:
        nums: Array of non-negative integers
        target: Target sum for the expression

    Returns:
        Number of different expressions that evaluate to target
    """
    total = sum(nums)
    if total < abs(target) or (total + target) % 2 == 1:
        return 0

    s_pos = (total + target) // 2
    dp = [0] * (s_pos + 1)
    dp[0] = 1

    for num in nums:
        for j in range(s_pos, num - 1, -1):
            dp[j] = dp[j] + dp[j - num]

    return dp[s_pos]


if __name__ == "__main__":
    # Example 1
    result1 = find_target_sum_ways([1, 1, 1, 1, 1], 3)
    expected1 = 5
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = find_target_sum_ways([1], 1)
    expected2 = 1
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
