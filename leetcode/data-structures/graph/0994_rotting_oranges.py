"""
LeetCode 994: Rotting Oranges
https://leetcode.com/problems/rotting-oranges/

Problem: You are given an m x n grid where each cell can have one of three values:
- 0 representing an empty cell
- 1 representing a fresh orange
- 2 representing a rotten orange
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange.
If this is impossible, return -1.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2.

Approach: Multi-source BFS (level-by-level)
- Initialize queue with ALL rotten oranges (they spread simultaneously)
- Process level-by-level: each level = one minute of rotting
- Track fresh_count to know when all oranges are rotted
- If any fresh remain after BFS, return -1 (impossible to reach)

Time: O(m × n)   Space: O(m × n)
"""

from collections import deque


def oranges_rotting(grid: list[list[int]]) -> int:
    """
    Return the minimum minutes until all oranges are rotten.
    Returns -1 if impossible.

    Args:
        grid: m x n grid with 0 (empty), 1 (fresh), 2 (rotten)

    Returns:
        Minimum minutes to rot all oranges, or -1 if impossible.
    """
    if not grid:
        return -1

    row, col = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # Step 1: Initialize - add all rotten oranges to the queue
    for i in range(row):
        for j in range(col):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh_count += 1

    # No fresh oranges to rot
    if fresh_count == 0:
        return 0
    # No rotten oranges to spread:
    if not queue and fresh_count > 0:
        return -1

    # Step 2: Muti-source BFS - spread level by level
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = 0
    while queue and fresh_count > 0:
        result += 1

        for _ in range(len(queue)):
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check bounds and if fresh
                if 0 <= nr < row and 0 <= nc < col and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # Rot it
                    fresh_count -= 1
                    queue.append((nr, nc))

    return result if fresh_count == 0 else -1


if __name__ == "__main__":
    # Example 1: Simple case
    result = oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]])
    assert result == 4, f"Got {result}"

    # Example 2: Impossible - fresh oranges isolated from rotten
    result = oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]])
    assert result == -1, f"Got {result}"

    # Example 3: Already no fresh oranges
    result = oranges_rotting([[0, 2]])
    assert result == 0, f"Got {result}"

    # Example 4: All fresh, no rotten
    result = oranges_rotting([[1, 1], [1, 1]])
    assert result == -1, f"Got {result}"

    # Example 5: Single rotten
    result = oranges_rotting([[2]])
    assert result == 0, f"Got {result}"

    # Example 6: Single fresh
    result = oranges_rotting([[1]])
    assert result == -1, f"Got {result}"

    # Example 7: Empty grid
    result = oranges_rotting([[0, 0], [0, 0]])
    assert result == 0, f"Got {result}"

    print("All tests passed.")
