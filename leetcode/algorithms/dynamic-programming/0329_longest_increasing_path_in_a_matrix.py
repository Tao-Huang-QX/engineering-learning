"""
LeetCode 329: Longest Increasing Path in a Matrix
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/

Problem: Given an m x n integers matrix, return the length of the longest increasing
path in matrix. From each cell, you can either move in four directions: left, right,
up, or down. You may NOT move diagonally or move outside the boundary.

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 2^31 - 1

Examples:
- Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
  Output: 4
  Explanation: The longest increasing path is [1, 2, 6, 9].

- Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
  Output: 4
  Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is
    not allowed.

Approach: DFS with memoization (top-down DP)
- Longest path starting at (r, c) = 1 + max over strictly larger neighbors
- Strictly increasing moves make the grid an implicit DAG — no visited marker needed
- Memoize each cell's result as an int; 0 means not computed (lengths always >= 1)

Time: O(m * n)   Space: O(m * n)
"""


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """
    Return the length of the longest increasing path in the matrix.

    Args:
        matrix: m x n grid of integers

    Returns:
        Length of the longest strictly increasing path
    """
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]  # 0 = not computed; lengths are always >= 1
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(r: int, c: int) -> int:
        if memo[r][c]:
            return memo[r][c]

        best = 1
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))

        memo[r][c] = best
        return best

    return max(dfs(r, c) for r in range(m) for c in range(n))


if __name__ == "__main__":
    # Example 1
    result1 = longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]])
    expected1 = 4
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = longest_increasing_path([[3, 4, 5], [3, 2, 6], [2, 2, 1]])
    expected2 = 4
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
