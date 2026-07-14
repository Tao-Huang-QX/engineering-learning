"""
LeetCode 55: Jump Game
https://leetcode.com/problems/jump-game/

Problem: Given an array of non-negative integers nums, you are initially positioned at the first index.
Each element represents your maximum jump length at that position. Return true if you can reach the last index.

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

Examples:
- Input: nums = [2,3,1,1,4], Output: true (Jump 1 to index 1, then 3 to last index)
- Input: nums = [3,2,1,0,4], Output: false (Cannot reach last index)

Approach: Greedy (Track Farthest Reachable)
- Maintain `farthest` position we can reach as we iterate
- If current index exceeds farthest, we're stuck (return False)
- Update farthest = max(farthest, i + jump) at each position

Time: O(n)   Space: O(1)
"""


def can_jump(nums: list[int]) -> bool:
    """
    Return True if you can reach the last index from the first index.

    Args:
        nums: Array where each element is max jump length at that position

    Returns:
        True if last index is reachable, False otherwise
    """
    """
    n = len(nums)
    if n == 1:
        return True
    queue = deque([(0, nums[0])])
    visited = set()
    while queue:
        curr, max_steps = queue.popleft()
        if curr in visited:
            continue
        else:
            visited.add(curr)
        if curr + max_steps >= n - 1:
            return True
        else:
            for s in range(curr + 1, curr + max_steps + 1):
                queue.append((s, nums[s]))
    return False
    """
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


if __name__ == "__main__":
    # Example 1: Can reach last index
    result = can_jump([2, 3, 1, 1, 4])
    assert result, f"Example 1 failed: got {result}, expected True"

    # Example 2: Cannot reach last index
    result = can_jump([3, 2, 1, 0, 4])
    assert not result, f"Example 2 failed: got {result}, expected False"

    # Single element
    result = can_jump([0])
    assert result, f"Single element failed: got {result}, expected True"

    # Two elements, can jump directly
    result = can_jump([1, 0])
    assert result, f"Two elements failed: got {result}, expected True"

    # Two elements, cannot jump
    result = can_jump([0, 1])
    assert not result, f"Cannot jump failed: got {result}, expected False"

    print("All tests passed.")


# solved: 2026-07-14, medium, 20min, Jump Game
