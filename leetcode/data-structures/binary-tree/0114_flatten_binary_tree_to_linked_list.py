"""
LeetCode 114: Flatten Binary Tree to Linked List
https://leetcode.com/problems/flatten-binary-tree-to-linked-list/

Problem: Given the root of a binary tree, flatten the tree into a "linked list":
- The "linked list" should use the same TreeNode class where the right child
  pointer points to the next node in the list and the left child pointer is
  always null.
- The "linked list" should be in the same order as a pre-order traversal of
  the binary tree.

Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -100 <= Node.val <= 100

Examples:
- Input: root = [1,2,5,3,4,null,6]
  Output: [1,null,2,null,3,null,4,null,5,null,6]

- Input: root = []
  Output: []

- Input: root = [0]
  Output: [0]

Approach: Stack-based pre-order simulation
- Push right child first, then left child — left pops first (stack LIFO)
- Wire current node's right to stack top (next pre-order node), then set left to None

Time: O(n)   Space: O(h)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def flatten(root: TreeNode | None) -> None:
    """
    Flatten a binary tree to a linked list in-place using pre-order traversal.

    Args:
        root: Root of the binary tree

    Returns:
        None (modifies the tree in-place)
    """
    if not root:
        return

    stack: list[TreeNode] = [root]

    while stack:
        node = stack.pop()

        # Push right first so left is processed next (stack is LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

        # Wire current node to the next pre-order node (top of stack)
        if stack:
            node.right = stack[-1]
        node.left = None


def _tree_to_list(root: TreeNode | None) -> list[int | None]:
    """Helper to convert flattened tree to list for testing (right pointers only)."""
    result: list[int | None] = []
    node = root
    while node:
        result.append(node.val)
        node = node.right
        if node:
            result.append(None)  # left is always null
    return result


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
    # Example 1
    root1 = _list_to_tree([1, 2, 5, 3, 4, None, 6])
    flatten(root1)
    result1 = _tree_to_list(root1)
    expected1 = [1, None, 2, None, 3, None, 4, None, 5, None, 6]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    root2 = _list_to_tree([])
    flatten(root2)
    assert root2 is None, "Example 2: expected None"

    # Example 3
    root3 = _list_to_tree([0])
    flatten(root3)
    result3 = _tree_to_list(root3)
    expected3 = [0]
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
