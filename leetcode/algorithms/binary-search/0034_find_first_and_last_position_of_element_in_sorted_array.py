"""
LeetCode 34: Find First and Last Position of Element in Sorted Array
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

Problem: Given an array of integers nums sorted in non-decreasing order,
find the starting and ending position of a given target value. If target
is not found in the array, return [-1, -1]. You must write an algorithm
with O(log n) runtime complexity.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array
- -10^9 <= target <= 10^9

Examples:
- Input: nums = [5,7,7,8,8,10], target = 8
  Output: [3,4]

- Input: nums = [5,7,7,8,8,10], target = 6
  Output: [-1,-1]

- Input: nums = [], target = 0
  Output: [-1,-1]

Approach: Two half-open bounds — the predicates differ by one comparator
- lower_bound: first index with nums[i] >= target (bisect_left); move lo
  past everything strictly less
- upper_bound: first index with nums[i] > target (bisect_right); the <=
  lets equal elements move lo too — lands one past the duplicate run
- Search space [0, n] (NOT n-1): insertion points may equal n (all-target
  array makes upper = n, last = n-1); also makes the empty case free
- last = upper - 1 is index-safe because the first-check proved the run
  exists, so upper >= first + 1; no negative indexing possible
- Never scan outward from a found hit — that's O(n) on all-duplicate input

Time: O(log n)   Space: O(1)
"""


def search_range(nums: list[int], target: int) -> list[int]:
    """
    Return the first and last index of target in sorted nums.

    Args:
        nums: Sorted (non-decreasing) integers, possibly empty
        target: Value to locate

    Returns:
        [first_index, last_index], or [-1, -1] if target is absent
    """

    def lower_bound() -> int:
        """First index with nums[i] >= target (bisect_left)."""
        lo, hi = 0, len(nums)  # half-open: answer may be len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def upper_bound() -> int:
        """First index with nums[i] > target (bisect_right)."""
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] <= target:  # <- the only difference: <= vs <
                lo = mid + 1
            else:
                hi = mid
        return lo

    first = lower_bound()
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, upper_bound() - 1]


if __name__ == "__main__":
    # Example 1: target present with duplicates
    result1 = search_range([5, 7, 7, 8, 8, 10], 8)
    expected1 = [3, 4]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: target absent (falls between values)
    result2 = search_range([5, 7, 7, 8, 8, 10], 6)
    expected2 = [-1, -1]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3: empty array
    result3 = search_range([], 0)
    expected3 = [-1, -1]
    assert result3 == expected3, f"Empty: got {result3}, expected {expected3}"

    # Edge: single element, hit and miss
    assert search_range([1], 1) == [0, 0], f"Single hit: got {search_range([1], 1)}"
    assert search_range([1], 2) == [-1, -1], f"Single miss: got {search_range([1], 2)}"

    # Edge: entire array is the target
    assert search_range([2, 2, 2, 2], 2) == [0, 3], (
        f"All target: got {search_range([2, 2, 2, 2], 2)}"
    )

    # Edge: target at the extremes
    assert search_range([1, 2, 3], 1) == [0, 0], f"First: got {search_range([1, 2, 3], 1)}"
    assert search_range([1, 2, 3], 3) == [2, 2], f"Last: got {search_range([1, 2, 3], 3)}"

    # Edge: target beyond both ends
    assert search_range([5, 7], 4) == [-1, -1], f"Below: got {search_range([5, 7], 4)}"
    assert search_range([5, 7], 9) == [-1, -1], f"Above: got {search_range([5, 7], 9)}"

    # Edge: negatives
    assert search_range([-5, -5, -3, 0], -5) == [0, 1], (
        f"Negatives: got {search_range([-5, -5, -3, 0], -5)}"
    )

    print("All tests passed.")


# solved: 2026-11-15, medium, 40min, Find First and Last Position of Element in Sorted Array
