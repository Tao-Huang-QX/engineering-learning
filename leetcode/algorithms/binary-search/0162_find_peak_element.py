"""
LeetCode 162: Find Peak Element
https://leetcode.com/problems/find-peak-element/

Problem: Given a 0-indexed integer array nums, find a peak element and return its
index. A peak element is an element that is strictly greater than its neighbors.
If the array contains multiple peaks, return the index to any of the peaks. You may
imagine that nums[-1] = nums[n] = -∞. The array is guaranteed to have no adjacent
elements that are equal.

Constraints:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i

Follow-up: Your solution should run in O(log n) time.

Approach: Binary search on the rising slope
- Compare nums[mid] with nums[mid + 1] to decide which half contains a peak
- If nums[mid] < nums[mid + 1], we're on an ascending slope → peak is on the right
- Otherwise, we're at or past a peak → peak is on the left (or at mid)
- Narrow until left == right → that index is a peak

Time: O(log n)   Space: O(1)
"""


def find_peak_element(nums: list[int]) -> int:
    """
    Find a peak element in the array and return its index.

    A peak element is an element that is strictly greater than its neighbors.
    For corner elements, only consider one neighbor (nums[-1] = nums[n] = -∞).

    Args:
        nums: Array of integers with no adjacent equal elements.

    Returns:
        Index of any peak element.
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left  # or right - they converge


if __name__ == "__main__":
    # Test cases from the problem description
    assert find_peak_element([1, 2, 3, 1]) in [2]  # peak at index 2 (value 3)
    assert find_peak_element([1, 2, 1, 3, 5, 6, 4]) in [1, 5]  # peaks at index 1 (2) or 5 (6)
    # Single element is a peak
    assert find_peak_element([5]) in [0]
    # Two elements - either can be peak
    assert find_peak_element([1, 2]) in [1]  # 2 > 1
    assert find_peak_element([2, 1]) in [0]  # 2 > 1
    # Strictly increasing - last element is peak
    assert find_peak_element([1, 2, 3, 4, 5]) in [4]
    # Strictly decreasing - first element is peak
    assert find_peak_element([5, 4, 3, 2, 1]) in [0]
    # Multiple peaks
    assert find_peak_element([1, 3, 2, 4, 1, 5, 2]) in [1, 3, 5]  # peaks at 3, 4, or 5

    print("All tests passed.")
