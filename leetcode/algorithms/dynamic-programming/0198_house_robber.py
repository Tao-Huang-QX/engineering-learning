"""
LeetCode 198: House Robber
https://leetcode.com/problems/house-robber/

Problem: You are a robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

Approach: 1D DP take/skip
- At each house, decide: rob it (add to best from i-2) or skip it (take best from i-1)
- prev and prev_prev store the best sum achieveable up to previous houses

Time: O(n)   Space: O(1)
"""


def rob(nums: list[int]) -> int:
    """
    Calculate the maximum amount that can be robbed without alerting police.

    Args:
        nums: List of integers representing money in each house

    Returns:
        Maximum amount that can be robbed
    """
    prev_prev = prev = 0
    for num in nums:
        current = max(num + prev_prev, prev)
        prev, prev_prev = current, prev
    return prev


if __name__ == "__main__":
    # Example 1
    assert rob([1, 2, 3, 1]) == 4

    # Example 2
    assert rob([2, 7, 9, 3, 1]) == 12

    # Example 3: Single house
    assert rob([5]) == 5

    # Example 4: Two houses
    assert rob([1, 2]) == 2

    # Example 5: All same value
    assert rob([2, 2, 2, 2]) == 4

    print("All tests passed.")
