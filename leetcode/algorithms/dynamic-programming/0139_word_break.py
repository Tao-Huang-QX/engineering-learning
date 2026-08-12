"""
LeetCode 139: Word Break
https://leetcode.com/problems/word-break/

Problem: Given a string s and a dictionary of strings wordDict, return true if s
can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.
- All the strings of wordDict are unique.

Examples:
- Input: s = "leetcode", wordDict = ["leet","code"]
  Output: true
  Explanation: "leet" + "code" = "leetcode"

- Input: s = "applepenapple", wordDict = ["apple","pen"]
  Output: true
  Explanation: "apple" + "pen" + "apple" = "applepenapple"

- Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
  Output: false
  Explanation: No valid segmentation — "cats"+"and"+"og" leaves "og" (not in dict),
    "cat"+"sand"+"og" same issue, etc.

Approach: 1D DP — dp[i] = s[:i] can be segmented
- wordDict in a set for O(1) lookup
- dp[0] = True (empty prefix), for each i check all j < i:
  dp[i] = dp[j] and s[j:i] in word_set; break on first match

Time: O(n²)   Space: O(n)
"""


def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Return True if s can be segmented into words from wordDict.

    Args:
        s: Input string
        word_dict: List of valid dictionary words

    Returns:
        True if s can be segmented
    """
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    word_set = set(word_dict)

    for i in range(n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


if __name__ == "__main__":
    # Example 1
    result1 = word_break("leetcode", ["leet", "code"])
    expected1 = True
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = word_break("applepenapple", ["apple", "pen"])
    expected2 = True
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
    expected3 = False
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
