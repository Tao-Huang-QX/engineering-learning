"""
LeetCode 394: Decode Ways
https://leetcode.com/problems/decode-ways/

Problem: A message containing letters from A-Z can be encoded into numbers using
the mapping A -> "1", B -> "2", ..., Z -> "26". Given a string s containing only
digits, return the number of ways to decode it.

Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s)

Examples:
- Input: s = "12"
  Output: 2
  Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

- Input: s = "226"
  Output: 3
  Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

- Input: s = "06"
  Output: 0
  Explanation: "06" cannot be mapped to "F" because of the leading zero
    ("06" is not equal to "6").

Approach: Bottom-up 1D DP on prefix length (climbing stairs with validity masks)
- dp[i] = ways to decode the first i characters; dp[0] = 1 (empty prefix)
- Take one digit: dp[i-1], only if s[i-1] != '0' ('0' maps to nothing alone)
- Take two digits: dp[i-2], only if 10 <= int(s[i-2:i]) <= 26 (rejects
  leading-zero pairs like "06")

Time: O(n)   Space: O(n)   (O(1) space possible with two rolling variables)
"""


def num_decodings(s: str) -> int:
    """
    Return the number of ways to decode the digit string.

    Args:
        s: Digit string where '1'-'26' map to 'A'-'Z'

    Returns:
        Number of possible decodings (0 if none valid)
    """
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        dp[i] = (dp[i - 1] if s[i - 1] != "0" else 0) + (
            dp[i - 2] if i >= 2 and 10 <= int(s[i - 2 : i]) <= 26 else 0
        )
    return dp[n]


if __name__ == "__main__":
    # Example 1
    result1 = num_decodings("12")
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = num_decodings("226")
    expected2 = 3
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = num_decodings("06")
    expected3 = 0
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")


# solved: 2026-08-19, medium, 50min, Decode Ways
