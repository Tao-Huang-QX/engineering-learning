"""
LeetCode 1109: Corporate Flight Bookings
https://leetcode.com/problems/corporate-flight-bookings/

Problem: There are n flights labeled 1 to n. You are given an array of
flight bookings bookings, where bookings[i] = [first_i, last_i,
seats_i] represents a booking for flights first_i through last_i
(inclusive) with seats_i seats reserved for each flight in the range.
Return an array answer of length n, where answer[i] is the total number
of seats booked on flight i + 1.

Constraints:
- 1 <= n <= 2 * 10^4
- 1 <= bookings.length <= 2 * 10^4
- 1 <= first_i <= last_i <= n
- 1 <= seats_i <= 10^4

Examples:
- Input: bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
  Output: [10,55,45,25,25]
  Explanation: flight 1 has 10 seats; flight 2 has 10 + 20 + 25 = 55;
    flight 3 has 20 + 25 = 45; flights 4 and 5 have 25 each.

Approach: Difference array — boundaries only, then one prefix pass
- Per booking: delta[first - 1] += seats, delta[last] -= seats (exit
  gate one past the covered cell, hence delta sized n + 1)
- Running sum over the first n cells rebuilds the totals

Time: O(B + n)   Space: O(n)
"""


def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:
    """
    Return total reserved seats per flight from the range bookings.

    Args:
        bookings: Each [first, last, seats] adds `seats` to every
            flight numbered first through last, inclusive
        n: Number of flights, labeled 1 through n

    Returns:
        Length-n array where index i holds the total seats on flight
        i + 1
    """
    delta: list[int] = [0] * (n + 1)  # +1 slot: a booking ending at flight n needs its exit gate
    for first, last, seats in bookings:
        delta[first - 1] += seats  # 1-indexed first -> 0-indexed entry cell
        delta[last] -= seats  # exit fires at index `last`, one past the covered cell

    result: list[int] = []
    running = 0
    for i in range(n):
        running += delta[i]
        result.append(running)
    return result


if __name__ == "__main__":
    # Example: overlapping range bookings
    result1 = corp_flight_bookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5)
    expected1 = [10, 55, 45, 25, 25]
    assert result1 == expected1, f"Example: got {result1}, expected {expected1}"

    # Edge: single flight, single booking
    assert corp_flight_bookings([[1, 1, 5]], 1) == [5], (
        f"Single: got {corp_flight_bookings([[1, 1, 5]], 1)}"
    )

    # Edge: one booking covering every flight
    assert corp_flight_bookings([[1, 5, 3]], 5) == [3, 3, 3, 3, 3], (
        f"Cover-all: got {corp_flight_bookings([[1, 5, 3]], 5)}"
    )

    # Edge: disjoint bookings leave untouched flights at zero
    assert corp_flight_bookings([[1, 2, 10], [4, 4, 7]], 5) == [10, 10, 0, 7, 0], (
        f"Disjoint: got {corp_flight_bookings([[1, 2, 10], [4, 4, 7]], 5)}"
    )

    print("All tests passed.")


# solved: 2026-11-21, medium, 25min, Corporate Flight Bookings
