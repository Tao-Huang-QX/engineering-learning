"""
LeetCode 81: Search in Rotated Sorted Array II
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/

Problem: Given a rotated sorted array with duplicates, determine if a target value exists.
Return true if target exists, false otherwise.

Approach: Modified binary search
- At least one half is always sorted in a rotated array
- If nums[left] < nums[mid], left half is sorted; check if target is in that range
- If nums[left] > nums[mid], right half is sorted; check if target is in that range
- If nums[left] == nums[mid] == nums[right], can't determine sorted half—shrink both bounds
- Use <= in loop to check the final remaining element

Time: O(n) worst case (all duplicates), O(log n) average   Space: O(1)
"""


def search(nums: list[int], target: int) -> bool:
    """
    Return True if target exists in the rotated sorted array.

    Args:
        nums: Rotated sorted array (may contain duplicates)
        target: Value to search for

    Returns:
        True if target is in nums, False otherwise
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        # At least a half is sorted
        if nums[mid] == target:
            return True
        elif nums[left] == nums[mid] == nums[right]:
            # Escape the duplicates
            left += 1
            right -= 1
        elif nums[left] < nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return False


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (nums, target, expected)
        ([2, 5, 6, 0, 0, 1, 4], 0, True),
        ([2, 5, 6, 0, 0, 1, 4], 3, False),
        ([1, 0, 1, 1, 1], 0, True),
    ]

    for nums, target, expected in test_cases:
        result = search(nums, target)
        assert result == expected, (
            f"nums={nums}, target={target}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Search in Rotated Sorted Array II
