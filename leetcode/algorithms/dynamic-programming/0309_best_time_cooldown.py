"""
LeetCode 309: Best Time to Buy and Sell Stock with Cooldown
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/

Problem: Given an array prices where prices[i] is the stock price on day i, find the
maximum profit with unlimited transactions but with a cooldown: after selling, you
cannot buy on the next day.

Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000

Examples:
- Input: prices = [1,2,3,0,2]
  Output: 3
  Explanation: transactions = [buy, sell, cooldown, buy, sell]

- Input: prices = [1]
  Output: 0

Approach: DP with states, space-optimized
- Track hold, sold, rest as scalars (only need previous day)
- hold = max(prev_hold, prev_rest - price) — keep holding or buy today
- sold = prev_hold + price — sell what we held yesterday
- rest = max(prev_rest, prev_sold) — stay resting or finish cooldown
- Cooldown enforced: cannot buy directly from sold state

Time: O(n)   Space: O(1) - only need previous day
"""


def max_profit(prices: list[int]) -> int:
    """
    Return the maximum profit achievable with unlimited transactions and a cooldown
    after each sell (cannot buy on the next day).

    Args:
        prices: List of stock prices for each day

    Returns:
        Maximum achievable profit
    """
    """
    n = len(prices)
    if n == 1:
        return 0

    # hold[i]: net cost of holding a stock at end of day i
    # sold[i]: profit of selling today (on day i)
    # rest[i]: max profit not holding, not just sold (cooldown done or never bought)
    hold = [0] * n
    sold = [0] * n
    rest = [0] * n

    # Day 0: hold means we bought, sold/rest are impossible
    hold[0] = -prices[0]
    sold[0] = float("-inf")  # pyright: ignore[reportCallIssue, reportArgumentType]
    rest[0] = 0

    for i in range(1, n):
        # Keep holding, or buy from rest state
        hold[i] = max(hold[i - 1], rest[i - 1] - prices[i])
        # Sell what we held yesterday
        sold[i] = hold[i - 1] + prices[i]
        # Stay resting, or finish cooldown from yesterday's sell
        rest[i] = max(rest[i - 1], sold[i - 1])

    # End in rest or sold (holding stock means unrealized profit)
    return max(sold[-1], rest[-1])
    """
    hold, sold, rest = -prices[0], 0, 0
    for price in prices[1:]:
        pre_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(pre_hold, prev_rest - price)
        sold = pre_hold + price
        rest = max(prev_rest, prev_sold)
    return max(sold, rest)


if __name__ == "__main__":
    # Example 1: prices = [1,2,3,0,2] → 3
    # Transactions: buy@1, sell@2, cooldown, buy@0, sell@2 = profit (2-1) + (2-0) = 3
    assert max_profit([1, 2, 3, 0, 2]) == 3

    # Example 2: Single day, no transaction possible → 0
    assert max_profit([1]) == 0

    # Edge case: Two days, buy low sell high → profit
    assert max_profit([1, 2]) == 1

    # Edge case: Declining prices, no profit → 0
    assert max_profit([3, 2, 1]) == 0

    print("All tests passed.")
