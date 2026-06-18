"""
LeetCode 234: Palindrome Linked List
https://leetcode.com/problems/palindrome-linked-list/

Problem: Given the head of a singly linked list, return True if it is a
palindrome, or False otherwise.

Constraints:
- The number of nodes in the list is in the range [1, 10^5].
- 0 <= Node.val <= 9

Follow-up: Could you do it in O(n) time and O(1) space?

Approach: Fast/slow pointer + reverse second half + compare
- Slow/fast pointers find the left-middle node: the loop guard
  `fast.next and fast.next.next` stops `slow` at the first node of the
  second half for even length, and at the true middle for odd length.
- Reverse the second half in place starting at slow.next.
- Walk l1 (head) and l2 (reversed second half) in lockstep; any value
  mismatch means not a palindrome. The left-middle choice makes l2 the
  shorter half, so it exhausts first and the loop compares exactly the
  needed pairs — the odd-length middle node is correctly skipped.

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def is_palindrome(head: ListNode | None) -> bool:
    """
    Check whether the linked list is a palindrome.

    Args:
        head: Head of the singly linked list

    Returns:
        True if the list reads the same forwards and backwards, else False
    """
    if not head or not head.next:
        return True

    slow = fast = head
    while fast.next and fast.next.next:
        fast = fast.next.next
        slow = slow.next  # pyright: ignore[reportOptionalMemberAccess]

    prev = None
    curr = slow.next  # pyright: ignore[reportOptionalMemberAccess]
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    l1, l2 = head, prev
    while l1 and l2:
        if l1.val != l2.val:
            return False
        l1 = l1.next
        l2 = l2.next
    return True


if __name__ == "__main__":

    def create_list(values: list[int]) -> ListNode | None:
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    # Test cases from the problem description
    test_cases = [
        # (input, expected)
        ([1, 2, 2, 1], True),  # even-length palindrome
        ([1, 2], False),  # not a palindrome
        ([1], True),  # single node
        ([1, 2, 1], True),  # odd-length palindrome
        ([1, 2, 3], False),
    ]

    for vals, expected in test_cases:
        head = create_list(vals)
        result = is_palindrome(head)
        assert result == expected, f"input={vals}: got {result}, expected {expected}"

    print("All tests passed.")
