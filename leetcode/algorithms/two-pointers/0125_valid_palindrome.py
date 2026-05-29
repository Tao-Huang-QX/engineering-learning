"""
LeetCode 125: Valid Palindrome
https://leetcode.com/problems/valid-palindrome/

Problem: A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Approach:
- two pointers from each end of the string
- skip the non-alphanumeric characters and duplicate characters
- compare the lower case version of characters

Time: O(n)   Space: O(1)
"""


def is_palindrome(s: str) -> bool:
    """
    Return True if s is a palindrome after removing non-alphanumeric chars and ignoring case.

    Args:
        s: Input string

    Returns:
        True if the cleaned string is a palindrome
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_result)
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),  # Empty string is palindrome
        ("", True),  # Empty string is palindrome
        ("a", True),  # Single character is palindrome
        ("ab", False),
        ("aba", True),
        ("0P", False),
    ]

    for s, expected in test_cases:
        result = is_palindrome(s)
        assert result == expected, f"{s!r}: got {result}, expected {expected}"

    print("All tests passed.")
