"""
LeetCode 124: Binary Tree Maximum Path Sum
https://leetcode.com/problems/binary-tree-maximum-path-sum/

Problem: A path in a binary tree is a sequence of nodes where each pair of adjacent
nodes in the sequence has an edge connecting them. A node can only appear in the
sequence at most once. The path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.

Constraints:
- The number of nodes in the tree is in the range [1, 3 * 10^4].
- -1000 <= Node.val <= 1000

Examples:
- Input: root = [1,2,3]
  Output: 6
  Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

- Input: root = [-10,9,20,null,null,15,7]
  Output: 42
  Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

Approach: Post-order DFS with global max
- DFS returns max single-branch gain (no split) — used by parent to extend its path
- At each node, compute Λ-shaped path (left + node + right) and update global max
- max(gain, 0) prunes negative children from being passed up

Time: O(n)   Space: O(h)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(root: TreeNode | None) -> int:
    """
    Return the maximum path sum of any non-empty path in the binary tree.

    Args:
        root: Root of the binary tree

    Returns:
        Maximum path sum
    """
    max_sum = float("-inf")

    def dfs(node: TreeNode | None) -> int:
        """Return max single-branch from this node (no splits)."""
        nonlocal max_sum
        if not node:
            return 0

        # Max contribution from each child (ignore negatives)
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)

        # Full path using this node as the apex (Λ shape)
        full_path = node.val + left_gain + right_gain
        max_sum = max(max_sum, full_path)

        # Pass up: can only take one branch to stay a single path
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum  # pyright: ignore[reportReturnType]


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
    root1 = _list_to_tree([1, 2, 3])
    result1 = max_path_sum(root1)
    expected1 = 6
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    root2 = _list_to_tree([-10, 9, 20, None, None, 15, 7])
    result2 = max_path_sum(root2)
    expected2 = 42
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
