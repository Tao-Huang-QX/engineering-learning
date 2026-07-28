"""
LeetCode 300: Longest Increasing Subsequence
https://leetcode.com/problems/longest-increasing-subsequence/

Problem: Given an integer array nums, return the length of the longest strictly increasing subsequence.

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

Examples:
- Input: nums = [10,9,2,5,3,7,101,18]
  Output: 4
  Explanation: The longest increasing subsequence is [2,3,7,101].

- Input: nums = [0,1,0,3,2,3]
  Output: 4

- Input: nums = [7,7,7,7,7,7,7]
  Output: 1

Follow up: Can you come up with an algorithm that runs in O(n log n) time complexity?

Approach: Patience Sorting with Binary Search
- tails[i] stores the smallest tail of all increasing subsequences of length i+1
- For each num: binary search to find first tail >= num (lower_bound)
- If num > all tails: append (found longer subsequence)
- Else: replace tails[pos] with num (keeps tails minimal, maximizing room for future elements)
- tails array is always sorted, enabling binary search

Time: O(n log n)   Space: O(n)
"""


def length_of_lis(nums: list[int]) -> int:
    """
    Return the length of the longest strictly increasing subsequence.

    Args:
        nums: Input array of integers

    Returns:
        Length of the longest strictly increasing subsequence
    """
    """
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)
    """
    # tails[i] = smallest tail of all increasing subsequences of length i+1
    tails: list[int] = []
    for num in nums:
        # Binary search: find first tail >= num
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid

        # If num is larger than all tails, extend
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num

    return len(tails)


if __name__ == "__main__":
    # Example 1: [10,9,2,5,3,7,101,18] → 4
    # LIS is [2,3,7,101]
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # Example 2: [0,1,0,3,2,3] → 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4

    # Example 3: [7,7,7,7,7,7,7] → 1
    # All elements equal, longest increasing subsequence is any single element
    assert length_of_lis([7, 7, 7, 7, 7, 7, 7]) == 1

    # Edge case: single element
    assert length_of_lis([1]) == 1

    # Edge case: already increasing
    assert length_of_lis([1, 2, 3, 4, 5]) == 5

    # Edge case: decreasing
    assert length_of_lis([5, 4, 3, 2, 1]) == 1

    print("All tests passed.")
