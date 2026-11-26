"""
LeetCode 973: K Closest Points to Origin
https://leetcode.com/problems/k-closest-points-to-origin/

Problem: Given an array of points where points[i] = [xi, yi]
represents a point on the X-Y plane and an integer k, return the k
closest points to the origin (0, 0). The distance is the Euclidean
distance. You may return the answer in any order; the answer is
guaranteed to be unique except for its order.

Constraints:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

Examples:
- Input: points = [[1,3],[-2,2]], k = 1
  Output: [[-2,2]]
  Explanation: squared distances are 1 + 9 = 10 and 4 + 4 = 8; the
    closer point is (-2,2).

- Input: points = [[3,3],[5,-1],[-2,4]], k = 2
  Output: [[3,3],[-2,4]]   (any order is accepted)

Approach: Size-k max-heap via inverted __lt__
- Candidate caches d2 = x^2 + y^2 once; __lt__ inverted (self.d2 >
  other.d2) so heapq's root is the FARTHEST kept — evictions discard
  the worst, never the wanted
- Seed pushes while len(heap) < k, then heapreplace only when a
  newcomer beats the root; the < gate sets the capacity invariant —
  <= would seed k+1 and heapreplace cements it forever

Time: O(n log k)   Space: O(k)
"""

import heapq


class Candidate:
    def __init__(self, point: list[int]) -> None:
        self.point: list[int] = point
        self.d2: int = point[0] * point[0] + point[1] * point[1]

    def __lt__(self, other: "Candidate"):
        return self.d2 > other.d2


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Return the k points closest to the origin.

    Args:
        points: List of [x, y] coordinate pairs
        k: How many of the closest points to return (1 <= k <= len)

    Returns:
        The k closest points in any order
    """
    heap: list[Candidate] = []
    for point in points:
        c = Candidate(point)
        if len(heap) < k:
            heapq.heappush(heap, c)
        elif c.d2 < heap[0].d2:
            heapq.heapreplace(heap, c)
    return [c.point for c in heap]


if __name__ == "__main__":

    def dist2(p: list[int]) -> int:
        return p[0] * p[0] + p[1] * p[1]

    # Example 1: single closest point
    result1 = k_closest([[1, 3], [-2, 2]], 1)
    assert result1 == [[-2, 2]], f"Example 1: got {result1}"

    # Example 2: two closest, any order
    result2 = sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2))
    assert result2 == sorted([[3, 3], [-2, 4]]), f"Example 2: got {result2}"

    # Edge: k equals the length — everything comes back
    result3 = k_closest([[1, 1], [2, 2], [3, 3]], 3)
    assert sorted(result3) == [[1, 1], [2, 2], [3, 3]], f"K=len: got {result3}"

    # Edge: distance ties — pick any k=2 of the three by squared distance
    result4 = k_closest([[0, 0], [1, 1], [-1, -1]], 2)
    assert sorted(map(dist2, result4)) == [0, 2], f"Ties: got {result4}"

    # Edge: duplicate points both belong in the answer
    result5 = k_closest([[2, 2], [2, 2], [5, 5]], 2)
    assert sorted(result5) == [[2, 2], [2, 2]], f"Dups: got {result5}"

    # Edge: origin itself is trivially closest
    result6 = k_closest([[5, 5], [0, 0]], 1)
    assert result6 == [[0, 0]], f"Origin: got {result6}"

    print("All tests passed.")


# solved: 2026-11-26, medium, 30min, K Closest Points to Origin
