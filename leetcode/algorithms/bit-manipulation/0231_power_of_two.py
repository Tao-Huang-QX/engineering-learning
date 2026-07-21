"""
LeetCode 231: Power of Two
https://leetcode.com/problems/power-of-two/

Problem: Given an integer n, return true if it is a power of two, otherwise return false.

Constraints:
- -2^31 <= n <= 2^31 - 1

Examples:
- Input: n = 1
  Output: true
  Explanation: 2^0 = 1

- Input: n = 16
  Output: true
  Explanation: 2^4 = 16

- Input: n = 3
  Output: false

Approach: Bit trick - powers of two have exactly one bit set
- n > 0 ensures positive numbers only (negative numbers are not powers of two)
- n & (n-1) clears the lowest set bit; if result is 0, exactly one bit was set
- Example: n=16 (0b10000), n-1=15 (0b01111), n&(n-1)=0

Time: O(1) — single bitwise operation   Space: O(1)
"""


def is_power_of_two(n: int) -> bool:
    """
    Return true if n is a power of two, otherwise return false.

    Args:
        n: An integer

    Returns:
        True if n is a power of two, False otherwise
    """
    """
    if n < 0:
        return False  # Negative are not power of 2
    # Count bit in 2-bit pair
    n = (n & 0x55555555) + ((n >> 1) & 0x55555555)
    # Count bit in 4-bit pair
    n = (n & 0x33333333) + ((n >> 2) & 0x33333333)
    # Count bit in 8-bit pair
    n = (n & 0x0F0F0F0F) + ((n >> 4) & 0x0F0F0F0F)
    n = (n & 0xFF) + ((n >> 8) & 0xFF) + ((n >> 16) & 0xFF) + ((n >> 24) & 0xFF)
    return n == 1
    """
    return n > 0 and (n & (n - 1)) == 0


if __name__ == "__main__":
    # Example 1: n = 1
    assert is_power_of_two(1)
    # Example 2: n = 16
    assert is_power_of_two(16)

    # Example 3: n = 3
    assert not is_power_of_two(3)

    # Edge case: n = 0
    assert not is_power_of_two(0)

    # Edge case: negative number
    assert not is_power_of_two(-16)

    print("All tests passed.")
