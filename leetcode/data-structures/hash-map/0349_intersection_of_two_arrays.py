"""
LeetCode 349: Intersection of Two Arrays
https://leetcode.com/problems/intersection-of-two-arrays/

Problem: Given two integer arrays nums1 and nums2, return an array of their
intersection. Each element in the result must be unique and the result may be
returned in any order.

Constraints:
- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 1000

Examples:
- Input: nums1 = [1,2,2,1], nums2 = [2,2]
  Output: [2]

- Input: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
  Output: [9,4]
  Explanation: [4,9] is also accepted (any order).

Approach: Set membership with remove-on-emit dedupe
- candidates = set(nums1); sweep nums2 emitting any num still in candidates
- Emitting removes the value from candidates, so `in candidates` is both
  the membership check and the not-already-emitted check (no flag needed)
- Explored alternative: values are bounded 0..1000, so a big-int bitmask
  per array (bit v = value v) makes intersection one word-parallel AND,
  with members peeled via x & -x — ~125 bytes vs tens of KB

Time: O(n + m)   Space: O(distinct values of nums1)
"""


def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Return the unique intersection of the two arrays.

    Args:
        nums1: First array of integers
        nums2: Second array of integers

    Returns:
        Array of distinct values present in both (any order)
    """
    candidates = set(nums1)
    result: list[int] = []
    for num in nums2:
        if num in candidates:
            result.append(num)
            candidates.remove(num)
    return result


if __name__ == "__main__":
    # Example 1
    result1 = intersection([1, 2, 2, 1], [2, 2])
    expected1 = [2]
    assert sorted(result1) == sorted(expected1), f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = intersection([4, 9, 5], [9, 4, 9, 8, 4])
    expected2 = [9, 4]
    assert sorted(result2) == sorted(expected2), f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
