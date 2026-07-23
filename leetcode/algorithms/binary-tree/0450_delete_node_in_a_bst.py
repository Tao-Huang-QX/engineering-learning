"""
LeetCode 450: Delete Node in a BST
https://leetcode.com/problems/delete-node-in-a-bst/

Problem: Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference of the BST.

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -10^5 <= Node.val <= 10^5
- Each node has a unique value.
- key is a value existing in the BST (when deleting, the key is guaranteed to exist).

Examples:
- Input: root = [5,3,6,2,4,null,7], key = 3
  Output: [5,4,6,2,null,null,7]
  Explanation: Node with value 3 is deleted. Its inorder successor (4) replaces it.

- Input: root = [5,3,6,2,4,null,7], key = 0
  Output: [5,3,6,2,4,null,7]
  Explanation: Key not found, tree unchanged.

- Input: root = [], key = 0
  Output: []

Approach: Iterative BST deletion with parent tracking
- Search for node while tracking parent and whether node is left/right child
- Case 1 & 2 (0 or 1 child): Replace node with its only child (or None)
- Case 3 (two children): Find inorder successor (minimum in right subtree), copy its value, then delete the successor (which has 0 or 1 child by definition)

Time: O(h) — h is tree height, O(log n) balanced, O(n) worst-case
Space: O(1) — only pointer variables, no recursion stack
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    """
    Delete the node with the given key from the BST and return the new root.

    Args:
        root: The root of the BST
        key: The value of the node to delete

    Returns:
        The root of the modified BST
    """
    """
    def dfs(node: TreeNode, key: int):
        if not node:
            return None
        # Search
        if key < node.val:
            node.left = dfs(node.left, key)  # pyright: ignore[reportArgumentType]
        elif key > node.val:
            node.right = dfs(node.right, key)  # pyright: ignore[reportArgumentType]
        else:
            # Node found
            # Leaf
            if not node.left and not node.right:
                return None
            # One child
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Two children: find inorder successor (smallest in right subtree)
            succ = node.right
            while succ.left:
                succ = succ.left
            node.val = succ.val  # Replace val
            node.right = dfs(node.right, succ.val)  # Delete successor
    dfs(root, key)  # pyright: ignore[reportArgumentType]
    return root
    """
    if not root:
        return None

    # Find node to delete and its parent
    curr = root
    parent = None
    is_left_child = False

    while curr and curr.val != key:
        parent = curr

        if key < curr.val:
            curr = curr.left
            is_left_child = True
        else:
            curr = curr.right
            is_left_child = False

    if not curr:
        return root

    # Case 1 & 2: Node has 0 or 1 child
    if not curr.left or not curr.right:
        child = curr.left or curr.right

        # Node is root
        if not parent:
            return child

        # Attach child to parent
        if is_left_child:
            parent.left = child
        else:
            parent.right = child
    # Case 3: Node has two children
    else:
        # Find inorder successor (min in right subtree) and its parent
        succ_parent = curr
        succ = curr.right

        while succ.left:
            succ_parent = succ
            succ = succ.left

        # Copy successor's val
        curr.val = succ.val

        # Delete successor (has 0 or 1 child - no left child by definition)
        if succ_parent == curr:
            succ_parent.right = succ.right
        else:
            succ_parent.left = succ.right

    return root


if __name__ == "__main__":
    # Example 1: root = [5,3,6,2,4,null,7], key = 3
    #       5
    #      / \
    #     3   6
    #    / \   \
    #   2   4   7
    root1 = TreeNode(5)
    root1.left = TreeNode(3)
    root1.right = TreeNode(6)
    root1.left.left = TreeNode(2)
    root1.left.right = TreeNode(4)
    root1.right.right = TreeNode(7)

    result1 = delete_node(root1, 3)
    # Expected: [5,4,6,2,null,null,7]
    #       5
    #      / \
    #     4   6
    #    /     \
    #   2       7

    # Example 2: key not found
    root2 = TreeNode(5)
    root2.left = TreeNode(3)
    root2.right = TreeNode(6)
    root2.left.left = TreeNode(2)
    root2.left.right = TreeNode(4)
    root2.right.right = TreeNode(7)
    result2 = delete_node(root2, 0)
    # Tree should be unchanged

    # Example 3: empty tree
    result3 = delete_node(None, 0)
    assert result3 is None

    print("All tests passed.")
