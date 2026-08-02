"""
LeetCode 242: Valid Anagram
https://leetcode.com/problems/valid-anagram/

Problem: Given two strings s and t, return true if t is an anagram of s, and false otherwise.

Approach:
- Use dictionary to count frequency of characters in s and t, then compare the two dictionaries
- Python dict comparison checks if they have the same keys with the same values, so we can directly compare freq_s and freq_t

Time: O(n)   Space: O(k) where k is the number of unique characters in s and t
"""


def is_anagram(s: str, t: str) -> bool:
    """
    Return True if t is an anagram of s, False otherwise.

    Args:
        s: First string
        t: Second string

    Returns:
        True if t contains the same characters as s (same frequency, any order)
    """
    if len(s) != len(t):
        return False

    freq_s = {}  # or collections.Counter(s) can be used for a more concise implementation
    for char in s:
        freq_s[char] = freq_s.get(char, 0) + 1
    freq_t = {}
    for char in t:
        freq_t[char] = freq_t.get(char, 0) + 1
    return freq_s == freq_t


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (s, t, expected_result)
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "a", True),
        ("", "", True),  # empty strings are anagrams
        ("ab", "a", False),  # different lengths
    ]

    for s, t, expected in test_cases:
        result = is_anagram(s, t)
        assert result == expected, f"{s!r}, {t!r}: got {result}, expected {expected}"

    print("All tests passed.")
