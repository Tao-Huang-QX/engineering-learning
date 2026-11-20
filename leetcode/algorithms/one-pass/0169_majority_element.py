"""
LeetCode 169: Majority Element
https://leetcode.com/problems/majority-element/

Problem: Given an array nums of size n, return the majority element.
The majority element is the element that appears more than floor(n / 2)
times. You may assume that the majority element always exists in the
array.

Follow-up: could you solve the problem in linear time and in O(1)
space?

Constraints:
- n == nums.length
- 1 <= n <= 5 * 10^4
- -10^9 <= nums[i] <= 10^9

Examples:
- Input: nums = [3,2,3]
  Output: 3

- Input: nums = [2,2,1,1,1,2,2]
  Output: 2

Approach: Boyer–Moore voting — cancellation against a guaranteed surplus
- One pass carrying candidate + count: count == 0 adopts the current
  element; a match increments, a mismatch decrements
- Why it survives: every decrement pairs the candidate against a distinct
  other element and cancels both — the majority outnumbers all others
  combined, so no pairing can eliminate it; the last candidate standing
  is the majority
- Load-bearing premise: existence is guaranteed. Without it the survivor
  is garbage ([1,2,3] -> 3) — LC 229 (> n/3) must verify or multi-track

Time: O(n)   Space: O(1)
"""


def majority_element(nums: list[int]) -> int:
    """
    Return the element appearing more than floor(n / 2) times.

    Args:
        nums: Non-empty array guaranteed to contain a majority element

    Returns:
        The majority element
    """
    candidate, count = None, 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate  # pyright: ignore[reportReturnType]


if __name__ == "__main__":
    # Example 1
    result1 = majority_element([3, 2, 3])
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = majority_element([2, 2, 1, 1, 1, 2, 2])
    expected2 = 2
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: single element — trivially the majority
    assert majority_element([1]) == 1, f"Single: got {majority_element([1])}"

    # Edge: bare minimum majority — exactly floor(n/2) + 1 occurrences
    assert majority_element([1, 2, 1]) == 1, f"Minimal: got {majority_element([1, 2, 1])}"

    # Edge: majority at the far end
    assert majority_element([6, 5, 5]) == 5, f"End: got {majority_element([6, 5, 5])}"

    # Edge: negative values
    assert majority_element([-1, -1, 2]) == -1, f"Negative: got {majority_element([-1, -1, 2])}"

    print("All tests passed.")


# solved: 2026-11-20, easy, 30min, Majority Element
