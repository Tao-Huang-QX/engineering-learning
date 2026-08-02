"""
LeetCode 323: Number of Connected Components in an Undirected Graph
https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

Problem: Given n nodes labeled from 0 to n - 1 and a list of undirected edges, count the number of connected components in an undirected graph.

Constraints:
- 1 <= n <= 2000
- 1 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= ai <= bi <= n - 1
- ai != bi
- No duplicate edges
- Graph is undirected

Examples:
- Input: n = 5, edges = [[0,1], [1,2], [3,4]]
  Output: 2
  Explanation: Components: {0,1,2} and {3,4}

- Input: n = 5, edges = [[0,1], [1,2], [2,3], [3,4]]
  Output: 1
  Explanation: All nodes are connected.

Approach: Union-Find (Disjoint Set Union) with path compression and union by rank
- Initialize each node as its own parent (n separate components)
- For each edge, union the two nodes: find their roots, merge if different
- Path compression in find(): flatten tree structure for future queries
- Union by rank: attach smaller tree under larger to keep trees balanced
- Count unique roots at end — each root represents one component

Time: O(E × α(n)) — α is inverse Ackermann, practically O(1)
Space: O(n) — parent and rank arrays
"""


def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count the number of connected components in an undirected graph.

    Args:
        n: Number of nodes (labeled 0 to n-1)
        edges: List of undirected edges

    Returns:
        Number of connected components
    """
    """
    adj = [[] for _ in range(n)]
    # Add edges (undirected = add both directions)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    components = 0
    for i in range(n):
        if not visited[i]:
            components += 1
            visited[i] = True
            stack = [i]
            while stack:
                node = stack.pop()
                for neighbor in adj[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
    return components
    """
    parent = list(range(n))
    rank = [0] * n  # Track tree depth for union by rank

    def find(x: int) -> int:
        """Find root with path compression"""
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        """Union by rank - attach smaller tree under larger"""
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1

    # Union all edges
    for u, v in edges:
        union(u, v)

    # Count unique roots
    unique_root = {find(i) for i in range(n)}
    return len(unique_root)


if __name__ == "__main__":
    # Example 1: n = 5, edges = [[0,1], [1,2], [3,4]]
    # Graph: 0-1-2  and  3-4 (two components)
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2

    # Example 2: n = 5, edges = [[0,1], [1,2], [2,3], [3,4]]
    # Graph: 0-1-2-3-4 (one component)
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1

    # Example 3: n = 4, edges = []
    # Graph: 0, 1, 2, 3 (four isolated nodes)
    assert count_components(4, []) == 4

    print("All tests passed.")
