"""
LeetCode 416: Partition Equal Subset Sum
https://leetcode.com/problems/partition-equal-subset-sum/

Problem: Given an integer array nums, return true if you can partition the array
into two subsets such that the sum of the elements in both subsets is equal, or
false otherwise.

Constraints:
- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100

Examples:
- Input: nums = [1,5,11,5]
  Output: true
  Explanation: The array can be partitioned as [1,5,5] and [11].

- Input: nums = [1,2,3,5]
  Output: false
  Explanation: The array cannot be partitioned into equal sum subsets.

Approach: 0/1 knapsack DP (subset sum)
- Reduce: partition into two equal sums → find subset that sums to total/2
- If total is odd, impossible immediately
- dp[j] = True if some subset of nums seen so far sums to j
- For each num, iterate j backwards from target to num:
  dp[j] = dp[j] or dp[j - num]  (take or skip)
- Backwards iteration ensures each number is used at most once

Time: O(n * target) — n=200, target ≤ 10000, ~2M operations
Space: O(target) — 1D DP array
"""


def can_partition(nums: list[int]) -> bool:
    """
    Return True if nums can be partitioned into two equal-sum subsets.

    Args:
        nums: Array of positive integers

    Returns:
        True if equal-sum partition exists
    """
    total = sum(nums)

    # Odd total can't be split into two equad halves
    if total % 2 == 1:
        return False

    target = total // 2
    dp = [False] * (total + 1)
    dp[0] = True  # empty subset sums to 0

    for num in nums:  # outer loop: items
        for j in range(target, num - 1, -1):  # inner: capacities, backwards
            dp[j] = dp[j] or dp[j - num]

    return dp[target]


if __name__ == "__main__":
    # Example 1
    result1 = can_partition([1, 5, 11, 5])
    expected1 = True
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = can_partition([1, 2, 3, 5])
    expected2 = False
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
