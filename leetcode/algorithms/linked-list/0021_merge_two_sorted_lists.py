"""
LeetCode 21: Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/

Problem: You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Approach:
- Use dummy head node to handle edge cases easily
- Compare and link smaller node, advance that pointer
- After loop, link remaining nodes from non-empty list
- Return dummy.next as the head of merged list

Time: O(m + n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    """
    Merge two sorted linked lists into one sorted list.

    Args:
        list1: Head of first sorted linked list
        list2: Head of second sorted linked list

    Returns:
        Head of the merged sorted linked list
    """
    head = current = ListNode()  # Dummy node to simplify edge cases
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    # Append any remaining nodes from either list
    current.next = list1 or list2
    return head.next  # Skip the dummy node


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
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([-5, -2, 3], [-10, -5, 0, 7], [-10, -5, -5, -2, 0, 3, 7]),
    ]

    for vals1, vals2, expected in test_cases:
        l1 = create_list(vals1)
        l2 = create_list(vals2)
        result = merge_two_lists(l1, l2)
        assert to_list(result) == expected, f"got {to_list(result)}, expected {expected}"

    print("All tests passed.")
