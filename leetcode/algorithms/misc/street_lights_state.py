"""
Street Lights State After M Days

Problem: Given initial states of street lights, simulate M days of state changes.
A light goes OFF if adjacent lights were both ON or both OFF, else ON.
End lights have one adjacent neighbor (virtual neighbor = 0).

Approach: Simulation
- Iterate M times, each time computing next state from current
- For each position, compare left and right neighbors

Time: O(M * N)   Space: O(N)
"""


def street_lights_state(n: int, current_state: list[int], days: int) -> list[int]:
    """
    Simulate street light state changes over M days.

    Args:
        n: Number of street lights.
        current_state: Initial state of each light (0 = OFF, 1 = ON).
        days: Number of days to simulate.

    Returns:
        Final state after M days.
    """
    if n == 1:
        return [1]

    next_state = [0] * n

    def compute_next_state(curr_state: list[int], nxt_state: list[int]) -> None:
        for i in range(len(curr_state)):
            if i == 0:
                nxt_state[i] = 0 if curr_state[i + 1] == 0 else 1
            elif i == n - 1:
                nxt_state[i] = 0 if curr_state[i - 1] == 0 else 1
            else:
                if curr_state[i - 1] == 0 and curr_state[i + 1] == 0:
                    nxt_state[i] = 0
                elif curr_state[i - 1] == 1 and curr_state[i + 1] == 1:
                    nxt_state[i] = 0
                else:
                    nxt_state[i] = 1

    for i in range(1, days + 1):
        if i % 2 == 1:
            compute_next_state(current_state, next_state)
        else:
            compute_next_state(next_state, current_state)

    return next_state if days % 2 == 1 else current_state


if __name__ == "__main__":
    # Test cases from the problem description
    test_cases = [
        (8, [1, 1, 1, 0, 1, 1, 1, 1], 2, [0, 0, 0, 0, 0, 1, 1, 0]),
        (3, [0, 1, 0], 1, [1, 0, 1]),
        (1, [1], 5, [1]),  # Single light stays same
        (5, [1, 0, 1, 0, 1], 0, [1, 0, 1, 0, 1]),  # 0 days, no change
        (2, [0, 0], 3, [0, 0]),  # Both OFF, stay OFF (virtual neighbors both 0)
    ]

    for n, state, days, expected in test_cases:
        result = street_lights_state(n, state, days)
        assert result == expected, (
            f"n={n}, state={state}, days={days}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Street Lights
