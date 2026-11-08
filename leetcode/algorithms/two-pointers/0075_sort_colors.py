"""
LeetCode 75: Sort Colors
https://leetcode.com/problems/sort-colors/

Problem: Given an array nums with n objects colored red, white, or blue,
represented by the numbers 0, 1, and 2, sort them IN-PLACE so that objects
of the same color are adjacent, with the colors in the order red, white,
and blue (0s, then 1s, then 2s). You must solve this problem without using
the library's sort function.

Follow-up: Could you come up with a one-pass algorithm using only constant
extra space?

Constraints:
- 1 <= nums.length <= 300
- nums[i] is 0, 1, or 2

Examples:
- Input: nums = [2,0,2,1,1,0]
  Output: [0,0,1,1,2,2]

- Input: nums = [2,0,1]
  Output: [0,1,2]

Approach: Dutch national flag — one-pass three-way partition
- Invariant: [settled 0s | settled 1s | unexamined | settled 2s] with
  boundaries left / mid / right; every iteration shrinks the unexamined
  middle by one
- Asymmetric advancement is the whole trick: after swapping with left,
  the value arriving at mid CAME FROM the settled-1s region (a known 1)
  so mid advances; after swapping with right, the arriving value is
  UNEXAMINED, so mid stays and re-reads it — advancing there lets a 0
  ride past the left region forever ([1,2,0] is the trap input)
- The 1 case needs no swap: mid's region is exactly where 1s belong
- Two-pass counting sort (count, rewrite) is the same asymptotics but
  two passes; the flag partition answers the one-pass follow-up
- Generalizes beyond three values poorly (quicksort's 3-way partition
  uses this exact shape for equal keys)

Time: O(n)   Space: O(1)   (each element swapped at most twice)
"""


def sort_colors(nums: list[int]) -> None:
    """
    Sort an array of 0s, 1s, and 2s in place.

    Args:
        nums: Array whose elements are each 0, 1, or 2

    Returns:
        None (nums is reordered in place)
    """
    left = 0  # everything before left is a settled 0
    mid = 0  # the scanner; [left..mid) is settled 1s
    right = len(nums) - 1  # everything after right is a settled 2

    while mid <= right:
        if nums[mid] == 0:
            nums[left], nums[mid] = nums[mid], nums[left]
            left += 1
            mid += 1  # safe to advance: what came in from the left is a settled 1
        elif nums[mid] == 2:
            nums[mid], nums[right] = nums[right], nums[mid]
            right -= 1
            # mid does NOT advance: the value swapped in from the right is unexamined
        else:
            mid += 1


if __name__ == "__main__":
    # Example 1
    nums1 = [2, 0, 2, 1, 1, 0]
    sort_colors(nums1)
    expected1 = [0, 0, 1, 1, 2, 2]
    assert nums1 == expected1, f"Example 1: got {nums1}, expected {expected1}"

    # Example 2
    nums2 = [2, 0, 1]
    sort_colors(nums2)
    expected2 = [0, 1, 2]
    assert nums2 == expected2, f"Example 2: got {nums2}, expected {expected2}"

    # Edge: already sorted
    nums3 = [0, 0, 1, 1, 2, 2]
    sort_colors(nums3)
    assert nums3 == [0, 0, 1, 1, 2, 2], f"Sorted: got {nums3}"

    # Edge: reverse sorted
    nums4 = [2, 2, 1, 1, 0, 0]
    sort_colors(nums4)
    assert nums4 == [0, 0, 1, 1, 2, 2], f"Reverse: got {nums4}"

    # Edge: all same value, each kind
    for v in (0, 1, 2):
        nums5 = [v] * 5
        sort_colors(nums5)
        assert nums5 == [v] * 5, f"All {v}s: got {nums5}"

    # Edge: single element
    nums6 = [1]
    sort_colors(nums6)
    assert nums6 == [1], f"Single: got {nums6}"

    # Edge: the classic trap — 0 swapped in from the right, then re-read
    nums7 = [1, 2, 0]
    sort_colors(nums7)
    assert nums7 == [0, 1, 2], f"Trap: got {nums7}"

    print("All tests passed.")


# solved: 2026-11-08, medium, 40min, Sort Colors
