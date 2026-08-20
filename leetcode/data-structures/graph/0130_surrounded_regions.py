"""
LeetCode 130: Surrounded Regions
https://leetcode.com/problems/surrounded-regions/

Problem: You are given an m x n matrix board containing the characters 'X' and
'O'. Capture regions that are surrounded: replace all 'O's that are surrounded
by 'X's with 'X'. A region is captured by surrounding it with 'X's in all
directions (a group of 'O's is surrounded if no 'O' lies on the border of the
board and no 'O' is connected to an 'O' on the border, 4-directionally).

Do not return anything; modify board in-place instead.

Constraints:
- m == board.length, n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'

Examples:
- Input: board = [["X","X","X","X"],
                  ["X","O","O","X"],
                  ["X","X","O","X"],
                  ["X","O","X","X"]]
  Output: [["X","X","X","X"],
           ["X","X","X","X"],
           ["X","X","X","X"],
           ["X","O","X","X"]]
  Explanation: The bottom 'O' is on the border, so it and its region survive;
    the middle blob is fully surrounded and is captured.

- Input: board = [["X"]]
  Output: [["X"]]

Approach: Border-first flood fill (invert the capture rule)
- A region survives iff it touches the border, so flood only from border
  'O's, marking each border-connected cell '#' as it is PUSHED (never on
  pop — no cell enters the stack twice)
- Sweep once: unmarked 'O' is not border-connected -> capture to 'X';
  '#' is provably safe -> restore to 'O'
- Uses '#' sentinel in the board itself as the visited set (in-place)

Time: O(m · n)   Space: O(m · n)   (worst-case stack: one giant safe region)
"""


def solve(board: list[list[str]]) -> None:
    """
    Capture all regions surrounded by 'X' in place.

    Args:
        board: m x n grid of 'X' and 'O' entries

    Returns:
        None (board is modified in place)
    """
    m, n = len(board), len(board[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def mark_safe(start_r: int, start_c: int) -> None:
        """Mark every border-connected 'O' with '#' (provisionally safe)."""
        board[start_r][start_c] = "#"
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack.pop()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                    board[nr][nc] = "#"
                    stack.append((nr, nc))

    # 1. start floods only on the border ring
    for c in range(n):
        if board[0][c] == "O":
            mark_safe(0, c)
        if board[m - 1][c] == "O":
            mark_safe(m - 1, c)
    for r in range(1, m - 1):
        if board[r][0] == "O":
            mark_safe(r, 0)
        if board[r][n - 1] == "O":
            mark_safe(r, n - 1)

    # 2 + 3. capture the unmarked, restore the safe
    for r in range(m):
        for c in range(n):
            if board[r][c] == "O":
                board[r][c] = "X"
            if board[r][c] == "#":
                board[r][c] = "O"


if __name__ == "__main__":
    # Example 1
    board1 = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    solve(board1)
    expected1 = [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],
    ]
    assert board1 == expected1, f"Example 1: got {board1}, expected {expected1}"

    # Example 2
    board2 = [["X"]]
    solve(board2)
    expected2 = [["X"]]
    assert board2 == expected2, f"Example 2: got {board2}, expected {expected2}"

    print("All tests passed.")
