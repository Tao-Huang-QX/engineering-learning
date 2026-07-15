"""
LeetCode 122: Best Time to Buy and Sell Stock II
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

Problem: You are given an integer array prices where prices[i] is the price of a given
stock on the ith day. On each day, you may decide to buy and/or sell the stock. You
can only hold at most one share of the stock at any time. However, you can buy it
then immediately sell it on the same day. Find and return the maximum profit.

Constraints:
- 1 <= prices.length <= 3 * 10^4
- 0 <= prices[i] <= 10^4

Examples:
- Input: prices = [7,1,5,3,6,4], Output: 7 (Buy 1, sell 5 (4), buy 3, sell 6 (3))
- Input: prices = [1,2,3,4,5], Output: 4 (Buy 1, sell 5, or buy/sell each day)
- Input: prices = [7,6,4,3,1], Output: 0 (No transaction)

Approach: Greedy
- Sum all positive differences between consecutive days
- Every upward move contributes profit regardless of holding period
- Equivalent to capturing all profitable buy/sell opportunities

Time: O(n)   Space: O(1)
"""


def max_profit(prices: list[int]) -> int:
    """
    Return the maximum profit from buying and selling stock.

    Args:
        prices: Array where prices[i] is the stock price on day i

    Returns:
        Maximum profit achievable with unlimited transactions
    """
    profit = 0
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff <= 0:
            continue
        else:
            profit += diff
    return profit


if __name__ == "__main__":
    # Example 1: Buy at 1 sell at 5, buy at 3 sell at 6 = 4 + 3 = 7
    result = max_profit([7, 1, 5, 3, 6, 4])
    assert result == 7, f"Example 1 failed: got {result}, expected 7"

    # Example 2: Monotonic increase, buy at 1 sell at 5 = 4
    result = max_profit([1, 2, 3, 4, 5])
    assert result == 4, f"Example 2 failed: got {result}, expected 4"

    # Example 3: Monotonic decrease, no profit possible
    result = max_profit([7, 6, 4, 3, 1])
    assert result == 0, f"Example 3 failed: got {result}, expected 0"

    print("All tests passed.")
