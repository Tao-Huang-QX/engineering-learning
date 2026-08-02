"""
LeetCode 94: Binary Tree Inorder Traversal
https://leetcode.com/problems/binary-tree-inorder-traversal/

Problem: Given the root of a binary tree, return the inorder traversal of its
nodes' values (left subtree -> root -> right subtree).

Constraints:
- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100.

Follow-up: Recursive solution is trivial — could you do it iteratively?

Approach (iterative):
- Walk left from the current node, pushing each node onto a stack
- When you can't go further left, pop a node and record its value
- Move to its right child, then repeat
- Loop while there's a current node or anything left on the stack

Time: O(n)   Space: O(h) for the explicit stack
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root: TreeNode | None) -> list[int]:
    """
    Return the inorder traversal (left -> root -> right) of a binary tree.

    Args:
        root: Root of the binary tree.

    Returns:
        List of node values in inorder order.
    """
    """
    result = []
    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result
    """
    result = []
    stack = []
    curr = root

    while stack or curr:
        # Walk left to the bottom, remembering each node along the way
        while curr:
            stack.append(curr)
            curr = curr.left
        # Can't go left anymore -> the top of the stack is "due"
        curr = stack.pop()
        result.append(curr.val)  # visit the node
        curr = curr.right  # then move to its right subtree

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

    # Test cases from the problem description
    assert inorder_traversal(build_tree([1, None, 2, None, None, 3])) == [1, 3, 2]
    assert inorder_traversal(build_tree([])) == []
    assert inorder_traversal(build_tree([1])) == [1]
    # Extra coverage: a small balanced tree
    #     2
    #    / \
    #   1   3   -> inorder: [1, 2, 3]
    assert inorder_traversal(build_tree([2, 1, 3])) == [1, 2, 3]

    print("All tests passed.")
