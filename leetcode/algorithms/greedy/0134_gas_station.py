"""
LeetCode 134: Gas Station
https://leetcode.com/problems/gas-station/

Problem: There are n gas stations along a circular route, where the
amount of gas at the i-th station is gas[i]. You have a car with an
unlimited gas tank and it costs cost[i] of gas to travel from the i-th
station to its next (i + 1)-th station. You begin the journey with an
empty tank at one of the gas stations. Given two integer arrays gas and
cost, return the starting gas station's index if you can travel around
the circuit once in the clockwise direction, otherwise return -1. If
there exists a solution, it is guaranteed to be unique.

Constraints:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4
- The input is generated such that the answer is unique

Examples:
- Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
  Output: 3
  Explanation: Starting at station 3 (index 3): fill 4, travel to 4
    (tank = 4 - 1 + 5 = 8), travel to 0 (tank = 8 - 2 + 1 = 7), travel
    to 1 (tank = 7 - 3 + 2 = 6), travel to 2 (tank = 6 - 4 + 3 = 5),
    travel to 3 (tank = 5 - 5 = 0). The tank never drops below 0.

- Input: gas = [2,3,4], cost = [3,4,3]
  Output: -1
  Explanation: You can't start at station 0 or 1 (not enough gas to
    reach the next station). Starting at 2: tank = 4 - 3 = 1 at station
    0, then 1 - 3 = -2 at station 1 — short by 1 no matter the start.

Approach: Greedy single pass — running total for feasibility, tank jump for location
- delta feeds two accumulators: total (circle sum — negative is the only
  failure mode, no start can work) and tank (prefix from the candidate)
- On a negative tank, jump start = station + 1 and reset tank — every
  start in the dead stretch dies on that same negative prefix (the
  dropped head ran >= 0); the survivor's wrap closes since total >= 0

Time: O(n)   Space: O(1)
"""


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    """
    Return the starting station index that completes the circuit.

    Args:
        gas: Gas available at each station along the circular route
        cost: Gas needed to travel from station i to station i + 1

    Returns:
        The unique valid starting index, or -1 if the circuit is
        impossible from any start
    """
    total = tank = 0
    start = 0
    for station in range(len(gas)):
        delta = gas[station] - cost[station]
        total += delta
        tank += delta
        if tank < 0:
            start = station + 1
            tank = 0
    return start if total >= 0 else -1


if __name__ == "__main__":
    # Example 1: unique answer is station 3
    result1 = can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    expected1 = 3
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: total gas (9) < total cost (10) — impossible
    result2 = can_complete_circuit([2, 3, 4], [3, 4, 3])
    expected2 = -1
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: single station, doable and not doable
    assert can_complete_circuit([5], [4]) == 0, f"Single ok: got {can_complete_circuit([5], [4])}"
    assert can_complete_circuit([4], [5]) == -1, (
        f"Single fail: got {can_complete_circuit([4], [5])}"
    )

    # Edge: start at index 0 works
    assert can_complete_circuit([1, 2], [1, 2]) == 0, (
        f"Start 0: got {can_complete_circuit([1, 2], [1, 2])}"
    )

    # Edge: zero gas and zero cost everywhere — any start works, unique answer is 0
    assert can_complete_circuit([0, 0, 0], [0, 0, 0]) == 0, (
        f"All zeros: got {can_complete_circuit([0, 0, 0], [0, 0, 0])}"
    )

    print("All tests passed.")


# solved: 2026-11-17, medium, 60min, Gas Station
