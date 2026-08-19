"""
LeetCode 695: Max Area of Island
https://leetcode.com/problems/max-area-of-island/

Problem: You are given an m x n binary matrix grid. An island is a group of 1's
(land) connected 4-directionally (horizontal or vertical). The area of an island
is the number of cells with a value 1 in the island. Return the maximum area of
an island in grid. If there is no island, return 0.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0 or 1

Examples:
- Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],
                 [0,0,0,0,0,0,0,1,1,1,0,0,0],
                 [0,1,1,0,1,0,0,0,0,0,0,0,0],
                 [0,1,0,0,1,1,0,0,1,0,1,0,0],
                 [0,1,0,0,1,1,0,0,1,1,1,0,0],
                 [0,0,0,0,0,0,0,0,0,0,1,0,0],
                 [0,0,0,0,0,0,0,1,1,1,0,0,0],
                 [0,0,0,0,0,0,0,1,1,0,0,0,0]]
  Output: 6
  Explanation: The largest island has an area of 6.

- Input: grid = [[0,0,0,0,0,0,0,0]]
  Output: 0

Approach: Flood fill with an explicit stack (iterative DFS)
- Scan every cell; on land, flood the whole island via a stack, sinking
  each cell to 0 as it is PUSHED (never on pop — no cell enters twice)
- Count cells popped per flood; track the max across islands
- Mutates grid (sinks visited land to 0) instead of a separate visited set

Time: O(m · n)   Space: O(m · n)   (worst-case stack: one giant island)
"""


def max_area_of_island(grid: list[list[int]]) -> int:
    """
    Return the maximum area of an island in the grid.

    Args:
        grid: m x n binary matrix of 0 (water) and 1 (land)

    Returns:
        Number of cells in the largest 4-directionally connected land mass
    """
    m, n = len(grid), len(grid[0])
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    def island_area(start_r: int, start_c: int) -> int:
        grid[start_r][start_c] = 0
        stack = [(start_r, start_c)]
        area = 0

        while stack:
            r, c = stack.pop()
            area += 1

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 0
                    stack.append((nr, nc))
        return area

    result = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                result = max(result, island_area(r, c))
    return result


if __name__ == "__main__":
    # Example 1
    result1 = max_area_of_island(
        [
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        ]
    )
    expected1 = 6
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = max_area_of_island([[0, 0, 0, 0, 0, 0, 0, 0]])
    expected2 = 0
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")


# solved: 2026-08-19, medium, 35min, Max Area of Island
