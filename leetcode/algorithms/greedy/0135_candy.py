"""
LeetCode 135: Candy
https://leetcode.com/problems/candy/

Problem: There are n children standing in a line. Each child is assigned a
rating value given in the integer array ratings. You are giving candies to
these children subjected to the following requirements:
- Each child must have at least one candy.
- Children with a higher rating get more candies than their immediate
  neighbors with a lower rating.
Return the minimum number of candies you need to have to distribute.

Constraints:
- n == ratings.length
- 1 <= n <= 2 * 10^4
- 0 <= ratings[i] <= 2 * 10^4

Examples:
- Input: ratings = [1,0,2]
  Output: 5
  Explanation: Distribute 2, 1, 2 candies — the 0-rating child gets fewer
    than both higher-rated neighbors, everyone satisfies the rules.

- Input: ratings = [1,2,2]
  Output: 4
  Explanation: Distribute 1, 2, 1 — the two equal-rating children are NOT
    required to differ: only strictly higher ratings demand more candy.

Approach: Greedy two-pass — each sweep enforces one neighbor direction
- Wave structure: valleys (local minima, equal neighbors included) anchor
  at 1 candy; counts climb +1 per step away from a valley in either
  direction; a peak pays the MAX of its two climb lengths
- Pass 1 (L->R) enforces "higher than my left neighbor": ascending step
  gets candies[i-1] + 1 (the += works because [1]*n pre-set the slot),
  anything else stays at its initial 1 — resets are free
- Pass 2 (R->L) enforces "higher than my right neighbor" with MAX, never
  overwrite: lowering a value would silently un-fix pass 1 (breaks on
  long-left-climb / short-right-drop shapes like [1,2,3,4,2])
- Equal ratings are cliffs: neither side owes the other, so runs break
  and restart at 1 ([1,2,2] -> 1,2,1)
- Minimal because each pass is individually minimal for its constraint
  and max-merging two individually-minimal requirements is minimal

Time: O(n)   Space: O(n)   (O(1) variant exists: slope-run counting in one walk)
"""


def candy(ratings: list[int]) -> int:
    """
    Return the minimum total candies satisfying the neighbor rules.

    Args:
        ratings: Rating of each child in line

    Returns:
        Minimum number of candies to distribute
    """
    n = len(ratings)
    candies = [1] * n  # every child gets at least one; also pre-sets both passes' resets

    # Pass 1 (left -> right): enforce "higher than my LEFT neighbor"
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] += candies[i - 1]

    # Pass 2 (right -> left): enforce "higher than my RIGHT neighbor"
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


if __name__ == "__main__":
    # Example 1
    result1 = candy([1, 0, 2])
    expected1 = 5
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: equal ratings do not need to differ
    result2 = candy([1, 2, 2])
    expected2 = 4
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: single child
    result3 = candy([5])
    expected3 = 1
    assert result3 == expected3, f"Single child: got {result3}, expected {expected3}"

    # Edge: strictly increasing — candies must climb 1,2,3,4
    result4 = candy([1, 2, 3, 4])
    expected4 = 10
    assert result4 == expected4, f"Increasing: got {result4}, expected {expected4}"

    # Edge: strictly decreasing — mirror of the above
    result5 = candy([4, 3, 2, 1])
    expected5 = 10
    assert result5 == expected5, f"Decreasing: got {result5}, expected {expected5}"

    # Edge: equal plateau — everyone gets one
    result6 = candy([3, 3, 3])
    expected6 = 3
    assert result6 == expected6, f"Plateau: got {result6}, expected {expected6}"

    # Edge: peak between two valleys
    result7 = candy([1, 3, 2, 2, 1])
    expected7 = 7
    assert result7 == expected7, f"Peak: got {result7}, expected {expected7}"

    # Classic: twin peaks of equal height
    result8 = candy([1, 2, 87, 87, 87, 2, 1])
    expected8 = 13
    assert result8 == expected8, f"Twin peaks: got {result8}, expected {expected8}"

    print("All tests passed.")


# solved: 2026-11-06, hard, 45min, Candy
