"""
LeetCode 235: Lowest Common Ancestor of a Binary Search Tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Problem: Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.

Constraints:
- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the BST.

Examples:
- Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
  Output: 6
  Explanation: The LCA of nodes 2 and 8 is 6.

- Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
  Output: 2
  Explanation: The LCA of nodes 2 and 4 is 2, since node 2 is an ancestor of node 4.

Approach: BST property - traverse toward split point
- If both p, q < current: go left (both in left subtree)
- If both p, q > current: go right (both in right subtree)
- Otherwise: current is LCA (split point, or p/q is ancestor)
- No need to search both sides - BST guarantees unique path

Time: O(h) — h is tree height, O(log n) balanced, O(n) worst-case
Space: O(1) — only pointer traversal
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Find the lowest common ancestor of two nodes in a BST.

    Args:
        root: The root of the BST
        p: First node (guaranteed to exist in tree)
        q: Second node (guaranteed to exist in tree)

    Returns:
        The LCA node
    """
    curr = root

    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr


if __name__ == "__main__":
    # Example 1: p=2, q=8, LCA=6
    #       6
    #      / \
    #     2   8
    #    / \ / \
    #   0  4 7  9
    #     / \
    #    3   5
    root1 = TreeNode(6)
    root1.left = TreeNode(2)
    root1.right = TreeNode(8)
    root1.left.left = TreeNode(0)
    root1.left.right = TreeNode(4)
    root1.right.left = TreeNode(7)
    root1.right.right = TreeNode(9)
    root1.left.right.left = TreeNode(3)
    root1.left.right.right = TreeNode(5)

    p1 = root1.left  # node 2
    q1 = root1.right  # node 8
    result1 = lowest_common_ancestor(root1, p1, q1)
    assert result1.val == 6

    # Example 2: p=2, q=4, LCA=2 (p is ancestor of q)
    p2 = root1.left  # node 2
    q2 = root1.left.right  # node 4
    result2 = lowest_common_ancestor(root1, p2, q2)
    assert result2.val == 2

    print("All tests passed.")
