"""
LeetCode 100: Same Tree
https://leetcode.com/problems/same-tree/

Problem: Given the roots of two binary trees p and q, check if they are the same
tree. Two binary trees are considered the same if they are structurally identical,
and the nodes have the same value.

Constraints:
- The number of nodes in both trees is in the range [0, 100].
- -10^4 <= Node.val <= 10^4.

Approach: Iterative DFS with parallel inorder traversal
- Use two stacks to traverse both trees simultaneously in inorder
- Walk left to the bottom, pushing nodes onto respective stacks
- Compare stack lengths to verify structural equivalence
- Pop and compare node values, then move to right subtrees
- Base cases: both None → True; only one None → False

Time: O(n)   Space: O(h) for the two stacks
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


def is_same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    """
    Check if two binary trees are the same (structurally identical and same values).

    Args:
        p: Root of the first binary tree.
        q: Root of the second binary tree.

    Returns:
        True if the trees are the same, False otherwise.
    """
    """
    if not p and not q:
        return True
    elif not p or not q:
        return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
    """
    if not p and not q:
        return True
    elif not p or not q:
        return False

    stack_p = []
    stack_q = []
    curr_p = p
    curr_q = q
    while stack_p or stack_q or curr_p or curr_q:
        while curr_p:
            stack_p.append(curr_p)
            curr_p = curr_p.left

        while curr_q:
            stack_q.append(curr_q)
            curr_q = curr_q.left

        if len(stack_p) != len(stack_q):
            return False

        curr_p = stack_p.pop()
        curr_q = stack_q.pop()
        if curr_p.val != curr_q.val:
            return False

        curr_p = curr_p.right
        curr_q = curr_q.right

    return True


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
    #     1         1
    #    / \       / \
    #   2   3     2   3  -> same
    assert is_same_tree(build_tree([1, 2, 3]), build_tree([1, 2, 3]))
    #     1         1
    #    /           \
    #   2             2  -> NOT same (different structure)
    assert not is_same_tree(build_tree([1, 2]), build_tree([1, None, 2]))
    #     1         1
    #    / \       / \
    #   2   1     1   2  -> NOT same (different values)
    assert not is_same_tree(build_tree([1, 2, 1]), build_tree([1, 1, 2]))
    # Both empty trees are the same
    assert is_same_tree(build_tree([]), build_tree([]))
    # One empty, one not -> NOT same
    assert not is_same_tree(build_tree([]), build_tree([1]))
    # Single node, same values -> same
    assert is_same_tree(build_tree([1]), build_tree([1]))
    # Single node, different values -> NOT same
    assert not is_same_tree(build_tree([1]), build_tree([2]))

    print("All tests passed.")
