"""
LeetCode 23: Merge k Sorted Lists
https://leetcode.com/problems/merge-k-sorted-lists/

Problem: You are given an array of k linked-lists lists, each linked-list is sorted
in ascending order. Merge all the linked-lists into one sorted linked-list and
return its head.

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order
- The sum of lists[i].length will not exceed 10^4

Examples:
- Input: lists = [[1,4,5],[1,3,4],[2,6]]
  Output: [1,1,2,3,4,4,5,6]
  Explanation: The linked-lists are:
    1->4->5, 1->3->4, 2->6
    merged: 1->1->2->3->4->4->5->6

- Input: lists = []
  Output: []

- Input: lists = [[]]
  Output: []

Approach: Divide & conquer with in-place merging (interval doubling)
- Base cases: 0 lists → None, 1 list → itself
- Reuse the merge_two_lists pattern (dummy head, compare-and-link, append the rest)
- Pair adjacent lists with a gap that doubles each round: interval = 1, 2, 4, ...
- For each pair (i, i+interval), merge and write back into lists[i] — in-place,
  no extra array allocation
- After each round, interval doubles and the number of surviving heads halves
  → log k rounds, each round touches all N nodes once

Time: O(N log k) — N total nodes, each node touched once per round for log k rounds
Space: O(1) — only the interval counter and merge pointers (no recursion stack,
  no heap allocation)
"""


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    """
    Merge k sorted linked lists into one sorted linked list.

    Args:
        lists: Array of heads of sorted linked lists

    Returns:
        Head of the merged sorted linked list
    """
    k = len(lists)
    if k < 2:
        return lists[0] if k == 1 else None

    def merge_two(list1: ListNode, list2: ListNode) -> ListNode:
        dummy = tail = ListNode()
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next  # pyright: ignore[reportAssignmentType]
            else:
                tail.next = list2
                list2 = list2.next  # pyright: ignore[reportAssignmentType]
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next

    interval = 1
    while interval < k:
        for i in range(0, k - interval, interval * 2):
            lists[i] = merge_two(lists[i], lists[i + interval])  # pyright: ignore[reportArgumentType]
        interval *= 2

    return lists[0]


def build_list(vals: list[int]) -> ListNode | None:
    """Build a linked list from a list of values."""
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    """Convert a linked list to a list of values."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    # Example 1
    lists1 = [
        build_list([1, 4, 5]),
        build_list([1, 3, 4]),
        build_list([2, 6]),
    ]
    result1 = merge_k_lists(lists1)
    expected1 = [1, 1, 2, 3, 4, 4, 5, 6]
    assert to_list(result1) == expected1, f"Example 1: got {to_list(result1)}, expected {expected1}"

    # Example 2
    result2 = merge_k_lists([])
    expected2 = []
    assert to_list(result2) == expected2, f"Example 2: got {to_list(result2)}, expected {expected2}"

    # Example 3
    result3 = merge_k_lists([None])
    expected3 = []
    assert to_list(result3) == expected3, f"Example 3: got {to_list(result3)}, expected {expected3}"

    print("All tests passed.")
