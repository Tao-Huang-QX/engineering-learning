"""
LeetCode 560: Subarray Sum Equals K
https://leetcode.com/problems/subarray-sum-equals-k/

Problem: Given an array of integers nums and an integer k, return the total
number of contiguous subarrays whose sum equals k.

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Examples:
- Input: nums = [1,1,1], k = 2
  Output: 2
  Explanation: [1,1] found at positions 0-1 and 1-2.

- Input: nums = [1,2,3], k = 3
  Output: 2
  Explanation: [1,2] and [3].

Approach: Prefix sums + hash map — Two Sum's complement trick on prefixes
- Identity: sum(nums[i+1..j]) = prefix(j) - prefix(i), so a subarray
  ending at j sums to k iff some EARLIER prefix equals running - k
- The map holds prefix_sum -> COUNT of prefixes with that value; at each
  position the lookup answers "how many earlier prefixes pair with me",
  each being one distinct subarray ending here
- Seed {0: 1} — the empty prefix (COUNT one, not zero); without it,
  subarrays starting at index 0 are invisible when running == k
- Order matters: lookup BEFORE inserting the current running — reversed,
  k=0 lets the current prefix match itself and counts zero-length
  subarrays (same read-before-write family as Candy's max-merge)
- Negatives are why sliding window fails: sums are non-monotone, so
  growing/shrinking the window can't decide when to stop — the map
  handles any sign mix in one pass

Time: O(n)   Space: O(n)
"""


def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count contiguous subarrays whose elements sum to k.

    Args:
        nums: Array of integers (negatives allowed)
        k: Target sum

    Returns:
        Number of contiguous subarrays summing to k
    """
    prefix_count: dict[int, int] = {0: 1}  # empty prefix - make whole-prefix matches visible
    running = 0
    result = 0
    for num in nums:
        running += num
        # Every earlier prefix with value running - k pairs with us
        result += prefix_count.get(running - k, 0)
        # Record the CURRENT prefix only after the lookup (k=0 selft-match guard)
        prefix_count[running] = prefix_count.get(running, 0) + 1
    return result


if __name__ == "__main__":
    # Example 1
    result1 = subarray_sum([1, 1, 1], 2)
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = subarray_sum([1, 2, 3], 3)
    expected2 = 2
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: negatives — the reason sliding window fails here
    result3 = subarray_sum([1, -1, 1, -1], 0)
    expected3 = 4
    assert result3 == expected3, f"Negatives: got {result3}, expected {expected3}"

    # Edge: whole array is one match
    result4 = subarray_sum([2, 3], 5)
    expected4 = 1
    assert result4 == expected4, f"Whole array: got {result4}, expected {expected4}"

    # Edge: single element equal to k
    result5 = subarray_sum([7], 7)
    expected5 = 1
    assert result5 == expected5, f"Single: got {result5}, expected {expected5}"

    # Edge: no match at all
    result6 = subarray_sum([1, 2, 3], 100)
    expected6 = 0
    assert result6 == expected6, f"No match: got {result6}, expected {expected6}"

    # Edge: multiple matches from repeated prefix sums
    result7 = subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7)
    expected7 = 4
    assert result7 == expected7, f"Classic: got {result7}, expected {expected7}"

    print("All tests passed.")


# solved: 2026-11-07, medium, 30min, Subarray Sum Equals K
