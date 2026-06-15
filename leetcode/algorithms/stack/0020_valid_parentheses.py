"""
LeetCode 20: Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Problem: Given a string s containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

Approach:
- Push opening brackets onto a stack
- For closing brackets, check if the top matches (using dict)
- Invalid if stack is empty when closing or wrong bracket type
- Valid if stack is empty at the end

Time: O(n)   Space: O(n) in worst case (all opening brackets)
"""


def is_valid(s: str) -> bool:
    """
    Return True if the string contains valid bracket pairs.

    Args:
        s: String containing only '(){}[]'

    Returns:
        True if brackets are properly matched and nested
    """
    if len(s) % 2 != 0:
        return False
    stack = []
    matches = {"}": "{", "]": "[", ")": "("}
    for char in s:
        if char in matches:
            if not stack or stack.pop() != matches[char]:
                return False
        else:
            stack.append(char)  #  opening bracket goes into the stack
    return not stack


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_result)
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("", True),  # Empty string is valid
        ("(", False),  # Single opening bracket
        (")", False),  # Single closing bracket
        ("((()))", True),
        ("([{}])", True),
    ]

    for s, expected in test_cases:
        result = is_valid(s)
        assert result == expected, f"{s!r}: got {result}, expected {expected}"

    print("All tests passed.")
