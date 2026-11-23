"""
LeetCode 118: Pascal's Triangle
https://leetcode.com/problems/pascals-triangle/

Problem: Given an integer numRows, return the first numRows of
Pascal's triangle. In Pascal's triangle, each number is the sum of the
two numbers directly above it.

Constraints:
- 1 <= numRows <= 30

Examples:
- Input: numRows = 5
  Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

- Input: numRows = 1
  Output: [[1]]

Approach: Persistent rolling row, updated in place
- row IS the previous row: append the trailing 1, then update interior
  cells right-to-left (row[j] += row[j - 1]) — RTL keeps row[j - 1]
  holding the previous row's value until consumed
- Each row is stored as a copy (row.copy()): appending the live buffer
  would alias every stored row to the final one

Time: O(n^2)   Space: O(n^2) output, O(n) rolling buffer
"""


def generate_pascals_triangle(num_rows: int) -> list[list[int]]:
    """
    Return the first num_rows rows of Pascal's triangle.

    Args:
        num_rows: Number of rows to build (1 to 30)

    Returns:
        List of rows; row i has i + 1 entries, each the sum of the two
        entries above it, bounded by 1s
    """
    result: list[list[int]] = []
    row: list[int] = []
    for i in range(num_rows):
        row.append(1)
        for j in range(i - 1, 0, -1):
            row[j] += row[j - 1]
        result.append(row.copy())
    return result


if __name__ == "__main__":
    # Example 1: five rows
    result1 = generate_pascals_triangle(5)
    expected1 = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: minimum size
    assert generate_pascals_triangle(1) == [[1]], f"Example 2: got {generate_pascals_triangle(1)}"

    # Edge: two and three rows
    assert generate_pascals_triangle(2) == [[1], [1, 1]], (
        f"Two rows: got {generate_pascals_triangle(2)}"
    )
    assert generate_pascals_triangle(3) == [[1], [1, 1], [1, 2, 1]], (
        f"Three rows: got {generate_pascals_triangle(3)}"
    )

    # Property: every row is a palindrome and sums to 2^row
    triangle = generate_pascals_triangle(10)
    for i, row in enumerate(triangle):
        assert row == row[::-1], f"Row {i} not palindromic: {row}"
        assert sum(row) == 2**i, f"Row {i} sums to {sum(row)}, want {2**i}"

    # Edge: maximum size — row 30 has 30 entries, palindromic, sum 2^29
    big = generate_pascals_triangle(30)
    assert len(big) == 30 and len(big[-1]) == 30, f"Row 30 shape: {[len(r) for r in big]}"
    assert big[-1][0] == 1 and big[-1][-1] == 1, f"Row 30 ends: {big[-1][:2]}, {big[-1][-2:]}"

    print("All tests passed.")


# solved: 2026-11-23, easy, 30min, Pascal's Triangle
