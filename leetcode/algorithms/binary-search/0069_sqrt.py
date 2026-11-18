"""
LeetCode 69: Sqrt(x)
https://leetcode.com/problems/sqrtx/

Problem: Given a non-negative integer x, return the square root of x
rounded down to the nearest integer. The returned integer should be
non-negative as well. You must NOT use any built-in exponent function
or operator — no pow(x, 0.5), no x ** 0.5, no math.sqrt.

Constraints:
- 0 <= x <= 2^31 - 1

Examples:
- Input: x = 4
  Output: 2

- Input: x = 8
  Output: 2
  Explanation: sqrt(8) = 2.82842..., rounded down to 2.

Approach: Binary search on the answer (keep-candidate form, bisect_right − 1 semantics)
- Search k in [0, 46340] — inclusive top: 46340 = isqrt(2^31 - 1) is the
  largest answer any allowed x can have, and it must stay inside the window
- Ceiling mid certifies mid > left, keeping both updates valid: mid dead
  (x < mid^2) -> right = mid - 1, excluded from the window; mid alive
  (mid^2 <= x) -> left = mid, kept as a live answer
- Converges to the largest kept candidate = last k with k^2 <= x = floor;
  no post-fix offset needed since the answer is held, not walled

Time: O(log x)   Space: O(1)
"""


def my_sqrt(x: int) -> int:
    """
    Return floor(sqrt(x)) without exponent operators or math.sqrt.

    Args:
        x: Non-negative integer, up to 2^31 - 1

    Returns:
        Largest integer whose square is <= x
    """
    """
    # Alternative: boundary form — half-open window [0, 46341), floor mid,
    # wall parks on first k with k^2 > x, answer = wall - 1:
    left, right = 0, 46341  # half-open: sentinel past the last candidate
    while left < right:
        mid = (left + right) // 2  # floor mid - certificate: mid < right
        if mid * mid <= x:
            left = mid + 1
        else:
            right = mid
    return left - 1
    """
    left, right = 0, 46340  # inclusive top: 46340 itself can be the answer
    while left < right:
        mid = (left + right + 1) // 2  # ceiling mid, certificate: mid > left
        if x < mid * mid:  # mid disqualified — drop it
            right = mid - 1
        else:
            left = mid  # mid² <= x — mid is a live answer, keep it
    return left


if __name__ == "__main__":
    # Example 1: perfect square
    result1 = my_sqrt(4)
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: non-square rounds down
    result2 = my_sqrt(8)
    expected2 = 2
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: 0 and 1 — the identities
    assert my_sqrt(0) == 0, f"x=0: got {my_sqrt(0)}"
    assert my_sqrt(1) == 1, f"x=1: got {my_sqrt(1)}"

    # Edge: one below a perfect square
    assert my_sqrt(3) == 1, f"x=3: got {my_sqrt(3)}"
    assert my_sqrt(15) == 3, f"x=15: got {my_sqrt(15)}"

    # Edge: int-max input — 46340^2 = 2147395600 <= 2^31 - 1 < 46341^2
    assert my_sqrt(2**31 - 1) == 46340, f"x=2^31-1: got {my_sqrt(2**31 - 1)}"
    assert my_sqrt(2147395600) == 46340, f"x=46340^2: got {my_sqrt(2147395600)}"

    print("All tests passed.")


# solved: 2026-11-18, easy, 40min, Sqrt(x)
