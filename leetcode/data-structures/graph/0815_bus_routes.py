"""
LeetCode 815: Bus Routes
https://leetcode.com/problems/bus-routes/

Problem: You are given an array routes representing bus routes where
routes[i] is a bus route that the i-th bus repeats forever. You start
at the bus stop source (not on any bus initially) and want to reach
the bus stop target. You can board a bus at stop x and ride it to any
stop y in the same route. Return the least number of buses you must
take to travel from source to target, or -1 if it is not possible.

Constraints:
- 1 <= routes.length <= 500
- 1 <= routes[i].length <= 10^5, sum of routes[i].length <= 10^5
- All values of routes[i] are unique
- 0 <= routes[i][j] < 10^6
- 0 <= source, target < 10^6

Examples:
- Input: routes = [[1,2,7],[3,6,7]], source = 1, target = 6
  Output: 2
  Explanation: board bus 0 at stop 1, ride to stop 7, then board bus 1
    to stop 6.

- Input: routes = [[7,12],[4,5,15],[6],[15,19],[9,12,13]],
  source = 15, target = 12
  Output: -1

Approach: Multi-source BFS over buses, not stops
- stop -> [bus ids] buckets; seed the queue with every bus through
  source (all at one boarding); boarded holds bus ids — re-boarding
  never helps, while stops may be revisited freely
- Boarding a bus unlocks its entire stop list at once; unvisited buses
  at those stops join the next level; target inside a boarded route
  returns the current level (boardings)
- Each bus is processed once and its stops scanned once -> O(sum route
  lengths)

Time: O(sum route lengths)   Space: O(sum route lengths)
"""

from collections import defaultdict, deque


def num_buses_to_destination(routes: list[list[int]], source: int, target: int) -> int:
    """
    Return the minimum number of buses to ride from source to target.

    Args:
        routes: routes[i] lists every stop the i-th bus visits forever
        source: Starting bus stop
        target: Destination bus stop

    Returns:
        Minimum number of buses boarded, 0 if source == target, -1 if
        the destination is unreachable
    """
    if source == target:
        return 0

    stop_routes = defaultdict(list[int])
    for bus_id, stops in enumerate(routes):
        for stop in stops:
            stop_routes[stop].append(bus_id)

    queue: deque[int] = deque(stop_routes[source])
    boarded: set[int] = set()
    boardings = 0
    while queue:
        boardings += 1
        for _ in range(len(queue)):
            bus = queue.popleft()
            if bus in boarded:
                continue
            boarded.add(bus)
            for stop in routes[bus]:
                if stop == target:
                    return boardings
                else:
                    queue.extend(b for b in stop_routes[stop] if b not in boarded)

    return -1


if __name__ == "__main__":
    # Example 1: one transfer
    result1 = num_buses_to_destination([[1, 2, 7], [3, 6, 7]], 1, 6)
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: unreachable
    result2 = num_buses_to_destination([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12)
    expected2 = -1
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: source equals target — no bus needed
    assert num_buses_to_destination([[1, 2, 7]], 7, 7) == 0, (
        f"Same stop: got {num_buses_to_destination([[1, 2, 7]], 7, 7)}"
    )

    # Edge: single route covers both ends
    assert num_buses_to_destination([[1, 2, 7]], 1, 7) == 1, (
        f"Direct: got {num_buses_to_destination([[1, 2, 7]], 1, 7)}"
    )

    # Edge: multiple buses through the same stop — still one boarding
    assert num_buses_to_destination([[1, 2], [2, 3], [1, 3]], 1, 3) == 1, (
        f"Shared stop: got {num_buses_to_destination([[1, 2], [2, 3], [1, 3]], 1, 3)}"
    )

    print("All tests passed.")


# solved: 2026-11-25, hard, 90min, Bus Routes
