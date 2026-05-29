"""
LeetCode 200: Number of Islands
https://leetcode.com/problems/number-of-islands/

Problem: Given an m x n 2D binary grid where 1 represents land and 0 represents water,
count the number of islands formed by connecting adjacent lands horizontally or vertically.

Approach:
- DFS flood fill (iterative with stack)
- BFS flood fill (iterative with queue) in comments
- When finding unvisited land ("1"), increment island count
- Sink the island by marking all connected land cells as "0"
- Explore 4-directionally (up, down, left, right)

Time: O(m * n)   Space: O(m * n)
"""


def num_islands(grid: list[list[str]]) -> int:
    """
    Count the number of islands in a 2D grid.

    Args:
        grid: 2D list of strings "1" (land) or "0" (water)

    Returns:
        Number of islands
    """
    """
    Can use DFS or BFS in this quiz, implemented DFS using stack.
    Here's the BFS implementation using a queue:
    count = 0
    if not grid or not grid[0]:
        return count
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "1":
                count += 1
                grid[i][j] = "0"
                q = deque([(i, j)])
                while q:
                    r, c = q.popleft()
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"
                            q.append((nr, nc))
    return count
    """
    count = 0
    if not grid or not grid[0]:
        return count
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "1":
                count += 1
                # Mark the entire island as visited (e.g., change "1" to "0")
                grid[i][j] = "0"
                # This can be done using DFS
                stack = [(i, j)]
                while stack:
                    r, c = stack.pop()
                    # Add adjacent cells to the stack
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"  # Mark as visited
                            stack.append((nr, nc))
    return count


if __name__ == "__main__":
    # Example 1
    grid1 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(grid1) == 3

    # Example 2
    grid2 = [["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]
    assert num_islands(grid2) == 1

    # Example 3: All water
    grid3 = [["0", "0"], ["0", "0"]]
    assert num_islands(grid3) == 0

    print("All tests passed.")
