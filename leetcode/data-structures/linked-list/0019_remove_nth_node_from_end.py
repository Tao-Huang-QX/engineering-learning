"""
LeetCode 19: Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Problem: Given the head of a linked list, remove the n-th node from
the end of the list and return its head.

Follow-up: could you do this in one pass?

Constraints:
- The number of nodes in the list is sz
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

Examples:
- Input: head = [1,2,3,4,5], n = 2
  Output: [1,2,3,5]

- Input: head = [1], n = 1
  Output: []

- Input: head = [1,2], n = 1
  Output: [1]

Approach: Dummy head + fixed-gap two pointers, one pass
- leader advances n hops first (stays on-list: n <= sz), then both
  walk in lockstep until leader is the tail — follower parks on the
  (n+1)-th-from-end, the victim's predecessor
- dummy guarantees a predecessor exists even when the victim is the
  head; one wiring (follower.next = victim.next) covers tail and head
  deletion without special cases

Time: O(sz)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def remove_nth_from_end(head: ListNode, n: int) -> ListNode | None:
    """
    Remove the n-th node from the end of the list.

    Args:
        head: Head of the singly linked list
        n: 1-based position from the end of the node to remove
            (1 <= n <= list length)

    Returns:
        Head of the modified list
    """
    dummy = leader = follower = ListNode(0, head)
    for _ in range(n):
        leader = leader.next  # pyright: ignore[reportOptionalMemberAccess]

    # find the node to delete
    while leader.next:  # pyright: ignore[reportOptionalMemberAccess]
        follower = follower.next  # pyright: ignore[reportOptionalMemberAccess]
        leader = leader.next  # pyright: ignore[reportOptionalMemberAccess]

    # follower's next is the victim
    to_del = follower.next  # pyright: ignore[reportOptionalMemberAccess]
    follower.next = to_del.next  # pyright: ignore[reportOptionalMemberAccess]

    return dummy.next


if __name__ == "__main__":

    def build(values: list[int]) -> ListNode | None:
        """Build a linked list from a Python list."""
        head = None
        for val in reversed(values):
            head = ListNode(val, head)
        return head

    def to_list(head: ListNode | None) -> list[int]:
        """Convert a linked list back to a Python list."""
        out: list[int] = []
        while head:
            out.append(head.val)
            head = head.next
        return out

    def remove_nth_from_end_list(values: list[int], n: int) -> list[int]:
        node = build(values)
        assert node is not None  # contract: sz >= 1, tests never pass []
        return to_list(remove_nth_from_end(node, n))

    # Example 1: remove 4th-from-front (2nd-from-end)
    assert remove_nth_from_end_list([1, 2, 3, 4, 5], 2) == [1, 2, 3, 5], (
        f"Example 1: got {remove_nth_from_end_list([1, 2, 3, 4, 5], 2)}"
    )

    # Example 2: remove the only node
    assert remove_nth_from_end_list([1], 1) == [], (
        f"Example 2: got {remove_nth_from_end_list([1], 1)}"
    )

    # Example 3: remove the tail
    assert remove_nth_from_end_list([1, 2], 1) == [1], (
        f"Example 3: got {remove_nth_from_end_list([1, 2], 1)}"
    )

    # Edge: remove the head — return value changes
    assert remove_nth_from_end_list([1, 2, 3], 3) == [2, 3], (
        f"Head: got {remove_nth_from_end_list([1, 2, 3], 3)}"
    )

    print("All tests passed.")


# solved: 2026-11-27, medium, 30min, Remove Nth Node From End of List
