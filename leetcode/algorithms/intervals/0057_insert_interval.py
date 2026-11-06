"""
LeetCode 57: Insert Interval
https://leetcode.com/problems/insert-interval/

Problem: You are given an array of non-overlapping intervals where intervals[i]
= [start_i, end_i] represent the start and end of the i-th interval. The
intervals are sorted by start_i. You are also given an interval newInterval =
[start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in
ascending order by start_i and intervals still does not have any overlapping
intervals (merge overlapping intervals if necessary). Return intervals after
the insertion.

Constraints:
- 0 <= intervals.length <= 10^4
- intervals[i].length == newInterval.length == 2
- 0 <= start <= end <= 10^5
- intervals are sorted ascending by start_i and non-overlapping

Examples:
- Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
  Output: [[1,5],[6,9]]

- Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
  Output: [[1,2],[3,10],[12,16]]
  Explanation: [4,8] overlaps [3,5], [6,7], [8,10] and absorbs them — note the
    boundary touch at 8 counts as overlap.

Approach: Three-phase single pass — the new interval is a first-class object
- Phase 1 copies everything ending strictly before it (end < its start)
- Phase 2 absorbs everything overlapping (start <= its end): pull the
  merged start DOWN with min and the end UP with max — start pullback is
  required when it begins before the first interval it touches
- Phase 2 then appends the new interval exactly once — overlapping or not,
  it can never vanish (the bug class where a mid-gap interval disappears)
- Phase 3 copies the tail; since phase 2 consumed all starts <= its end,
  everything remaining is strictly after
- Boundary touch merges by the guard pairing (strict < in phase 1,
  <= in phase 2); empty input / before / after / swallow-all all fall
  out of the phases, no special cases
- Mutates new_interval while absorbing (fine for the judge; copy to be pure)

Time: O(n)   Space: O(n)
"""


def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """
    Insert new_interval into the sorted non-overlapping intervals, merging as needed.

    Args:
        intervals: Sorted, non-overlapping [start, end] intervals
        new_interval: The [start, end] interval to insert

    Returns:
        Merged interval list, still sorted and non-overlapping
    """
    result: list[list[int]] = []
    i, n = 0, len(intervals)

    # Phase 1: everything strictly before the new interval (end < its start)
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: everything overlapping (start <= its end) - absorb into it
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])  # <-- the start pull back
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)  # first-class: always inserted exactly once

    # Phase 3: everything strictly after
    while i < n and new_interval[1] < intervals[i][0]:
        result.append(intervals[i])
        i += 1

    return result


if __name__ == "__main__":
    # Example 1
    result1 = insert([[1, 3], [6, 9]], [2, 5])
    expected1 = [[1, 5], [6, 9]]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: absorbs three intervals, boundary touch at 8 merges
    result2 = insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])
    expected2 = [[1, 2], [3, 10], [12, 16]]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: empty list
    result3 = insert([], [5, 7])
    expected3 = [[5, 7]]
    assert result3 == expected3, f"Empty: got {result3}, expected {expected3}"

    # Edge: entirely before / entirely after, no overlap
    result4 = insert([[3, 5], [8, 9]], [1, 2])
    expected4 = [[1, 2], [3, 5], [8, 9]]
    assert result4 == expected4, f"Before: got {result4}, expected {expected4}"

    result5 = insert([[3, 5], [8, 9]], [10, 12])
    expected5 = [[3, 5], [8, 9], [10, 12]]
    assert result5 == expected5, f"After: got {result5}, expected {expected5}"

    # Edge: the new interval swallows everything
    result6 = insert([[2, 3], [6, 7], [9, 10]], [1, 11])
    expected6 = [[1, 11]]
    assert result6 == expected6, f"Swallow all: got {result6}, expected {expected6}"

    # Edge: exact boundary adjacency merges ([1,3] + [3,5])
    result7 = insert([[1, 3], [6, 9]], [3, 5])
    expected7 = [[1, 5], [6, 9]]
    assert result7 == expected7, f"Boundary touch: got {result7}, expected {expected7}"

    # Edge: fits in a gap touching neither neighbor (must not vanish)
    result8 = insert([[16, 19], [38, 41]], [32, 34])
    expected8 = [[16, 19], [32, 34], [38, 41]]
    assert result8 == expected8, f"Mid-gap: got {result8}, expected {expected8}"

    # Edge: starts before the first interval and overlaps it (start must pull back)
    result9 = insert([[3, 5], [6, 9]], [1, 4])
    expected9 = [[1, 5], [6, 9]]
    assert result9 == expected9, f"Start pullback: got {result9}, expected {expected9}"

    print("All tests passed.")


# solved: 2026-11-06, medium, min, Insert Interval
