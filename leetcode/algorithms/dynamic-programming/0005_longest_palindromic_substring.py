"""
LeetCode 5: Longest Palindromic Substring
https://leetcode.com/problems/longest-palindromic-substring/

Problem: Given a string s, return the longest palindromic substring in s.

Constraints:
- 1 <= s.length <= 1000
- s consists of only digits and English letters.

Approach: Manacher's Algorithm
- Transform string with '#' separators to handle odd/even lengths uniformly
- Use radius array and mirror positions for O(n) time complexity
- Track center/right boundary to avoid redundant comparisons

Time: O(n)   Space: O(n)
"""


def longest_palindromic_substring(s: str) -> str:
    """
    Return the longest palindromic substring in s.

    Args:
        s: Input string consisting of digits and English letters

    Returns:
        The longest palindromic substring
    """
    """
    O(n^2) time O(1) space
    def expand(left: int, right: int) -> str:
        # Expand around center and return palindrome
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1 : right]
    longest = ""
    for i in range(len(s)):
        # Odd length: center at i (e.g., "aba")
        palindrome1 = expand(i, i)
        # Even length: center between i and i+1 (e.g., "abba")
        palindrome2 = expand(i, i + 1)
        longest = max(longest, palindrome1, palindrome2, key=len)
    return longest
    """
    # Step 1: Transform "babad" -> #b#a#b#a#d#
    t = "#" + "#".join(s) + "#"
    n = len(t)
    radius = [0] * n
    center = right = 0

    for i in range(n):
        # Step 2: Use mirror information if i is within current boundary
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])
            # Why min? Mirror's radius might extend past right boundary,
            # and we can't guarantee those characters match

        # Step 3: Try to expand (at least 1 step)
        while (
            i - radius[i] - 1 >= 0
            and i + radius[i] + 1 < n
            and t[i - radius[i] - 1] == t[i + radius[i] + 1]
        ):
            radius[i] += 1

        # Step 4: Update center/right if we expanded past current boundary
        if i + radius[i] > right:
            center, right = i, i + radius[i]

    # Find max radius
    max_idx = max(range(n), key=lambda i: radius[i])
    start = (max_idx - radius[max_idx]) // 2
    return s[start : start + radius[max_idx]]


if __name__ == "__main__":
    # Example 1: "bab" or "aba" is the longest palindrome
    result = longest_palindromic_substring("babad")
    assert result in ("bab", "aba"), f"Example 1 failed: got {result}, expected 'bab' or 'aba'"

    # Example 2: "bb" is the longest palindrome
    result = longest_palindromic_substring("cbbd")
    assert result == "bb", f"Example 2 failed: got {result}, expected 'bb'"

    print("All tests passed.")
