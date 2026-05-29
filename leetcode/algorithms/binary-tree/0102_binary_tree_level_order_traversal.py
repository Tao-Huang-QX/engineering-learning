"""
LeetCode 102: Binary Tree Level Order Traversal
https://leetcode.com/problems/binary-tree-level-order-traversal/

Problem: Return the level order traversal of a binary tree (level by level, left to right).

Approach:
- Use deque for O(1) popleft aperations
- level_size captures nodes at current level before processing
- Process exactly level_size nodes per iteration to maintain level boundaries

Time: O(n)   Space: O(w) where w = max tree width
"""

from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode | None) -> list[list[int]]:
    """
    Return level order traversal of a binary tree.

    Args:
        root: Root of the binary tree

    Returns:
        List of lists, where each inner list contains node values at that level
    """
    result = []
    queue = deque([root])  # Queue for BFS
    while queue:
        level_size = len(queue)  # Number of nodes at current level
        level_values = []
        for _ in range(level_size):
            node = queue.popleft()  # Get next node in the queue
            level_values.append(node.val)  # type: ignore

            # Add children to the queue for next level
            if node.left:  # type: ignore
                queue.append(node.left)  # type: ignore
            if node.right:  # type: ignore
                queue.append(node.right)  # type: ignore
        result.append(level_values)
    return result


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
    assert level_order(build_tree([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert level_order(build_tree([1])) == [[1]]
    assert level_order(build_tree([])) == []

    print("All tests passed.")
