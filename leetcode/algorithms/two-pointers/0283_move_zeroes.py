"""
LeetCode 283: Move Zeroes
https://leetcode.com/problems/move-zeroes/

Problem: Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Approach: [FILL AFTER SOLVING]
- Use read pointer to scan array, write pointer to track next non-zero position
- First pass: Move non-zero elements to the front
- Second pass: Fill remaining positions with zeroes

Time: O(n)   Space: O(1)
"""


def move_zeroes(nums: list[int]) -> None:
    """
    Move all zeroes to the end of the array in-place.

    Args:
        nums: List of integers (modified in-place)
    """
    r, w = 0, 0  # read and write pointers
    while r < len(nums):
        if nums[r] != 0:
            nums[w] = nums[r]
            w += 1
        r += 1
    while w < len(nums):  # fill the rest of the array with zeroes
        nums[w] = 0
        w += 1


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_output)
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2, 3], [1, 2, 3]),  # No zeros
        ([0, 0, 1], [1, 0, 0]),  # Leading zeros
        ([1, 0, 0], [1, 0, 0]),  # Trailing zeros
    ]

    for nums_input, expected in test_cases:
        nums = nums_input[:]  # Copy since function modifies in-place
        move_zeroes(nums)
        assert nums == expected, f"got {nums}, expected {expected}"

    print("All tests passed.")
