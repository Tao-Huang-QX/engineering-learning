"""
LeetCode 53: Maximum Subarray
https://leetcode.com/problems/maximum-subarray/

Problem: Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

Approach: Kadane's algorithm
- At each element, decide: extend previous subarray or start fresh
- max(num, current_sum + num) captures this decision in one line

Time: O(n)   Space: O(1)
"""


def max_sub_array(nums: list[int]) -> int:
    """
    Find the contiguous subarray with the largest sum.

    Args:
        nums: List of integers (can be negative)

    Returns:
        The maximum sum of any contiguous subarray
    """
    """
    Devide and conquer approach:
    Time: O(n log n) Space; O(log n)
    def max_sub_array(nums, left, right):
        if left == right:
            return nums[left]
        mid = (left + right) // 2
        # Case 1: Max in left half
        left_max = max_sub_array(nums, left, mid)
        # Case 2: Max in right half
        right_max = max_sub_array(nums, mid + 1, right)
        # Case 3: Max crossing the midpoint
        # Find best sum from mid going left
        cross_left = float("-inf")
        sum_left = 0
        for i in range(mid, left - 1, -1):
            sum_left += nums[i]
            cross_left = max(cross_left, sum_left)
        # Find best sum from mid+1 going right
        cross_right = float("-inf")
        sum_right = 0
        for i in range(mid + 1, right + 1):
            sum_right += nums[i]
            cross_right = max(cross_right, sum_right)
        cross_max = cross_left + cross_right
        return max(left_max, right_max, cross_max)
    """
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        # Is current number hurting or helping the sum?
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum


if __name__ == "__main__":
    # Example 1: Mixed positive and negative
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

    # Example 2: All positive
    assert max_sub_array([1, 2, 3, 4, 5]) == 15

    # Example 3: Single element
    assert max_sub_array([5]) == 5

    # Example 4: All negative
    assert max_sub_array([-2, -1]) == -1

    # Example 5: Mixed with large negative drop
    assert max_sub_array([1, 2, -1, 2, -1, 2, -10, 3]) == 5

    print("All tests passed.")
