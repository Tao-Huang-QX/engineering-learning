"""
LeetCode 201: Bitwise AND of Numbers Range
https://leetcode.com/problems/bitwise-and-of-numbers-range/

Problem: Given two integers left and right, return the bitwise AND of all numbers
in the range [left, right] inclusive.

Constraints:
- 0 <= left <= right <= 2^31 - 1

Examples:
- Input: left = 5, right = 7
  Output: 4
  Explanation: 5 & 6 & 7 = 4 (101 & 110 & 111 = 100)

- Input: left = 0, right = 0
  Output: 0

- Input: left = 1, right = 2147483647
  Output: 0

Approach: Common prefix (bit shift)
- The bitwise AND of a range is determined by the bits that never change
- Any bit that flips between left and right gets AND-ed to 0
- Right-shift both numbers until they're equal (dropping the flipping bits
  from the right), counting shifts — what remains is the common prefix
- Left-shift the common prefix back by the shift count to restore magnitude

Time: O(1) — at most 31 iterations for a 32-bit integer
Space: O(1)
"""


def range_bitwise_and(left: int, right: int) -> int:
    """
    Return the bitwise AND of all integers in [left, right].

    Args:
        left: Lower bound of the range (inclusive)
        right: Upper bound of the range (inclusive)

    Returns:
        The bitwise AND of all numbers in the range
    """
    shift = 0
    while left != right:
        shift += 1
        left, right = left >> 1, right >> 1
    return left << shift


if __name__ == "__main__":
    # Example 1
    result1 = range_bitwise_and(5, 7)
    expected1 = 4
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = range_bitwise_and(0, 0)
    expected2 = 0
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = range_bitwise_and(1, 2147483647)
    expected3 = 0
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
