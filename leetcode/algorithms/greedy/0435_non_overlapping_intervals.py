"""
LeetCode 435: Non-overlapping Intervals
https://leetcode.com/problems/non-overlapping-intervals/

Problem: Given an array of intervals intervals where intervals[i] =
[start_i, end_i], return the minimum number of intervals you need to
remove to make the rest of the intervals non-overlapping. Intervals
that only touch at a point are non-overlapping — [1, 2] and [2, 3]
do not overlap.

Constraints:
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2
- -5 * 10^4 <= start_i < end_i <= 5 * 10^4

Examples:
- Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
  Output: 1
  Explanation: [1,3] can be removed and the rest are non-overlapping.

- Input: intervals = [[1,2],[1,2],[1,2]]
  Output: 2
  Explanation: You need to remove two of the three intervals.

- Input: intervals = [[1,2],[2,3]]
  Output: 0
  Explanation: Already non-overlapping (touching doesn't count).

Approach: Greedy interval scheduling — minimize removals = maximize keeps
- removals = n - kept_max; kept_max is classic activity selection: sort
  by END (same-end intervals always overlap each other, so tie order is
  irrelevant), sweep and keep every interval with start >= last kept end
  (>= : touching endpoints are legal)
- On overlap drop the CURRENT one — the kept interval's end is <= the
  current end by sort order, so it leaves more room for the future

Time: O(n log n)   Space: O(n) sorted copy (O(1) extra sorting in place)
"""


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    Return the minimum number of intervals to remove so none overlap.

    Args:
        intervals: List of [start, end] pairs (start < end guaranteed)

    Returns:
        Minimum removal count so the remaining intervals pairwise
        non-overlap (touching endpoints allowed)
    """
    ordered = sorted(intervals, key=lambda iv: iv[1])  # sort by end

    kept = 0
    last_end = float("-inf")
    for start, end in ordered:
        if start >= last_end:  # >=: touching endpoints are legal
            kept += 1
            last_end = end
        # else: overlap - drop THIS one, keep last_end where it is
    return len(intervals) - kept


if __name__ == "__main__":
    # Example 1: remove [1,3]
    result1 = erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]])
    expected1 = 1
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: three identical — remove two
    result2 = erase_overlap_intervals([[1, 2], [1, 2], [1, 2]])
    expected2 = 2
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3: touching endpoints are non-overlapping
    result3 = erase_overlap_intervals([[1, 2], [2, 3]])
    expected3 = 0
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    # Edge: single interval — nothing to remove
    assert erase_overlap_intervals([[5, 7]]) == 0, (
        f"Single: got {erase_overlap_intervals([[5, 7]])}"
    )

    # Edge: one fat interval swallowing three thin ones — keep the thin
    assert erase_overlap_intervals([[1, 10], [2, 3], [4, 5], [6, 7]]) == 1, (
        f"Nested: got {erase_overlap_intervals([[1, 10], [2, 3], [4, 5], [6, 7]])}"
    )

    # Edge: unsorted input
    assert erase_overlap_intervals([[3, 4], [1, 2], [2, 3]]) == 0, (
        f"Unsorted: got {erase_overlap_intervals([[3, 4], [1, 2], [2, 3]])}"
    )

    # Edge: negative bounds
    assert erase_overlap_intervals([[-5, -1], [-3, 2], [2, 4]]) == 1, (
        f"Negatives: got {erase_overlap_intervals([[-5, -1], [-3, 2], [2, 4]])}"
    )

    print("All tests passed.")


# solved: 2026-11-18, medium, 35min, Non-overlapping Intervals
