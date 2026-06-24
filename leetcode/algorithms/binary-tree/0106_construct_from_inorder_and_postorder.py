"""
LeetCode 106: Construct Binary Tree from Inorder and Postorder Traversal
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/

Problem: Given two integer arrays inorder and postorder where inorder is the inorder
traversal and postorder is the postorder traversal of a binary tree, construct and
return the binary tree.

Constraints:
- 1 <= inorder.length, postorder.length <= 3000
- inorder.length == postorder.length
- -3000 <= inorder[i], postorder[i] <= 3000
- inorder and postorder consist of unique values.
- All values in inorder and postorder are unique.

Approach: Iterative construction with hashmap and stack
- Build a value-to-index map for O(1) inorder lookup
- Root is postorder[-1] (last element in postorder)
- Use stack to process nodes with (inorder_range, postorder_range)
- For each node: find inorder index, calculate left subtree size
- In postorder, left subtree comes first, then right subtree
- Use left_size to index into postorder correctly

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


def build_tree(inorder: list[int], postorder: list[int]) -> TreeNode | None:
    """
    Construct a binary tree from its inorder and postorder traversal sequences.

    Args:
        inorder: Inorder traversal sequence (left -> root -> right).
        postorder: Postorder traversal sequence (left -> right -> root).

    Returns:
        Root of the constructed binary tree, or None if arrays are empty.
    """
    """
    if not postorder:
        return None
    root = TreeNode(postorder[-1])
    idx = inorder.index(postorder[-1])
    root.left = build_tree(inorder[:idx + 1], postorder[:idx])
    root.right = build_tree(inorder[idx + 1:], postorder[idx: - 1])
    return root
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}

    root = TreeNode(postorder[-1])
    # node, in_start, in_end, post_start, post_end
    stack = [(root, 0, len(inorder) - 1, 0, len(postorder) - 1)]

    while stack:
        node, in_start, in_end, post_start, post_end = stack.pop()

        in_idx = inorder_map[node.val]
        left_size = in_idx - in_start
        if left_size > 0:
            left_val = postorder[post_start + left_size - 1]
            node.left = TreeNode(left_val)
            stack.append((node.left, in_start, in_idx - 1, post_start, post_start + left_size - 1))

        right_size = in_end - in_idx
        if right_size > 0:
            right_val = postorder[post_end - 1]
            node.right = TreeNode(right_val)
            stack.append((node.right, in_idx + 1, in_end, post_start + left_size, post_end - 1))

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
    # inorder: [9,3,15,20,7], postorder: [9,15,7,20,3]
    #     3
    #    / \
    #   9  20
    #     /  \
    #    15   7
    assert to_list(build_tree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])) == [
        3,
        9,
        20,
        None,
        None,
        15,
        7,
    ]
    # inorder: [-1], postorder: [-1]
    #    -1
    assert to_list(build_tree([-1], [-1])) == [-1]

    print("All tests passed.")
