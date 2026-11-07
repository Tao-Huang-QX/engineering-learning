"""
LeetCode 287: Find the Duplicate Number
https://leetcode.com/problems/find-the-duplicate-number/

Problem: Given an array nums containing n + 1 integers where each integer is
in the range [1, n] inclusive, there is only one repeated number in nums.
Return this repeated number. The duplicate may appear multiple times.

You must solve the problem WITHOUT modifying the array nums and using only
constant extra space.

Constraints:
- 1 <= n <= 10^5
- nums.length == n + 1
- 1 <= nums[i] <= n
- All the integers in nums appear only once except for precisely one
  integer which appears two or more times

Examples:
- Input: nums = [1,3,4,2,2]
  Output: 2

- Input: nums = [3,1,3,4,2]
  Output: 3

Approach: Floyd cycle detection — the array is a linked list in disguise
- Treat index i as a node whose next-pointer is nums[i]; values in [1, n]
  over n+1 nodes means pigeonhole guarantees a collision, and the duplicate
  value d gives node d TWO incoming edges — d is the cycle entry
- Node 0 cannot be in the cycle (values >= 1), so the walk from 0 has the
  rho shape Floyd requires
- Phase 1: slow moves 1 step, fast moves 2; meet INSIDE the cycle
  (advance first, test after — testing before the first move deadlocks
  at the start since slow == fast == 0)
- Phase 2: reset slow to 0, both move 1 step; they meet at the cycle ENTRY,
  and the entry's INDEX is the duplicate — returned as-is, no dereference
  (the node's identity is the answer, not its content)
- Meet conditions compare POSITIONS (slow == fast), never values —
  nums[slow] == nums[fast] can hold for different nodes
- Same algorithm as Linked List Cycle II (row 180) on a real list; here
  "node" = index, "next" = nums[i]

Time: O(n)   Space: O(1)
"""


def find_duplicate(nums: list[int]) -> int:
    """
    Return the single repeated number in nums.

    Args:
        nums: n + 1 integers, each in [1, n]; exactly one value repeats

    Returns:
        The repeated value
    """
    slow = fast = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


if __name__ == "__main__":
    # Example 1
    result1 = find_duplicate([1, 3, 4, 2, 2])
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = find_duplicate([3, 1, 3, 4, 2])
    expected2 = 3
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: smallest case — two 1s
    result3 = find_duplicate([1, 1])
    expected3 = 1
    assert result3 == expected3, f"[1,1]: got {result3}, expected {expected3}"

    # Edge: the duplicate fills the array
    result4 = find_duplicate([2, 2, 2, 2, 2])
    expected4 = 2
    assert result4 == expected4, f"All same: got {result4}, expected {expected4}"

    # Edge: duplicate appearing three times
    result5 = find_duplicate([1, 4, 4, 4, 2, 3])
    expected5 = 4
    assert result5 == expected5, f"Triple: got {result5}, expected {expected5}"

    # Edge: self-loop shape — nums[0] points at itself via the duplicate
    result6 = find_duplicate([5, 1, 2, 3, 4, 5])
    expected6 = 5
    assert result6 == expected6, f"Self-ish loop: got {result6}, expected {expected6}"

    print("All tests passed.")


# solved: 2026-11-07, medium, 30min, Find the Duplicate Number
