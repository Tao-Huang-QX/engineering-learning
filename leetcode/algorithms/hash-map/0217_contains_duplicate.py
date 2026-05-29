"""
LeetCode 217: Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

Problem: Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Approach:
- set is also hashed and even simpler than dictionary, the lookup operation is O(1)
- safety: return False

Time: O(n)   Space: O(n)
"""


def contains_duplicate(nums: list[int]) -> bool:
    """
    Return True if any value appears at least twice, False otherwise.

    Args:
        nums: List of integers

    Returns:
        True if duplicate exists, False if all elements are distinct
    """
    seen = set()  # To track seen numbers
    for num in nums:
        if num in seen:
            return True  # Duplicate found
        seen.add(num)  # Otherwise, add it to the seen set
    return False


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (nums, expected_result)
        ([1, 2, 3, 1], True),  # 1 appears twice
        ([1, 2, 3, 4], False),  # all distinct
        ([1, 1, 1, 3, 3, 4, 3], True),  # multiple duplicates
        ([], False),  # empty array has no duplicates
        ([1], False),  # single element has no duplicate
    ]

    for nums, expected in test_cases:
        result = contains_duplicate(nums)
        assert result == expected, f"{nums}: got {result}, expected {expected}"

    print("All tests passed.")
