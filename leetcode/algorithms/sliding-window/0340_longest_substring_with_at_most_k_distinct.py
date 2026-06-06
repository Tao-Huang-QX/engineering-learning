"""
LeetCode 340: Longest Substring with At Most K Distinct Characters
https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

Problem: Given a string s and an integer k, return the length of the longest
substring that contains at most k distinct characters.

Approach: Sliding window with character count
- Expand window by adding characters from right
- When distinct chars exceed k, shrink from left
- Track max length throughout

Time: O(n)   Space: O(k)
"""


def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Return the length of the longest substring with at most k distinct characters.

    Args:
        s: Input string
        k: Maximum number of distinct characters allowed

    Returns:
        Length of longest valid substring
    """
    char_count = {}
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Expand: add current character
        char_count[s[right]] = char_count.get(s[right], 0) + 1

        while len(char_count) > k:
            # Shrink window
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        # Window is now valid, update max
        max_len = max(max_len, right - left + 1)
    return max_len


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (s, k, expected_length)
        ("eceba", 2, 3),  # "ece" is the longest substring with at most 2 distinct chars
        ("aa", 1, 2),  # "a" is the longest substring with at most 1 distinct char
        ("abaccc", 2, 4),  # "accc" is the longest with at most 2 distinct chars
    ]

    for s, k, expected in test_cases:
        result = length_of_longest_substring_k_distinct(s, k)
        assert result == expected, f"s={s}, k={k}: got {result}, expected {expected}"

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Longest Substring with At Most K Distinct
