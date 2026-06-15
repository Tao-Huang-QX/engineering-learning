"""
LeetCode 167: Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Problem: Given a 1-indexed array sorted in ascending order, find two numbers that add up to a target.

Approach: Two pointers (greedy)
- Start with left=0, right=len-1 (widest range)
- If sum < target: move left right (need larger sum)
- If sum > target: move right left (need smaller sum or either if equal)

Time: O(n)   Space: O(1)
"""


def two_sum(numbers: list[int], target: int) -> list[int]:  # pyright: ignore[reportReturnType]
    """
    Return the 1-indexed positions of two numbers that add up to target.

    Args:
        numbers: 1-indexed array sorted in non-decreasing order
        target: Target sum

    Returns:
        List of two 1-indexed positions whose values sum to target
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1


if __name__ == "__main__":
    # Example 1
    assert two_sum([2, 7, 11, 15], 9) == [1, 2]

    # Example 2
    assert two_sum([2, 3, 4], 6) == [1, 3]

    # Example 3
    assert two_sum([-1, 0], -1) == [1, 2]

    print("All tests passed!")
