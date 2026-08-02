"""
LeetCode 212: Word Search II
https://leetcode.com/problems/word-search-ii/

Problem: Given an m x n board of characters and a list of strings words, return all
words on the board. Each word must be constructed from letters of sequentially
adjacent cells, where adjacent cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once in a word.

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 12
- board[i][j] is a lowercase English letter
- 1 <= words.length <= 3 * 10^4
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters
- All the strings of words are unique

Examples:
- Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
         words = ["oath","pea","eat","rain"]
  Output: ["eat","oath"]

- Input: board = [["a","b"],["c","d"]], words = ["abcb"]
  Output: []

Approach: Trie + DFS with backtracking and pruning
- Build a Trie from all words for O(1) per-character prefix lookup
- Lockstep traversal: DFS the board while walking the Trie in parallel
  (if board char isn't in current Trie node's children, backtrack immediately)
- Backtracking: mark cell visited with "#" during a path, restore after
  exploring all 4 directions — prevents reuse within the same word
- Dedup via is_end: set node.is_end = False after adding a word (avoids a set)
- Trie pruning: post-backtrack, remove child nodes that have no remaining
  children — shrinks the Trie as words are found, accelerating later searches
- Recursion depth bounded by max word length (10), safe from stack overflow

Time: O(m * n * 4^L) where L = max word length (10)
  - At worst, explore every cell with all 4 directions for L depth
  - Trie pruning and lockstep filtering make this much faster in practice
Space: O(W + L) where W = total characters in all words (Trie)
  - Call stack: max depth 10
"""


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Return all words from the list that can be formed on the board.

    Args:
        board: m x n grid of lowercase letters
        words: List of words to search for

    Returns:
        List of words found on the board (any order)
    """
    root = TrieNode()

    # Build Trie from all words
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    m, n = len(board), len(board[0])
    result: list[str] = []

    def dfs(r: int, c: int, node: TrieNode, path: str) -> None:
        if not (0 <= r < m and 0 <= c < n):
            return

        ch = board[r][c]
        if ch == "#" or ch not in node.children:
            return

        next_node = node.children[ch]
        path += ch

        if next_node.is_end:
            result.append(path)
            next_node.is_end = False  # Avoid duplicates

        board[r][c] = "#"
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dfs(r + dr, c + dc, next_node, path)
        board[r][c] = ch

        # Prune: if child has no children left, remove it
        if not next_node.children:
            del node.children[ch]

    for r in range(m):
        for c in range(n):
            dfs(r, c, root, "")

    return result


if __name__ == "__main__":
    # Example 1
    board1 = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    words1 = ["oath", "pea", "eat", "rain"]
    result1 = find_words(board1, words1)
    expected1 = {"eat", "oath"}
    assert set(result1) == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    board2 = [["a", "b"], ["c", "d"]]
    words2 = ["abcb"]
    result2 = find_words(board2, words2)
    expected2: list[str] = []
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
