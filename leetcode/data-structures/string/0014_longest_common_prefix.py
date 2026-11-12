"""
LeetCode 14: Longest Common Prefix
https://leetcode.com/problems/longest-common-prefix/

Problem: Write a function to find the longest common prefix string amongst
an array of strings. If there is no common prefix, return an empty string "".

Constraints:
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200
- strs[i] consists of only lowercase English letters

Examples:
- Input: strs = ["flower","flow","flight"]
  Output: "fl"

- Input: strs = ["dog","racecar","car"]
  Output: ""
  Explanation: There is no common prefix among the input strings.

Approach: Horizontal fold — pairwise shrink the running prefix
- Keep the current common prefix (seed: first string); fold each next
  string in, truncating to the matching head — min(len) bounds the scan,
  so an empty member collapses everything for free
- The prefix only ever shrinks, so the answer never exceeds the shortest
  string seen so far

Time: O(S) total characters   Space: O(1) beyond the slices
"""


def longest_common_prefix(strs: list[str]) -> str:
    """
    Return the longest common prefix of all strings.

    Args:
        strs: Non-empty list of lowercase strings (individual strings
            may be empty)

    Returns:
        The longest common prefix, "" if none
    """
    if len(strs) == 1:
        return strs[0]

    result = strs[0]

    for s in strs[1:]:
        match = 0

        for i in range(min(len(result), len(s))):
            if result[i] != s[i]:
                break
            else:
                match = i + 1

        result = s[:match]

    return result


if __name__ == "__main__":
    # Example 1
    result1 = longest_common_prefix(["flower", "flow", "flight"])
    expected1 = "fl"
    assert result1 == expected1, f"Example 1: got {result1!r}, expected {expected1!r}"

    # Example 2: no common prefix
    result2 = longest_common_prefix(["dog", "racecar", "car"])
    expected2 = ""
    assert result2 == expected2, f"Example 2: got {result2!r}, expected {expected2!r}"

    # Edge: a single string is its own prefix
    result3 = longest_common_prefix(["abcdef"])
    expected3 = "abcdef"
    assert result3 == expected3, f"Single: got {result3!r}, expected {expected3!r}"

    # Edge: one empty string caps everything
    result4 = longest_common_prefix(["abc", "", "abd"])
    expected4 = ""
    assert result4 == expected4, f"Empty member: got {result4!r}, expected {expected4!r}"

    # Edge: the shortest string is the whole answer
    result5 = longest_common_prefix(["ab", "abc", "abcd"])
    expected5 = "ab"
    assert result5 == expected5, f"Shortest: got {result5!r}, expected {expected5!r}"

    # Edge: identical strings
    result6 = longest_common_prefix(["same", "same", "same"])
    expected6 = "same"
    assert result6 == expected6, f"Identical: got {result6!r}, expected {expected6!r}"

    # Edge: single-character strings agreeing/disagreeing
    assert longest_common_prefix(["a"]) == "a"
    assert longest_common_prefix(["a", "b"]) == ""

    print("All tests passed.")


# solved: 2026-11-12, easy, 10min, Longest Common Prefix
