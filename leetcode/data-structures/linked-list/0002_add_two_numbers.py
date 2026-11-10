"""
LeetCode 2: Add Two Numbers
https://leetcode.com/problems/add-two-numbers/

Problem: You are given two non-empty linked lists representing two
non-negative integers. The digits are stored in REVERSE order, and each of
their nodes contains a single digit. Add the two numbers and return the sum
as a linked list. You may assume the two numbers do not contain any leading
zero, except the number 0 itself.

Constraints:
- The number of nodes in each list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have
  leading zeros

Examples:
- Input: l1 = 2 -> 4 -> 3, l2 = 5 -> 6 -> 4   (342 + 465)
  Output: 7 -> 0 -> 8                          (807)

- Input: l1 = 0, l2 = 0
  Output: 0

- Input: l1 = 9 -> 9 -> 9 -> 9 -> 9 -> 9 -> 9, l2 = 9 -> 9 -> 9 -> 9
  Output: 8 -> 9 -> 9 -> 9 -> 0 -> 0 -> 0 -> 1  (9999999 + 9999 = 10009998)

Approach: Schoolbook addition in one loop — dummy head, carry as loop citizen
- while l1 or l2 or carry: missing digits are 0, so unequal lengths and
  the trailing carry are loop iterations, not special cases (a spliced
  remainder phase would need separate carry repair — the seam drops it)
- divmod(sum, 10) splits digit and carry per node

Time: O(max(m, n))   Space: O(1) beyond the output
"""


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Add two non-negative numbers stored as reversed-digit linked lists.

    Args:
        l1: First number, least significant digit first
        l2: Second number, least significant digit first

    Returns:
        Head of the sum, least significant digit first
    """
    dummy = tail = ListNode()
    carry = 0

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        carry, digit = divmod(v1 + v2 + carry, 10)
        tail.next = ListNode(digit)
        tail = tail.next

        l1 = l1.next if l1 else None  # pyright: ignore[reportAssignmentType]
        l2 = l2.next if l2 else None  # pyright: ignore[reportAssignmentType]

    return dummy.next


if __name__ == "__main__":

    def to_list(node: ListNode | None) -> list[int]:
        out: list[int] = []
        while node:
            out.append(node.val)
            node = node.next
        return out

    def from_list(vals: list[int]) -> ListNode:
        head = ListNode(vals[0])
        cur = head
        for v in vals[1:]:
            cur.next = ListNode(v)
            cur = cur.next
        return head

    # Example 1: standard carry propagation
    result1 = add_two_numbers(from_list([2, 4, 3]), from_list([5, 6, 4]))
    assert to_list(result1) == [7, 0, 8], f"Example 1: got {to_list(result1)}"

    # Example 2: zeros
    result2 = add_two_numbers(from_list([0]), from_list([0]))
    assert to_list(result2) == [0], f"Example 2: got {to_list(result2)}"

    # Example 3: different lengths + final carry grows the result
    result3 = add_two_numbers(from_list([9, 9, 9, 9, 9, 9, 9]), from_list([9, 9, 9, 9]))
    assert to_list(result3) == [8, 9, 9, 9, 0, 0, 0, 1], f"Example 3: got {to_list(result3)}"

    # Edge: unequal lengths, no carries at all
    result4 = add_two_numbers(from_list([1, 2]), from_list([3]))
    assert to_list(result4) == [4, 2], f"Unequal: got {to_list(result4)}"

    # Edge: single-digit addition producing a carry chain
    result5 = add_two_numbers(from_list([5]), from_list([5]))
    assert to_list(result5) == [0, 1], f"Carry: got {to_list(result5)}"

    print("All tests passed.")


# solved: 2026-11-10, medium, 40min, Add Two Numbers
