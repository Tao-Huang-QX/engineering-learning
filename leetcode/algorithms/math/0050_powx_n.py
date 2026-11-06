"""
LeetCode 50: Pow(x, n)
https://leetcode.com/problems/powx-n/

Problem: Implement pow(x, n), which calculates x raised to the power n.

Constraints:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1 (n is an integer)
- Either x is nonzero or n will not be negative
- Answers within 10^-4 of the true value are accepted

Examples:
- Input: x = 2.00000, n = 10
  Output: 1024.00000

- Input: x = 2.10000, n = 3
  Output: 9.26100

- Input: x = 2.00000, n = -2
  Output: 0.25000
  Explanation: 2^-2 = 1 / 2^2 = 1 / 4 = 0.25

Approach: Fast exponentiation by squaring (halve the exponent, square the result)
- x^n = (x^(n/2))^2 when n is even; x * (x^((n-1)/2))^2 when odd — each
  level halves n, so ~log2(n) multiplications instead of n
- Precedence note: x * dfs(...) ** 2 parses as x * (dfs(...)**2) — the
  intended shape, since ** outranks *
- Negative exponent is handled at the BOUNDARY, not inside the recursion:
  x^(-n) = 1 / x^n — one inversion in the wrapper keeps dfs positive-only
  (recursing into my_pow with -n invites infinite recursion; and for
  negative odds, Python's -1 % 2 == 1 plus floor division makes
  dfs(-1) call itself)
- C/Java talking point: n = -n at n = -2^31 overflows a 32-bit int —
  widen before negating; Python ints make it a non-bug
- Float note: CPython's ** raises OverflowError (not inf) past ~1.8e308,
  and squaring amplifies relative error ~2x per level — tolerance for
  the deep-exponent test is 1e-6 for exactly that reason

Time: O(log n)   Space: O(log n) recursion depth
"""

import math


def my_pow(x: float, n: int) -> float:
    """
    Return x raised to the power n.

    Args:
        x: Base, a float with |x| < 100
        n: Integer exponent, may be negative

    Returns:
        x ** n computed with fast exponentiation
    """

    def dfs(n: int):
        if n == 0:
            return 1

        if n % 2 == 1:
            return x * dfs((n - 1) // 2) ** 2
        else:
            return dfs(n // 2) ** 2

    return dfs(n) if n > 0 else 1 / dfs(-n)


if __name__ == "__main__":
    # Example 1
    result1 = my_pow(2.0, 10)
    expected1 = 1024.0
    assert abs(result1 - expected1) < 1e-9, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = my_pow(2.1, 3)
    expected2 = 9.261
    assert abs(result2 - expected2) < 1e-9, f"Example 2: got {result2}, expected {expected2}"

    # Example 3: negative exponent
    result3 = my_pow(2.0, -2)
    expected3 = 0.25
    assert abs(result3 - expected3) < 1e-9, f"Example 3: got {result3}, expected {expected3}"

    # Edge: zero exponent
    result4 = my_pow(7.5, 0)
    expected4 = 1.0
    assert abs(result4 - expected4) < 1e-9, f"Zero exp: got {result4}, expected {expected4}"

    # Edge: exponent one
    result5 = my_pow(-3.0, 1)
    expected5 = -3.0
    assert abs(result5 - expected5) < 1e-9, f"One exp: got {result5}, expected {expected5}"

    # Edge: negative base, even and odd exponents
    result6 = my_pow(-2.0, 3)
    expected6 = -8.0
    assert abs(result6 - expected6) < 1e-9, f"Neg base odd: got {result6}, expected {expected6}"

    result7 = my_pow(-2.0, 4)
    expected7 = 16.0
    assert abs(result7 - expected7) < 1e-9, f"Neg base even: got {result7}, expected {expected7}"

    # Edge: the true int-min exponent n = -2^31 — kept at the real boundary.
    # x must sit barely above 1 so the magnitude stays in float range:
    # 1.0000001^(2^31) = e^(2.1e9 * 1e-7) ~ e^214.7 ~ 1e93.
    # (With x = 2.0 the result is ~10^646 million — beyond any float, and
    #  CPython's ** raises OverflowError instead of returning inf, so no
    #  implementation could pass; LeetCode never judges such magnitudes.)
    result8 = my_pow(1.0000001, -(2**31))
    expected8 = 1.0000001 ** -(2**31)
    # rel_tol 1e-6: each squaring doubles the base's ~1e-16 representation
    # error, so 31 levels amplify it to ~2^31 * 1e-16 ≈ 2e-7
    assert math.isclose(result8, expected8, rel_tol=1e-6), (
        f"Int min exp: got {result8}, expected {expected8}"
    )

    print("All tests passed.")


# solved: 2026-11-06, medium, 45min, Pow(x, n)
