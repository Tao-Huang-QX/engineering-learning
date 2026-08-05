"""
LeetCode 150: Evaluate Reverse Polish Notation
https://leetcode.com/problems/evaluate-reverse-polish-notation/

Problem: You are given an array of strings tokens that represents an arithmetic
expression in Reverse Polish Notation. Evaluate the expression. Return an integer
that represents the value of the expression.

Valid operators: +, -, *, /
Each operand may be an integer or another expression.
Division between two integers truncates toward zero.
There will not be any division by zero.
The given RPN expression is always valid.

Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator: "+", "-", "*", "/", or an integer in [-200, 200]

Examples:
- Input: tokens = ["2","1","+","3","*"]
  Output: 9
  Explanation: ((2 + 1) * 3) = 9

- Input: tokens = ["4","13","5","/","+"]
  Output: 6
  Explanation: (4 + (13 / 5)) = 6

- Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
  Output: 22
  Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
  = ((10 * (6 / (12 * -11))) + 17) + 5
  = ((10 * (6 / -132)) + 17) + 5
  = ((10 * 0) + 17) + 5
  = (0 + 17) + 5
  = 17 + 5
  = 22

Approach: Stack evaluation
- Push all operands (integers) onto a stack
- On operator: pop right, then left operand, compute, push result back
- Division: int(a / b) truncates toward zero (vs // which floors, wrong for negatives)
- After processing all tokens, the stack contains a single value — the answer

Time: O(n) — single pass through tokens
Space: O(n) — stack holds up to n/2 operands in the worst case
"""


def eval_rpn(tokens: list[str]) -> int:
    """
    Evaluate the value of an arithmetic expression in Reverse Polish Notation.

    Args:
        tokens: List of strings representing operands and operators

    Returns:
        Integer value of the evaluated expression
    """
    stack: list[int] = []
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token in operators:
            num2 = stack.pop()
            num1 = stack.pop()

            match token:
                case "+":
                    stack.append(num1 + num2)
                case "-":
                    stack.append(num1 - num2)
                case "*":
                    stack.append(num1 * num2)
                case "/":
                    stack.append(int(num1 / num2))
        else:
            stack.append(int(token))

    return stack[0]


if __name__ == "__main__":
    # Example 1
    result1 = eval_rpn(["2", "1", "+", "3", "*"])
    expected1 = 9
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = eval_rpn(["4", "13", "5", "/", "+"])
    expected2 = 6
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"])
    expected3 = 22
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
