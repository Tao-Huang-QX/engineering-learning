"""
LeetCode 480: Sliding Window Median
https://leetcode.com/problems/sliding-window-median/

Problem: The median is the middle value in an ordered integer list. If the
size of the list is even, there is no middle value. So the median is the mean
of the two middle values.

Given an integer array nums and an integer k, return the median of each
window of size k as it slides from left to right across nums.

Constraints:
- 1 <= k <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1

Examples:
- Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
  Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
  Window position                Median
  ---------------                ------
  [1  3  -1] -3  5  3  6  7       1
   1 [3  -1  -3] 5  3  6  7      -1
   1  3 [-1  -3  5] 3  6  7      -1
   1  3  -1 [-3  5  3] 6  7       3
   1  3  -1  -3 [5  3  6] 7       5
   1  3  -1  -3  5 [3  6  7]      6

- Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
  Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]

Approach: Two heaps with lazy deletion
- lo (max-heap via negated values): smaller half; hi (min-heap): larger half
- Invariant: lo_size == hi_size (even k) or lo_size == hi_size + 1 (odd k)
- Median: max of lo (odd) or average of both tops (even)
- Lazy deletion: on remove, mark value in delayed counter — cannot O(log k)
  delete from heap middle; let stale values surface to top, then prune
- Track effective sizes (lo_size, hi_size) separately — len() counts stale
  entries, balance() must use effective counts or rebalancing stalls
- Each element pushed once, popped once across all slides

Time: O(n log k) — each of n elements enters/leaves heaps once
Space: O(k) — heaps + delayed map
"""

import heapq


def median_sliding_window(nums: list[int], k: int) -> list[float]:
    """
    Return the median of each sliding window of size k.

    Two-heap approach with lazy deletion.
    - lo: max-heap (negated values) stores the smaller half
    - hi: min-heap stores the larger half
    - Invariant: len(lo) == len(hi) or len(low) == len(hi) + 1
    - Median: top of lo (odd k) or average of both tops (even k)
    - Lazy deletion: count removals in a hashmap, prune tops when stale

    Args:
        nums: Array of integers
        k: Size of the sliding window

    Returns:
        List of medians for each window position
    """
    lo: list[int] = []  # max-heap of negated values
    hi: list[int] = []  # min-heap
    lo_size = 0  # effective count in lo
    hi_size = 0  # effective count in hi
    delayed: dict[int, int] = {}  # value → pending lazy removals

    def prune_lo() -> None:
        while lo and delayed.get(-lo[0], 0) > 0:
            val = -heapq.heappop(lo)
            delayed[val] -= 1
            if delayed[val] == 0:
                del delayed[val]

    def prune_hi() -> None:
        while hi and delayed.get(hi[0], 0) > 0:
            val = heapq.heappop(hi)
            delayed[val] -= 1
            if delayed[val] == 0:
                del delayed[val]

    def balance() -> None:
        nonlocal lo_size, hi_size
        if lo_size > hi_size + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
            lo_size -= 1
            hi_size += 1
            prune_lo()
        elif hi_size > lo_size:
            heapq.heappush(lo, -heapq.heappop(hi))
            hi_size -= 1
            lo_size += 1
            prune_hi()

    def add(val: int) -> None:
        nonlocal lo_size, hi_size
        prune_lo()
        if not lo or val <= -lo[0]:
            heapq.heappush(lo, -val)
            lo_size += 1
        else:
            heapq.heappush(hi, val)
            hi_size += 1
        balance()

    def remove(val: int) -> None:
        nonlocal lo_size, hi_size
        delayed[val] = delayed.get(val, 0) + 1
        if lo and val <= -lo[0]:
            lo_size -= 1
        else:
            hi_size -= 1
        prune_lo()
        prune_hi()
        balance()

    def get_median() -> float:
        prune_lo()
        prune_hi()
        if k % 2 == 1:
            return float(-lo[0])
        else:
            return (-lo[0] + hi[0]) / 2.0

    result: list[float] = []
    for i in range(k):
        add(nums[i])
    result.append(get_median())

    for i in range(k, len(nums)):
        remove(nums[i - k])
        add(nums[i])
        result.append(get_median())

    return result


if __name__ == "__main__":
    # Example 1
    result = median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)
    expected = [1.00000, -1.00000, -1.00000, 3.00000, 5.00000, 6.00000]
    assert result == expected, f"Example 1 failed: got {result}, expected {expected}"

    # Example 2
    result = median_sliding_window([1, 2, 3, 4, 2, 3, 1, 4, 2], 3)
    expected = [2.00000, 3.00000, 3.00000, 3.00000, 2.00000, 3.00000, 2.00000]
    assert result == expected, f"Example 2 failed: got {result}, expected {expected}"

    print("All tests passed.")
