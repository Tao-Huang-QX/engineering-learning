"""
LeetCode 63: Unique Paths II
https://leetcode.com/problems/unique-paths-ii/

Problem: A robot is located at the top-left corner of an m x n grid. It can only
move down or right at any point and tries to reach the bottom-right corner. Some
cells contain obstacles (marked 1); free cells are marked 0. A path cannot pass
through an obstacle cell. Return the number of possible unique paths.

Constraints:
- m == obstacleGrid.length
- n == obstacleGrid[i].length
- 1 <= m, n <= 100
- obstacleGrid[i][j] is 0 or 1
- The start (top-left) and finish (bottom-right) cells may themselves be obstacles.

Examples:
- Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
  Output: 2
  Explanation: Obstacle in the center of a 3x3 grid; two paths reach bottom-right.

- Input: obstacleGrid = [[0,1],[0,0]]
  Output: 1

Approach: 2D dynamic programming
- If start or end cell is an obstacle, return 0 immediately
- dp[i][j] = number of unique paths to reach cell (i, j) from (0, 0), dp[0][0] = 1 (start)
- First row/column: only one way in (from the single neighbor), so dp[i][0] = dp[i-1][0], dp[0][j] = dp[0][j-1]; an obstacle zeroes out that cell and everything after it in that row/column
- For interior cells: dp[i][j] = dp[i-1][j] + dp[i][j-1] (paths from above + paths from left), but 0 if the cell itself is an obstacle

Time: O(m × n)   Space: O(m × n)
"""


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    """
    Return the number of unique paths from top-left to bottom-right,
    avoiding obstacle cells (cells with value 1).

    Args:
        obstacle_grid: m x n grid where 1 marks an obstacle and 0 marks a free cell

    Returns:
        Number of unique paths, or 0 if no path exists
    """
    row, col = len(obstacle_grid), len(obstacle_grid[0])

    # If start or end is blocked, no path exists
    if obstacle_grid[0][0] == 1 or obstacle_grid[row - 1][col - 1] == 1:
        return 0

    dp = [[0] * col for _ in range(row)]
    dp[0][0] = 1

    for i in range(1, row):
        if obstacle_grid[i][0] == 0:
            dp[i][0] = dp[i - 1][0]
    for j in range(1, col):
        if obstacle_grid[0][j] == 0:
            dp[0][j] = dp[0][j - 1]

    # Fill in the rest
    for r in range(1, row):
        for c in range(1, col):
            if obstacle_grid[r][c] == 0:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp[-1][-1]


if __name__ == "__main__":
    # Example 1: 3x3 grid, obstacle in center
    #   0 0 0
    #   0 1 0
    #   0 0 0
    assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2

    # Example 2: 2x2 grid, obstacle at (0,1)
    #   0 1
    #   0 0
    assert unique_paths_with_obstacles([[0, 1], [0, 0]]) == 1

    # Edge case: start cell is blocked — no paths possible
    assert unique_paths_with_obstacles([[1, 0], [0, 0]]) == 0

    print("All tests passed.")
