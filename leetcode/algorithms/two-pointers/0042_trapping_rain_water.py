"""
LeetCode 42: Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/

Problem: Given n non-negative integers representing an elevation map, compute how much water it can trap after raining.

Approach: Two pointers (greedy)
- Track left_max and right_max (highest bars seen from each side)
- Move pointer with smaller max (it's the bottleneck for that side)
- Water at position = current_max - height (max bounds the water level)

Time: O(n)   Space: O(1)
"""


def trap(height: list[int]) -> int:
    """
    Return the total amount of trapped rainwater.

    Args:
        height: Elevation map where each element is the height of a bar

    Returns:
        Total units of water that can be trapped
    """
    water = 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    while left < right:
        if left_max < right_max:
            # Process left position
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            # Process right position
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water


if __name__ == "__main__":
    # Example 1
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    # Example 2
    assert trap([4, 2, 0, 3, 2, 5]) == 9

    print("All tests passed!")
