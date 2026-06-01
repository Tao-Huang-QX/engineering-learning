"""
LeetCode 347: Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Problem: Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Approach: Counter + heap/bucket
- Use Counter to get frequencies in O(n)
- Create buckets array of size len(nums) + 1, where index = frequency
- Distribute numbers into buckets by frequency
- Collect from highest frequency bucket downwards until k elements gathered

Time: O(n)   Space: O(n)
"""

from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Return the k most frequent elements.

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements (any order)
    """
    """
    Can use heapq.nlargest to simplify the implementation
    count = Counter(nums)
    return heapq.nlargest(k, counter.keys(), key=counter.get)
    """
    counter = Counter(nums)

    # Create butckets: index = frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counter.items():
        buckets[freq].append(num)

    # Collect from highest frequency
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            break

    return result[:k]


if __name__ == "__main__":
    # Example 1
    result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert set(result) == {1, 2}

    # Example 2
    result = top_k_frequent([1], 1)
    assert result == [1]

    # Example 3: All unique
    nums = [1, 2, 3, 4, 5]
    result = top_k_frequent(nums, 3)
    assert len(result) == 3
    assert set(result).issubset({1, 2, 3, 4, 5})

    # Example 4: Negative numbers
    result = top_k_frequent([-1, -1, 0, 1, 2, 2], 2)
    assert set(result) == {-1, 2}

    # Example 5: k equals array length (all unique)
    result = top_k_frequent([1, 2, 3], 3)
    assert len(result) == 3

    print("All tests passed.")
