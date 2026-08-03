"""
LeetCode 847: Shortest Path Visiting All Nodes
https://leetcode.com/problems/shortest-path-visiting-all-nodes/

Problem: You have an undirected, connected graph of n nodes labeled from 0 to n - 1.
You are given an array graph where graph[i] is a list of all the nodes connected
with node i by an edge. Return the length of the shortest path that visits every
node. You may start and stop at any node, you may revisit nodes multiple times,
and you may reuse edges.

Constraints:
- n == graph.length
- 1 <= n <= 12
- 0 <= graph[i][j] < n
- graph[i][j] != i
- All the nodes of the graph are connected

Examples:
- Input: graph = [[1,2,3],[0],[0],[0]]
  Output: 4
  Explanation: One possible path is [1,0,2,0,3]

- Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
  Output: 4
  Explanation: One possible path is [0,1,4,2,3]

Approach: BFS over state space (node, bitmask)
- State = (current_node, visited_mask): an n-bit mask tracks which nodes
  have been visited so far (n ≤ 12 → 2¹² = 4096 states per node, tractable)
- Multi-source BFS: enqueue (node, 1 << node, 0) for every starting node
- Transitions: for each neighbor, new_mask = mask | (1 << neighbor)
- BFS guarantees the first time new_mask == all_visited, the path length
  is minimal — FIFO = level-order traversal over the state graph
- visited[node][mask] boolean array prevents revisiting the same state
  at a longer distance (n × 2ⁿ entries)

Time: O(n² * 2ⁿ) — n nodes × 2ⁿ states, each iterating up to n neighbors
Space: O(n * 2ⁿ) — visited array + BFS queue
"""

from collections import deque


def shortest_path_length(graph: list[list[int]]) -> int:
    """
    Return the length of the shortest path that visits every node.

    Args:
        graph: Adjacency list representation of an undirected, connected graph

    Returns:
        The minimum path length to visit all nodes
    """
    n = len(graph)
    if n == 1:
        return 0

    all_visited = (1 << n) - 1  # e.g., n=4 -> 1111 = 15

    # Multi-source BFS: start from every node simultaneously
    queue = deque()
    # visited[node][mask]: True if state (node, mask) has been enqueued.
    # BFS reaches each state at its shortest distance first - skip on re-encounter
    visited = [[False] * (1 << n) for _ in range(n)]

    for node in range(n):
        mask = 1 << node
        queue.append((node, mask, 0))  # (current_node, visisted_mask, path_length)
        visited[node][mask] = True

    while queue:
        node, mask, length = queue.popleft()

        for neighbor in graph[node]:
            new_mask = mask | (1 << neighbor)
            if new_mask == all_visited:
                return length + 1
            if not visited[neighbor][new_mask]:
                visited[neighbor][new_mask] = True
                queue.append((neighbor, new_mask, length + 1))

    return -1  # unreachable (shouldn't happen, graph is connected)


if __name__ == "__main__":
    # Example 1
    graph1 = [[1, 2, 3], [0], [0], [0]]
    result1 = shortest_path_length(graph1)
    expected1 = 4
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    graph2 = [[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]
    result2 = shortest_path_length(graph2)
    expected2 = 4
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
