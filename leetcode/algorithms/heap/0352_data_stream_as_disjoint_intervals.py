"""
LeetCode 352: Data Stream as Disjoint Intervals
https://leetcode.com/problems/data-stream-as-disjoint-intervals/

Problem: Given a data stream input of non-negative integers a1, a2, ..., an,
summarize the numbers seen so far as a list of disjoint intervals.

Implement the SummaryRanges class:
- SummaryRanges() Initializes the object with an empty stream.
- void addNum(int value) Adds the integer value to the stream.
- int[][] getIntervals() Returns a summary of the integers in the stream
  currently as a list of disjoint intervals [start_i, end_i].
  The answer should be sorted by start_i.

Constraints:
- 0 <= value <= 10^4
- At most 3 * 10^4 calls will be made to addNum and getIntervals.
- At most 10^2 calls will be made to getIntervals.

Follow up: What if there are lots of merges and the number of disjoint
intervals is small compared to the data stream's size?

Examples:
- Input:
    ["SummaryRanges", "addNum", "getIntervals", "addNum", "getIntervals",
     "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals"]
    [[], [1], [], [3], [], [7], [], [2], [], [6], []]
  Output:
    [null, null, [[1, 1]], null, [[1, 1], [3, 3]], null, [[1, 1], [3, 3], [7, 7]],
     null, [[1, 3], [7, 7]], null, [[1, 3], [6, 7]]]

Approach: Min-heap with lazy dedup + on-demand interval merge
- addNum: push (value, value) as 1-length interval to min-heap; use seen set
  for O(1) dedup — O(log n) per call
- getIntervals: drain all intervals from heap, merge overlapping/adjacent
  intervals (if start <= last_end + 1, extend; else start new), push merged
  intervals back — O(n log n) per call
- "Lots of merges, few intervals" follow-up: store intervals directly in heap
  rather than individual values — space is O(num_intervals) not O(num_values)
- Lazy evaluation: getIntervals is called rarely (≤100) vs addNum (≤30k)

Time: addNum O(log n), getIntervals O(n log n) where n = unique intervals
Space: O(k) where k = number of disjoint intervals
"""

import heapq

"""
class SummaryRanges:
    def __init__(self) -> None:
        self.heap = []  # min-heap of values + interval endpoints
        self.seen: set[int] = set()  # active values in heap (dedup + lazy delete)

    def add_num(self, value: int) -> None:
        # Push value to the heap; skip if already tracked.
        if value not in self.seen:
            self.seen.add(value)
            heapq.heappush(self.heap, value)

    def get_intervals(self) -> list[list[int]]:
        # 1. Drain all values, skip stale entries
        values: list[int] = []
        while self.heap:
            val = heapq.heappop(self.heap)
            self.seen.remove(val)
            values.append(val)

        if not values:
            return []

        # 2. Merge consecutive values into intervals
        intervals: list[list[int]] = []
        for val in values:
            if intervals and val == intervals[-1][1] + 1:
                intervals[-1][1] = val  # extend current interval
            else:
                intervals.append([val, val])  # start new interval

        # 3. Push only endpoints back - future addNum's land between them
        for start, end in intervals:
            for v in range(start, end + 1):
                heapq.heappush(self.heap, v)
                self.seen.add(v)

        return intervals
"""


class SummaryRanges:
    """A data structure that tracks a stream of integers and returns disjoint intervals."""

    def __init__(self) -> None:
        self.heap: list[tuple[int, int]] = []  # (start, end) intervals
        self.seen: set[tuple[int, int]] = set()

    def add_num(self, value: int) -> None:
        """
        Add a value to the data stream.

        Args:
            value: Non-negative integer to add to the stream

        Returns:
            None
        """
        interval = (value, value)
        if interval not in self.seen:
            self.seen.add(interval)
            heapq.heappush(self.heap, interval)

    def get_intervals(self) -> list[list[int]]:
        """
        Return disjoint intervals sorted by start.

        Args:
            None

        Returns:
            List of disjoint intervals [start_i, end_i] sorted by start_i
        """
        # Drain all intervals
        intervals: list[tuple[int, int]] = []
        while self.heap:
            iv = heapq.heappop(self.heap)
            self.seen.remove(iv)
            intervals.append(iv)

        if not intervals:
            return []

        # Merge: sorted by start (heap drain order), merge if start <= last_end + 1
        merged: list[list[int]] = []
        for start, end in intervals:
            if merged and start <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])

        # Push merged intervals back
        for s, e in merged:
            iv = (s, e)
            heapq.heappush(self.heap, iv)
            self.seen.add(iv)

        return merged


if __name__ == "__main__":
    # Example from problem statement
    sr = SummaryRanges()
    sr.add_num(1)
    assert sr.get_intervals() == [[1, 1]], f"After addNum(1): got {sr.get_intervals()}"
    sr.add_num(3)
    assert sr.get_intervals() == [[1, 1], [3, 3]], f"After addNum(3): got {sr.get_intervals()}"
    sr.add_num(7)
    assert sr.get_intervals() == [[1, 1], [3, 3], [7, 7]], (
        f"After addNum(7): got {sr.get_intervals()}"
    )
    sr.add_num(2)
    assert sr.get_intervals() == [[1, 3], [7, 7]], f"After addNum(2): got {sr.get_intervals()}"
    sr.add_num(6)
    assert sr.get_intervals() == [[1, 3], [6, 7]], f"After addNum(6): got {sr.get_intervals()}"

    # Edge: empty stream
    sr2 = SummaryRanges()
    assert sr2.get_intervals() == [], f"Empty stream: got {sr2.get_intervals()}"

    # Edge: duplicate values
    sr3 = SummaryRanges()
    sr3.add_num(1)
    sr3.add_num(1)
    assert sr3.get_intervals() == [[1, 1]], f"Duplicate: got {sr3.get_intervals()}"

    print("All tests passed.")
