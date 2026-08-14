"""
LeetCode 140: Word Break II
https://leetcode.com/problems/word-break-ii/

Problem: Given a string s and a dictionary of strings wordDict, add spaces in s to
construct a sentence where each word is a valid dictionary word. Return all such
possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Constraints:
- 1 <= s.length <= 20
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 10
- s and wordDict[i] consist of only lowercase English letters.
- All the strings of wordDict are unique.
- Input is generated in a way that the length of the answer doesn't exceed 10^5.

Examples:
- Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
  Output: ["cats and dog","cat sand dog"]
  Explanation: Two segmentations:
    "cats" + "and" + "dog" and "cat" + "sand" + "dog"

- Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
  Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]

- Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
  Output: []
  Explanation: No valid segmentation exists.

Approach: Memoized DFS on suffix
- dfs(pos) returns all sentences for s[pos:] (memoized by pos)
- For each dictionary word matching the current prefix, prepend to all sentences of the remainder
- Base case: pos == len(s) returns [""] (empty sentence)

Time: O(n² + output size)   Space: O(n · output size)
"""


def word_break(s: str, word_dict: list[str]) -> list[str]:
    """
    Return all sentences formed by segmenting s into dictionary words.

    Args:
        s: Input string
        word_dict: List of valid dictionary words

    Returns:
        List of all valid space-separated sentences
    """
    word_set = set(word_dict)
    memo: dict[int, list[str]] = {}

    def dfs(pos: int) -> list[str]:
        """Return all sentences for s[pos:]."""
        if pos in memo:
            return memo[pos]
        if pos == len(s):
            return [""]

        sentences: list[str] = []
        for end in range(pos + 1, len(s) + 1):
            word = s[pos:end]

            if word in word_set:
                for rest in dfs(end):
                    if rest:
                        sentences.append(word + " " + rest)
                    else:
                        sentences.append(word)

        memo[pos] = sentences
        return sentences

    return dfs(0)


if __name__ == "__main__":
    # Example 1
    result1 = word_break("catsanddog", ["cat", "cats", "and", "sand", "dog"])
    expected1 = ["cats and dog", "cat sand dog"]
    assert sorted(result1) == sorted(expected1), f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = word_break("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"])
    expected2 = ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]
    assert sorted(result2) == sorted(expected2), f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
    expected3: list[str] = []
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
