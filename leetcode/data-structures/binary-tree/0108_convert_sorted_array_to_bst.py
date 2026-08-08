"""
LeetCode 108: Convert Sorted Array to Binary Search Tree
https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

Problem: Given an integer array nums where the elements are sorted in ascending
order, convert it to a height-balanced binary search tree.

A height-balanced binary tree is a binary tree in which the depth of the two
subtrees of every node never differs by more than one.

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in a strictly increasing order.

Examples:
- Input: nums = [-10,-3,0,5,9]
  Output: [0,-3,9,-10,null,5]
  Explanation: [0,-10,5,null,-3,null,9] is also accepted (any height-balanced BST).

- Input: nums = [1,3]
  Output: [3,1]
  Explanation: [1,null,3] and [3,1] are both accepted.

Approach: Divide & conquer — midpoint as root
- Pick middle element as root for balanced split
- Recursively build left from [0, mid-1], right from [mid+1, n-1]
- BST property guaranteed: sorted input → left < mid < right

Time: O(n)   Space: O(log n)
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sorted_array_to_bst(nums: list[int]) -> TreeNode | None:
    """
    Convert a sorted array to a height-balanced BST.

    Args:
        nums: Array of integers sorted in ascending order

    Returns:
        Root of the height-balanced BST
    """

    def dfs(left: int, right: int) -> TreeNode | None:
        if left > right:
            return None

        mid = left + (right - left) // 2
        root = TreeNode(nums[mid])
        root.left = dfs(left, mid - 1)
        root.right = dfs(mid + 1, right)
        return root

    return dfs(0, len(nums) - 1)


def _bst_to_level_order(root: TreeNode | None) -> list[int | None]:
    """Helper to convert tree to level-order list for verification."""
    if not root:
        return []
    result: list[int | None] = []
    queue: list[TreeNode | None] = [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


if __name__ == "__main__":
    # Example 1: multiple valid outputs, verify one accepted form
    root1 = sorted_array_to_bst([-10, -3, 0, 5, 9])
    result1 = _bst_to_level_order(root1)
    # Both [0,-3,9,-10,null,5] and [0,-10,5,null,-3,null,9] are valid
    valid1 = result1 in ([0, -3, 9, -10, None, 5], [0, -10, 5, None, -3, None, 9])
    assert valid1, f"Example 1: got {result1}, expected a valid height-balanced BST"

    # Example 2
    root2 = sorted_array_to_bst([1, 3])
    result2 = _bst_to_level_order(root2)
    valid2 = result2 in ([1, None, 3], [3, 1])
    assert valid2, f"Example 2: got {result2}, expected a valid height-balanced BST"

    print("All tests passed.")
