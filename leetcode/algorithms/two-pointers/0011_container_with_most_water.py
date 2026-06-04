"""
LeetCode 11: Container With Most Water
https://leetcode.com/problems/container-with-most-water/

Problem: Find two lines that together with the x-axis form a container that holds the most water.

Approach: Two pointers (greedy)
- Start with widest container (left=0, right=len - 1)
- Move pointer at shorter line inward (hope to find taller line)
- Track max area during traversal

Time: O(n)   Space: O(1)
"""


def max_area(height: list[int]) -> int:
    """
    Return the maximum amount of water a container can store.

    Args:
        height: Array of heights where each index represents a vertical line

    Returns:
        Maximum area of water that can be contained
    """
    left, right = 0, len(height) - 1
    max_amount = 0
    while left < right:
        current_amount = min(height[left], height[right]) * (right - left)
        max_amount = max(current_amount, max_amount)
        if height[left] < height[right]:
            left += 1  # Move short line
        else:
            right -= 1  # Or either if equal
    return max_amount


if __name__ == "__main__":
    # Example 1
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    # Example 2
    assert max_area([1, 1]) == 1

    print("All tests passed!")
