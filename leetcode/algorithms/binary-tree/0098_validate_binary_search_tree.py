"""
LeetCode 98: Validate Binary Search Tree
https://leetcode.com/problems/validate-binary-search-tree/

Problem: Given the root of a binary tree, determine if it is a valid binary search
tree (BST). A BST is defined as: all nodes in the left subtree have values less
than the node's value, and all nodes in the right subtree have values greater than
the node's value. Both subtrees must also be BSTs.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1.

Approach: Iterative inorder traversal
- Inorder traversal of a BST produces sorted ascending order
- Walk left to the bottom, pushing nodes onto a stack
- Pop and visit each node, checking value > previous value
- Move to right subtree and repeat
- If any value <= previous, tree is invalid

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


def is_valid_bst(root: TreeNode) -> bool:
    """
    Determine whether a binary tree is a valid binary search tree.

    Args:
        root: Root of the binary tree.

    Returns:
        True if the tree is a valid BST, False otherwise.
    """
    """
    def dfs(node: TreeNode, min_val: int, max_val: int) -> bool:
        if not node:
            return True
        if not (min_val < node.val < max_val):
            return False
        return dfs(node.left, min_val, node.val) and dfs(node.right, node.val, max_val)
    return dfs(root, float('-inf'), float('inf'))
    """
    stack = []
    curr = root
    pre_val = None

    while stack or curr:
        # Walk left to the bottom, pushing each node
        while curr:
            stack.append(curr)
            curr = curr.left

        # Can't go left - visit the node
        curr = stack.pop()

        # Check: current value must be > previous value
        if pre_val and curr.val <= pre_val:
            return False
        pre_val = curr.val

        # Move to the right subtree
        curr = curr.right

    return True


if __name__ == "__main__":
    # Helper to build tree from list (level-order, None for missing nodes)
    def build_tree(values: list[int]) -> TreeNode:
        nodes = [TreeNode(v) if v is not None else None for v in values]
        for i in range(len(nodes)):
            if nodes[i]:
                left_idx = 2 * i + 1
                right_idx = 2 * i + 2
                if left_idx < len(nodes):
                    nodes[i].left = nodes[left_idx]  # pyright: ignore[reportOptionalMemberAccess]
                if right_idx < len(nodes):
                    nodes[i].right = nodes[right_idx]  # pyright: ignore[reportOptionalMemberAccess]
        return nodes[0]  # type: ignore

    # Test cases from the problem description
    #     2
    #    / \
    #   1   3  -> valid BST
    assert is_valid_bst(build_tree([2, 1, 3]))
    #     5
    #    / \
    #   1   4
    #      / \
    #     3   6  -> NOT valid BST (3 should be in right subtree of 5, but 4 < 5 violates BST)
    assert not is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6]))  # type: ignore
    # Single node is valid
    assert is_valid_bst(build_tree([1]))
    # Edge case: duplicate values violate BST
    #     2
    #    / \
    #   2   2  -> NOT valid BST (left must be strictly less, right must be strictly greater)
    assert not is_valid_bst(build_tree([2, 2, 2]))
    # Edge case: large tree, boundary values
    assert not is_valid_bst(
        build_tree([10, 5, 15, None, None, 6, 20])  # type: ignore
    )  # 6 in right subtree but < 10

    print("All tests passed.")
