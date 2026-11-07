"""
LeetCode 8: String to Integer (atoi)
https://leetcode.com/problems/string-to-integer-atoi/

Problem: Implement the myAtoi(string s) function, which converts a string to
a 32-bit signed integer (similar to C/C++'s atoi function).

The algorithm:
1. Whitespace: ignore any leading whitespace (" ").
2. Signedness: check the next character (if not already at the end) for
   '-' or '+'. Read this in if it is either.
3. Conversion: read in the digits until the next non-digit character or
   the end of the input. If no digits were read, the integer is 0.
4. Rounding: if the integer is out of the 32-bit signed integer range
   [-2^31, 2^31 - 1], clamp it to remain in range.

Constraints:
- 0 <= s.length <= 200
- s consists of English letters, digits, ' ', '+', '-', and '.'

Examples:
- Input: s = "42"            Output: 42
- Input: s = "   -42"        Output: -42   (whitespace + sign)
- Input: s = "4193 with words" Output: 4193 (stop at first non-digit)
- Input: s = "words and 987" Output: 0     (no leading digit)
- Input: s = "-91283472332"  Output: -2147483648 (clamped to the low bound)

Approach: Regex whitelist + clamp (evolved from an explicit parsing loop)
- re.match(r"[+-]?\\d+", s.lstrip()) states the conversion rule directly:
  optional sign, then digits, at the start after whitespace — anything
  else (letters, ".", junk of any alphabet) simply fails to match → 0
- The match, when present, is exactly the number prefix; int() it and
  clamp into [-2^31, 2^31 - 1]
- Post-hoc clamping is Pythonic and safe: big ints mean the parse can
  overshoot and be clamped after, where C must clamp during accumulation
- Journey note: the original loop version used a blacklist guard
  (isalpha / ".") that was complete only for LC's stated alphabet — the
  regex whitelist removed the alphabet dependency entirely, and made the
  dot check and empty-collected-string guards unreachable (deleted)

Time: O(n)   Space: O(n) for the stripped copy (O(1) beyond the match)
"""

import re


def my_atoi(s: str) -> int:
    """
    Convert a string to a 32-bit signed integer, atoi-style.

    Args:
        s: Input string; may contain whitespace, signs, digits, junk

    Returns:
        The parsed integer clamped to [-2^31, 2^31 - 1]; 0 if no digits
    """
    m = re.match(r"[+-]?\d+", s.lstrip())
    return max(-(2**31), min(2**31 - 1, int(m.group()))) if m else 0


if __name__ == "__main__":
    # Example 1
    assert my_atoi("42") == 42, f"Example 1: got {my_atoi('42')}"

    # Example 2: leading whitespace + sign
    assert my_atoi("   -42") == -42, f"Example 2: got {my_atoi('   -42')}"

    # Example 3: digits then trailing junk
    assert my_atoi("4193 with words") == 4193, f"Example 3: got {my_atoi('4193 with words')}"

    # Example 4: junk before digits — no conversion
    assert my_atoi("words and 987") == 0, f"Example 4: got {my_atoi('words and 987')}"

    # Example 5: underflow clamps to the low bound
    assert my_atoi("-91283472332") == -(2**31), f"Example 5: got {my_atoi('-91283472332')}"

    # Edge: overflow clamps to the high bound
    assert my_atoi("21474836460") == 2**31 - 1, f"Overflow: got {my_atoi('21474836460')}"

    # Edge: explicit plus sign
    assert my_atoi("+1") == 1, f"Plus: got {my_atoi('+1')}"

    # Edge: double sign — no conversion
    assert my_atoi("+-12") == 0, f"Double sign: got {my_atoi('+-12')}"

    # Edge: leading zeros collapse
    assert my_atoi("  000000000001234") == 1234, f"Zeros: got {my_atoi('  000000000001234')}"

    # Edge: digit-then-dot stops at the dot
    assert my_atoi("3.14159") == 3, f"Float: got {my_atoi('3.14159')}"

    # Edge: empty and sign-only strings
    assert my_atoi("") == 0, f"Empty: got {my_atoi('')}"
    assert my_atoi("+") == 0, f"Sign only: got {my_atoi('+')}"

    print("All tests passed.")


# solved: 2026-11-07, medium, 40min, String to Integer (atoi)
