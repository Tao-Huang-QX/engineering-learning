# Primary technique: linked-list deep copy (QUEUE.md pattern "Hash map clone").
# Placed in linked-list/ with the roadmap cluster (#13-15, #43-49); the hash-map
# approach is one valid solution, the O(1)-space interleaving is the follow-up.

"""
LeetCode 138: Copy List with Random Pointer
https://leetcode.com/problems/copy-list-with-random-pointer/

Problem: Given the head of a linked list where each node carries an extra `random`
pointer that may point to any node in the list or None, return a deep copy of the
entire list (all new Node objects, identical val/next/random structure).

Constraints:
- 0 <= number of nodes <= 1000
- -1000 <= Node.val <= 1000
- Node.random is None or points to a node within the list.

Follow-up: Can you do it in O(n) time and O(1) space?

Approach: Interleave clones between originals (O(1) space)
- Phase 1: splice each clone right after its original (A -> A' -> B -> B' ...)
- Phase 2: set clone.random = original.random.next (the clone of the random target)
- Phase 3: detach the clones into a new list, restoring the original next links

Time: O(n)   Space: O(1)
"""


# Definition for a Node.
class Node:
    def __init__(
        self,
        x: int,
        next: "Node | None" = None,
        random: "Node | None" = None,
    ) -> None:
        self.val = x
        self.next = next
        self.random = random


def copy_random_list(head: "Node | None") -> "Node | None":
    """
    Return a deep copy of a linked list whose nodes carry a `random` pointer.

    Args:
        head: Head of the original list (each node has val, next, random).

    Returns:
        Head of a new list mirroring the structure (val, next, random) of the
        original but built from entirely new Node objects.
    """
    if not head:
        return None

    # Phase 1 - interleave: A -> A' -> B -> B' -> ...
    curr = head
    while curr:
        next_node = curr.next
        curr.next = Node(curr.val, next_node, None)  # clone spliced after curr
        curr = next_node

    # Phase 2 - wire random: each clone sits right after its original,
    # so A'.random == A.random.next (the clone of A's random target).
    curr = head
    while curr:
        if curr.next and curr.random and curr.random.next:
            curr.next.random = curr.random.next
        curr = curr.next.next  # type: ignore # skip the clone

    # Phase 3 - detach: split the interleaved list back into two.
    dummy = Node(0)
    tail = dummy
    curr = head
    while curr:
        clone = curr.next
        tail.next = clone  # type: ignore
        curr.next = clone.next  # type: ignore
        tail = clone
        curr = curr.next

    return dummy.next


if __name__ == "__main__":

    def build_random_list(
        pairs: list[tuple[int, int | None]],
    ) -> Node | None:
        """Build a list from [(val, random_index), ...]; random_index is 0-based or None."""
        if not pairs:
            return None
        nodes = [Node(val) for val, _ in pairs]
        for i, (_, random_index) in enumerate(pairs):
            if i + 1 < len(nodes):
                nodes[i].next = nodes[i + 1]
            if random_index is not None:
                nodes[i].random = nodes[random_index]
        return nodes[0]

    def serialize(head: Node | None) -> list[tuple[int, int | None]]:
        """Convert a list back to [(val, random_index), ...] via index lookup."""
        if head is None:
            return []
        nodes: list[Node] = []
        current = head
        while current:
            nodes.append(current)
            current = current.next
        index = {node: i for i, node in enumerate(nodes)}
        return [(n.val, index[n.random] if n.random is not None else None) for n in nodes]

    def assert_deep_copy(original: Node | None, copy: Node | None) -> None:
        """Verify copy mirrors original but shares no Node objects with it."""
        while original and copy:
            assert original is not copy, "copied node shares identity with original"
            assert original.val == copy.val, f"val mismatch: {original.val} vs {copy.val}"
            original = original.next
            copy = copy.next
        assert original is None and copy is None, "lists differ in length"

    # Test cases from the problem description: [(val, random_index), ...]
    test_cases = [
        (
            [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],  # official example 1
            [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)],
        ),
        (
            [(1, 1), (2, 1)],  # official example 2
            [(1, 1), (2, 1)],
        ),
        (
            [(3, None), (3, 0), (3, None)],  # official example 3
            [(3, None), (3, 0), (3, None)],
        ),
        ([], []),  # empty list
    ]

    for original_pairs, expected_pairs in test_cases:
        head = build_random_list(original_pairs)
        copy = copy_random_list(head)
        actual_pairs = serialize(copy)
        assert actual_pairs == expected_pairs, (
            f"input={original_pairs}: got {actual_pairs}, expected {expected_pairs}"
        )
        assert_deep_copy(head, copy)

    print("All tests passed.")
