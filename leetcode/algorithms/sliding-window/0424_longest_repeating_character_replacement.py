"""
LeetCode 424: Longest Repeating Character Replacement
https://leetcode.com/problems/longest-repeating-character-replacement/

Problem: You are given a string s and an integer k. You can choose any character
of the string and change it to any other uppercase English character. You can
perform this operation at most k times. Return the length of the longest
substring containing the same letter after performing the above operations.

Constraints:
- 1 <= s.length <= 10^5
- s consists of only uppercase English letters
- 0 <= k <= s.length

Examples:
- Input: s = "ABAB", k = 2
  Output: 4
  Explanation: Replace the two 'A's with 'B's (or vice versa) — the whole string.

- Input: s = "AABABBA", k = 1
  Output: 4
  Explanation: Replace the 'A' at index 2 (or the one at index 3) — "ABBB"
    inside the string is the longest achievable run.

Approach: Sliding window with a deliberately stale max_freq
- Validity rule: a window is fixable iff window_len - count(most frequent
  letter) <= k — replace every minority character
- max_freq never decreases, even when the window slides past the letter
  that set it: staleness only STOPS shrinking (the window drags at the
  current best size like a template), it never admits an invalid window,
  and the answer only improves when max_freq genuinely improves
- Consequence: the window never shrinks — it grows or slides — so the
  answer is simply len(s) - left at the end; no per-iteration max()
- The while can be an if (window exceeds the record by at most one per
  step); kept as while for the explicit invariant
- No run counting or first-occurrence map: replacement means the winning
  letter need not be any natural run's letter — only frequencies matter

Time: O(n)   Space: O(1)   (26-letter alphabet)
"""


def character_replacement(s: str, k: int) -> int:
    """
    Return the length of the longest same-letter substring achievable
    with at most k replacements.

    Args:
        s: Uppercase English letters
        k: Maximum number of single-character replacements

    Returns:
        Length of the longest uniform substring after at most k changes
    """
    counts: dict[str, int] = {}
    left = 0
    max_freq = 0  # historical best: most frequent single letter seen in any window

    for right, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        max_freq = max(max_freq, counts[c])

        # invalid window: minority letters outnumber the budget - shrink (slide)
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1

    # with the never-shrink trick the final window IS the best
    return len(s) - left


if __name__ == "__main__":
    # Example 1
    result1 = character_replacement("ABAB", 2)
    expected1 = 4
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = character_replacement("AABABBA", 1)
    expected2 = 4
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Edge: k = 0 — longest natural run
    result3 = character_replacement("AABBB", 0)
    expected3 = 3
    assert result3 == expected3, f"k=0: got {result3}, expected {expected3}"

    # Edge: k covers the whole string
    result4 = character_replacement("ABCDE", 5)
    expected4 = 5
    assert result4 == expected4, f"k=n: got {result4}, expected {expected4}"

    # Edge: single character
    result5 = character_replacement("A", 0)
    expected5 = 1
    assert result5 == expected5, f"Single: got {result5}, expected {expected5}"

    # Edge: budget allows bridging a gap
    result6 = character_replacement("ABBB", 2)
    expected6 = 4
    assert result6 == expected6, f"Bridge: got {result6}, expected {expected6}"

    # Edge: no repeats at all, small budget
    result7 = character_replacement("ABCDE", 1)
    expected7 = 2
    assert result7 == expected7, f"Distinct: got {result7}, expected {expected7}"

    print("All tests passed.")


# solved: 2026-11-08, medium, 40min, Longest Repeating Character Replacement
