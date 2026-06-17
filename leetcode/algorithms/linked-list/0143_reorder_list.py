"""
LeetCode 143: Reorder List
https://leetcode.com/problems/reorder-list/

Problem: Given the head of a singly linked list, reorder it in place: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...
You may not modify the values in the list's nodes. Only nodes themselves can be changed.

Approach: Three-step in-place (find middle → reverse second half → merge)
- Slow/fast pointer finds the middle node; stopping at left-middle ensures
  the first half is never shorter than the second.
- Reverse the second half starting from slow.next, then disconnect
  (or simply let the merge overwrite the stale middle link).
- Interleave by weaving first and second pointers: for each pair,
  save both nexts, redirect first.next to second and second.next to
  the saved first.next, then advance. After the second half exhausts,
  the remaining first node is already the tail — set its next to None.

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
    if not head or not head.next:
        return  # Handles empty and single node

    slow = fast = head
    while fast.next and fast.next.next:  # pyright: ignore[reportOptionalMemberAccess]
        slow = slow.next  # pyright: ignore[reportOptionalMemberAccess]
        fast = fast.next.next  # pyright: ignore[reportOptionalMemberAccess]

    # Reverse the second half
    prev = None
    curr = slow.next  # pyright: ignore[reportOptionalMemberAccess]
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # Merge the first half with the reversed second half
    first = head
    second = prev
    while first and second:
        temp1 = first.next
        first.next = second
        temp2 = second.next
        second.next = temp1
        first = temp1
        second = temp2

    # Handle the termination
    if to_end := first:
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
