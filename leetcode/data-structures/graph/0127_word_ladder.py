"""
LeetCode 127: Word Ladder
https://leetcode.com/problems/word-ladder/

Problem: A transformation sequence from beginWord to endWord is a sequence of words
where every adjacent pair differs by a single letter, and each intermediate word
exists in wordList. Return the number of words in the shortest transformation
sequence from beginWord to endWord, or 0 if no such sequence exists.

Note: beginWord does not count as a transformation — only words in the sequence
after beginWord need to be in wordList.

Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.

Examples:
- Input: beginWord = "hit", endWord = "cog",
         wordList = ["hot","dot","dog","lot","log","cog"]
  Output: 5
  Explanation: One shortest transformation is
    "hit" -> "hot" -> "dot" -> "dog" -> "cog" (5 words total).

- Input: beginWord = "hit", endWord = "cog",
         wordList = ["hot","dot","dog","lot","log"]
  Output: 0
  Explanation: endWord "cog" is not in wordList, so no valid transformation exists.

Approach: Bidirectional BFS
- Two frontiers expand from beginWord and endWord simultaneously
- Always expand the smaller frontier (swap) to minimize work
- Generate neighbors: replace each char with a-z (26 * L per word), check set
- When frontiers intersect, return length + 1

Time: O(N * L * 26) where N = len(wordList), L = word length — each word explored at most once
through both frontiers; neighbor generation costs 26 * L per word
Space: O(N) — word_set + visited + frontiers at most cover all words
"""


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """
    Return the length of the shortest transformation sequence from beginWord to endWord.

    Args:
        begin_word: Starting word
        end_word: Target word
        word_list: List of valid transformation words

    Returns:
        Number of words in the shortest sequence, or 0 if impossible
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    forward = {begin_word}
    backward = {end_word}
    visited = {begin_word, end_word}
    length = 1
    word_len = len(begin_word)

    while forward:
        if len(forward) > len(backward):
            forward, backward = backward, forward  # always expand the smaller set

        next_frontier: set[str] = set()
        for word in forward:
            for i in range(word_len):
                for c in range(26):
                    candidate = word[:i] + chr(ord("a") + c) + word[i + 1 :]

                    if candidate in backward:
                        return length + 1

                    if candidate in word_set and candidate not in visited:
                        visited.add(candidate)
                        next_frontier.add(candidate)

        forward = next_frontier
        length += 1

    return 0


if __name__ == "__main__":
    # Example 1
    result1 = ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    expected1 = 5
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"])
    expected2 = 0
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
