"""
LeetCode 692: Top K Frequent Words
https://leetcode.com/problems/top-k-frequent-words/

Problem: Given an array of strings words and an integer k, return the k most frequent
strings. Return the answer sorted by the frequency from highest to lowest. Sort the
words with the same frequency by their lexicographical order.

Constraints:
- 1 <= words.length <= 500
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
- k is in the range [1, The number of unique words[i]]

Follow-up: Could you solve it in O(n log k) time and O(n) extra space?

Examples:
- Input: words = ["i","love","leetcode","i","love","coding"], k = 2
  Output: ["i","love"]
  Explanation: "i" and "love" are the two most frequent words.
    "i" comes before "love" due to lower alphabetical order (both frequency 2).

- Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
  Output: ["the","is","sunny","day"]
  Explanation: "the" (4), "is" (3), "sunny" (2), "day" (1).

Approach: Counter + size-k min-heap with custom comparator
- Candidate wrapper: __lt__ makes worst candidate "smallest" (low freq, or large word for ties)
- Push all, pop when heap > k — discards worst, keeps k best
- Pop and reverse: heap is worst→best, need best→worst

Time: O(n + u log k)   Space: O(u) where u = unique words
"""

import heapq
from collections import Counter


class Candidate:
    """Wrapper to invert word comparison for size-k min-heap."""

    def __init__(self, word: str, freq: int) -> None:
        self.word = word
        self.freq = freq

    def __lt__(self, other: "Candidate"):
        if self.freq == other.freq:
            return self.word > other.word  # larger word "smaller"
        return self.freq < other.freq  # lower freq "smaller"


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """
    Return the k most frequent words, sorted by frequency descending then alphabetically.

    Args:
        words: List of lowercase words
        k: Number of top frequent words to return

    Returns:
        List of k most frequent words
    """
    counter = Counter(words)
    heap: list[Candidate] = []

    for word, freq in counter.items():
        heapq.heappush(heap, Candidate(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)  # discard worst: lowest freq, or alphabetically larger

    # Heap has k items in min-heap order; pop and reverse
    result: list[str] = []
    while heap:
        result.append(heapq.heappop(heap).word)

    return result[::-1]


if __name__ == "__main__":
    # Example 1
    result1 = top_k_frequent(["i", "love", "leetcode", "i", "love", "coding"], 2)
    expected1 = ["i", "love"]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = top_k_frequent(
        ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4
    )
    expected2 = ["the", "is", "sunny", "day"]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
