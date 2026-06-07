"""
LeetCode 82: Remove Duplicates from Sorted List II
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/

Problem: Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

Approach: Dummy node + two-pointer with look-ahead
- Use dummy node to handle head deletion
- Look ahead to check if current value is duplicated
- If duplicated: skip ALL nodes with that value
- If unique: link it to result and advance prev

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def delete_duplicates(head: ListNode | None) -> ListNode | None:
    """
    Delete all nodes that have duplicate numbers from a sorted linked list.

    Args:
        head: Head of the sorted linked list

    Returns:
        Head of the linked list with only distinct numbers
    """
    if not head:
        return None

    dummy = ListNode(0, head)
    prev = dummy
    while head:
        # Check if current node has duplicates (look ahead)
        is_duplicate = False
        current = head
        # look ahead to see if current value is duplicated
        while current.next and current.next.val == head.val:
            is_duplicate = True
            current = current.next

        if is_duplicate:
            # Skip all nodes with head.val
            head = current.next
        else:
            # current is unique - link it
            prev.next = head
            prev = head
            head = head.next

    prev.next = None  # Terminate the list
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
        ([1, 2, 3, 3, 4, 4, 5], [1, 2, 5]),
        ([1, 1, 1, 2, 3], [2, 3]),
        ([], []),
        ([1, 1, 1], []),
    ]

    for vals, expected in test_cases:
        val_list = create_list(vals)
        result = delete_duplicates(val_list)
        assert to_list(result) == expected, f"got {to_list(result)}, expected {expected}"

    print("All tests passed.")
