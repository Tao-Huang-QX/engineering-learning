"""
LeetCode 383: Ransom Note
https://leetcode.com/problems/ransom-note/

Problem: Given two strings ransom_note and magazine, return true if
ransom_note can be constructed by using the letters from magazine, and
false otherwise. Each letter in magazine can only be used once in
ransom_note.

Constraints:
- 1 <= ransom_note.length, magazine.length <= 10^5
- ransom_note and magazine consist of lowercase English letters

Examples:
- Input: ransom_note = "a", magazine = "b"
  Output: false

- Input: ransom_note = "aa", magazine = "ab"
  Output: false

- Input: ransom_note = "aa", magazine = "aab"
  Output: true

Approach: Counter spend-down with a pigeonhole early exit
- O(1) reject if the note is longer than the magazine (counting alone)
- Counter(magazine) as the bank; counter[c] == 0 is both the missing-letter
  and the exhausted-letter test (Counter returns 0 for absent keys)
- Spend one count per note letter; reaching the end means covered

Time: O(n + m)   Space: O(1)   (26 lowercase keys)
"""

from collections import Counter


def can_construct(ransom_note: str, magazine: str) -> bool:
    """
    Return whether ransom_note can be built from magazine's letters.

    Args:
        ransom_note: String to construct
        magazine: Pool of available letters, each usable once

    Returns:
        True if magazine covers ransom_note's letter counts
    """
    if len(ransom_note) > len(magazine):
        return False

    counter = Counter(magazine)

    for c in ransom_note:
        if counter[c] == 0:
            return False
        counter[c] -= 1

    return True


if __name__ == "__main__":
    # Example 1
    result1 = can_construct("a", "b")
    expected1 = False
    assert result1 is expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: count shortfall — two a's needed, one available
    result2 = can_construct("aa", "ab")
    expected2 = False
    assert result2 is expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3
    result3 = can_construct("aa", "aab")
    expected3 = True
    assert result3 is expected3, f"Example 3: got {result3}, expected {expected3}"

    # Edge: exact counts, nothing spare
    result4 = can_construct("abc", "cba")
    expected4 = True
    assert result4 is expected4, f"Exact: got {result4}, expected {expected4}"

    # Edge: magazine has plenty of everything
    result5 = can_construct("note", "reonhteousandletters")
    expected5 = True
    assert result5 is expected5, f"Plenty: got {result5}, expected {expected5}"

    # Edge: one repeated letter missing entirely
    result6 = can_construct("fihjjjjei", "hjibagacbhadfaefdjaeaebgi")
    expected6 = False
    assert result6 is expected6, f"Repeated: got {result6}, expected {expected6}"

    print("All tests passed.")


# solved: 2026-11-10, easy, 15min, Ransom Note
