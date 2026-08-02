"""
LeetCode 49: Group Anagrams
https://leetcode.com/problems/group-anagrams/

Problem: Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Approach:
- an easy solution is to sort each string and use the sorted string as a key in a hash map to group anagrams together
- for long strings, a frequecy count of characters can be used as the key instead of sorting, which can be more efficient

Time: O(n * m)   Space: O(n * m)
Where n is the number of strings and m is the average length of the strings.
"""

from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams together from the input list.

    Args:
        strs: List of strings

    Returns:
        List of groups, where each group is a list of anagrams
    """
    """
    Sorting solution:
    groups = defaultdict(list)
    for s in strs:
        key = s.sorted()
        groups[key].append(s)
    return list(groups.values())
    """
    groups = defaultdict(list)
    for s in strs:
        key = get_anagram_key(s)
        groups[key].append(s)
    return list(groups.values())


def get_anagram_key(s: str) -> tuple[int, ...]:
    """
    Get a key that represent the anagram group for the input string.
    Args:
        s: Input string
    Returns:
        A tuple representing the count of each char in the string
    """
    # freq = {chr(i): 0 for i in range(ord("a"), ord("z") + 1)}
    freq = [0] * 26
    for char in s:
        freq[ord(char) - ord("a")] += 1
    return tuple(freq)


if __name__ == "__main__":
    # Test cases from problem description
    test_cases = [
        # (input, expected_output_groups - order doesn't matter)
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),
        ([""], [[""]]),  # Single empty string
        (["a"], [["a"]]),  # Single character
        (
            ["", ""],
            [["", ""]],  # Multiple empty strings (anagrams of each other)
        ),
    ]

    for strs, expected in test_cases:
        result = group_anagrams(strs)
        # Sort inner lists for comparison, then sort outer list
        result_sorted = sorted([sorted(g) for g in result])
        expected_sorted = sorted([sorted(g) for g in expected])
        assert result_sorted == expected_sorted, f"{strs}: got {result}, expected {expected}"

    print("All tests passed.")
