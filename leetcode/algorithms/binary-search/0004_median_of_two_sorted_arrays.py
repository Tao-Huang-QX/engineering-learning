"""
LeetCode 4: Median of Two Sorted Arrays
https://leetcode.com/problems/median-of-two-sorted-arrays/

Problem: Given two sorted arrays nums1 and nums2 of size m and n respectively,
return the median of the two sorted arrays.

Follow-up: The overall run time complexity should be O(log(m+n)).

Constraints:
- nums1.length == m, nums2.length == n
- 0 <= m <= 1000, 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

Examples:
- Input: nums1 = [1,3], nums2 = [2]
  Output: 2.00000
  Explanation: merged array = [1,2,3] and median is 2.

- Input: nums1 = [1,2], nums2 = [3,4]
  Output: 2.50000
  Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Approach: Binary search on the partition (median as a cut, not a position)
- The median splits all elements into halves where left <= right and sizes
  balance — search the cut, never merge
- Cut nums1 after i elements; then j = half - i is FORCED (half keeps the
  sizes balanced, +1 parks the odd extra element on the left)
- Valid partition iff the two cross-checks hold: nums1[i-1] <= nums2[j]
  and nums2[j-1] <= nums1[i] — each array's internal order comes free
- Search i over cut positions [0, m] of the SHORTER array so every forced
  j lands in [0, n]; move left if nums1[i-1] > nums2[j], right otherwise
- ±inf sentinels for cuts at the edges (i or j at 0 / end) replace all
  special cases
- Odd total: max of left boundaries; even: average of left-max, right-min

Time: O(log(min(m, n)))   Space: O(1)
"""


def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Return the median of the two sorted arrays.

    Args:
        nums1: First sorted array of integers
        nums2: Second sorted array of integers

    Returns:
        Median of all elements (float; average of two middles if even total)
    """
    # Binary search on the shorter array so every forced j = half - i is in range
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)

    half = (m + n + 1) // 2  # left half size; +1 puts the odd extra on the left
    left, right = 0, m  # cut position i:  number of nums1 elements on the left

    while left <= right:
        i = (left + right) // 2  # nums1 contributes nums1[:i]
        j = half - i  # nums2 contributes nums2[:j] (forced)

        # Boundary values with ±inf sentinels for cuts at the edges
        a_left = nums1[i - 1] if i > 0 else float("-inf")
        a_right = nums1[i] if i < m else float("inf")
        b_left = nums2[j - 1] if j > 0 else float("-inf")
        b_right = nums2[j] if j < n else float("inf")

        if a_left <= b_right and b_left <= a_right:  # valid partition
            if (m + n) % 2 == 1:
                return float(max(a_left, b_left))  # odd: extra element sits left
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:  # nums1's cut is too far right
            right = i - 1
        else:  # b_left > a_right: too far left
            left = i + 1

    raise ValueError("inputs are not sorted")


if __name__ == "__main__":
    # Example 1: odd total
    result1 = find_median_sorted_arrays([1, 3], [2])
    expected1 = 2.0
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: even total
    result2 = find_median_sorted_arrays([1, 2], [3, 4])
    expected2 = 2.5
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: one array empty (both empty is outside the constraints)
    result3 = find_median_sorted_arrays([], [1])
    expected3 = 1.0
    assert result3 == expected3, f"Empty nums1: got {result3}, expected {expected3}"

    result4 = find_median_sorted_arrays([2, 4, 6], [])
    expected4 = 4.0
    assert result4 == expected4, f"Empty nums2: got {result4}, expected {expected4}"

    # Edge: interleaved values, even total
    result5 = find_median_sorted_arrays([1, 5, 9], [2, 3, 7])
    expected5 = 4.0
    assert result5 == expected5, f"Interleaved: got {result5}, expected {expected5}"

    # Edge: negative values, very different lengths
    result6 = find_median_sorted_arrays([-5, -3, -1], [1000000])
    expected6 = -2.0
    assert result6 == expected6, f"Negatives: got {result6}, expected {expected6}"

    print("All tests passed.")


# solved: 2026-11-04, hard, 60min, Median of Two Sorted Arrays
