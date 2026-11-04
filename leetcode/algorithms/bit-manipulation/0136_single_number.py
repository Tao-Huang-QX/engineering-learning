"""
LeetCode 136: Single Number
https://leetcode.com/problems/single-number/

Problem: Given a non-empty array of integers nums, every element appears twice
except for one. Find that single one. You must implement a solution with
linear runtime complexity and without using extra memory.

Constraints:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element in nums appears twice except for one element which appears once

Examples:
- Input: nums = [2,2,1]
  Output: 1

- Input: nums = [4,1,2,1,2]
  Output: 4

- Input: nums = [1]
  Output: 1

Approach: XOR fold — pairs annihilate, the singleton survives
- Laws: x ^ x = 0, x ^ 0 = x, and XOR is commutative/associative — so the
  fold equals any rearrangement with pairs adjacent: 0 ^ 0 ^ ... ^ single
- Seed with 0 (XOR's identity); no nums[1:] slice (hidden O(n) copy)
- Safe on negatives: Python ints XOR as two's complement with infinite
  sign extension, so x ^ x == 0 holds for the whole constraint range
  without 32-bit masking
- Alternatives rejected: Counter / set (O(n) extra memory),
  2*sum(set(nums)) - sum(nums) (O(n) for the set) — XOR meets both
  stated constraints (linear time, no extra memory)

Time: O(n)   Space: O(1)
"""


def single_number(nums: list[int]) -> int:
    """
    Return the element that appears exactly once.

    Args:
        nums: Array where every element appears twice except one

    Returns:
        The single element that appears once
    """
    result = 0
    for num in nums:
        result ^= num
    return result


if __name__ == "__main__":
    # Example 1
    result1 = single_number([2, 2, 1])
    expected1 = 1
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = single_number([4, 1, 2, 1, 2])
    expected2 = 4
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3: single element
    result3 = single_number([1])
    expected3 = 1
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    # Edge: negative values
    result4 = single_number([-1, -1, -30000])
    expected4 = -30000
    assert result4 == expected4, f"Negatives: got {result4}, expected {expected4}"

    # Edge: single element at the boundary
    result5 = single_number([30000, 0, 30000])
    expected5 = 0
    assert result5 == expected5, f"Zero as answer: got {result5}, expected {expected5}"

    print("All tests passed.")


# solved: 2026-11-04, easy, 15min, Single Number
