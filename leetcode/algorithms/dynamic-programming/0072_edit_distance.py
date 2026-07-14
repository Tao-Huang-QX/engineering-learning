"""
LeetCode 72: Edit Distance
https://leetcode.com/problems/edit-distance/

Problem: Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2. Operations: insert a character, delete a character,
or replace a character.

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters

Examples:
- Input: word1 = "horse", word2 = "ros", Output: 3 (horse → rorse → rose → ros)
- Input: word1 = "intention", word2 = "execution", Output: 5

Approach: 2D Dynamic Programming
- Build DP table where dp[i][j] = min operations to convert word1[:i] to word2[:j]
- Base cases: first row = insertions, first column = deletions
- Recurrence: if chars match, use diagonal; else min(replace, insert, delete) + 1

Time: O(m*n)   Space: O(m*n)
"""


def min_distance(word1: str, word2: str) -> int:
    """
    Return the minimum number of operations to convert word1 to word2.

    Args:
        word1: Source string
        word2: Target string

    Returns:
        Minimum edit distance (number of insert/delete/replace operations)
    """
    l1, l2 = len(word1), len(word2)
    if l1 == 0 or l2 == 0:
        return abs(l1 - l2)

    dp = [[0] * (l2 + 1) for _ in range(l1 + 1)]
    # First row: converting empty string to word2[0:j] (j insertions)
    for j in range(l2 + 1):
        dp[0][j] = j
    # First column: converting word1[0:i] to empty string (i deletions)
    for i in range(l1 + 1):
        dp[i][0] = i

    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Increment on minimum of replacement, insertion or deletion opertions
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1

    return dp[-1][-1]


if __name__ == "__main__":
    # Example 1: horse → ros
    result = min_distance("horse", "ros")
    assert result == 3, f"Example 1 failed: got {result}, expected 3"

    # Example 2: intention → execution
    result = min_distance("intention", "execution")
    assert result == 5, f"Example 2 failed: got {result}, expected 5"

    # Empty strings
    result = min_distance("", "")
    assert result == 0, f"Empty strings failed: got {result}, expected 0"

    # One empty string (all inserts)
    result = min_distance("", "abc")
    assert result == 3, f"One empty failed: got {result}, expected 3"

    # One empty string (all deletes)
    result = min_distance("abc", "")
    assert result == 3, f"Delete all failed: got {result}, expected 3"

    # Same strings
    result = min_distance("abc", "abc")
    assert result == 0, f"Same strings failed: got {result}, expected 0"

    print("All tests passed.")
