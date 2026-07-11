"""
LeetCode 62: Unique Paths
https://leetcode.com/problems/unique-paths/

Problem: There is a robot on an m x n grid. The robot is located at the top-left corner.
The robot tries to move to the bottom-right corner. The robot can only move either down or
right at any point in time. How many possible unique paths are there?

Constraints:
- 1 <= m, n <= 100
- The answer will be less than or equal to 2 * 10^9

Approach: 2D Dynamic Programming
- Initialize first row and first column with 1s (only one path to reach cells on edges)
- For interior cells: paths[i][j] = paths[i-1][j] + paths[i][j-1]
- Can only reach cell (i,j) from above or left, so sum those possibilities

Time: O(m × n)   Space: O(m × n)
"""


def unique_paths(m: int, n: int) -> int:
    """
    Return the number of possible unique paths from top-left to bottom-right.

    Args:
        m: Number of rows
        n: Number of columns

    Returns:
        Number of unique paths moving only down or right
    """
    """
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
    """
    if m == 1 or n == 1:
        return 1

    grid: list[list[int]] = [[0] * n for _ in range(m)]
    for r in range(m):
        grid[r][0] = 1
    for c in range(n):
        grid[0][c] = 1

    for r in range(1, m):
        for c in range(1, n):
            grid[r][c] = grid[r - 1][c] + grid[r][c - 1]

    return grid[-1][-1]


if __name__ == "__main__":
    # Example 1: 3x2 grid
    result = unique_paths(3, 7)
    assert result == 28, f"Example 1 failed: got {result}, expected 28"

    # Example 2: 3x2 grid
    result = unique_paths(3, 2)
    assert result == 3, f"Example 2 failed: got {result}, expected 3"

    print("All tests passed.")
