"""
LeetCode 64: Minimum Path Sum
https://leetcode.com/problems/minimum-path-sum/

Problem: Given a m x n grid filled with non-negative numbers, find a path from top left to
bottom right that minimizes the sum of all numbers along its path. You can only move
either down or right at any point in time.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 200
- 0 <= grid[i][j] <= 200

Approach: 2D DP with in-place modification
- Initialize first row and first column with cumulative sums (base cases)
- For interior cells: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
- Reuse input grid as DP table for O(1) space

Time: O(m × n)   Space: O(1)
"""


def min_path_sum(grid: list[list[int]]) -> int:
    """
    Return the minimum path sum from top-left to bottom-right.

    Args:
        grid: m x n grid of non-negative integers

    Returns:
        Minimum sum of numbers along a path moving only down or right
    """
    row, col = len(grid), len(grid[0])
    accumulation = 0
    for r in range(0, row):
        accumulation += grid[r][0]
        grid[r][0] = accumulation

    accumulation = 0
    for c in range(0, col):
        accumulation += grid[0][c]
        grid[0][c] = accumulation

    for r in range(1, row):
        for c in range(1, col):
            grid[r][c] = grid[r][c] + min(grid[r - 1][c], grid[r][c - 1])

    return grid[-1][-1]


if __name__ == "__main__":
    # Example 1: Path 1 → 3 → 1 → 1 → 1 = 7
    result = min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
    assert result == 7, f"Example 1 failed: got {result}, expected 7"

    # Example 2: Path 1 → 2 → 3 → 6 = 12
    result = min_path_sum([[1, 2, 3], [4, 5, 6]])
    assert result == 12, f"Example 2 failed: got {result}, expected 12"

    print("All tests passed.")
