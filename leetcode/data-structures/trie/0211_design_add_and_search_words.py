"""
LeetCode 211: Design Add and Search Words Data Structure
https://leetcode.com/problems/design-add-and-search-words-data-structure/

Problem: Design a data structure that supports adding new words and finding
if a string matches any previously added word. Search supports '.' wildcard
that matches any single character.

Constraints:
- 1 <= word.length <= 25
- word consists of lowercase English letters or '.'
- At most 10^4 calls will be made to addWord and search
- All words consist of lowercase English letters

Examples:
- Input:
  wd = WordDictionary();
  wd.addWord("a");
  wd.search(".");  // returns True
  wd.addWord("at");
  wd.search(".at"); // returns True
  wd.search("at."); // returns False
  wd.search("a");   // returns True
  wd.search("aa");   // returns False
  wd.search("a");   // returns True

Approach: Trie with backtracking for wildcard search
- Add word: walk/create nodes for each character (same as standard Trie)
- Search without wildcard: direct path lookup
- Search with wildcard (.): backtracking - try ALL children recursively
- When `.` is found, iterate over all children and search each branch
- Tree must support multiple children per node for wildcard search to work

Time: O(L) for add_word, O(26^D) worst case for search with D wildcards
Space: O(total characters added) — each unique prefix creates one node
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    """Dictionary supporting addWord and search with '.' wildcard."""

    def __init__(self):
        """Initialize the data structure."""
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        """
        Add a word to the dictionary.

        Args:
            word: The word to add
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Search for a word in the dictionary.
        Word may contain '.' to match any single character.

        Args:
            word: The word to search for (may contain '.' wildcard)

        Returns:
            True if word matches any word in dictionary, False otherwise
        """
        return self._search_from_node(word, 0, self.root)

    def _search_from_node(self, word: str, idx: int, node: TrieNode) -> bool:
        if idx == len(word):
            return node.is_end

        char = word[idx]

        if char == ".":
            # Wildcard: try ALL children
            for child in node.children.values():
                if self._search_from_node(word, idx + 1, child):
                    return True
            return False
        else:
            # Normal char: follow specific path
            if char not in node.children:
                return False
            return self._search_from_node(word, idx + 1, node.children[char])


if __name__ == "__main__":
    # Example from problem description
    wd = WordDictionary()
    wd.add_word("a")
    assert wd.search("."), "search('.') should match 'a'"
    wd.add_word("at")
    assert wd.search(".t"), "search('.t') should match 'at'"
    assert not wd.search("at."), "search('at.') should not match"
    assert wd.search("a"), "search('a') should match"
    assert not wd.search("aa"), "search('aa') should not match"

    # Additional edge cases
    empty = WordDictionary()
    assert not empty.search("a"), "Empty dict should return False"

    # Wildcard matching
    t = WordDictionary()
    t.add_word("bad")
    t.add_word("dad")
    t.add_word("mad")
    assert not t.search("pad"), "pad should not match"
    assert t.search("bad"), "bad should match"
    assert t.search(".ad"), ".ad should match bad/dad/mad"
    assert t.search("b.."), "b.. should match bad"

    print("All tests passed.")
