"""
LeetCode 56: Merge Intervals
https://leetcode.com/problems/merge-intervals/

Problem: Given an array of intervals where intervals[i] = [start_i, end_i], merge all
overlapping intervals, and return an array of non-overlapping intervals that cover
all the intervals in the input.

Constraints:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4

Examples:
- Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
  Output: [[1,6],[8,10],[15,18]]
  Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

- Input: intervals = [[1,4],[4,5]]
  Output: [[1,5]]
  Explanation: Intervals [1,4] and [4,5] are considered overlapping (touching at 4).

Approach: Sort + greedy merge
- Sort intervals by start — overlapping intervals become adjacent
- Single pass: if current overlaps the last merged interval (start <= last_end),
  extend last_end to max(last_end, current_end); otherwise, start a new interval
- Touching at a point (e.g., [1,4] + [4,5]) counts as overlap

Time: O(n log n) — sorting dominates
Space: O(n) — result array
"""


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge all overlapping intervals and return non-overlapping intervals.

    Args:
        intervals: List of intervals [start_i, end_i]

    Returns:
        List of merged non-overlapping intervals
    """
    intervals.sort()
    result: list[list[int]] = []

    for s, e in intervals:
        if result and s <= result[-1][1]:
            result[-1][1] = max(result[-1][1], e)
        else:
            result.append([s, e])

    return result


if __name__ == "__main__":
    # Example 1
    result1 = merge([[1, 3], [2, 6], [8, 10], [15, 18]])
    expected1 = [[1, 6], [8, 10], [15, 18]]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = merge([[1, 4], [4, 5]])
    expected2 = [[1, 5]]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
