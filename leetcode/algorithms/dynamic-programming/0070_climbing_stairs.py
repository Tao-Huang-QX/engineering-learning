"""
LeetCode 70: Climbing Stairs
https://leetcode.com/problems/climbing-stairs/

Problem: You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Approach: Fibonacci-style DP
- To reach step n, you come from n-1 (1 step) or n-2 (2 steps)
- ways[n] = way[n-1] + way[n-2], exactly Fibonacci shifted

Time: O(n)   Space: O(1)
"""


def climb_stairs(n: int) -> int:
    """
    Calculate the number of distinct ways to climb n stairs.

    Args:
        n: Number of stairs to climb

    Returns:
        Number of distinct ways to reach the top
    """
    if n <= 2:
        return n

    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


if __name__ == "__main__":
    # Example 1
    assert climb_stairs(2) == 2

    # Example 2
    assert climb_stairs(3) == 3

    # Example 3: Single step
    assert climb_stairs(1) == 1

    # Example 4: More steps
    assert climb_stairs(4) == 5

    # Example 5: Even more
    assert climb_stairs(5) == 8

    print("All tests passed.")
