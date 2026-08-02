"""
LeetCode 61: Rotate List
https://leetcode.com/problems/rotate-list/

Problem: Given the head of a singly linked list, rotate the list to the right
by k places (each move shifts the last node to the front).

Constraints:
- The number of nodes in the list is in the range [0, 500].
- -100 <= Node.val <= 100
- 0 <= k <= 2 * 10^9

Approach: Close the ring, then cut
- Single pass measures length n and grabs the tail; normalize k via modulo, no-op if k == 0
- Walk n - k - 1 steps to the new tail, cut there, splice the old tail onto the old head

Time: O(n)   Space: O(1)
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def rotate_right(head: ListNode | None, k: int) -> ListNode | None:
    """
    Rotate the list to the right by k places (last node moves to front each time).

    Args:
        head: Head of the singly linked list
        k: Number of positions to rotate right (may exceed list length)

    Returns:
        Head of the rotated linked list
    """
    if not head or not head.next:
        return head

    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k %= length  # Deal with k larger than length
    if k == 0:  # k happens to be multiple of length
        return head

    # Walk to the new tail (length - k - 1)
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next  # pyright: ignore[reportOptionalMemberAccess]

    new_head = new_tail.next  # pyright: ignore[reportOptionalMemberAccess]
    # Cut
    new_tail.next = None  # pyright: ignore[reportOptionalMemberAccess]
    tail.next = head

    return new_head


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
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),  # official example 1
        ([0, 1, 2], 4, [2, 0, 1]),  # official example 2, k > n
        ([], 0, []),  # empty list
        ([1], 0, [1]),  # single node
        ([1, 2, 3], 4, [3, 1, 2]),  # k > n wraps (4 % 3 == 1)
        ([1, 2, 3], 3, [1, 2, 3]),  # k == n, no-op
    ]

    for vals, k, expected in test_cases:
        head = create_list(vals)
        result = rotate_right(head, k)
        got = to_list(result)
        assert got == expected, f"k={k}, input={vals}: got {got}, expected {expected}"

    print("All tests passed.")
