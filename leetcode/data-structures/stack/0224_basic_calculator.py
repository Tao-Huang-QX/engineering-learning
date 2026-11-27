r"""
LeetCode 224: Basic Calculator
https://leetcode.com/problems/basic-calculator/

Problem: Given a string s representing a valid expression, implement
a basic calculator to evaluate it, and return the result. You are not
allowed to use any built-in library function to directly evaluate the
expression such as eval().

Constraints:
- 1 <= s.length <= 3 * 10^5
- s consists of digits, '+', '-', '(', ')', and ' '
- s represents a valid expression
- '+' is not used as a unary operation
- '-' could be used as a unary operation (e.g., "-1" and "-(2 + 3)"
  are valid inputs)
- Every number and running calculation fits in a signed 32-bit integer

Examples:
- Input: s = "1 + 1"
  Output: 2

- Input: s = " 2-1 + 2 "
  Output: 3

- Input: s = "(1+(4+5+2)-3)+(6+8)"
  Output: 23

Approach: Regex scanner + scope-stack evaluation
- re.findall(r"\d+|[+\-()]", s) tokenizes: digit runs, parens, signs —
  spaces vanish at the scan
- One pass with result/sign and a scope stack: '(' freezes (result,
  sign) including any pending unary sign; ')' pops and folds the inner
  total back in
- '-' toggles the pending sign (unary minus and stacked double
  negation both come out right); '+' sets it absolutely — unary +
  doesn't exist; digits commit sign * value then reset

Time: O(n)   Space: O(n) tokens + nesting depth
"""

import re


def calculate(s: str) -> int:
    """
    Evaluate the arithmetic expression in s.

    Args:
        s: Expression with non-negative integers, '+', '-', parentheses,
           and spaces; '-' may appear as a unary operator

    Returns:
        The evaluated 32-bit integer result
    """
    tokens: list[str] = re.findall(r"\d+|[+\-()]", s)
    result, sign = 0, 1
    stack: list[tuple[int, int]] = []
    for tok in tokens:
        if tok == "(":
            stack.append((result, sign))  # freeze outer scope WITH the pending sign
            result, sign = 0, 1
        elif tok == ")":
            outer_result, outer_sign = stack.pop()
            result = outer_result + outer_sign * result
            sign = 1
        elif tok == "-":
            sign = -sign  # toggle - double negation comes out right
        elif tok == "+":
            sign = 1  # unary + doesn't exist: set absolutely
        else:  # digit run
            result += sign * int(tok)
            sign = 1

    return result


if __name__ == "__main__":
    # Example 1
    assert calculate("1 + 1") == 2, f"Example 1: got {calculate('1 + 1')}"

    # Example 2: spaces everywhere
    assert calculate(" 2-1 + 2 ") == 3, f"Example 2: got {calculate(' 2-1 + 2 ')}"

    # Example 3: nested parentheses
    assert calculate("(1+(4+5+2)-3)+(6+8)") == 23, (
        f"Example 3: got {calculate('(1+(4+5+2)-3)+(6+8)')}"
    )

    # Edge: unary minus at the start
    assert calculate("-1") == -1, f"Unary start: got {calculate('-1')}"
    assert calculate("-2+ 1") == -1, f"Unary mix: got {calculate('-2+ 1')}"

    # Edge: unary minus on a parenthesized group
    assert calculate("-(2+3)") == -5, f"Unary group: got {calculate('-(2+3)')}"

    # Edge: double parentheses
    assert calculate("((2+3))") == 5, f"Double parens: got {calculate('((2+3))')}"

    # Edge: multi-digit numbers
    assert calculate("123") == 123, f"Multi-digit: got {calculate('123')}"
    assert calculate("12-3") == 9, f"Subtract: got {calculate('12-3')}"

    print("All tests passed.")


# solved: 2026-11-27, hard, 60min, Basic Calculator
