"""
LeetCode 763: Partition Labels
https://leetcode.com/problems/partition-labels/

Problem: You are given a string s. Partition the string into as many parts as possible
so that each letter appears in at most one part. Return a list of integers representing
the size of these parts.

Approach: Greedy with sliding window
- First pass: record last occurrence of each character
- Second pass: track furthest last position in current partition
- Cut partition when current index equals furthest last position

Time: O(n)   Space: O(1)
"""


def partition_labels(s: str) -> list[int]:
    """
    Partition string so each letter appears in at most one part.

    Args:
        s: Input string consisting of lowercase English letters

    Returns:
        List of part sizes
    """
    # Get the last indices for all chars
    last_seen = {}
    for i, char in enumerate(s):
        last_seen[char] = i

    result = []
    part_end = 0  # Furthest last position in current partition
    start = 0  # Start of current partition
    for i, char in enumerate(s):
        part_end = max(part_end, last_seen[char])

        # When we reach the furthest last occurrence, cut here
        if i == part_end:
            result.append(i - start + 1)
            start = i + 1
    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        # (s, expected_part_sizes)
        ("abacbc", [6]),  # All chars overlap, single partition
        ("ababcbacadefegdehijhklij", [9, 7, 8]),  # "ababcbaca|defegde|hijhklij"
        ("eccbbbbdec", [10]),  # "eccbbbbdec" (single partition)
    ]

    for s, expected in test_cases:
        result = partition_labels(s)
        assert result == expected, f"s={s}: got {result}, expected {expected}"

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Partition Labels
