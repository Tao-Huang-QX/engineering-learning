"""
LeetCode 191: Number of 1 Bits
https://leetcode.com/problems/number-of-1-bits/

Problem: Count the number of 1 bits in the binary representation of an unsigned integer.

Constraints:
- Input is guaranteed to be a 32-bit unsigned integer

Examples:
- Input: n = 11 (binary: 1011)
  Output: 3
  Explanation: The binary representation 1011 has three 1 bits

- Input: n = 128 (binary: 10000000)
  Output: 1
  Explanation: The binary representation 10000000 has one 1 bit

- Input: n = 2147483648 (binary: 10000000000000000000000000000000)
  Output: 1

Approach: Parallel counting with divide-and-conquer
- Count bits in 2-bit pairs in parallel using mask 0x55555555 (0101...)
- Merge adjacent pairs to count 4-bit groups using mask 0x33333333 (0011...)
- Merge adjacent 4-bit groups to count bytes using mask 0x0F0F0F0F
- Sum the four 8-bit byte counts to get total
- Each step doubles the working chunk size: 2→4→8→32 bits

Time: O(1) — fixed 5 mask-and-shift operations
Space: O(1) — in-place bit manipulation
"""


def hamming_weight(n: int) -> int:
    """
    Count the number of 1 bits in the binary representation of n.

    Args:
        n: A 32-bit unsigned integer

    Returns:
        The count of 1 bits in n
    """
    """
    Solution 1, iteration
    result = 0
    for _ in range(32):
        if n & 1 == 1:
            result += 1
        n >>= 1
    return result
    Solution 2, O(1) C level optimization
    return n.bit_count()
    """
    # Step 1: count bits in each 2-bit pair
    n = (n & 0x55555555) + ((n >> 1) & 0x55555555)
    # Step 2: count bits in each 4-bit pair
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
    # Step 3: count bits in each 8-bit pair
    n = (n & 0x0F0F0F0F) + ((n >> 4) & 0x0F0F0F0F)
    # Step 4: sum bytes into final count
    n = (n & 0xFF) + ((n >> 8) & 0xFF) + ((n >> 16) & 0xFF) + ((n >> 24) & 0xFF)
    return n


if __name__ == "__main__":
    # Example 1: n = 11 (binary: 1011)
    assert hamming_weight(0b1011) == 3

    # Example 2: n = 128 (binary: 10000000)
    assert hamming_weight(0b10000000) == 1

    # Example 3: n = 2147483648 (binary: 10000000000000000000000000000000)
    assert hamming_weight(0b10000000000000000000000000000000) == 1

    # Edge case: all zeros
    assert hamming_weight(0) == 0

    # Edge case: all ones
    assert hamming_weight(0xFFFFFFFF) == 32

    print("All tests passed.")
