"""
LeetCode 1: Two Sum
https://leetcode.com/problems/two-sum/

Problem: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Approach:
- dict to store the number in the key and the lookup operation in O(1)
- safety: return an empty list

Time: O(n)   Space: O(n)
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Return indices of the two numbers that add up to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of two indices whose values sum to target
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (nums, target, expected_output)
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]

    for nums, target, expected in test_cases:
        result = two_sum(nums, target)
        # Order doesn't matter for indices
        assert sorted(result) == sorted(expected), (
            f"{nums}, target={target}: got {result}, expected {expected}"
        )

    print("All tests passed.")
