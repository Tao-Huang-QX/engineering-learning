"""
LeetCode 154: Find Minimum in Rotated Sorted Array
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Problem: Given a rotated sorted array with duplicates, find the minimum element.

Approach: Modified binary search
- When nums[left] == nums[right], can't determine sorted half—shrink by 1 from each end
- When nums[left] > nums[right], pivot is in right half—search right
- When nums[left] < nums[right], window is sorted—leftmost is minimum (early exit)

Time: O(log n) average, O(n) worst (all duplicates)   Space: O(1)
"""


def find_min(nums: list[int]) -> int:
    """
    Return the minimum element in the rotated sorted array.

    Args:
        nums: Rotated sorted array (may contain duplicates)

    Returns:
        The minimum element
    """
    left, right = 0, len(nums) - 1
    mid = 0

    while left <= right:
        mid = (left + right) // 2

        if nums[left] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] > nums[right]:
            left = mid + 1
        else:
            return nums[left]
    return nums[mid]


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (nums, expected_min)
        ([1, 1, 1, 1], 1),
        ([1, 3, 5], 1),
        ([2, 2, 2, 0, 1, 1], 0),
        ([3, 4, 5, 1, 2], 1),
    ]

    for nums, expected in test_cases:
        result = find_min(nums)
        assert result == expected, f"nums={nums}: got {result}, expected {expected}"

    print("All tests passed.")
