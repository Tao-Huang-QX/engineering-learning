"""
LeetCode 209: Minimum Size Subarray Sum
https://leetcode.com/problems/minimum-size-subarray-sum/

Problem: Given an array of positive integers nums and a positive integer target,
return the minimal length of a subarray whose sum is greater than or equal to target.
If there is no such subarray, return 0.

Approach: Sliding window
- Expand window by adding elements from right
- When sum >= target, shrink from left while condition holds
- Track minimal length throughout

Time: O(n)   Space: O(1)
"""


def min_sub_array_len(target: int, nums: list[int]) -> int:
    """
    Return the minimal length of a subarray with sum >= target.

    Args:
        target: Target sum to reach or exceed
        nums: List of positive integers

    Returns:
        Minimal subarray length, or 0 if no such subarray exists
    """
    min_len = float("inf")
    left = 0
    curr_sum = 0

    for right in range(len(nums)):
        curr_sum += nums[right]

        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            curr_sum -= nums[left]
            left += 1

    return min_len if min_len != float("inf") else 0  # pyright: ignore[reportReturnType]


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (target, nums, expected_length)
        (7, [2, 3, 1, 2, 4, 3], 2),  # [4,3] is the minimal subarray
        (4, [1, 4, 4], 1),  # [4] is the minimal subarray
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),  # No subarray sums to 11
    ]

    for target, nums, expected in test_cases:
        result = min_sub_array_len(target, nums)
        assert result == expected, (
            f"target={target}, nums={nums}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Minimum Size Subarray Sum
