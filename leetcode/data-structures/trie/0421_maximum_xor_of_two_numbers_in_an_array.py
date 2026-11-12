"""
LeetCode 421: Maximum XOR of Two Numbers in an Array
https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/

Problem: Given an integer array nums, return the maximum result of
nums[i] XOR nums[j], where 0 <= i <= j < n.

Constraints:
- 1 <= nums.length <= 2 * 10^5
- 0 <= nums[i] <= 2^31 - 1

Examples:
- Input: nums = [3,10,5,25,2,8]
  Output: 28
  Explanation: The maximum result is 5 XOR 25 = 28.

- Input: nums = [0]
  Output: 0

- Input: nums = [2,4]
  Output: 6

- Input: nums = [8,10,2]
  Output: 10

- Input: nums = [14,70,53,83,49,91,36,80,92,51,66,70]
  Output: 127

Approach: Bitwise trie — prefix shelves + opposite-bit greedy descent
- Insert all numbers MSB-first (Most Significant Bit) at fixed width 31
  (aligns mixed bit lengths; full-depth paths mean no query walk falls off)
- Query each number: prefer the OPPOSITE-bit child at every level —
  child existence is the prefix-membership test; a hit sets that XOR
  bit, a miss follows the own bit for 0; answer = max over numbers
- Hash-set alternative kept in a comment below (same greedy, one scale)

Time: O(31n)   Space: O(31n)
"""


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[int, TrieNode] = {}  # key = the bit (0 or 1)


def find_maximum_xor(nums: list[int]) -> int:
    """
    Return the maximum XOR of any two numbers in nums (i == j allowed).

    Args:
        nums: Non-negative integers up to 2^31 - 1

    Returns:
        Maximum nums[i] XOR nums[j]
    """
    """
    best = 0
    mask = 0
    for level in range(30, -1, -1):  # decide the answer MSB-first
        mask |= 1 << level  # mask keeps bits 30..level
        prefixes = {x & mask for x in nums}  # prefixes in NORMAL scale
        candidate = best | (1 << level)
        # a ^ b == candidate ⟺ a == candidate ^ b
        # so the bit is achivable iff some two prefixes differ by exactly `candidate`
        if any((candidate ^ p) in prefixes for p in prefixes):
            best = candidate
    return best
    """
    width = 31  # bit 30..0 - fixed depth so every number's bit k sits at depth 30-k

    def insert(root: TrieNode, num: int) -> None:
        """Shelve num by its binary prefix, MSB first."""
        node = root
        for level in range(width - 1, -1, -1):
            bit = (num >> level) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def best_partner_xor(root: TrieNode, num: int) -> int:
        """Walk the shelves preferring the OPPOSITE bit; return the best XOR for num."""
        node = root
        val = 0
        for level in range(width - 1, -1, -1):
            bit = (num >> level) & 1
            want = 1 - bit
            if want in node.children:
                node = node.children[want]
                val |= 1 << level
            else:
                node = node.children[bit]
        return val

    root = TrieNode()
    for num in nums:
        insert(root, num)

    return max(best_partner_xor(root, num) for num in nums)


if __name__ == "__main__":
    # Example 1
    result1 = find_maximum_xor([3, 10, 5, 25, 2, 8])
    expected1 = 28
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: single element — i == j, XOR with itself is 0
    result2 = find_maximum_xor([0])
    expected2 = 0
    assert result2 == expected2, f"Single: got {result2}, expected {expected2}"

    # Example 3: pair XOR
    assert find_maximum_xor([2, 4]) == 6, f"[2,4]: got {find_maximum_xor([2, 4])}"

    # Example 4: 2 XOR 8 = 10
    assert find_maximum_xor([8, 10, 2]) == 10, f"[8,10,2]: got {find_maximum_xor([8, 10, 2])}"

    # Example 5
    result5 = find_maximum_xor([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70])
    expected5 = 127
    assert result5 == expected5, f"Example 5: got {result5}, expected {expected5}"

    # Edge: identical elements — every pair XORs to 0
    assert find_maximum_xor([7, 7, 7]) == 0, f"Dupes: got {find_maximum_xor([7, 7, 7])}"

    # Edge: zeros mixed in
    assert find_maximum_xor([0, 0]) == 0
    assert find_maximum_xor([0, 1]) == 1

    print("All tests passed.")


# solved: 2026-11-12, medium, 90min, Maximum XOR of Two Numbers in an Array
