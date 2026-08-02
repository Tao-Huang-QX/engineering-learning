"""
LeetCode 105: Construct Binary Tree from Preorder and Inorder Traversal
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Problem: Given two integer arrays preorder and inorder where preorder is the preorder
traversal of a binary tree and inorder is the inorder traversal of the same tree,
construct and return the binary tree.

Constraints:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- All values in preorder and inorder are unique.

Approach: Iterative construction with hashmap and stack
- Build a value-to-index map for O(1) inorder lookup
- Use stack to process nodes, storing (node, preorder_range, inorder_range)
- For each node: find its inorder index, calculate left subtree size
- Create left/right children based on subtree sizes, push to stack
- Avoid repeated array slicing and index() calls

Time: O(n)   Space: O(n) for hashmap and stack
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    """
    Construct a binary tree from its preorder and inorder traversal sequences.

    Args:
        preorder: Preorder traversal sequence (root -> left -> right).
        inorder: Inorder traversal sequence (left -> root -> right).

    Returns:
        Root of the constructed binary tree, or None if arrays are empty.
    """
    """
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    idx = inorder.index(preorder[0])
    root.left = build_tree(preorder[1:idx + 1], inorder[:idx])
    root.right = build_tree(preorder[idx + 1:], inorder[idx + 1:])
    return root
    """
    # Build a value-to-index map for O(1) lookup in inorder
    inorder_map = {val: i for i, val in enumerate(inorder)}

    # Stack stores tuples of (node, preorder_start, preorder_end, inorder_start, inorder_end)
    # Start with root and full ranges
    root = TreeNode(preorder[0])
    stack = [(root, 0, len(preorder) - 1, 0, len(inorder) - 1)]

    while stack:
        node, pre_start, pre_end, in_start, in_end = stack.pop()

        # Find root position in inorder
        in_idx = inorder_map[node.val]
        left_size = in_idx - in_start  # Number of nodes in left subtree

        # Build left child if exists
        if left_size > 0:
            left_val = preorder[pre_start + 1]
            node.left = TreeNode(left_val)
            stack.append((node.left, pre_start + 1, pre_start + left_size, in_start, in_idx - 1))

        # Build right child if exists
        right_size = in_end - in_idx
        if right_size > 0:
            right_val = preorder[pre_start + left_size + 1]
            node.right = TreeNode(right_val)
            stack.append((node.right, pre_start + left_size + 1, pre_end, in_idx + 1, in_end))

    return root


if __name__ == "__main__":
    # Helper to convert tree back to list (level-order) for verification
    def to_list(root: TreeNode | None) -> list[int | None]:
        if not root:
            return []
        from collections import deque

        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)  # pyright: ignore[reportArgumentType]
                queue.append(node.right)  # pyright: ignore[reportArgumentType]
            else:
                result.append(None)
        # Remove trailing None values
        while result and result[-1] is None:
            result.pop()
        return result

    # Test cases from the problem description
    # preorder: [3,9,20,15,7], inorder: [9,3,15,20,7]
    #     3
    #    / \
    #   9  20
    #     /  \
    #    15   7
    assert to_list(build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [
        3,
        9,
        20,
        None,
        None,
        15,
        7,
    ]
    # preorder: [-1], inorder: [-1]
    #    -1
    assert to_list(build_tree([-1], [-1])) == [-1]

    print("All tests passed.")
