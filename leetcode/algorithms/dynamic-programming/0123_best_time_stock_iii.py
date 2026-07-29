"""
LeetCode 123: Best Time to Buy and Sell Stock III
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/

Problem: Given an array prices where prices[i] is the stock price on day i, find the
maximum profit achievable with at most TWO transactions. You may not engage in multiple
transactions simultaneously (must sell before buying again).

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^5

Examples:
- Input: prices = [3,3,5,0,0,3,1,4]
  Output: 6
  Explanation: Buy@0 (day 4), sell@3 (day 6), profit=3; buy@1 (day 7), sell@4 (day 8), profit=3.

- Input: prices = [1,2,3,4,5]
  Output: 4
  Explanation: Buy@1 (day 1), sell@5 (day 5), profit=4.

- Input: prices = [7,6,4,3,1]
  Output: 0
  Explanation: No profitable transaction.

Approach: DP with states (4 sequential states, O(1) space)
- buy1: max profit after the 1st buy (most negative cost so far) = max(buy1, -price)
- sell1: max profit after the 1st sell = max(sell1, buy1 + price)
- buy2: max profit after the 2nd buy (reuses profit from sell1) = max(buy2, sell1 - price)
- sell2: max profit after the 2nd sell = max(sell2, buy2 + price)
- Update in reverse order (sell2 → buy1) so each uses yesterday's earlier states, chaining two transactions without overlap

Time: O(n)   Space: O(1)
"""


def max_profit(prices: list[int]) -> int:
    """
    Return the maximum profit achievable with at most two transactions.

    Args:
        prices: List of stock prices for each day

    Returns:
        Maximum achievable profit
    """
    buy1 = float("-inf")
    sell1 = 0
    buy2 = float("-inf")
    sell2 = 0
    for price in prices:
        # Process in order so each uses today's updated earlier states correctly:
        # update sell2 first (use old buy2), then buy2 (use old sell1). etc.
        sell2 = max(sell2, buy2 + price)
        buy2 = max(buy2, sell1 - price)
        sell1 = max(sell1, buy1 + price)
        buy1 = max(buy1, -price)

    return sell2  # pyright: ignore[reportReturnType]


if __name__ == "__main__":
    # Example 1: prices = [3,3,5,0,0,3,1,4] → 6
    # Two transactions: buy@0 sell@3 (profit 3), buy@1 sell@4 (profit 3)
    assert max_profit([3, 3, 5, 0, 0, 3, 1, 4]) == 6

    # Example 2: prices = [1,2,3,4,5] → 4
    # Single transaction spanning the whole rise
    assert max_profit([1, 2, 3, 4, 5]) == 4

    # Example 3: prices = [7,6,4,3,1] → 0
    # Declining prices, no profitable transaction
    assert max_profit([7, 6, 4, 3, 1]) == 0

    # Edge case: Single day, no transaction possible → 0
    assert max_profit([1]) == 0

    print("All tests passed.")
