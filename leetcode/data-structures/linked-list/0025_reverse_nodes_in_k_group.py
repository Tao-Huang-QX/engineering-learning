"""
LeetCode 25: Reverse Nodes in k-Group
https://leetcode.com/problems/reverse-nodes-in-k-group/

Problem: Given the head of a linked list, reverse the nodes of the list k at
a time and return the modified list. k is a positive integer and is less than
or equal to the length of the linked list. If the number of nodes is not a
multiple of k, the last left-out nodes should remain as-is.

You may not alter the values in the nodes' values — only nodes themselves may
be changed.

Constraints:
- 1 <= number of nodes <= 5000
- 1 <= k <= n (length of the list)
- 0 <= Node.val <= 1000

Follow-up: Can you solve the problem in O(1) extra memory space?

Approach: Sentinel + look-ahead reverse
- Dummy node so the first group is rewired uniformly; return dummy.next
- Before each group, probe k nodes forward; stop if we fall off the end (leftover < k stays as-is)
- Reverse k nodes in place, reconnect: prev-group tail -> new head, old first -> next group

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    """
    Reverse the nodes of the list k at a time, leaving any leftover tail as-is.

    Args:
        head: Head of the singly linked list
        k: Group size to reverse

    Returns:
        Head of the modified linked list
    """
    dummy = tail = ListNode(next=head)
    while tail:
        # Probe: are there >= k nodes left?
        probe = tail
        for _ in range(k):
            probe = probe.next  # pyright: ignore[reportOptionalMemberAccess]
            if not probe:  # pyright: ignore[reportOptionalMemberAccess]
                return dummy.next

        prev, curr = tail, tail.next
        for _ in range(k):
            next_node = curr.next  # pyright: ignore[reportOptionalMemberAccess]
            curr.next = prev  # pyright: ignore[reportOptionalMemberAccess]
            prev = curr
            curr = next_node

        # Interchange the pointers to the first and last nodes of the sub list
        first_node = tail.next
        tail.next = prev  # Link to the last node of the sub list
        first_node.next = curr  # pyright: ignore[reportOptionalMemberAccess]
        tail = first_node  # Now the original first node became the last of the sub list

    return dummy.next


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

    def to_list(head: ListNode | None) -> list[int]:
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    # Test cases from the problem description
    test_cases = [
        # (input, k, expected)
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),  # two full groups, leftover 5
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),  # one full group, leftover 4,5
        ([1, 2, 3, 4, 5, 6, 7], 3, [3, 2, 1, 6, 5, 4, 7]),  # leftover 7
        ([1, 2], 2, [2, 1]),  # whole list is one group
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4, 5]),  # k=1 is a no-op
        ([1, 2, 3, 4, 5], 5, [5, 4, 3, 2, 1]),  # whole list reversed
        ([1], 1, [1]),  # single node
    ]

    for vals, k, expected in test_cases:
        head = create_list(vals)
        result = reverse_k_group(head, k)
        got = to_list(result)
        assert got == expected, f"k={k}, input={vals}: got {got}, expected {expected}"

    print("All tests passed.")
