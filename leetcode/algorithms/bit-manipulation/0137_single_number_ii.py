"""
LeetCode 137: Single Number II
https://leetcode.com/problems/single-number-ii/

Problem: Given an integer array nums where every element appears three
times except for one, which appears exactly once. Find the single element
and return it. You must implement a solution with linear runtime
complexity and without using extra memory (a hash map / Counter counts
as extra memory).

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -2^31 <= nums[i] <= 2^31 - 1
- Each element in nums appears exactly three times except for one
  element which appears once

Examples:
- Input: nums = [2,2,3,2]
  Output: 3

- Input: nums = [0,1,0,1,0,1,99]
  Output: 99

Approach: Per-bit counting mod 3 (XOR is the mod-2 special case)
- Sum each bit position over all numbers; triplets contribute 0 mod 3,
  the singleton's bits survive — rebuild from the survivors
- Sign fix-up: 32-slot accumulation is unsigned, so if bit 31 is set,
  subtract 2^32 (bit 31 weighs -2^31 on the signed line, +2^31 unsigned)

Time: O(32n)   Space: O(1)
"""


def single_number(nums: list[int]) -> int:
    """
    Return the element that appears exactly once (all others thrice).

    Args:
        nums: Integers where every value occurs three times except one

    Returns:
        The singleton value
    """
    width = 32
    result: int = 0
    for level in range(width):
        bit_count = 0
        for num in nums:
            bit_count += num >> level & 1
        if bit_count % 3 == 1:
            result |= 1 << level
    return result - (1 << width) if result >= (1 << width - 1) else result


if __name__ == "__main__":
    # Example 1
    result1 = single_number([2, 2, 3, 2])
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = single_number([0, 1, 0, 1, 0, 1, 99])
    expected2 = 99
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: minimal input — one singleton, one triplet
    assert single_number([5, 7, 7, 7]) == 5, f"Minimal: got {single_number([5, 7, 7, 7])}"

    # Edge: singleton is the last element
    assert single_number([3, 3, 3, -4]) == -4, f"Last: got {single_number([3, 3, 3, -4])}"

    # Edge: negative singleton among positive triplets
    assert single_number([9, 9, 9, -2, 4, 4, 4]) == -2, (
        f"Negative: got {single_number([9, 9, 9, -2, 4, 4, 4])}"
    )

    # Edge: singleton at the int bound
    assert single_number([0, 0, 0, -(2**31)]) == -(2**31), (
        f"Int min: got {single_number([0, 0, 0, -(2**31)])}"
    )
    assert single_number([1, 1, 1, 2**31 - 1]) == 2**31 - 1, (
        f"Int max: got {single_number([1, 1, 1, 2**31 - 1])}"
    )

    print("All tests passed.")


# solved: 2026-11-16, medium, 45min, Single Number II
