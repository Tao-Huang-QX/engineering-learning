"""
LeetCode 543: Diameter of Binary Tree
https://leetcode.com/problems/diameter-of-binary-tree/

Problem: Given the root of a binary tree, return the length of the diameter
of the tree. The diameter of a binary tree is the length of the longest path
between any two nodes in a tree. This path may or may not pass through the
root. The length of a path between two nodes is represented by the number
of edges between them.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -100 <= Node.val <= 100

Examples:
- Input: root = [1,2,3,4,5]
  Output: 3
  Explanation: The longest path is [4,2,1,3] or [5,2,1,3] — 3 edges.

- Input: root = [1]
  Output: 0

Approach: Post-order DFS — gains carry edges, a global max records through-paths
- dfs returns the longest downward path IN EDGES from a node; each gain
  includes its connector (+1 iff the child exists), so through-path edges
  at a node = left_gain + right_gain exactly — the node itself contributes
  zero edges, so no extra +1 anywhere (a through-leaf path is 0 edges)
- Missing-children sides contribute gain 0 via the conditional — empty
  subtrees need no special case
- result is a nonlocal max updated at EVERY node: no node knows where the
  best path bends (deep-left-subtree / empty-right case: the answer 2h is
  recorded at the subtree root; the global root's h+1 tail-candidate loses)
- Same skeleton as 0124 Maximum Path Sum (values -> edges) and the
  node-depth formulation (leaf returns 1, result = left + right) is the
  equivalent B-form
- Scaffold lesson recorded: a buggy level-order build() wired node1.left
  to node1 — a self-cycle presenting as RecursionError in correct dfs code

Time: O(n)   Space: O(h) recursion depth
"""


class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def diameter_of_binary_tree(root: TreeNode) -> int:
    """
    Return the diameter of the binary tree (longest path in edges).

    Args:
        root: Root of the binary tree (at least one node)

    Returns:
        Number of edges on the longest path between any two nodes
    """
    result = 0

    def dfs(node: TreeNode) -> int:
        nonlocal result
        if not node.left and not node.right:
            return 0

        left_gain = dfs(node.left) + 1 if node.left else 0
        right_gain = dfs(node.right) + 1 if node.right else 0

        result = max(result, left_gain + right_gain)
        return max(left_gain, right_gain)

    dfs(root)
    return result


if __name__ == "__main__":

    def build(vals: list[int | None]) -> TreeNode:
        """Build a tree from level-order values with None holes."""
        nodes = [TreeNode(v) if v is not None else None for v in vals]
        for i, node in enumerate(nodes):
            if node:
                if 2 * i + 1 < len(nodes):
                    node.left = nodes[2 * i + 1]  # pyright: ignore[reportOptionalMemberAccess]
                if 2 * i + 2 < len(nodes):
                    node.right = nodes[2 * i + 2]  # pyright: ignore[reportOptionalMemberAccess]
        return nodes[0]  # pyright: ignore[reportReturnType]

    # Example 1: complete small tree, diameter through the root
    result1 = diameter_of_binary_tree(build([1, 2, 3, 4, 5]))
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: single node — zero edges
    result2 = diameter_of_binary_tree(build([1]))
    expected2 = 0
    assert result2 == expected2, f"Single: got {result2}, expected {expected2}"

    # Edge: left-skewed chain of 4 — diameter 3, depth also 3
    tree3 = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
    result3 = diameter_of_binary_tree(tree3)
    expected3 = 3
    assert result3 == expected3, f"Left chain: got {result3}, expected {expected3}"

    # Edge: right-skewed chain
    tree4 = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
    result4 = diameter_of_binary_tree(tree4)
    expected4 = 3
    assert result4 == expected4, f"Right chain: got {result4}, expected {expected4}"

    # Edge: diameter NOT through the root — best path lives in the left subtree
    #        1
    #       /
    #      2
    #     / \
    #    3   4
    #   /     \
    #  5       6
    tree5 = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(5)), TreeNode(4, None, TreeNode(6))))
    result5 = diameter_of_binary_tree(tree5)
    expected5 = 4  # 5-3-2-4-6
    assert result5 == expected5, f"Off-root: got {result5}, expected {expected5}"

    print("All tests passed.")


# solved: 2026-11-09, easy, 30min, Diameter of Binary Tree
