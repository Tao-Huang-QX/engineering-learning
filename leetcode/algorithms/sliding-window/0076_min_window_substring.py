"""
LeetCode 76: Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Problem: Given two strings s and t of lengths m and n respectively,
return the minimum window substring of s such that every character in
t (including duplicates) is included in the window. If there is no
such substring, return the empty string "". The testcases are
generated such that the answer is unique.

Follow-up: could you find an algorithm that runs in O(m + n) time?

Constraints:
- m == s.length
- n == t.length
- 1 <= m, n <= 10^5
- s and t consist of uppercase and lowercase English letters
  (comparison is case-sensitive)

Examples:
- Input: s = "ADOBECODEBANC", t = "ABC"
  Output: "BANC"
  Explanation: the minimum window substring "BANC" includes 'A', 'B',
    and 'C' from string t.

- Input: s = "a", t = "a"
  Output: "a"
  Explanation: the entire string s is the minimum window.

- Input: s = "a", t = "aa"
  Output: ""
  Explanation: both 'a's must be included, but s has only one.

Approach: Elastic sliding window — grow to cover, shrink to minimize
- need = Counter(t); formed ticks +1 when a char's window count crosses
  up to need[c], -1 when it drops below; the window covers t iff
  formed == len(need)
- Grow right until covered, then shrink left while it holds, recording
  the best window as indices before each pop — record-and-pop order
  measures every covering window; slice once at return
- Coverage ticks are O(1) per slide, so pointers move O(m) total:
  O(m + n), no per-window Counter comparisons

Time: O(m + n)   Space: O(1) — counters bounded by the 52-letter alphabet
"""

from collections import Counter


def min_window(s: str, t: str) -> str:
    """
    Return the shortest substring of s containing all of t's characters.

    Args:
        s: Source string to search in
        t: Pattern whose characters (with multiplicity) must be covered

    Returns:
        The unique minimum covering window, or "" if s cannot cover t
    """
    need = Counter(t)
    window: Counter = Counter()
    required = len(need)  # distinct chars that must be satisfied
    formed = 0  # how many are currently satisfied

    best_left, best_len = 0, len(s) + 1  # indices only - slice once at the end
    left = 0

    for right, c in enumerate(s):
        window[c] += 1
        if c in need and window[c] == need[c]:  # cross upward into satisfied
            formed += 1

        while formed == required:
            if right - left + 1 < best_len:
                best_left, best_len = left, right - left + 1
            d = s[left]
            window[d] -= 1
            if d in need and window[d] < need[d]:  # fell from satisfied to short
                formed -= 1
            left += 1

    return "" if best_len == len(s) + 1 else s[best_left : best_left + best_len]


if __name__ == "__main__":
    # Example 1: classic case
    result1 = min_window("ADOBECODEBANC", "ABC")
    expected1 = "BANC"
    assert result1 == expected1, f"Example 1: got {result1!r}, expected {expected1!r}"

    # Example 2: whole string is the window
    assert min_window("a", "a") == "a", f"Example 2: got {min_window('a', 'a')!r}"

    # Example 3: multiplicity unsatisfiable
    assert min_window("a", "aa") == "", f"Example 3: got {min_window('a', 'aa')!r}"

    # Edge: t longer than s
    assert min_window("ab", "abc") == "", f"Longer t: got {min_window('ab', 'abc')!r}"

    # Edge: window must be the entire string
    assert min_window("abc", "abc") == "abc", f"Full: got {min_window('abc', 'abc')!r}"

    # Edge: duplicate requirements in t
    assert min_window("aa", "aa") == "aa", f"Dup: got {min_window('aa', 'aa')!r}"
    assert min_window("ab", "b") == "b", f"Pick: got {min_window('ab', 'b')!r}"

    # Edge: case-sensitive — 'A' does not satisfy 'a'
    assert min_window("A", "a") == "", f"Case: got {min_window('A', 'a')!r}"

    print("All tests passed.")


# solved: 2026-11-22, hard, 45min, Minimum Window Substring
