"""
LeetCode 572: Subtree of Another Tree
https://leetcode.com/problems/subtree-of-another-tree/

Problem: Given the roots of two binary trees root and sub_root, return true if there is
a subtree of root with the same structure and node values as sub_root, otherwise return false.
A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's
descendants. The tree tree could also be considered as a subtree of itself.

Constraints:
- The number of nodes in both trees is in the range [0, 100].
- -10^4 <= root.val <= 10^4
- sub_root is not guaranteed to be a subtree of root.

Approach: Iterative DFS with in-order comparison
Approach: Iterative DFS with in-order comparison
- Degenerate cases resolve at the boundary: an empty sub_root is a subtree
  of anything (True); an empty root cannot contain a non-empty sub_root
  (False) — everything below runs in a None-free world
- Walk root in order with a stack (exactly one cur = cur.right advance
  per pop); at each node, compare its subtree against sub_root
- is_sametree: two synchronized stacks traverse both trees in order;
  equal stack lengths each round pin down the shape, and popped values
  must match — an upfront root-value check rejects wrong-root candidates
  in O(1) before any stack work

Time: O(n × m)   Space: O(h + m)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    """
    Check if sub_root is a subtree of root (same structure and values).

    Args:
        root: Root of the main binary tree.
        sub_root: Root of the potential subtree.

    Returns:
        True if sub_root is a subtree of root, False otherwise.
    """
    if not sub_root:
        return True
    if not root:
        return False

    def is_sametree(left: TreeNode, right: TreeNode) -> bool:
        if left.val != right.val:
            return False

        stack_l: list[TreeNode] = []
        stack_r: list[TreeNode] = []
        cur_l = left
        cur_r = right

        while stack_l or cur_l or stack_r or cur_r:
            while cur_l:
                stack_l.append(cur_l)
                cur_l = cur_l.left
            while cur_r:
                stack_r.append(cur_r)
                cur_r = cur_r.left

            if len(stack_l) != len(stack_r):
                return False

            cur_l = stack_l.pop()
            cur_r = stack_r.pop()
            if cur_l.val != cur_r.val:
                return False

            cur_l = cur_l.right
            cur_r = cur_r.right

        return True

    stack: list[TreeNode] = []
    cur = root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left

        cur = stack.pop()
        if is_sametree(cur, sub_root):
            return True

        cur = cur.right
    return False


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
    # root:     3    sub_root:   4
    #          / \              / \
    #         4   5            1   2
    #        / \
    #       1   2
    assert is_subtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 2]))
    # root and sub_root are the same tree
    assert is_subtree(build_tree([3, 4, 5, 1, 2]), build_tree([3, 4, 5, 1, 2]))
    # Empty sub_root is always a subtree
    assert is_subtree(build_tree([1, 2, 3]), build_tree([]))
    # Not a subtree - different values
    assert not is_subtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 3]))
    # Not a subtree - different structure
    assert not is_subtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1]))
    # Single node subtree match
    assert not is_subtree(build_tree([1, 2, 3]), build_tree([1]))
    # Single node subtree no match
    assert not is_subtree(build_tree([1, 2, 3]), build_tree([4]))

    print("All tests passed.")
