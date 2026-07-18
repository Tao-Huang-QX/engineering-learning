"""
LeetCode 208: Implement Trie (Prefix Tree)
https://leetcode.com/problems/implement-trie-prefix-tree/

Problem: Implement a trie (prefix tree) with insert, search, and startsWith methods.

Constraints:
- 1 <= word.length, prefix.length <= 2000
- word and prefix consist only of lowercase English letters
- At most 3 * 10^4 calls will be made to insert, search, and startsWith

Examples:
- Input:
  trie = Trie();
  trie.insert("apple");
  trie.search("apple");   // returns True
  trie.search("app");     // returns False
  trie.startsWith("app"); // returns True
  trie.insert("app");
  trie.search("app");     // returns True

Approach: Trie (Prefix Tree)
- Each node stores children dict (char → node) and is_end flag
- Insert: walk/create nodes for each character, mark is_end at end
- Search: walk nodes, return True only if path exists AND is_end
- startsWith: walk nodes, return True if path exists (ignore is_end)
- Tree structure encodes character sequences via paths, not dict ordering

Time: O(L) per operation where L = word/prefix length
Space: O(total characters) — each unique prefix creates one node
"""


class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False  # Marks complete word


class Trie:
    """Prefix tree supporting insert, search, and prefix operations."""

    def __init__(self):
        """Initialize the trie data structure."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Args:
            word: The word to insert
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True  # Mark complete word

    def search(self, word: str) -> bool:
        """
        Search for a complete word in the trie.

        Args:
            word: The word to search for

        Returns:
            True if the word exists in the trie, False otherwise
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end  # Must be a complete word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.

        Args:
            prefix: The prefix to check

        Returns:
            True if there is any word with this prefix, False otherwise
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True  # Path exists, that's enough


if __name__ == "__main__":
    # Example from problem description
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple"), "search('apple') should return True"
    assert not trie.search("app"), "search('app') should return False"
    assert trie.starts_with("app"), "startsWith('app') should return True"
    trie.insert("app")
    assert trie.search("app"), "search('app') should return True after insert"

    # Additional edge cases
    empty_trie = Trie()
    assert not empty_trie.search(""), "Empty string search should return False"

    # Single character operations
    t = Trie()
    t.insert("a")
    assert t.search("a")
    assert t.starts_with("a")
    assert not t.starts_with("b")

    print("All tests passed.")
