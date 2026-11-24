"""
LeetCode 297: Serialize and Deserialize Binary Tree
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Problem: Serialization converts a data structure into a sequence so it
can be stored or transmitted and reconstructed later. Design an
algorithm to serialize and deserialize a binary tree. There is no
restriction on the format — you only need to guarantee that
deserialize(serialize(root)) rebuilds the exact original tree.

Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -1000 <= Node.val <= 1000

Examples:
- Input: root = [1,2,3,null,null,4,5]
  Output: [1,2,3,null,null,4,5]   (round trip)

- Input: root = []
  Output: []                       (empty tree round trip)

Approach: Level-order wire format with explicit nulls
- serialize: level-order traversal (BFS queue) emitting two child slots
  per real node (value or N); nulls spawn nothing — slots pin the
  wiring, so the stream is self-describing
- deserialize: level-order rebuild — the iterator is the shared cursor;
  each dequeued real parent consumes exactly two tokens (left, right),
  N leaves the slot empty

Time: O(n) both directions   Space: O(n)
"""

# Definition for a binary tree node.
from collections import deque


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "TreeNode | None" = None,
        right: "TreeNode | None" = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        """
        Encode a tree into a single string.

        Args:
            root: Root of the tree to encode (may be None)

        Returns:
            Encoded string from which the identical tree can be rebuilt
        """
        tokens: list[str] = []
        queue: deque[TreeNode | None] = deque([root])
        while queue:
            cur = queue.popleft()

            if cur is None:
                tokens.append("N")
                continue

            tokens.append(str(cur.val))
            queue.append(cur.left)
            queue.append(cur.right)

        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        """
        Decode the encoded string back to the original tree.

        Args:
            data: String produced by serialize

        Returns:
            Root of the rebuilt tree, or None for an empty tree
        """
        tokens = iter(data.split(","))
        first = next(tokens)
        if first == "N":
            return None

        root = TreeNode(int(first))
        queue: deque[TreeNode] = deque([root])
        while queue:
            node = queue.popleft()
            tok = next(tokens)
            if tok != "N":
                node.left = TreeNode(int(tok))
                queue.append(node.left)

            tok = next(tokens)
            if tok != "N":
                node.right = TreeNode(int(tok))
                queue.append(node.right)

        return root


if __name__ == "__main__":

    def build(values: list[int | None]) -> TreeNode | None:
        """Build a tree from a level-order list (LeetCode style)."""
        if not values:
            return None
        root = TreeNode(values[0])  # pyright: ignore[reportArgumentType]
        queue = [root]
        i = 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values):
                node.left = TreeNode(values[i]) if values[i] is not None else None  # pyright: ignore[reportArgumentType]
                if values[i] is not None:
                    queue.append(node.left)  # pyright: ignore[reportArgumentType]
                i += 1
            if i < len(values):
                node.right = TreeNode(values[i]) if values[i] is not None else None  # pyright: ignore[reportArgumentType]
                if values[i] is not None:
                    queue.append(node.right)  # pyright: ignore[reportArgumentType]
                i += 1
        return root

    def to_list(root: TreeNode | None) -> list[int | None]:
        """Flatten a tree back to a level-order list (trailing Nones trimmed)."""
        if root is None:
            return []
        out: list[int | None] = []
        queue = [root]
        while queue:
            node = queue.pop(0)
            out.append(node.val if node else None)
            if node:
                queue.append(node.left)  # pyright: ignore[reportArgumentType]
                queue.append(node.right)  # pyright: ignore[reportArgumentType]
        while out and out[-1] is None:
            out.pop()
        return out

    codec = Codec()

    # Round trip: classic mixed tree
    tree1 = [1, 2, 3, None, None, 4, 5]
    assert to_list(codec.deserialize(codec.serialize(build(tree1)))) == tree1, (
        f"Round trip failed: {to_list(codec.deserialize(codec.serialize(build(tree1))))}"
    )

    # Edge: empty tree
    assert to_list(codec.deserialize(codec.serialize(None))) == [], "Empty tree"

    # Edge: single node
    assert to_list(codec.deserialize(codec.serialize(build([1])))) == [1], "Single node"

    # Edge: left-skewed chain
    tree2 = [1, 2, None, 3, None, 4]
    assert to_list(codec.deserialize(codec.serialize(build(tree2)))) == tree2, "Left skew"

    # Edge: right-skewed chain
    tree3 = [1, None, 2, None, 3]
    assert to_list(codec.deserialize(codec.serialize(build(tree3)))) == tree3, "Right skew"

    # Edge: negative values survive the encoding
    tree4 = [1, -2, 3, None, -4]
    assert to_list(codec.deserialize(codec.serialize(build(tree4)))) == tree4, "Negatives"

    print("All tests passed.")


# solved: 2026-11-24, hard, 90min, Serialize and Deserialize Binary Tree
