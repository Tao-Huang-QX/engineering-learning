"""
LeetCode 977: Squares of a Sorted Array
https://leetcode.com/problems/squares-of-a-sorted-array/

Problem: Given an integer array nums sorted in non-decreasing order,
return an array of the squares of each number sorted in non-decreasing
order.

Follow-up: squaring each element and sorting the new array is very
trivial — could you find an O(n) solution using a different approach?

Constraints:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order

Examples:
- Input: nums = [-4,-1,0,3,10]
  Output: [0,1,9,16,100]
  Explanation: after squaring, the array becomes [16,1,0,9,100];
    after sorting, [0,1,9,16,100].

- Input: nums = [-7,-3,2,3,11]
  Output: [4,9,9,49,121]

Approach: Two pointers + back-fill
- Largest |value| sits at an end: compare abs at both ends, write the
  winner into result from the back — descending slots yield ascending
  output, no reverse
- One pointer advances per step (the claimed side); left <= right
  gives the survivor its own slot

Time: O(n)   Space: O(n)
"""


def sorted_squares(nums: list[int]) -> list[int]:
    """
    Return the squares of nums, sorted non-decreasing.

    Args:
        nums: Array sorted non-decreasing, possibly containing negatives

    Returns:
        New array of squared values in non-decreasing order
    """
    left, right = 0, len(nums) - 1
    result: list[int] = [0] * len(nums)
    pos = len(nums) - 1

    while left <= right:
        if abs(nums[left]) > abs(nums[right]):
            result[pos] = nums[left] * nums[left]
            left += 1
        else:
            result[pos] = nums[right] * nums[right]
            right -= 1
        pos -= 1

    return result


if __name__ == "__main__":
    # Example 1: negatives flip to the top of the squares
    result1 = sorted_squares([-4, -1, 0, 3, 10])
    expected1 = [0, 1, 9, 16, 100]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: mixed signs with duplicate squares
    result2 = sorted_squares([-7, -3, 2, 3, 11])
    expected2 = [4, 9, 9, 49, 121]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: all negative — squares descend, so the answer is reversed input
    assert sorted_squares([-5, -3, -1]) == [1, 9, 25], (
        f"All neg: got {sorted_squares([-5, -3, -1])}"
    )

    # Edge: all positive — squares already sorted
    assert sorted_squares([1, 2, 3]) == [1, 4, 9], f"All pos: got {sorted_squares([1, 2, 3])}"

    # Edge: single element, negative and positive
    assert sorted_squares([-7]) == [49], f"Single neg: got {sorted_squares([-7])}"
    assert sorted_squares([4]) == [16], f"Single pos: got {sorted_squares([4])}"

    # Edge: zero in the middle
    assert sorted_squares([-1, 0, 1]) == [0, 1, 1], f"Zero: got {sorted_squares([-1, 0, 1])}"

    # Edge: duplicate values across the sign boundary square identically
    assert sorted_squares([-3, -3, 3]) == [9, 9, 9], f"Dup: got {sorted_squares([-3, -3, 3])}"

    print("All tests passed.")


# solved: 2026-11-23, easy, 25min, Squares of a Sorted Array
