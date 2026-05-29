"""
LeetCode 141: Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/

Problem: Given head of a linked list, determine if it has a cycle.

Approach:
- Slow pointer moves 1 step, fast pointer moves 2 steps
- If they meet, cycle exists; if fast reaches end, no cycle

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x: int):
        self.val = x
        self.next: ListNode | None = None


def has_cycle(head: ListNode | None) -> bool:
    """
    Determine if a linked list has a cycle.

    Args:
        head: Head of the linked list

    Returns:
        True if there is a cycle, False otherwise
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next  # pyright: ignore[reportOptionalMemberAccess]
        fast = fast.next.next  # pyright: ignore[reportOptionalMemberAccess]
        if slow == fast:
            return True
    return False


if __name__ == "__main__":
    # Helper to create a list with optional cycle
    def create_list_with_cycle(values: list[int], cycle_pos: int = -1) -> ListNode | None:
        if not values:
            return None
        nodes = [ListNode(v) for v in values]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if cycle_pos >= 0 and cycle_pos < len(nodes):
            nodes[-1].next = nodes[cycle_pos]
        return nodes[0]

    # Test cases
    assert has_cycle(create_list_with_cycle([3, 2, 0, -4], 1))
    assert has_cycle(create_list_with_cycle([1, 2], 0))
    assert not has_cycle(create_list_with_cycle([1], -1))

    print("All tests passed.")
