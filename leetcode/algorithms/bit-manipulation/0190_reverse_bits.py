"""
LeetCode 190: Reverse Bits
https://leetcode.com/problems/reverse-bits/

Problem: Reverse bits of a given 32-bit unsigned integer.

Constraints:
- Input is guaranteed to be a 32-bit unsigned integer
- Return value must also be a 32-bit unsigned integer

Examples:
- Input: n = 00000010100101000001111010011100 (binary)
  Output: 00111001011110000010100101000000 (binary)
  Explanation: The binary string is reversed bit by bit

- Input: n = 11111111111111111111111111111101 (binary)
  Output: 10111111111111111111111111111111 (binary)

Approach: Divide and conquer bit reversal (merge sort on bits)
- Swap 16-bit halves: left half ↔ right half
- Recursively swap 8-bit, 4-bit, 2-bit, and 1-bit halves
- Uses bitwise masks to isolate and shift halves in parallel
- Each step doubles the granularity: 16→8→4→2→1 bit swaps

Time: O(log 32) = O(1) — fixed 5 mask-shift-or operations
Space: O(1) — in-place bit manipulation
"""


def reverse_bits(n: int) -> int:
    """
    Reverse the bits of a 32-bit unsigned integer.

    Args:
        n: A 32-bit unsigned integer

    Returns:
        The 32-bit unsigned integer with bits reversed
    """
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
    """
    n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
    return n


if __name__ == "__main__":
    # Example 1: n = 43261596 (00000010100101000001111010011100)
    # Expected: 964176192 (00111001011110000010100101000000)
    assert reverse_bits(0b00000010100101000001111010011100) == 0b00111001011110000010100101000000

    # Example 2: n = 4294967293 (11111111111111111111111111111101)
    # Expected: 3221225471 (10111111111111111111111111111111)
    assert reverse_bits(0b11111111111111111111111111111101) == 0b10111111111111111111111111111111

    # Edge case: all zeros
    assert reverse_bits(0b00000000000000000000000000000000) == 0b00000000000000000000000000000000

    # Edge case: single bit set at position 0
    assert reverse_bits(0b00000000000000000000000000000001) == 0b10000000000000000000000000000000

    # Edge case: single bit set at position 31
    assert reverse_bits(0b10000000000000000000000000000000) == 0b00000000000000000000000000000001

    print("All tests passed.")
