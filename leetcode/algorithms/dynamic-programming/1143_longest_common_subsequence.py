"""
LeetCode 1143: Longest Common Subsequence
https://leetcode.com/problems/longest-common-subsequence/

Problem: Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0. A subsequence is a sequence
that appears in the same relative order, but not necessarily contiguous.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English letters.

Approach: 2D Dynamic Programming
- Build (m+1) × (n+1) table where dp[i][j] = LCS length of text1[0:i] and text2[0:j]
- When characters match: extend diagonal by 1 (dp[i-1][j-1] + 1)
- When characters don't match: take max of top and left (max(dp[i-1][j], dp[i][j-1]))
- First row/col are 0 (empty string has no common subsequence)

Time: O(m × n)   Space: O(m × n)
where m = len(text1), n = len(text2)
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Return the length of the longest common subsequence between two strings.

    Args:
        text1: First string
        text2: Second string

    Returns:
        Length of the longest common subsequence
    """
    """
    # Use shorter string for space optimization
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    prev = [0] * (len(text2) + 1)
    for i in range(1, len(text1) + 1):
        curr = [0] * (len(text2) + 1)
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[-1]
    """
    dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


if __name__ == "__main__":
    # Example 1: "abc" is common
    result = longest_common_subsequence("abcde", "ace")
    assert result == 3, f"Example 1 failed: got {result}, expected 3"

    # Example 2: "abc" is common
    result = longest_common_subsequence("abc", "abc")
    assert result == 3, f"Example 2 failed: got {result}, expected 3"

    # Example 3: No common subsequence
    result = longest_common_subsequence("abc", "def")
    assert result == 0, f"Example 3 failed: got {result}, expected 0"

    print("All tests passed.")
