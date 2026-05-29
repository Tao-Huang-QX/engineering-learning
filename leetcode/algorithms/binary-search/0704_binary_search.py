"""
LeetCode 704: Binary Search
https://leetcode.com/problems/binary-search/

Problem: Given an array of integers nums which is sorted in ascending order, and an integer target, return the index of target in nums. If target does not exist, return -1.

Approach:
- Maintain left and right pointers to track the current search range in the sorted array
- Compare the middle element to target
- Narrow search by half each iteration (move left or right pointer)
- When left > right, target doesn't exist

Time: O(log n)   Space: O(1)
"""


def search(nums: list[int], target: int) -> int:
    """
    Return the index of target in sorted array nums.

    Args:
        nums: Sorted array of integers (ascending)
        target: Integer to find

    Returns:
        Index of target, or -1 if not found
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (nums, target, expected_index)
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        ([5], 5, 0),
        ([5], -5, -1),
        ([1, 2, 3, 4, 5], 1, 0),
        ([1, 2, 3, 4, 5], 5, 4),
        ([-10, -5, 0, 5, 10], -10, 0),
    ]

    for nums, target, expected in test_cases:
        result = search(nums, target)
        assert result == expected, f"{nums}, target={target}: got {result}, expected {expected}"

    print("All tests passed.")
