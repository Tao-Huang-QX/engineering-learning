"""
LeetCode 128: Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Problem: Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence. You must write an algorithm that runs in O(n) time.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Examples:
- Input: nums = [100, 4, 200, 1, 3, 2]
  Output: 4
  Explanation: The longest consecutive sequence is [1, 2, 3, 4]

- Input: nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
  Output: 9

Approach: HashSet with sequence-start detection
- Convert nums to a set for O(1) membership lookups
- Only start counting from a number that has no left neighbor (num - 1 not in set)
  — this guarantees each consecutive sequence is built exactly once, from its true start
- For each start, walk forward (num + 1, num + 2, ...) until the chain breaks
- Track the maximum count seen
- Despite the nested loop, each element enters the inner while loop at most once,
  so total work is O(n)

Time: O(n) — each number looked up at most ~3 times (set build, "is start?" check,
  and inner walk)
Space: O(n) — HashSet
"""


def longest_consecutive(nums: list[int]) -> int:
    """
    Return the length of the longest consecutive sequence.

    Args:
        nums: Unsorted array of integers

    Returns:
        Length of the longest consecutive elements sequence
    """
    unique_nums = set(nums)
    result = 0

    for num in unique_nums:
        left = num - 1

        if left not in unique_nums:
            cur = num
            count = 0

            while cur in unique_nums:
                cur += 1
                count += 1

            result = max(result, count)

    return result


if __name__ == "__main__":
    # Example 1
    result1 = longest_consecutive([100, 4, 200, 1, 3, 2])
    expected1 = 4
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])
    expected2 = 9
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
