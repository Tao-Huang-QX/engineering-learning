"""
LeetCode 79: Word Search
https://leetcode.com/problems/word-search/

Problem: Given an m x n grid of characters board and a string word, return true if
word exists in the grid. The word can be constructed from letters of sequentially
adjacent cells, where adjacent cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once.

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters.

Examples:
- Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
  Output: true
  Explanation: A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)

- Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
  Output: true
  Explanation: S(1,0) → E(2,0) → E(2,1)

- Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
  Output: false

Approach: DFS with backtracking
- Start DFS from each cell matching word[0]
- Mark visited with "#", restore original char on backtrack
- Short-circuit: return True immediately when any branch finds the word

Time: O(m * n * 4^L)   Space: O(L)
"""


def exist(board: list[list[str]], word: str) -> bool:
    """
    Return True if word exists in the character grid.

    Args:
        board: m x n grid of characters
        word: Target word to search for

    Returns:
        True if the word can be constructed from adjacent cells
    """
    m, n = len(board), len(board[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(r: int, c: int, i: int) -> bool:
        if not (0 <= r < m and 0 <= c < n):
            return False

        if board[r][c] == "#" or board[r][c] != word[i]:
            return False

        if i == len(word) - 1:
            return True

        board[r][c] = "#"  # backtrack
        for dr, dc in directions:
            if dfs(r + dr, c + dc, i + 1):
                board[r][c] = word[i]  # restore before success
                return True
        board[r][c] = word[i]  # restore after failure

        return False

    for r in range(m):
        for c in range(n):
            if dfs(r, c, 0):
                return True
    return False


if __name__ == "__main__":
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]

    # Example 1
    result1 = exist(board, "ABCCED")
    assert result1 is True, f"Example 1: got {result1}, expected True"

    # Example 2
    result2 = exist(board, "SEE")
    assert result2 is True, f"Example 2: got {result2}, expected True"

    # Example 3
    result3 = exist(board, "ABCB")
    assert result3 is False, f"Example 3: got {result3}, expected False"

    print("All tests passed.")
