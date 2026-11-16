"""
LeetCode 279: Perfect Squares
https://leetcode.com/problems/perfect-squares/

Problem: Given an integer n, return the least number of perfect square
numbers that sum to n. A perfect square is an integer that is the square
of an integer; in other words, it is the product of some integer with
itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11
are not.

Constraints:
- 1 <= n <= 10^4

Examples:
- Input: n = 12
  Output: 3
  Explanation: 12 = 4 + 4 + 4.

- Input: n = 13
  Output: 2
  Explanation: 13 = 4 + 9.

Approach: Unbounded knapsack — squares as coins (Coin Change, quiz 28)
- Coins: i*i for i = 1 .. isqrt(n); dp[t] = min coins summing to t
- dp[t] = min over coins s <= t of dp[t - s] + 1; dp[0] = 0
- Greedy (largest square first) fails: 12 -> 9 then 3 strands at 1+1+1
  (4 coins) while 4+4+4 uses 3 — hence DP, not greedy

Time: O(n * sqrt(n))   Space: O(n)
"""

from math import sqrt


def num_squares(n: int) -> int:
    """
    Return the least number of perfect squares summing to n.

    Args:
        n: Target sum, at least 1

    Returns:
        Minimum count of perfect squares (with repetition) summing to n
    """
    squares = [i * i for i in range(1, int(sqrt(n)) + 1)]
    dp = [n + 1] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for square in squares:
            if square <= i:
                dp[i] = min(dp[i], dp[i - square] + 1)
    return dp[n]


if __name__ == "__main__":
    # Example 1
    result1 = num_squares(12)
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = num_squares(13)
    expected2 = 2
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: n is itself a perfect square
    assert num_squares(1) == 1, f"n=1: got {num_squares(1)}"
    assert num_squares(16) == 1, f"n=16: got {num_squares(16)}"

    # Edge: n = 2 — 1 + 1
    assert num_squares(2) == 2, f"n=2: got {num_squares(2)}"

    # Edge: greedy trap — 12: greedy takes 9, remainder 3 -> 1+1+1 (4 total);
    # optimal is 4+4+4 (3)
    assert num_squares(12) == 3, f"Greedy trap: got {num_squares(12)}"

    # Edge: known Lagrange-four case — 7 needs 4 squares (4+1+1+1)
    assert num_squares(7) == 4, f"n=7: got {num_squares(7)}"

    # Edge: larger value
    assert num_squares(100) == 1, f"n=100: got {num_squares(100)}"
    assert num_squares(9999) == 4, f"n=9999: got {num_squares(9999)}"

    print("All tests passed.")


# solved: 2026-11-16, medium, 30min, Perfect Squares
