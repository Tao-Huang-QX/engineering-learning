"""
LeetCode 155: Min Stack
https://leetcode.com/problems/min-stack/

Problem: Design a stack that supports push, pop, top, and retrieving the
minimum element in CONSTANT time.

Implement the MinStack class:
- MinStack() initializes the stack object
- push(val) pushes the element val onto the stack
- pop() removes the element on the top of the stack
- top() gets the top element of the stack
- get_min() retrieves the minimum element in the stack

Each function runs in O(1) time.

Constraints:
- -2^31 <= val <= 2^31 - 1
- Methods pop, top, and get_min will always be called on non-empty stacks
- At most 3 * 10^4 calls in total

Examples:
- Input: ["MinStack","push","push","push","getMin","pop","top","getMin"]
        [[],[-2],[0],[-3],[],[],[],[]]
  Output: [null, null, null, null, -3, null, 0, -2]
  Explanation: after pushing -2, 0, -3 -> min is -3; pop removes -3;
    top is 0; min is back to -2.

Approach: Min-event stack (monotonic non-increasing companion)
- stack keeps pure push order (LIFO identity, never reorganized)
- min_stack records only NEW minimums: push when val <= its top
  (<= keeps duplicate minimums, so each copy pops its own record)
- pop releases a record iff the popped value equals min_stack's top;
  get_min reads min_stack[-1] — no scans, no shuffles, all O(1)
- Rejected earlier design: sorted companion list — behavior was correct
  but push's insertion shuffle and pop's list.remove were O(n), violating
  the all-O(1) spec (16.5s for 30k ops vs 0.003s here)

Time: all operations O(1)   Space: O(n)
"""


class MinStack:
    def __init__(self) -> None:
        """
        Initialize the stack.
        """
        # stack holds the pushed values in order (LIFO identity, never reorganized)
        self.stack: list[int] = []
        # min_stack records only new minimums — monotonic non-increasing,
        # top is always the current min
        self.min_stack: list[int] = []

    def push(self, val: int) -> None:
        """
        Push val onto the stack.

        Args:
            val: Integer in [-2^31, 2^31 - 1]
        """
        self.stack.append(val)

        if not self.min_stack or self.min_stack[-1] >= val:
            self.min_stack.append(val)

    def pop(self) -> None:
        """
        Remove the top element (stack is non-empty).
        """
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        """
        Return the top element.

        Returns:
            The top element (stack is non-empty)
        """
        return self.stack[-1]

    def get_min(self) -> int:
        """
        Return the minimum element.

        Returns:
            The current minimum (stack is non-empty)
        """
        return self.min_stack[-1]


if __name__ == "__main__":
    # Example walkthrough
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)
    assert stack.get_min() == -3, f"Step 4: got {stack.get_min()}"
    stack.pop()
    assert stack.top() == 0, f"Step 6: got {stack.top()}"
    assert stack.get_min() == -2, f"Step 8: got {stack.get_min()}"

    # Edge: min released by pop, then a new min arrives
    s2 = MinStack()
    for v in (5, 3, 7):
        s2.push(v)
    assert s2.get_min() == 3
    s2.pop()  # 7 gone, min still 3
    s2.pop()  # 3 gone, min back to 5
    assert s2.get_min() == 5, f"Min after pops: got {s2.get_min()}"
    s2.push(1)
    assert s2.get_min() == 1, f"New min: got {s2.get_min()}"

    # Edge: duplicates of the minimum
    s3 = MinStack()
    for v in (2, 2, 1, 1):
        s3.push(v)
    s3.pop()  # one 1 gone, the other 1 must still report as min
    assert s3.get_min() == 1, f"Duplicate min: got {s3.get_min()}"
    s3.pop()
    assert s3.get_min() == 2, f"Min restored: got {s3.get_min()}"

    # Edge: single element, negatives at int bounds
    s4 = MinStack()
    s4.push(-(2**31))
    assert s4.get_min() == -(2**31) and s4.top() == -(2**31)
    s4.pop()
    s4.push(2**31 - 1)
    assert s4.get_min() == 2**31 - 1

    print("All tests passed.")


# solved: 2026-11-12, medium, 30min, Min Stack
