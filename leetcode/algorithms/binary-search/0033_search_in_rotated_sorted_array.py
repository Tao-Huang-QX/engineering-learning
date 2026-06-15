"""
LeetCode 33: Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

Problem: There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is rotated at an unknown pivot index k. Given the array nums after the rotation and an integer target, return the index of target in nums, or -1 if it is not in nums. You must write an algorithm with O(log n) runtime complexity.

Approach:
- At least one half of the array is always sorted in a rotated array
- Check which half is sorted (number[left] < number[middle])
- Determine if target is in the sorted half
- Narrow search to the half that contains target

Time: O(log n)   Space: O(1)
"""


def search(nums: list[int], target: int) -> int:
    """
    Return the index of target in a rotated sorted array.

    Args:
        nums: Rotated sorted array with distinct values
        target: Integer to find

    Returns:
        Index of target, or -1 if not found
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = (left + right) // 2

        # Handle 2-element case
        if left == middle and nums[right] == target:
            return right

        if nums[middle] == target:
            return middle
        elif nums[left] < nums[middle]:  # Left half is sorted
            if nums[left] <= target < nums[middle]:  # Target in left half
                right = middle - 1
            else:  # Target in the right half
                left = middle + 1
        else:  # Right half is sorted
            if nums[middle] < target <= nums[right]:  # Target in right half
                left = middle + 1
            else:  # Target in the left half
                right = middle - 1
    return -1


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (nums, target, expected_index)
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1, 3], 3, 1),
        ([5, 1, 3], 5, 0),
        ([3, 1], 1, 1),
    ]

    for nums, target, expected in test_cases:
        result = search(nums, target)
        assert result == expected, f"{nums}, target={target}: got {result}, expected {expected}"

    print("All tests passed.")
