"""
LeetCode 101: Symmetric Tree
https://leetcode.com/problems/symmetric-tree/

Problem: Given the root of a binary tree, check whether it is a mirror of itself
(i.e., symmetric around its center). A tree is symmetric if the left subtree is a
mirror reflection of the right subtree.

Constraints:
- The number of nodes in the tree is in the range [1, 1000].
- -100 <= Node.val <= 100.

Approach: Iterative mirror traversal with two stacks
- Traverse left subtree leftward, right subtree rightward (mirror paths)
- Compare stack lengths to verify structural equivalence
- Pop and compare node values, then cross to opposite sides
- Left's right child mirrors Right's left child

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


def is_symmetric(root: TreeNode | None) -> bool:
    """
    Check if a binary tree is symmetric (mirror of itself).

    Args:
        root: Root of the binary tree.

    Returns:
        True if the tree is symmetric, False otherwise.
    """
    """
    if not root:
        return True
    def is_mirror(left: TreeNode | None, right: TreeNode | None) -> bool:
        if not left and not right:
            return True

        if not left or not right:
            return False

        return left.val == right.val and is_mirror(left.left, right.right) and is_mirror(left.right, right.left) # type: ignore
    return is_mirror(root.left, root.right)
    """
    if not root:
        return True

    stack_l = []
    stack_r = []
    curr_l = root.left
    curr_r = root.right
    while stack_l or stack_r or curr_l or curr_r:
        while curr_l:
            stack_l.append(curr_l)
            curr_l = curr_l.left

        while curr_r:
            stack_r.append(curr_r)
            curr_r = curr_r.right

        if len(stack_l) != len(stack_r):
            return False

        curr_l = stack_l.pop()
        curr_r = stack_r.pop()
        if curr_l.val != curr_r.val:
            return False

        curr_l = curr_l.right
        curr_r = curr_r.left

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
    #     1
    #    / \
    #   2   2  -> symmetric
    #  / \ / \
    # 3  4 4  3
    assert is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3]))
    #     1
    #    / \
    #   2   2  -> NOT symmetric
    #    \   \
    #    3    3
    assert not is_symmetric(build_tree([1, 2, 2, None, 3, None, 3]))
    # Single node is symmetric
    assert is_symmetric(build_tree([1]))
    # Empty tree is symmetric (though constraint says min 1 node)
    assert is_symmetric(build_tree([]))
    #     1
    #    / \
    #   2   2  -> symmetric
    #      / \
    #     3   3
    assert is_symmetric(build_tree([1, 2, 2, 3, 3, 3, 3]))

    print("All tests passed.")
