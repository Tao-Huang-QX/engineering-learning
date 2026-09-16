"""
LeetCode 701: Insert into a Binary Search Tree
https://leetcode.com/problems/insert-into-a-binary-search-tree/

Problem: Given the root node of a BST and a value to insert, insert the value into the BST. Return the root node of the BST after the insertion.

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -10^8 <= Node.val <= 10^8
- All values in the tree are unique.
- -10^8 <= val <= 10^8
- It's guaranteed that val does not exist in the original BST.

Examples:
- Input: root = [4,2,7,1,3], val = 5
  Output: [4,2,7,1,3,5]
  Explanation: 5 becomes the left child of 7.

Approach: Iterative BST insertion with parent tracking
- Traverse down the tree: left if val < current, right if val > current
- Track parent node and direction (left or right child) during traversal
- When reaching null, insert new node as appropriate child of parent
- Empty tree case: new node becomes root

Time: O(h) — h is tree height, O(log n) balanced, O(n) worst-case
Space: O(1) — only pointer variables, no recursion stack
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insert_into_bst(root: TreeNode | None, val: int) -> TreeNode:
    """
    Insert a value into the BST and return the root.

    Args:
        root: The root of the BST
        val: The value to insert

    Returns:
        The root of the BST after insertion
    """
    if not root:
        return TreeNode(val)

    curr = root
    parent = None
    is_left_child = False
    while curr:
        parent = curr

        if curr.val < val:
            curr = curr.right
            is_left_child = False
        else:
            curr = curr.left
            is_left_child = True

    if is_left_child:
        parent.left = TreeNode(val)  # pyright: ignore[reportOptionalMemberAccess]
    else:
        parent.right = TreeNode(val)  # pyright: ignore[reportOptionalMemberAccess]
    return root


if __name__ == "__main__":

    def inorder(node: TreeNode | None, out: list[int]) -> None:
        """Append node values to out in left → root → right order."""
        if node:
            inorder(node.left, out)
            out.append(node.val)
            inorder(node.right, out)

    # Example 1: root = [4,2,7,1,3], val = 5
    #       4              4
    #      / \            / \
    #     2   7    →     2   7
    #    / \            / \ /
    #   1   3          1  3 5
    root1 = TreeNode(4)
    root1.left = TreeNode(2)
    root1.right = TreeNode(7)
    root1.left.left = TreeNode(1)
    root1.left.right = TreeNode(3)

    result1 = insert_into_bst(root1, 5)
    assert (
        result1.right is not None and result1.right.left is not None and result1.right.left.val == 5
    ), "Example 1: 5 should land as the left child of 7"
    seq1: list[int] = []
    inorder(result1, seq1)
    assert seq1 == [1, 2, 3, 4, 5, 7], f"Example 1 inorder: got {seq1}"

    # Example 2: root = [40,20,60,10,30,50,70], val = 25
    #       40                  40
    #      /  \                /  \
    #     20   60             20   60
    #    / \   / \           / \   / \
    #   10 30 50 70    →    10 30 50 70
    #      /                   /
    #     25                  25
    root2 = TreeNode(40)
    root2.left = TreeNode(20)
    root2.right = TreeNode(60)
    root2.left.left = TreeNode(10)
    root2.left.right = TreeNode(30)
    root2.right.left = TreeNode(50)
    root2.right.right = TreeNode(70)

    result2 = insert_into_bst(root2, 25)
    assert (
        result2.left is not None
        and result2.left.right is not None
        and result2.left.right.left is not None
        and result2.left.right.left.val == 25
    ), "Example 2: 25 should land as the left child of 30"
    seq2: list[int] = []
    inorder(result2, seq2)
    assert seq2 == [10, 20, 25, 30, 40, 50, 60, 70], f"Example 2 inorder: got {seq2}"

    # Example 3: empty tree
    result3 = insert_into_bst(None, 5)
    assert result3.val == 5
    assert result3.left is None
    assert result3.right is None

    print("All tests passed.")
