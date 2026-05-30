"""
LeetCode 322: Coin Change
https://leetcode.com/problems/coin-change/

Problem: You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

Approach: Unbounded knapsack DP
- dp[i] = min coins to make mount i
- For each amount, try all coins as the "last coin" used
- dp[i] = min(dp[i], dp[i - coin] + 1) across all valid coins

Time: O(amount × len(coins))   Space: O(amount)
"""


def coin_change(coins: list[int], amount: int) -> int:
    """
    Calculate the minimum number of coins to make the amount.

    Args:
        coins: List of coin denominations
        amount: Target amount to make

    Returns:
        Minimum number of coins, or -1 if impossible
    """
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != amount + 1 else -1


if __name__ == "__main__":
    # Example 1
    assert coin_change([1, 2, 5], 11) == 3

    # Example 2
    assert coin_change([2], 3) == -1

    # Example 3
    assert coin_change([1], 0) == 0

    # Example 4: Single coin matches
    assert coin_change([5], 5) == 1

    # Example 5: Multiple coins needed
    assert coin_change([1, 3, 4], 6) == 2

    print("All tests passed.")
