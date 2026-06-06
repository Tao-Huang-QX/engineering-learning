"""
LeetCode 438: Find All Anagrams in a String
https://leetcode.com/problems/find-all-anagrams-in-a-string/

Problem: Given two strings s and p, return an array of all the start indices of p's
anagrams in s. An anagram is a word or phrase formed by rearranging the letters
of a different word or phrase, typically using all the original letters exactly once.

Approach: Sliding window with character count matching
- Use Counter to track pattern and window character frequencies
- Maintain "match" count of distinct characters with equal counts
- Slide window: update match when adding/removing characters
- When match equals distinct char count, we found an anagram

Time: O(n)   Space: O(k) where k is distinct chars in p
"""

from collections import Counter


def find_anagrams(s: str, p: str) -> list[int]:
    """
    Return all start indices of p's anagrams in s.

    Args:
        s: String to search within
        p: Pattern string to find anagrams of

    Returns:
        List of start indices where anagrams of p begin in s
    """
    if len(s) < len(p):
        return []

    p_counter = Counter(p)
    window_counter = Counter(s[: len(p)])
    result = []
    left = 0
    match = 0
    for char in p_counter:
        if window_counter[char] == p_counter[char]:
            match += 1
    if match == len(p_counter):
        result.append(0)

    for right in range(len(p), len(s)):
        # Handle s[left] leaving
        if s[left] in p_counter:
            if p_counter[s[left]] == window_counter[s[left]]:
                match -= 1
            window_counter[s[left]] -= 1
            if p_counter[s[left]] == window_counter[s[left]]:
                match += 1

        if s[right] in p_counter:
            if p_counter[s[right]] == window_counter[s[right]]:
                match -= 1
            window_counter[s[right]] += 1
            if p_counter[s[right]] == window_counter[s[right]]:
                match += 1

        left += 1
        if match == len(p_counter):
            result.append(left)
    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (s, p, expected_indices)
        ("cbaebabacd", "abc", [0, 6]),  # "cba" at 0, "bac" at 6
        ("abab", "ab", [0, 1, 2]),  # "ab" at 0, "ba" at 1, "ab" at 2
    ]

    for s, p, expected in test_cases:
        result = find_anagrams(s, p)
        assert result == expected, f"s={s}, p={p}: got {result}, expected {expected}"

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Find All Anagrams in a String
