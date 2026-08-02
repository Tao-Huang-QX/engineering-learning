"""
LeetCode 86: Partition List
https://leetcode.com/problems/partition-list/

Problem: Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x. You should preserve the original relative order of the nodes in each of the two partitions.

Approach: Read-write pointers with in-place reordering
- Use write pointer (w) to mark where next < x node should go
- Use read pointer (r) to scan ahead for nodes < x
- When r finds < x node: unlink from current position, insert after w
- Save references before overwriting (temp.next = w.next before w.next = temp)

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def partition(head: ListNode | None, x: int) -> ListNode | None:
    """
    Partition the linked list around value x.

    Args:
        head: Head of the linked list
        x: Partition value

    Returns:
        Head of the partitioned linked list
    """
    if not head:
        return None

    dummy = ListNode(0, head)
    # write pointer - where to place next < x
    w = dummy

    while w.next and w.next.val < x:
        w = w.next

    # read pointer starts from write position
    r = w
    while r.next:
        if r.next.val < x:
            # Found a node < x that needs to move to w position
            temp = r.next
            # Unlink it from current position, r.next skips temp -> points to the node after temp
            r.next = temp.next
            # insert after w, temp now points to what w was pointing to
            temp.next = w.next
            w.next = temp  # link it
            w = w.next  # advance w
        else:
            r = r.next

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
        # (head values, x, expected result)
        ([1, 4, 3, 2, 5, 2], 3, [1, 2, 2, 4, 3, 5]),
        ([2, 1], 2, [1, 2]),
        ([], 1, []),
        ([1], 0, [1]),
        ([1], 2, [1]),
    ]

    for vals, x, expected in test_cases:
        val_list = create_list(vals)
        result = partition(val_list, x)
        assert to_list(result) == expected, f"x={x}: got {to_list(result)}, expected {expected}"

    print("All tests passed.")
