"""
LeetCode 206: Reverse Linked List
https://leetcode.com/problems/reverse-linked-list/

Problem: Given the head of a singly linked list, reverse the list, and return the reversed list.

Approach:
- Maintain three pointers: prev, current and next_node
- Save next node before breaking the link
- Reverse the link by pointing current.next to prev
- Move prev and current one step forward
- Return prev as the new head (originally the tail)

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def reverse_list(head: ListNode | None) -> ListNode | None:
    """
    Reverse a singly linked list in-place.

    Args:
        head: Head of the linked list

    Returns:
        New head of the reversed list
    """
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev


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
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([1, 2], [2, 1]),
        ([], []),
    ]

    for input_vals, expected in test_cases:
        head = create_list(input_vals)
        result = reverse_list(head)
        assert to_list(result) == expected, f"got {to_list(result)}, expected {expected}"

    print("All tests passed.")
