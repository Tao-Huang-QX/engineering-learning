"""
LeetCode 567: Permutation in String
https://leetcode.com/problems/permutation-in-string/

Problem: Given two strings s1 and s2, return true if s2 contains a permutation of s1.

Approach: Fixed-size sliding window with match count optimization
- Build frequency map for s1 and initial window in s2
- Track how many character frequencies match
- Slide window: update freq and matches in O(1) per step
- When all chars match, permutation found

Time: O(n)   Space: O(1) - 26 char alphabet
"""

from collections import Counter


def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains a permutation of s1.

    Args:
        s1: The pattern string to find permutation of
        s2: The string to search in

    Returns:
        True if s2 contains a permutation of s1, False otherwise
    """
    freq_s1 = Counter(s1)
    window_size = len(s1)

    # Initial window
    freq_window = Counter(s2[:window_size])

    # Count matching characters
    matches = 0
    for c in freq_s1:
        if freq_window[c] == freq_s1[c]:
            matches += 1
    if matches == len(freq_s1):
        return True

    # Slide the window
    for right in range(window_size, len(s2)):
        left_char = s2[right - window_size]
        right_char = s2[right]

        # Process left char (removing)
        if left_char in freq_s1:
            if freq_window[left_char] == freq_s1[left_char]:
                matches -= 1  # was matching, now won't
            freq_window[left_char] -= 1
            if freq_window[left_char] == freq_s1[left_char]:
                matches += 1  # now matches again

        # Process right char (adding)
        if right_char in freq_s1:
            if freq_window[right_char] == freq_s1[right_char]:
                matches -= 1  # was matching, now won't
            freq_window[right_char] += 1
            if freq_window[right_char] == freq_s1[right_char]:
                matches += 1  # now matches again

        if matches == len(freq_s1):
            return True

    return False


if __name__ == "__main__":
    # Example 1
    assert check_inclusion("ab", "eidbaooo")

    # Example 2
    assert not check_inclusion("ab", "eidboaoo")

    # Example 3: Single character
    assert check_inclusion("a", "a")

    # Example 4: s1 longer than s2
    assert not check_inclusion("abc", "ab")

    # Example 5: Exact match
    assert check_inclusion("abc", "abc")

    print("All tests passed.")
