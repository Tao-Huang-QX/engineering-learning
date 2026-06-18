"""
Unique Lines from a Point

Problem: Given Tim's house coordinates (x0, y0) and N friends' house coordinates (xi, yi),
find the number of unique lines that can be drawn from Tim's house to each friend's house.

Approach: Slope normalization with GCD
- Two points define a line; friends on same line from Tim's house have same slope
- Normalize slope (dy/dx) to simplest form using GCD
- Handle vertical lines (dx = 0) and horizontal lines (dy = 0) as special cases
- Use set to count unique slopes

Time: O(N log(max_coord))   Space: O(N)
"""

from math import gcd


def count_unique_lines(friends: list[tuple[int, int]], tim_x: int, tim_y: int) -> int:
    """Return number of unique lines from Tim's house to all friends' houses."""
    unique_slopes = set()

    for friend_x, friend_y in friends:
        dx = friend_x - tim_x
        dy = friend_y - tim_y

        # Normalize slope to simplest form
        if dx == 0:
            # Vertical line - all points with same x coordinate as Tim
            slope = (0, 1)  # Represent as (0, 1) for vertical
        elif dy == 0:
            # Horizontal line
            slope = (1, 0)
        else:
            # Reduce to simplest form
            g = gcd(dx, dy)
            dx //= g
            dy //= g
            # Ensure consistent sign (dx always positive, dy carries sign)
            if dx < 0:
                dx = -dx
                dy = -dy
            slope = (dx, dy)

        unique_slopes.add(slope)

    return len(unique_slopes)


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([(1, 1), (-1, 2), (3, 0)], 0, 0, 3),
        ([(1, 0), (2, 0), (3, 0)], 0, 0, 1),  # All horizontal
        ([(0, 1), (0, 2), (0, 3)], 0, 0, 1),  # All vertical
        ([(1, 1), (2, 2)], 0, 0, 1),  # Same line
        ([(1, 0), (0, 1)], 0, 0, 2),  # Horizontal and vertical
    ]

    for friends, tx, ty, expected in test_cases:
        result = count_unique_lines(friends, tx, ty)
        assert result == expected, f"got {result}, expected {expected}"

    print("All tests passed.")

# solved: 2026-06-17, easy, 15min, Unique Lines from Point
