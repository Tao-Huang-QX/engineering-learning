"""
LeetCode 115: Distinct Subsequences
https://leetcode.com/problems/distinct-subsequences/

Problem: Given two strings s and t, return the number of distinct subsequences of s
which equals t.

The test cases are generated so that the answer fits on a 32-bit signed integer.

Constraints:
- 1 <= s.length <= 1000
- 1 <= t.length <= 1000
- s and t consist of only lowercase English letters.

Examples:
- Input: s = "rabbbit", t = "rabbit"
  Output: 3
  Explanation: Three ways to form "rabbit" from "rabbbit":
    rabb b it, ra b bbit, rabb b it

- Input: s = "babgbag", t = "bag"
  Output: 5
  Explanation: Five ways to form "bag" from "babgbag".

Approach: 2D DP — dp[i][j] = ways to form t[j:] from s[i:]
- Skip s[i]: always available, dp[i+1][j]
- Match s[i] with t[j]: only when s[i] == t[j], dp[i+1][j+1]
- Base: dp[i][n] = 1 (empty t), dp[m][j] = 0 (s exhausted)

Time: O(m * n)   Space: O(m * n)
"""


def num_distinct(s: str, t: str) -> int:
    """
    Return the number of distinct subsequences of s which equals t.

    Args:
        s: Source string
        t: Target subsequence string

    Returns:
        Number of distinct subsequences of s equal to t
    """
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][n] = 1  # t exhausted -> 1 way, skip everything remaining

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            dp[i][j] = dp[i + 1][j]  # go down, neglect s[i]

            if s[i] == t[j]:
                dp[i][j] += dp[i + 1][j + 1]  # diagonal: match both

    return dp[0][0]


if __name__ == "__main__":
    # Example 1
    result1 = num_distinct("rabbbit", "rabbit")
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = num_distinct("babgbag", "bag")
    expected2 = 5
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
