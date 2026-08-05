"""
LeetCode 239: Sliding Window Maximum
https://leetcode.com/problems/sliding-window-maximum/

Problem: You are given an array of integers nums, there is a sliding window of size
k which is moving from the very left of the array to the very right. You can only
see the k numbers in the window. Each time the sliding window moves right by one
position. Return the max sliding window.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

Examples:
- Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
  Output: [3,3,5,5,6,7]
  Explanation:
    Window position                Max
    ---------------                ---
    [1  3  -1] -3  5  3  6  7       3
     1 [3  -1  -3] 5  3  6  7       3
     1  3 [-1  -3  5] 3  6  7       5
     1  3  -1 [-3  5  3] 6  7       5
     1  3  -1  -3 [5  3  6] 7       6
     1  3  -1  -3  5 [3  6  7]      7

- Input: nums = [1], k = 1
  Output: [1]

Approach: Monotonic deque (indices, values descending)
- Deque stores indices; their values are strictly decreasing
- On each new element: pop right while deque's values <= current —
  smaller values are permanently dominated and can never be the max
- Pop left when the front index exits the window (index <= i - k)
- After forming the first full window, deque[0] is the max for that window
- Each index enters and leaves the deque exactly once

Time: O(n) — amortized O(1) per element
Space: O(k) — deque holds at most k indices
"""

from collections import deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Return the maximum value in each sliding window of size k.

    Args:
        nums: Array of integers
        k: Size of the sliding window

    Returns:
        List of maximums for each window position
    """
    queue: deque[int] = deque()  # indices, values descending
    result: list[int] = []

    for i in range(len(nums)):
        # 1. Pop right: discard indices whose value <= current
        while queue and nums[queue[-1]] <= nums[i]:
            queue.pop()
        queue.append(i)

        # 2. Pop left: remove index that fell out of the window
        if queue[0] <= i - k:
            queue.popleft()

        # 3. Output: once the first window is formed
        if i >= k - 1:
            result.append(nums[queue[0]])

    return result


if __name__ == "__main__":
    # Example 1
    result1 = max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)
    expected1 = [3, 3, 5, 5, 6, 7]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = max_sliding_window([1], 1)
    expected2 = [1]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
