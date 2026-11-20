"""
LeetCode 33: Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

Problem: There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is rotated at an unknown pivot index k. Given the array nums after the rotation and an integer target, return the index of target in nums, or -1 if it is not in nums. You must write an algorithm with O(log n) runtime complexity.

Approach:
- At least one half of the array is always sorted in a rotated array
- Check which half is sorted (nums[left] <= nums[middle]; the equal sign
  matters — see the note at the branch in the code)
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
        # Ceiling mid certifies mid > left while left < right, so the
        # strict compare below never self-compares. A 1-wide window
        # self-compares again (mid == left), but the equality check has
        # already cleared that element — the containment test a < t <= a
        # is unsatisfiable, and right = mid - 1 exits with a correct -1.
        mid = (left + right + 1) // 2

        if nums[mid] == target:
            return mid
        elif nums[left] < nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:  # Target in left half
                right = mid - 1
            else:  # Target in the right half
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:  # Target in right half
                left = mid + 1
            else:  # Target in the left half
                right = mid - 1
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
