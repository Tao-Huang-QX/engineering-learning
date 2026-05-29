"""
LeetCode 121: Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

Problem: You are given an array prices where prices[i] is the price of a given stock on the i-th day. You want to maximize your profit by choosing a single day to buy and a different day in the future to sell. Return the maximum profit.

Approach:
- initialize min_price to infinity and max_profit to 0

Time: O(n)   Space: O(1)
"""


def max_profit(prices: list[int]) -> int:
    """
    Return the maximum profit from one buy and one sell transaction.

    Args:
        prices: List of stock prices

    Returns:
        Maximum profit (0 if no profit possible)
    """
    min_price = float("inf")
    max_profit = 0
    for price in prices:
        potential_profit = price - min_price
        min_price = min(min_price, price)
        max_profit = max(max_profit, potential_profit)
    return max_profit  # type: ignore[retype-arg]


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (prices, expected_profit)
        ([7, 1, 5, 3, 6, 4], 5),  # Buy at 1, sell at 6
        ([7, 6, 4, 3, 1], 0),  # No profit possible
        ([1, 2], 1),  # Buy at 1, sell at 2
        ([2, 4, 1], 2),  # Buy at 2, sell at 4
    ]

    for prices, expected in test_cases:
        result = max_profit(prices)
        assert result == expected, f"{prices}: got {result}, expected {expected}"

    print("All tests passed.")
