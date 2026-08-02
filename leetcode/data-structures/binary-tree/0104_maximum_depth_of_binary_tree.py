"""
LeetCode 104: Maximum Depth of Binary Tree
https://leetcode.com/problems/maximum-depth-of-binary-tree/

Problem: Find the maximum depth of a binary tree (number of nodes along longest path from root to leaf).

Approach:
- Track (node, depth) pairs with explicit stack
- Update max_depth at each visited node
- Only push valid children to stack

Time: O(n)   Space: O(h) where h is the height of the tree
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode | None) -> int:
    """
    Find the maximum depth of a binary tree.

    Args:
        root: Root of the binary tree

    Returns:
        Maximum depth (number of nodes along longest root-to-leaf path)
    """
    """
    Recursion approach:
    Time: O(n)   Space: O(h) call stack depth where h is the height of the tree
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
    """
    max_depth = 0
    stack: list[tuple[TreeNode, int]] = [(root, 1)] if root else []
    while stack:
        node, depth = stack.pop()
        if node:
            max_depth = max(max_depth, depth)
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
    return max_depth


if __name__ == "__main__":
    # Helper to build tree from list (level-order, None for missing nodes)
    def build_tree(values: list[int | None]) -> TreeNode | None:
        if not values or values[0] is None:
            return None
        nodes = [TreeNode(v) if v is not None else None for v in values]
        for i in range(len(nodes)):
            if nodes[i]:
                left_idx = 2 * i + 1
                right_idx = 2 * i + 2
                if left_idx < len(nodes):
                    nodes[i].left = nodes[left_idx]  # pyright: ignore[reportOptionalMemberAccess]
                if right_idx < len(nodes):
                    nodes[i].right = nodes[right_idx]  # pyright: ignore[reportOptionalMemberAccess]
        return nodes[0]

    # Test cases from problem description
    assert max_depth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
    assert max_depth(build_tree([1, None, 2])) == 2
    assert max_depth(build_tree([])) == 0
    assert max_depth(build_tree([1])) == 1

    print("All tests passed.")
