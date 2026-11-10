"""
LeetCode 295: Find Median from Data Stream
https://leetcode.com/problems/find-median-from-data-stream/

Problem: The median is the middle value in an ordered integer list. If the
size of the list is even, there is no middle value, and the median is the
mean of the two middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the object
- add_num(num) adds an integer from the data stream to the structure
- find_median() returns the median of all elements so far

Examples:
- Input: ["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
        [[],[1],[2],[],[3],[]]
  Output: [null, null, null, 1.5, null, 2.0]
  Explanation: after 1,2 -> median (1+2)/2 = 1.5; after 1,2,3 -> median 2.

Constraints:
- -10^5 <= num <= 10^5
- At most 10^4 calls to add_num and find_median
- If the count is even, the median is the mean of the two middle values

Follow-up: If all integers are in [0, 100], could you do it with a fixed
array? With a count array / bucket approach?

Approach: Two heaps — max-heap low (smaller half), min-heap high (larger half)
- Invariant: max(low) <= min(high); low holds the extra when odd
- Insert routes by the LOW top only (if/else, never a second peek —
  a gap value matching neither peek condition was silently dropped)
- Rebalance each insert: sizes within one, low the bigger side
- Follow-up [0,100]: 101-slot count array — add O(1), median O(V) walk

Time: add O(log n), median O(1)   Space: O(n)
"""

import heapq


class MedianFinder:
    def __init__(self) -> None:
        """
        Initialize the two-heap structure.
        """
        # low: max heap, high: min heap
        self.low: list[int] = []
        self.high: list[int] = []

    def add_num(self, num: int) -> None:
        """
        Add an integer from the stream.

        Args:
            num: Integer in [-10^5, 10^5]
        """
        if not self.low or num <= -self.low[0]:
            heapq.heappush(self.low, -num)
        else:
            heapq.heappush(self.high, num)

        # rebalance if not even or low is longer than high by more than 1
        if len(self.low) < len(self.high):
            heapq.heappush(self.low, -heapq.heappop(self.high))
        elif len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))

    def find_median(self) -> float:
        """
        Return the median of all added numbers.

        Returns:
            Median as a float (mean of the two middles when count is even)
        """
        result: float = 0

        if (len(self.low) + len(self.high)) % 2 == 1:
            result = -float(self.low[0])
        else:
            result = (-self.low[0] + self.high[0]) / 2

        return result


if __name__ == "__main__":
    # Example walkthrough
    finder = MedianFinder()
    finder.add_num(1)
    finder.add_num(2)
    result1 = finder.find_median()
    expected1 = 1.5
    assert result1 == expected1, f"Steps 1-2: got {result1}, expected {expected1}"

    finder.add_num(3)
    result2 = finder.find_median()
    expected2 = 2.0
    assert result2 == expected2, f"Step 3: got {result2}, expected {expected2}"

    # Edge: single element
    solo = MedianFinder()
    solo.add_num(7)
    assert solo.find_median() == 7.0, f"Single: got {solo.find_median()}"

    # Edge: running stream with alternating parity — medians after each add
    stream = [5, 15, 1, 3, 2, 8, 7, 9, 10, 6, 11, 4]
    runner = MedianFinder()
    for i, num in enumerate(stream):
        runner.add_num(num)
        got = runner.find_median()
        window = sorted(stream[: i + 1])
        n = i + 1
        exp = float(window[n // 2]) if n % 2 else (window[n // 2 - 1] + window[n // 2]) / 2
        assert got == exp, f"after add {num} (step {n}): got {got}, expected {exp}"

    # Edge: negatives and duplicates
    dup = MedianFinder()
    for v in (-1, -1, 0, 2, 2, 2):
        dup.add_num(v)
    assert dup.find_median() == 1.0, f"Dup/negatives: got {dup.find_median()}, expected 1.0"

    print("All tests passed.")


# solved: 2026-11-10, hard, 50min, Find Median from Data Stream
