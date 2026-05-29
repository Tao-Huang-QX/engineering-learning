"""
LeetCode 238: Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Problem: Given an integer array nums, return an array answer where answer[i] is equal to the product of all the elements of nums except nums[i].

Approach:
- easily got a O(n2) solution, but we can do better by using prefix and suffix products by 2 passes through the array

Time: O(n)   Space: O(1)
"""


def product_except_self(nums: list[int]) -> list[int]:
    """
    Return an array where answer[i] is the product of all elements except nums[i].

    Args:
        nums: List of integers

    Returns:
        List where each element is the product of all other elements
    """
    results = [1] * len(nums)
    prefix = 1
    for i in range(len(nums)):
        results[i] *= prefix
        prefix *= nums[i]  #  Skip the current element for being multiplied by itself
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        results[i] *= suffix
        suffix *= nums[i]  #  Skip the current element for being multiplied by itself
    return results


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_output)
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([1, 2, 3, 4, 5], [120, 60, 40, 30, 24]),
    ]

    for nums, expected in test_cases:
        result = product_except_self(nums)
        assert result == expected, f"{nums}: got {result}, expected {expected}"

    print("All tests passed.")
