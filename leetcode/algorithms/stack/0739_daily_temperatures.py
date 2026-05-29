"""
LeetCode 739: Daily Temperatures
https://leetcode.com/problems/daily-temperatures/

Problem: Given daily temperatures, return how many days until a warmer temperature for each day.

Approach:
- Stack stores indices of days waiting for warmer temperature
- For each day, pop all previous days that are cooler (find their answer)
- Maintain decreasing temperatures in stack
- Each index pushes/popes at most once

Time: O(n)   Space: O(n)
"""


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    Calculate days to wait for a warmer temperature.

    Args:
        temperatures: List of daily temperatures

    Returns:
        List where answer[i] is days until warmer temperature, or 0 if none exists
    """
    answer = [0] * len(temperatures)
    stack = []  # stores indices of days waiting for warmer temperatures
    for today, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            answer[prev_day] = today - prev_day
        stack.append(today)
    return answer


if __name__ == "__main__":
    # Example 1
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]

    # Example 2
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]

    # Example 3
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]

    # Example 4: Decreasing temperatures
    assert daily_temperatures([90, 80, 70, 60]) == [0, 0, 0, 0]

    # Example 5: Single day
    assert daily_temperatures([50]) == [0]

    print("All tests passed.")
