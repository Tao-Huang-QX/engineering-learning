"""
LeetCode 143: Reorder List
https://leetcode.com/problems/reorder-list/

Problem: You are given the head of a singly linked-list. The list can be
represented as: L0 → L1 → … → Ln - 1 → Ln. Reorder the list to be on the
following form: L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …. You may not modify
the values in the list's nodes. Only nodes themselves may be changed.

Constraints:
- The number of nodes in the list is in the range [1, 5 * 10^4]
- 1 <= Node.val <= 1000

Examples:
- Input: head = [1,2,3,4]
  Output: [1,4,2,3]

- Input: head = [1,2,3,4,5]
  Output: [1,5,2,4,3]

Approach: Three-step in-place (find middle → reverse second half → merge)
- Slow/fast pointers (advance while fast and fast.next) park slow on the
  right-middle node for even lengths, exact middle for odd lengths
- Reverse the second half starting AT slow itself (inclusive) — for even
  lengths the halves then overlap at one node, and the node before it
  keeps a stale pointer into the reversed part
- Weave the halves pair by pair: save both nexts, point first.next at the
  reversed node and its next at the saved first.next, advance both
- The overlap makes the middle node briefly point to itself; the merge
  loop clears it (odd lengths) or the final to_end.next = None does
  (even lengths), which also terminates the list

Time: O(n) — each node visited O(1) times across all phases   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def reorder_list(head: ListNode | None) -> None:
    """
    Reorder the linked list in place: L0 → Ln → L1 → Ln-1 → ...

    Args:
        head: Head of the singly linked list

    Returns:
        None (modifies list in place)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # pyright: ignore[reportOptionalMemberAccess]
        fast = fast.next.next

    # Reverse the second half
    prev = None
    cur = slow  # pyright: ignore[reportOptionalMemberAccess]
    while cur:
        next_node = cur.next
        cur.next = prev
        prev = cur
        cur = next_node

    # Merge the first half with the reversed second half
    l1, l2 = head, prev
    while l1 and l2:
        temp1 = l1.next
        l1.next = l2
        temp2 = l2.next
        l2.next = temp1
        l1 = temp1
        l2 = temp2

    # Handle the termination
    if to_end := l1:
        to_end.next = None  # pyright: ignore[reportOptionalMemberAccess]


if __name__ == "__main__":
    # Helper function to create list from Python list
    def create_list(values: list[int]) -> ListNode | None:
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    # Helper function to convert list to Python list
    def to_list(head: ListNode | None) -> list[int]:
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    # Test cases from problem description
    test_cases = [
        # (input, expected_output)
        ([1, 2, 3, 4], [1, 4, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3]),
        ([], []),
        ([1], [1]),
    ]

    for vals, expected in test_cases:
        val_list = create_list(vals)
        reorder_list(val_list)
        result = to_list(val_list)
        assert result == expected, f"got {result}, expected {expected}"

    print("All tests passed.")
