"""
LeetCode 148: Sort List
https://leetcode.com/problems/sort-list/

Problem: Given the head of a linked list, return the list after sorting it in ascending order.

Approach: Bottom-up iterative merge sort
- Iteratively merge adjacent sublists of size 1, 2, 4, 8, ... until size ≥ length.
- Each pass: use `split(head, size)` to carve out left and right segments,
  merge them, and stitch the result back via `prev.next = merged`.
- Advance `prev` to the tail of the merged segment so the next pair links correctly.
- After log n passes, the list is fully sorted.
- Uses O(1) space — the `dummy` sentinel + `prev` pointer replace the recursion stack.

Time: O(n log n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def sort_list(head: ListNode | None) -> ListNode | None:
    """
    Sort the linked list in ascending order.

    Args:
        head: Head of the singly linked list

    Returns:
        Head of the sorted linked list
    """
    if not head or not head.next:
        return head

    # Count the length
    length = 0
    curr = head
    while curr:
        length += 1
        curr = curr.next

    dummy = ListNode(next=head)

    # Bottom-up: merge sublists of size 1, 2, 4, 8, ...
    size = 1
    while size < length:
        prev = dummy
        curr = dummy.next

        while curr:
            # Split off the first sublist of `size` nodes
            left = curr
            right = split(left, size)
            # Split off the second sublist of `size` nodes
            curr = split(right, size)

            # Merge the two sorted sublists and splice into result
            merged = merge(left, right)
            prev.next = merged

            # Advance prev to the end of the merged segment
            while prev.next:
                prev = prev.next

        size *= 2

    return dummy.next


def split(head: ListNode | None, size: int) -> ListNode | None:
    """
    Break off the first `size` nodes from head. Return the rest.
    """
    if not head:
        return None
    for _ in range(size - 1):
        if not head.next:
            break
        head = head.next
    rest = head.next
    head.next = None
    return rest


def merge(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """
    Merge two sorted linked lists.
    """
    tail = dummy = ListNode()
    while l1 and l2:
        if l1.val < l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


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
        ([4, 2, 1, 3], [1, 2, 3, 4]),
        ([-1, 5, 3, 4, 0], [-1, 0, 3, 4, 5]),
        ([], []),
    ]

    for vals, expected in test_cases:
        val_list = create_list(vals)
        result = sort_list(val_list)
        assert to_list(result) == expected, f"got {to_list(result)}, expected {expected}"

    print("All tests passed.")
