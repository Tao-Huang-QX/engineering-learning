"""
LeetCode 215: Kth Largest Element in an Array
https://leetcode.com/problems/kth-largest-element-in-an-array/

Problem: Given an integer array nums and integer k, return the kth largest element.

Approach: Min-heap of size k
- Maintain heap of k largest elements seen so far
- When heap exceeds k elments, remove smallest
- At end, heap[0] is kth largest (smallest of top k)

Time: O(n log k)   Space: O(k) n pushes, each O(log k). Pops also O(log k)
"""

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Find the kth largest element in the array.

    Args:
        nums: List of integers
        k: The kth largest to find (1 = largest)

    Returns:
        The kth largest element
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # Keep only k largest
    return heap[0]


if __name__ == "__main__":
    # Example 1
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    # Example 2
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # Example 3: Single element
    assert find_kth_largest([1], 1) == 1

    # Example 4: K equals array length
    assert find_kth_largest([3, 2, 1], 3) == 1

    # Example 5: Duplicates
    assert find_kth_largest([2, 2, 2, 2], 1) == 2

    print("All tests passed.")
