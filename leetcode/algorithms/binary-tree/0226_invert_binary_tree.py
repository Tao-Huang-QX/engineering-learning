"""
LeetCode 226: Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/

Problem: Given the root of a binary tree, invert the tree, and return its root.

Approach: DFS post-order recursion
- Recursively invert left and right subtrees
- Swap the children at each node

Time: O(n)   Space: O(h) where h is tree height
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """
    Invert a binary tree by swapping left and right children at every node.

    Args:
        root: Root of the binary tree

    Returns:
        Root of the inverted tree
    """
    """
    Note there's an iteration approach available (in case call stack depth is a concern):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return root
    """
    if root:
        # Recursively invert left and right subtrees
        left_inverted = invert_tree(root.left)
        right_inverted = invert_tree(root.right)
        # Swap left and right children
        root.left, root.right = right_inverted, left_inverted
    return root


if __name__ == "__main__":
    # Helper function to build tree from list (BFS order, None for missing nodes)
    def build_tree(values: list[int | None]) -> TreeNode | None:
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])  # type: ignore[arg-type]
        from collections import deque

        q = deque[TreeNode | None]([root])
        i = 1
        while q and i < len(values):
            node = q.popleft()
            if node is None:
                i += 2
                continue
            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])  # type: ignore[arg-type]
                q.append(node.left)
            i += 1
            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])  # type: ignore[arg-type]
                q.append(node.right)
            i += 1
        return root

    # Helper function to convert tree to list (BFS order)
    def to_list(root: TreeNode | None) -> list[int | None]:
        if not root:
            return []
        from collections import deque

        result: list[int | None] = []
        q: deque[TreeNode | None] = deque([root])
        while q:
            node = q.popleft()
            if node:
                result.append(node.val)
                q.append(node.left)
                q.append(node.right)
            else:
                result.append(None)
        # Remove trailing Nones
        while result and result[-1] is None:
            result.pop()
        return result

    # Test cases from problem description
    # [4,2,7,1,3,6,9] -> [4,7,2,9,6,3,1]
    root1 = build_tree([4, 2, 7, 1, 3, 6, 9])
    result1 = invert_tree(root1)
    assert to_list(result1) == [4, 7, 2, 9, 6, 3, 1], f"got {to_list(result1)}"

    # [2,1,3] -> [2,3,1]
    root2 = build_tree([2, 1, 3])
    result2 = invert_tree(root2)
    assert to_list(result2) == [2, 3, 1], f"got {to_list(result2)}"

    # [] -> []
    result3 = invert_tree(None)
    assert result3 is None

    print("All tests passed.")
