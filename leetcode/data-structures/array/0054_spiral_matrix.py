"""
LeetCode 54: Spiral Matrix
https://leetcode.com/problems/spiral-matrix/

Problem: Given an m x n matrix, return all elements of the matrix in spiral
order (clockwise, starting from the top-left).

Constraints:
- m == matrix.length, n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

Examples:
- Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
  Output: [1,2,3,6,9,8,7,4,5]

- Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
  Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Approach: Boundary simulation — four shrinking walls, one ring per loop
- Walls top/bottom/left/right bracket the unconsumed rectangle; each walk
  emits one side then shrinks that wall, and later walks read the ALREADY
  shrunk bounds — that ordering is what keeps corners from double-visiting
- Walks 3 and 4 need guards: after walks 1-2 shrink top/right, the
  remainder can be a single row (top == bottom) or column — walk 1
  already emitted it, so an unguarded bottom-walk re-emits it (the
  extra-6 bug on 3x4), and unguarded walk 4 mirrors it on tall matrices
- Guards ask "does that side still exist": top <= bottom before walk 3,
  left <= right before walk 4
- Outer while re-checks after every ring; odd squares end on a single
  center cell admitted by the same condition

Time: O(m * n)   Space: O(1) beyond the output
"""


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    Return the matrix elements in clockwise spiral order.

    Args:
        matrix: Non-empty m x n grid of integers

    Returns:
        All elements in spiral order, row-major count m * n
    """
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result: list[int] = []

    while top <= bottom and left <= right:
        # walk 1: across the top row, left -> right
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1  # top wall consumed

        # walk 2: down the right column, top -> bottom
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1  # right wall consumed

        # walk 3: only if an unconsumed row remains below the new top, back along the bottom row, right -> left
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1  # bottom wall consumed

        # walk 4: only if an unconsumed column remains left of the new right, up the left column, bottom -> top
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1  # left wall consumed

    return result


if __name__ == "__main__":
    # Example 1: square
    result1 = spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    expected1 = [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: wide rectangle
    result2 = spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    expected2 = [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: single row — the left/right walks must not double-visit
    result3 = spiral_order([[1, 2, 3]])
    expected3 = [1, 2, 3]
    assert result3 == expected3, f"Single row: got {result3}, expected {expected3}"

    # Edge: single column — the up walk must not double-visit
    result4 = spiral_order([[1], [2], [3]])
    expected4 = [1, 2, 3]
    assert result4 == expected4, f"Single column: got {result4}, expected {expected4}"

    # Edge: single element
    result5 = spiral_order([[7]])
    expected5 = [7]
    assert result5 == expected5, f"Single element: got {result5}, expected {expected5}"

    # Edge: two rows — inner layer is a single row
    result6 = spiral_order([[1, 2], [3, 4]])
    expected6 = [1, 2, 4, 3]
    assert result6 == expected6, f"2x2: got {result6}, expected {expected6}"

    # Edge: tall matrix — inner layer is a single column
    result7 = spiral_order([[1, 2], [3, 4], [5, 6], [7, 8]])
    expected7 = [1, 2, 4, 6, 8, 7, 5, 3]
    assert result7 == expected7, f"Tall: got {result7}, expected {expected7}"

    print("All tests passed.")


# solved: 2026-11-08, medium, 40min, Spiral Matrix
