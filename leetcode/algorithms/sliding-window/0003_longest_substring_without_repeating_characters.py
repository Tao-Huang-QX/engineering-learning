"""
LeetCode 3: Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Problem: Find the length of the longest substring without repeating characters.

Approach: Sliding window with character index tracking
- Maintain left pointer and dict of char -> last index
- When duplicate found, jump left past previous occurrence
- Track max window size throughout

Time: O(n)   Space: O(min(n, charset))
"""


def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.

    Args:
        s: Input string

    Returns:
        Length of the longest substring with all unique characters
    """
    seen = {}  # character -> last index
    left = 0
    max_length = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1  # move left pointer past last occurrence
        seen[char] = right  # update last index of char
        max_length = max(max_length, right - left + 1)
    return max_length


if __name__ == "__main__":
    # Example 1
    assert length_of_longest_substring("abcabcbb") == 3

    # Example 2
    assert length_of_longest_substring("bbbbb") == 1

    # Example 3
    assert length_of_longest_substring("pwwkew") == 3

    # Example 4: Empty string
    assert length_of_longest_substring("") == 0

    # Example 5: All unique
    assert length_of_longest_substring("abcdef") == 6

    print("All tests passed.")
