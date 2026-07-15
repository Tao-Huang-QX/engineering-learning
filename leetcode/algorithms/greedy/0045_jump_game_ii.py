"""
LeetCode 45: Jump Game II
https://leetcode.com/problems/jump-game-ii/

Problem: Given an array of non-negative integers nums, you are initially positioned
at the first index. Each element represents your maximum jump length at that position.
Return the minimum number of jumps to reach the last index. You can assume you can
always reach the last index.

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

Examples:
- Input: nums = [2,3,1,1,4], Output: 2 (Jump 1 step from index 0 to 1, then 3 steps to last)
- Input: nums = [2,3,0,1,4], Output: 2

Approach: Greedy (BFS Level Simulation)
- Track current level boundary (farthest reachable with current jumps)
- Track farthest position reachable from all positions in current level
- When reaching current boundary, increment jumps and extend boundary

Time: O(n)   Space: O(1)
"""


def jump(nums: list[int]) -> int:
    """
    Return the minimum number of jumps to reach the last index.

    Args:
        nums: Array where each element is max jump length at that position

    Returns:
        Minimum number of jumps to reach the last index
    """
    if len(nums) == 1:
        return 0

    jumps = 0
    current_end = 0  # Farthest position reachable with `jumps` jumps
    farthest = 0  # Farthest position reachable with `jumps + 1` jumps

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        # When we reach the boundary of current level, must jump
        if i == current_end:
            jumps += 1
            current_end = farthest

            if current_end >= len(nums) - 1:
                break

    return jumps


if __name__ == "__main__":
    # Example 1: Minimum jumps is 2
    result = jump([2, 3, 1, 1, 4])
    assert result == 2, f"Example 1 failed: got {result}, expected 2"

    # Example 2: Minimum jumps is 2
    result = jump([2, 3, 0, 1, 4])
    assert result == 2, f"Example 2 failed: got {result}, expected 2"

    # Single element (already at last index)
    result = jump([0])
    assert result == 0, f"Single element failed: got {result}, expected 0"

    # Two elements, one jump
    result = jump([1, 2])
    assert result == 1, f"Two elements failed: got {result}, expected 1"

    # Longer case
    result = jump([1, 1, 1, 1, 1])
    assert result == 4, f"Longer case failed: got {result}, expected 4"

    print("All tests passed.")
