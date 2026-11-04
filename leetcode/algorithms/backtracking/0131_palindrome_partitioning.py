"""
LeetCode 131: Palindrome Partitioning
https://leetcode.com/problems/palindrome-partitioning/

Problem: Given a string s, partition s such that every substring of the
partition is a palindrome. Return all possible palindrome partitioning of s.

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters

Examples:
- Input: s = "aab"
  Output: [["a","a","b"],["aa","b"]]
  Explanation: Both partitions consist entirely of palindromes.

- Input: s = "a"
  Output: [["a"]]

Approach: Backtracking over cut points + precomputed palindrome table
- pal[i][j] built inside-out in O(n^2): s[i..j] is a palindrome iff ends
  match and the inside (pal[i+1][j-1]) is one; True-initialized rows make
  length-1 and empty-inside cases free
- backtrack(start) extends the current partition with s[start:i] for every
  end i in (start, n]; the table turns each candidate check into O(1)
- Base case start == n records sol.copy() — pieces always have length >= 1,
  so every recursion strictly advances start
- Enumeration is output-bound: 2^(n-1) cut subsets, each partition copied
  in O(n) — the table only shaves the per-node constant

Time: O(n^2 + n · 2^n)   Space: O(n^2) table + O(n) recursion depth
"""


def partition(s: str) -> list[list[str]]:
    """
    Return all palindrome partitions of s.

    Args:
        s: Input lowercase string

    Returns:
        List of partitions, each a list of palindromic substrings
    """
    n = len(s)
    result: list[list[str]] = []

    # pal[i][j]: s[i..j] is a palindrome - build inside-out
    # (ends match AND the inside is a palindrome; length-1 is trivially True)
    pal = [[True] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            pal[i][j] = s[i] == s[j] and pal[i + 1][j - 1]

    def backtrack(sol: list[str], start: int) -> None:
        if start == n:
            result.append(sol.copy())
            return

        for i in range(start + 1, n + 1):
            if pal[start][i - 1]:  # O(1) check: s[start:i]
                sol.append(s[start:i])
                backtrack(sol, i)
                sol.pop()

    backtrack([], 0)
    return result


if __name__ == "__main__":
    # Example 1
    result1 = partition("aab")
    expected1 = [["a", "a", "b"], ["aa", "b"]]
    assert sorted(map(tuple, result1)) == sorted(map(tuple, expected1)), (
        f"Example 1: got {result1}, expected {expected1}"
    )

    # Example 2
    result2 = partition("a")
    expected2 = [["a"]]
    assert sorted(map(tuple, result2)) == sorted(map(tuple, expected2)), (
        f"Example 2: got {result2}, expected {expected2}"
    )

    # Edge case: single palindrome, one partition of the whole string
    result3 = partition("aba")
    expected3 = [["a", "b", "a"], ["aba"]]
    assert sorted(map(tuple, result3)) == sorted(map(tuple, expected3)), (
        f"Edge aba: got {result3}, expected {expected3}"
    )

    # Edge case: all same characters - every split is palindromic
    result4 = partition("aaa")
    expected4 = [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
    assert sorted(map(tuple, result4)) == sorted(map(tuple, expected4)), (
        f"Edge aaa: got {result4}, expected {expected4}"
    )

    print("All tests passed.")


# solved: 2026-11-04, medium, 60min, Palindrome Partitioning
