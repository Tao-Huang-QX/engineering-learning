"""
LeetCode 133: Clone Graph
https://leetcode.com/problems/clone-graph/

Problem: Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

Approach: BFS/DFS + clone map
- Dictionary tracks visited nodes: original -> clone (acts as visited set)
- Create clone BEFORE processing neighbors (so cycle can find it)
- Stack/queue handles traversal, dictionary prevents revisiting

Time: O(V + E)   Space: O(V) Vertice Edge
"""

from __future__ import annotations


class Node:
    def __init__(self, val: int = 0, neighbors: list[Node] | None = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Node | None) -> Node | None:
    """
    Return a deep copy of the connected graph starting from the given node.

    Args:
        node: Reference node in the original graph

    Returns:
        Reference node in the cloned graph, or None if input is None
    """
    """
    if not node:
        return None
    clones = {}
    def dfs(original: Node) -> Node:
        # Recursively clone a node and all its neighbors
        if original not in clones:
            # Create clone and store it BEFORE recursing
            clones[original] = Node(original.val)
            # Recursively clone all neighbors
            for neighbor in original.neighbors:
                clones[original].neighbors.append(dfs(neighbor))
        return clones[original]
    return dfs(node)
    """
    if not node:
        return None

    clones = {}
    stack = [node]  # Can use deque for BFS
    clones[node] = Node(node.val)  # pyright: ignore[reportInvalidTypeArguments]

    while stack:
        curr = stack.pop()
        for neighbor in curr.neighbors:
            if neighbor not in clones:
                clones[neighbor] = Node(neighbor.val)
                stack.append(neighbor)
            clones[curr].neighbors.append(clones[neighbor])

    return clones[node]


if __name__ == "__main__":
    # Example 1: Single node
    n1 = Node(1)
    assert clone_graph(n1).val == 1  # pyright: ignore[reportOptionalMemberAccess]

    # Example 2: Two connected nodes
    n1 = Node(1)
    n2 = Node(2)
    n1.neighbors = [n2]
    n2.neighbors = [n1]
    cloned = clone_graph(n1)
    assert cloned.val == 1  # pyright: ignore[reportOptionalMemberAccess]
    assert cloned.neighbors[0].val == 2  # pyright: ignore[reportOptionalMemberAccess]
    assert cloned.neighbors[0].neighbors[0].val == 1  # pyright: ignore[reportOptionalMemberAccess]
    assert cloned is not n1  # Deep copy, not same reference

    # Example 3: Three nodes in line
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.neighbors = [n2]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2]
    cloned = clone_graph(n1)
    assert cloned.val == 1  # pyright: ignore[reportOptionalMemberAccess]
    assert cloned.neighbors[0].val == 2  # pyright: ignore[reportOptionalMemberAccess]
    assert cloned.neighbors[0].neighbors[1].val == 3  # pyright: ignore[reportOptionalMemberAccess]

    print("All tests passed.")
