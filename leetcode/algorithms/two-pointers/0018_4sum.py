"""
LeetCode 18: 4Sum
https://leetcode.com/problems/4sum/

Problem: Given an array nums of n integers and a target, return all unique
quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
- 0 <= a, b, c, d < n
- a, b, c, and d are distinct
- nums[a] + nums[b] + nums[c] + nums[d] == target

Approach: Two pointers + dedupe
- Sort array first
- Fix two elements, use two pointers for remaining two
- Skip duplicates at each level (a, b, left, right)

Time: O(n³)   Space: O(1)
"""


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    Return all unique quadruplets that sum to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List of unique quadruplets that sum to target
    """
    nums.sort()
    result = []

    for a in range(len(nums) - 3):
        if a > 0 and nums[a] == nums[a - 1]:
            continue

        for b in range(a + 1, len(nums) - 2):
            if b > a + 1 and nums[b] == nums[b - 1]:
                continue

            left, right = b + 1, len(nums) - 1
            while left < right:
                curr = nums[a] + nums[b] + nums[left] + nums[right]

                if curr == target:
                    result.append([nums[a], nums[b], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif curr < target:
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                else:
                    right -= 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (nums, target, expected_quadruplets)
        (
            [1, 0, -1, 0, -2, 2],
            0,
            [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
        ),
        ([2, 2, 2, 2, 2], 8, [[2, 2, 2, 2]]),
    ]

    for nums, target, expected in test_cases:
        result = four_sum(nums, target)
        # Sort for comparison (order may vary)
        result_sorted = sorted([sorted(q) for q in result])
        expected_sorted = sorted([sorted(q) for q in expected])
        assert result_sorted == expected_sorted, (
            f"nums={nums}, target={target}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, 4Sum
