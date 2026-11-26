"""
LeetCode 454: 4Sum II
https://leetcode.com/problems/4sum-ii/

Problem: Given four integer arrays nums1, nums2, nums3, and nums4 all
of length n, return the number of tuples (i, j, k, l) such that:
- 0 <= i, j, k, l < n
- nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0

Constraints:
- n == nums1.length == nums2.length == nums3.length == nums4.length
- 1 <= n <= 200
- -2^28 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 2^28

Examples:
- Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
  Output: 2
  Explanation: the two tuples are (0,0,0,1) -> 1 + (-2) + (-1) + 2 = 0
    and (1,1,0,0) -> 2 + (-2) + (-1) + 0 = 0.

- Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
  Output: 1
  Explanation: the single tuple (0,0,0,0) sums to 0 + 0 + 0 + 0 = 0.

Approach: Meet-in-the-middle pair counts
- Phase 1: count every nums1[i] + nums2[j] into a map — n^2 pairs
- Phase 2: for each nums3[k] + nums4[l], add the count of first-half
  pairs whose sum negates it; map holds counts, so tuple multiplicity
  survives (all-zeros case -> 4 x 4 = 16)

Time: O(n^2)   Space: O(n^2)
"""


def four_sum_count(nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]) -> int:
    """
    Count index tuples whose four-way sum is zero.

    Args:
        nums1, nums2, nums3, nums4: Four equal-length integer arrays

    Returns:
        Number of (i, j, k, l) index tuples with a zero total; tuples
        are counted per index, so equal values count separately
    """
    n = len(nums1)
    pair_sums: dict[int, int] = {}
    for i in range(n):
        for j in range(n):
            pair_sums[nums1[i] + nums2[j]] = pair_sums.get(nums1[i] + nums2[j], 0) + 1

    total = 0
    for k in range(n):
        for j in range(n):
            total += pair_sums.get(-(nums3[k] + nums4[j]), 0)

    return total


if __name__ == "__main__":
    # Example 1: two zero-sum tuples
    result1 = four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2])
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: one tuple, summing to zero
    result2 = four_sum_count([0], [0], [0], [0])
    expected2 = 1
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: no zero-sum combination at all
    assert four_sum_count([1], [1], [1], [1]) == 0, (
        f"No zeros: got {four_sum_count([1], [1], [1], [1])}"
    )

    # Edge: all zeros — every combination counts (2^4 tuples)
    assert four_sum_count([0, 0], [0, 0], [0, 0], [0, 0]) == 16, (
        f"All zeros: got {four_sum_count([0, 0], [0, 0], [0, 0], [0, 0])}"
    )

    # Edge: single elements summing to zero
    assert four_sum_count([1], [-1], [0], [0]) == 1, (
        f"Single: got {four_sum_count([1], [-1], [0], [0])}"
    )

    # Edge: negatives mirrored by positives — zero sum needs exactly two
    # +1's among four picks: C(4,2) = 6 tuples
    assert four_sum_count([1, -1], [1, -1], [1, -1], [1, -1]) == 6, (
        f"Mirrored: got {four_sum_count([1, -1], [1, -1], [1, -1], [1, -1])}"
    )

    print("All tests passed.")


# solved: 2026-11-26, medium, 30min, 4Sum II
