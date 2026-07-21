"""
LeetCode 145: Binary Tree Postorder Traversal
https://leetcode.com/problems/binary-tree-postorder-traversal/

Problem: Given the root of a binary tree, return the postorder traversal of its nodes' values.

Constraints:
- The number of nodes is in the range [0, 100].
- -100 <= Node.val <= 100

Examples:
- Input: root = [1,null,2,3]
  Output: [3,2,1]
  Explanation: Postorder: left → right → root

Approach: Iterative postorder with stack and last-visited pointer
- Go deep left while pushing nodes to stack
- When can't go left, peek at stack top
- If right child exists AND not yet visited, go right
- Otherwise (no right or right already visited): visit node, pop, mark as last_visited
- last_visited tells us if we already processed the right subtree

Time: O(n) — each node visited once
Space: O(h) — stack height, where h is tree height (worst O(n) for skewed tree)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def postorder_traversal(root: TreeNode | None) -> list[int]:
    """
    Return the postorder traversal of a binary tree.

    Args:
        root: The root of the binary tree

    Returns:
        List of node values in postorder (left → right → root)
    """
    """
    result =[]
    def dfs(node: TreeNode):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)
    dfs(root)
    return result
    """
    if not root:
        return []

    stack = []
    result = []
    curr = root
    last_visited = None

    while stack or curr:
        # Go as deep left as possible
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            # Peek at top of stack
            temp = stack[-1]
            # If right child exists and Not visited it yet, go right
            if temp.right and temp.right != last_visited:
                curr = temp.right
            # Both children processed -> this is time to visit
            else:
                result.append(temp.val)
                last_visited = temp
                stack.pop()

    return result


if __name__ == "__main__":
    # Example 1: root = [1,null,2,3]
    #     1
    #      \
    #       2
    #      /
    #     3
    root1 = TreeNode(1)
    root1.right = TreeNode(2)
    root1.right.left = TreeNode(3)
    assert postorder_traversal(root1) == [3, 2, 1]

    # Edge case: empty tree
    assert postorder_traversal(None) == []

    # Edge case: single node
    root2 = TreeNode(1)
    assert postorder_traversal(root2) == [1]

    # Edge case: left-skewed tree
    #     1
    #    /
    #   2
    #  /
    # 3
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    root3.left.left = TreeNode(3)
    assert postorder_traversal(root3) == [3, 2, 1]

    print("All tests passed.")
