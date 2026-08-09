"""
LeetCode 1011: Capacity To Ship Packages Within D Days
https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/

Problem: A conveyor belt has packages that must be shipped from one port to another
within days days. The ith package has a weight of weights[i]. Each day, we load the
ship with packages on the conveyor belt (in the order given by weights). We may not
load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages
on the conveyor belt being shipped within days days.

Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500

Examples:
- Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
  Output: 15
  Explanation: Ship capacity 15 is the minimum to ship in 5 days.
    Day 1: 1 + 2 + 3 + 4 + 5 = 15
    Day 2: 6 + 7 = 13
    Day 3: 8 = 8
    Day 4: 9 = 9
    Day 5: 10 = 10

- Input: weights = [3,2,2,4,1,4], days = 3
  Output: 6
  Explanation: Ship capacity 6 is the minimum to ship in 3 days.
    Day 1: 3 + 2 + 1 = 6   (or 3 + 2 = 5)
    Day 2: 2 + 4 = 6
    Day 3: 4 = 4       (or: 1 + 4 = 5)

- Input: weights = [1,2,3,1,1], days = 4
  Output: 3
  Explanation: Ship capacity 3 is the minimum to ship in 4 days.
    Day 1: 1 + 2 = 3
    Day 2: 3 = 3
    Day 3: 1 + 1 = 2
    (All packages shipped in 3 days)

Approach: Binary search on answer
- Search space: [max(weights), sum(weights)]
- can_ship(C): greedy pass, start new day when load exceeds capacity
- If C works → try smaller (right = mid); else → need bigger (left = mid + 1)

Time: O(n log S)   Space: O(1)
"""


def ship_within_days(weights: list[int], days: int) -> int:
    """
    Return the minimum ship capacity to ship all packages within the given days.

    Args:
        weights: List of package weights (must be shipped in order)
        days: Maximum number of days allowed

    Returns:
        Minimum ship capacity
    """

    def can_ship(capacity: int) -> bool:
        """Check if all packages can be shipped within 'days' days with this capacity."""
        day_count = 1
        current_load = 0

        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = 0
            current_load += w
        return day_count <= days

    # left: smallest possible capacity (can't split a package)
    # right: largest possible capacity (all in one day)
    left, right = max(weights), sum(weights)

    while left < right:
        mid = (left + right) // 2

        if can_ship(mid):
            right = mid  # mid works, try smaller
        else:
            left = mid + 1  # mid too small, must go bigger

    return left


if __name__ == "__main__":
    # Example 1
    result1 = ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    expected1 = 15
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = ship_within_days([3, 2, 2, 4, 1, 4], 3)
    expected2 = 6
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = ship_within_days([1, 2, 3, 1, 1], 4)
    expected3 = 3
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    print("All tests passed.")
