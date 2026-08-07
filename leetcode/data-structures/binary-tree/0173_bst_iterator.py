"""
LeetCode 173: Binary Search Tree Iterator
https://leetcode.com/problems/binary-search-tree-iterator/

Problem: Implement the BSTIterator class that represents an iterator over the
in-order traversal of a binary search tree (BST):

- BSTIterator(TreeNode root): Initializes the iterator. The pointer should be
  positioned before the first element (i.e., the smallest number).
- int next(): Moves the pointer to the right, then returns the number at the pointer.
- boolean has_next(): Returns true if there exists a number to the right of the
  pointer, false otherwise.

You may assume that next() calls will always be valid (called only when has_next()
is true).

Constraints:
- The number of nodes in the tree is in the range [1, 10^5].
- 0 <= Node.val <= 10^6
- At most 10^5 calls will be made to has_next() and next().

Follow-up: Can you implement next() and has_next() to run in average O(1) time and
use O(h) memory, where h is the height of the tree?

Examples:
- Input:
    ["BSTIterator", "next", "next", "has_next", "next", "has_next", "next",
     "has_next", "next", "has_next"]
    [[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
  Output:
    [null, 3, 7, true, 9, true, 15, true, 20, false]
  Explanation:
    BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
    bSTIterator.next();      // return 3
    bSTIterator.next();      // return 7
    bSTIterator.has_next();  // return True
    bSTIterator.next();      // return 9
    bSTIterator.has_next();  // return True
    bSTIterator.next();      // return 15
    bSTIterator.has_next();  // return True
    bSTIterator.next();      // return 20
    bSTIterator.has_next();  // return False

Approach: Controlled inorder traversal (stack)
- __init__: push root and all left descendants onto a stack (top = smallest)
- next(): pop top, then push the popped node's right child + all its left descendants
- has_next(): stack is non-empty — each node is pushed/popped exactly once

Time: O(1) amortized   Space: O(h)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    """Iterator for in-order traversal of a BST."""

    def __init__(self, root: TreeNode):
        """
        Initialize the iterator positioned before the first element.

        Args:
            root: Root of the BST
        """
        self.stack: list[TreeNode] = []
        cur = root

        while cur:
            self.stack.append(cur)
            cur = cur.left

    def next(self) -> int:
        """
        Move the pointer right and return the current number.

        Returns:
            The next number in the in-order traversal
        """
        next_node = self.stack.pop()
        cur = next_node.right

        while cur:
            self.stack.append(cur)
            cur = cur.left
        return next_node.val

    def has_next(self) -> bool:
        """
        Return True if there are more nodes to traverse.

        Returns:
            True if the iterator has a next element
        """
        return bool(self.stack)


def _list_to_tree(values: list[int | None]) -> TreeNode | None:
    """Helper to build a tree from level-order list representation."""
    if not values:
        return None
    root = TreeNode(values[0])  # pyright: ignore[reportArgumentType]
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])  # pyright: ignore[reportArgumentType]
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])  # pyright: ignore[reportArgumentType]
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    # Example from problem description
    root = _list_to_tree([7, 3, 15, None, None, 9, 20])
    iterator = BSTIterator(root)  # pyright: ignore[reportArgumentType]

    assert iterator.next() == 3, "first next() should return 3"
    assert iterator.next() == 7, "second next() should return 7"
    assert iterator.has_next() is True, "has_next() should be True after 7"
    assert iterator.next() == 9, "third next() should return 9"
    assert iterator.has_next() is True, "has_next() should be True after 9"
    assert iterator.next() == 15, "fourth next() should return 15"
    assert iterator.has_next() is True, "has_next() should be True after 15"
    assert iterator.next() == 20, "fifth next() should return 20"
    assert iterator.has_next() is False, "has_next() should be False after 20"

    print("All tests passed.")
