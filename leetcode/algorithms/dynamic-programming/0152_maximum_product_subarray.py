"""
LeetCode 152: Maximum Product Subarray
https://leetcode.com/problems/maximum-product-subarray/

Problem: Given an integer array nums, find a subarray (contiguous non-empty
sequence) that has the largest product, and return the product.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any subarray of nums is guaranteed to fit in a 32-bit integer

Examples:
- Input: nums = [2,3,-2,4]
  Output: 6
  Explanation: [2,3] has the largest product 6.

- Input: nums = [-2,0,-1]
  Output: 0
  Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Approach: Kadane with a two-component state (max and min tracks)
- Multiplication is not monotone: a negative flips signs, so the WORST
  product ending at i-1 can become the BEST ending at i — a single
  running accumulator discards the buried minimum it will need
- Carry both tracks; each is fed by the same three candidates:
  restart at x, extend the max track, extend the min track
- Simultaneous update (tuple assign from candidates computed off both
  OLD values) — writing one track before reading the other goes wrong
  on sign-flip inputs
- The restart candidate x handles zeros for free: x=0 collapses both
  tracks and the next element starts clean, no special-casing
- Same shape as 0053 Kadane (1-D over positions) but with the state
  widened to two variables, like 0309's hold/sold/rest

Time: O(n)   Space: O(1)
"""


def max_product(nums: list[int]) -> int:
    """
    Return the largest product of any contiguous subarray.

    Args:
        nums: Array of integers

    Returns:
        Maximum subarray product
    """
    result = nums[0]
    max_end = min_end = nums[0]  # best/worst product of a subarray ending here
    for i in range(1, len(nums)):
        x = nums[i]
        # three candidates for each track: restart at x, extended the max track, extend the min track
        cand_max = max(x, max_end * x, min_end * x)
        cand_min = min(x, max_end * x, min_end * x)
        max_end, min_end = cand_max, cand_min  # simultaneous update - read both old values first
        result = max(result, max_end)
    return result


if __name__ == "__main__":
    # Example 1
    result1 = max_product([2, 3, -2, 4])
    expected1 = 6
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: zeros break the subarray
    result2 = max_product([-2, 0, -1])
    expected2 = 0
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: single element
    result3 = max_product([-5])
    expected3 = -5
    assert result3 == expected3, f"Single negative: got {result3}, expected {expected3}"

    # Edge: even count of negatives flips the sign to a win
    result4 = max_product([-2, 3, -4])
    expected4 = 24
    assert result4 == expected4, f"Even negatives: got {result4}, expected {expected4}"

    # Edge: a late negative resurrects a buried minimum
    result5 = max_product([2, -5, -2, -4, 3])
    expected5 = 24
    assert result5 == expected5, f"Sign flip: got {result5}, expected {expected5}"

    # Edge: zeros reset everything
    result6 = max_product([3, -1, 4, 0, -2, 6])
    expected6 = 6
    assert result6 == expected6, f"Zeros reset: got {result6}, expected {expected6}"

    print("All tests passed.")


# solved: 2026-11-06, medium, 30min, Maximum Product Subarray
