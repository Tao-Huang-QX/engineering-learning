"""
LeetCode 15: 3Sum
https://leetcode.com/problems/3sum/

Problem: Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Approach:
- sort the array to enable two-pointer technique
- if sum is less than 0, move left pointer to increase sum
- if sum is greater than 0, move right pointer to decrease sum

Time: O(n^2)   Space: O(1) (not counting output space)
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Return all unique triplets that sum to zero.

    Args:
        nums: List of integers

    Returns:
        List of triplets (each triplet is a list of 3 integers)
    """
    nums.sort()
    results = []
    for i in range(len(nums) - 2):  # Reserve last two for left and right pointers
        # Skip duplicate values for the first element of the triplet
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                results.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1

                # Skip duplicate values for the second and third elements of the triplet
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
    return results


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_output)
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),  # No triplets sum to 0
        ([0, 0, 0, 0], [[0, 0, 0]]),  # All zeros
        ([], []),  # Empty array
        ([0], []),  # Single element
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
    ]

    for nums, expected in test_cases:
        result = three_sum(nums)
        # Sort for comparison (order of triplets and elements within triplets doesn't matter)
        result_sorted = sorted([sorted(t) for t in result])
        expected_sorted = sorted([sorted(t) for t in expected])
        assert result_sorted == expected_sorted, f"{nums}: got {result}, expected {expected}"

    print("All tests passed.")
