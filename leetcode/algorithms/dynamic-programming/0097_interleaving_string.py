"""
LeetCode 97: Interleaving String
https://leetcode.com/problems/interleaving-string/

Problem: Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.
An interleaving of two strings s and t is a configuration where s and t are divided into
n and m substrings respectively, and the interleaving alternates between s and t substrings.

Constraints:
- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.

Examples:
- Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
  Output: true
  Explanation: Split s1 into "aa" + "bc" + "c", s2 into "dbbc" + "a".
  Interleave: "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac"

- Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
  Output: false
  Explanation: Impossible to interleave s2 to obtain s3.

- Input: s1 = "", s2 = "", s3 = ""
  Output: true

Approach: 2D Dynamic Programming
- dp[i][j] = True if s1[:i] and s2[:j] can interleave to form s3[:i+j]
- Initialize first row: only s2 contributes (match s2[j-1] == s3[j-1])
- Initialize first column: only s1 contributes (match s1[i-1] == s3[i-1])
- Transition: if s1[i-1] matches s3[k], take from above (dp[i-1][j]); if s2[j-1] matches s3[k], take from left (dp[i][j-1])

Time: O(m × n)   Space: O(m × n)
"""


def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    Return whether s3 is formed by an interleaving of s1 and s2.

    Args:
        s1: First source string
        s2: Second source string
        s3: Target string to check

    Returns:
        True if s3 can be formed by interleaving s1 and s2, False otherwise
    """
    len1, len2, t_len = len(s1), len(s2), len(s3)
    if len1 + len2 != t_len:
        return False

    dp = [[False] * (len2 + 1) for _ in range(len1 + 1)]
    dp[0][0] = True

    # Initialize first row (only s2 contributes)
    for j in range(1, len2 + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]

    # Initialize first column (only s1 contributes)
    for i in range(1, len1 + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            k = i + j - 1  # Index in s3
            if s1[i - 1] == s3[k]:
                dp[i][j] = dp[i][j] or dp[i - 1][j]
            if s2[j - 1] == s3[k]:
                dp[i][j] = dp[i][j] or dp[i][j - 1]

    return dp[len1][len2]


if __name__ == "__main__":
    # Example 1: s1="aabcc", s2="dbbca", s3="aadbbcbcac" → True
    # s1 split: "aa" + "bc" + "c", s2 split: "dbbc" + "a"
    # Interleave: "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac"
    assert is_interleave("aabcc", "dbbca", "aadbbcbcac")

    # Example 2: s1="aabcc", s2="dbbca", s3="aadbbbaccc" → False
    # Impossible to interleave s2 to obtain s3
    assert not is_interleave("aabcc", "dbbca", "aadbbbaccc")

    # Example 3: All empty strings → True
    assert is_interleave("", "", "")

    # Edge case: s2 empty, s3 equals s1 → True
    assert is_interleave("a", "", "a")

    # Edge case: s1 empty, s3 equals s2 → True
    assert is_interleave("", "abc", "abc")

    # Edge case: Length mismatch → False
    assert not is_interleave("a", "b", "abc")

    print("All tests passed.")
