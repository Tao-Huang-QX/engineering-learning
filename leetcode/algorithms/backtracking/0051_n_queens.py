"""
LeetCode 51: N-Queens
https://leetcode.com/problems/n-queens/

Problem: The n-queens puzzle is the problem of placing n queens on an
n x n chessboard such that no two queens attack each other. Given an
integer n, return all distinct solutions to the n-queens puzzle. You may
return the answer in any order. Each solution contains a distinct board
configuration of the n-queens' placement, where 'Q' and '.' indicate
occupied and free squares respectively.

Constraints:
- 1 <= n <= 9

Examples:
- Input: n = 4
  Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
  Explanation: The two distinct solutions. ("Q...","...Q",".Q..","..Q.")
    is the mirror of solution 2 and equals solution 1 rotated — the two
    listed boards are the only distinct ones up to exact layout.

- Input: n = 1
  Output: [["Q"]]

Approach: Row-by-row backtracking with three constraint sets
- Rows are structural: one queen placed per recursion level, never
  re-checked; the only decision per row is the column
- Attack model as three set memberships: cols, diag (r-c constant),
  anti_diag (r+c constant) — O(1) safety tests, no board scanning;
  |dr| == |dc| splits into dr==dc (same diag) or dr==-dc (same anti),
  so the two diagonal sets are complete
- Why the constants: stepping along a diag changes r and c together
  (difference frozen); along an anti-diag they trade (sum frozen) — the
  constant is the line's ID, so "same diagonal" == "same ID" == one
  set lookup
- placement[r] = col is the record (sets are unordered and can't
  reconstruct); choose/unchoose moves all four structures together
- Board emitted at row == n: "." * col + "Q" + "." * (n-col-1) per row

Time: O(n!)-ish search with heavy pruning (exact work is input-dependent)   Space: O(n) recursion + sets
"""


def solve_n_queens(n: int) -> list[list[str]]:
    """
    Return all distinct n-queens board configurations.

    Args:
        n: Board size and queen count (1 <= n <= 9)

    Returns:
        List of boards, each a list of n strings ('Q' queen, '.' empty)
    """
    result: list[list[str]] = []
    cols: set[int] = set()
    diag: set[int] = set()
    anti_diag: set[int] = set()

    def backtrack(row: int, placement: list[int]) -> None:
        if row == n:  # every row holds exactly one queen
            result.append(build_board(placement))
            return

        for col in range(n):  # the ONLY decision: which column for this row
            if col in cols or (row - col) in diag or (row + col) in anti_diag:  # three set check
                continue

            # choose - all four structures move together
            placement.append(col)
            cols.add(col)
            diag.add(row - col)
            anti_diag.add(row + col)

            backtrack(row + 1, placement)

            # unchoose - the mirror
            placement.pop()
            cols.remove(col)
            diag.remove(row - col)
            anti_diag.remove(row + col)

    def build_board(placement: list[int]) -> list[str]:
        return ["." * col + "Q" + "." * (n - col - 1) for col in placement]

    backtrack(0, [])
    return result


if __name__ == "__main__":
    # Example 1: n = 4 has exactly two distinct solutions
    result1 = solve_n_queens(4)
    expected1 = [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    assert sorted(map(tuple, result1)) == sorted(map(tuple, expected1)), f"n=4: got {result1}"

    # Example 2: trivial board
    result2 = solve_n_queens(1)
    expected2 = [["Q"]]
    assert result2 == expected2, f"n=1: got {result2}"

    # Edge: n = 2 and n = 3 have NO solutions
    assert solve_n_queens(2) == [], f"n=2: got {solve_n_queens(2)}"
    assert solve_n_queens(3) == [], f"n=3: got {solve_n_queens(3)}"

    # Known counts: n -> number of distinct solutions
    known_counts = {1: 1, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
    for size, count in known_counts.items():
        got = len(solve_n_queens(size))
        assert got == count, f"n={size}: got {got} solutions, expected {count}"

    # Validity check on a sample: every solution has n queens, one per
    # row and column, no two sharing a diagonal
    for board in solve_n_queens(6):
        cols = [row.index("Q") for row in board]
        assert len(set(cols)) == len(cols), f"column clash in {board}"
        diags = {r - c for r, c in enumerate(cols)}
        anti = {r + c for r, c in enumerate(cols)}
        assert len(diags) == len(cols) and len(anti) == len(cols), f"diagonal clash in {board}"

    print("All tests passed.")


# solved: 2026-11-15, hard, 60min, N-Queens
