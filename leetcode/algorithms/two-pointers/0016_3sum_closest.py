"""
LeetCode 16: 3Sum Closest
https://leetcode.com/problems/3sum-closest/

Problem: Given an integer array nums and a target, find three integers in nums whose
sum is closest to the target. Return the sum of the three integers.

Approach: Two pointers
- Sort array first
- Fix one element, use two pointers for remaining two
- Track closest sum by comparing absolute differences

Time: O(n²)   Space: O(1)
"""


def three_sum_closest(nums: list[int], target: int) -> int:
    """
    Return the sum of three integers in nums that is closest to target.

    Args:
        nums: List of integers
        target: Target sum to approach

    Returns:
        The sum of three integers closest to target
    """
    nums.sort()
    result = nums[0] + nums[1] + nums[2]

    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1

        while left < right:
            curr = nums[i] + nums[left] + nums[right]
            result = curr if abs(curr - target) < abs(result - target) else result

            if curr == target:
                return curr
            elif curr < target:
                left += 1
            else:
                right -= 1
    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (nums, target, expected_closest_sum)
        ([-1, 2, 1, -4], 1, 2),
        ([0, 0, 0], 1, 0),
    ]

    for nums, target, expected in test_cases:
        result = three_sum_closest(nums, target)
        assert result == expected, (
            f"nums={nums}, target={target}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, 3Sum Closest
