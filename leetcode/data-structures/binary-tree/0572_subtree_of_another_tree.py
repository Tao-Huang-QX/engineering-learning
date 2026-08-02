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
- For each node in root, use is_sametree to check if the subtree matches sub_root exactly
- A subtree match requires identical structure AND values — not just finding a node with the same value

Time: O(n × m)   Space: O(h + m)
where n = nodes in root, m = nodes in sub_root, h = height of root
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
        stack_l = []
        stack_r = []
        curr_l = left
        curr_r = right

        while stack_l or curr_l or stack_r or curr_r:
            while curr_l:
                stack_l.append(curr_l)
                curr_l = curr_l.left
            while curr_r:
                stack_r.append(curr_r)
                curr_r = curr_r.left

            if len(stack_l) != len(stack_r):
                return False

            curr_l = stack_l.pop()
            curr_r = stack_r.pop()
            if curr_l.val != curr_r.val:
                return False

            curr_l = curr_l.right
            curr_r = curr_r.right

        return True

    stack = []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        if is_sametree(curr, sub_root):
            return True

        curr = curr.right
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
