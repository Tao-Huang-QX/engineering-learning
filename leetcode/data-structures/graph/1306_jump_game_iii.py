"""
LeetCode 1306: Jump Game III
https://leetcode.com/problems/jump-game-iii/

Problem: Given an array of non-negative integers arr, you are initially positioned at start index.
When you are at index i, you can jump to i + arr[i] or i - arr[i]. Check if you can reach any
index with value 0. You cannot jump outside the array.

Constraints:
- 1 <= arr.length <= 5 * 10^4
- 0 <= arr[i] < arr.length
- 0 <= start < arr.length

Approach: BFS with visited tracking
- Treat each index as a node with edges to i ± arr[i]
- Use BFS to find shortest path to any 0-valued index
- Track visited indices to avoid cycles

Time: O(n)   Space: O(n)
"""

from collections import deque


def can_reach(arr: list[int], start: int) -> bool:
    """
    Return True if you can reach any index with value 0 starting from start index.

    Args:
        arr: Array of non-negative integers representing jump distances
        start: Starting index

    Returns:
        True if any index with value 0 is reachable, False otherwise
    """
    queue = deque([start])
    visited = set()

    while queue:
        curr = queue.popleft()
        visited.add(curr)

        if arr[curr] == 0:
            return True
        else:
            diff = curr - arr[curr]
            sum_ = curr + arr[curr]
            if 0 <= diff and diff not in visited:
                queue.append(diff)
            if sum_ < len(arr) and sum_ not in visited:
                queue.append(sum_)

    return False


if __name__ == "__main__":
    # Example 1: Can reach index 3 with value 0
    # Path: 5 -> 4 -> 1 -> 3 or 5 -> 6 -> 4 -> 1 -> 3
    result = can_reach([4, 2, 3, 0, 3, 1, 2], 5)
    assert result, f"Example 1 failed: got {result}, expected True"

    # Example 2: Can reach index 3 with value 0
    # Path: 0 -> 4 -> 1 -> 3
    result = can_reach([4, 2, 3, 0, 3, 1, 2], 0)
    assert result, f"Example 2 failed: got {result}, expected True"

    # Example 3: Cannot reach index 1 with value 0
    result = can_reach([3, 0, 2, 1, 2], 2)
    assert not result, f"Example 3 failed: got {result}, expected False"

    print("All tests passed.")
