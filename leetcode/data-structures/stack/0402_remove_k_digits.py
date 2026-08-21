"""
LeetCode 402: Remove K Digits
https://leetcode.com/problems/remove-k-digits/

Problem: Given string num representing a non-negative integer and an integer k,
remove k digits from num so that the resulting number is the smallest possible.
Return the result as a string.

Constraints:
- 1 <= k <= num.length <= 10^5
- num consists of only digits
- num does not have any leading zeros except for the zero itself

Examples:
- Input: num = "1432219", k = 3
  Output: "1219"
  Explanation: Remove the three digits 4, 3, and 2 to form "1219", the
    smallest number possible.

- Input: num = "10200", k = 1
  Output: "200"
  Explanation: Remove the leading 1 and the number is "200"; the result has
    no leading zeros.

- Input: num = "10", k = 2
  Output: "0"
  Explanation: Remove all the digits; the result is "0".

Approach: Monotonic increasing stack with a removal budget
- Scan left to right; while the kept-digit stack top is bigger than the
  incoming digit and budget remains, pop (spend one k) — replacing a large
  digit in a more significant position always wins
- Equal digits push (strict >): popping on ties wastes budget
- Leftover k after the scan means digits were non-decreasing — spend the
  remainder on the tail (least significant positions): stack[:-k]
- Strip leading zeros with string ops (lstrip), never an int() round-trip
  (CPython caps int/str conversion at 4300 digits; constraint is 10^5)

Time: O(n)   Space: O(n)
"""


def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits from num to form the smallest possible integer.

    Args:
        num: String of digits
        k: Number of digits to remove (1 <= k <= len(num))

    Returns:
        Smallest integer achievable, as a string ("0" if all removed)
    """
    stack: list[str] = []
    for digit in num:
        while stack and stack[-1] > digit and k > 0:
            stack.pop()
            k -= 1
        stack.append(digit)

    # leftover k: digits were non-decreasing, so the biggest (least
    # significant) digits are at the tail - drop them there
    stack = stack[:-k] if k else stack

    result = "".join(stack).lstrip("0")
    return result or "0"


if __name__ == "__main__":
    # Example 1
    result1 = remove_k_digits("1432219", 3)
    expected1 = "1219"
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = remove_k_digits("10200", 1)
    expected2 = "200"
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = remove_k_digits("10", 2)
    expected3 = "0"
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")


# solved: 2026-08-21, medium, 90min, Remove K Digits
