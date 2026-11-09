"""
LeetCode 743: Network Delay Time
https://leetcode.com/problems/network-delay-time/

Problem: You are given a network of n nodes, labeled from 1 to n. You are
also given times, a list of travel times as directed edges times[i] =
(ui, vi, wi), where ui is the source node, vi is the target node, and wi
is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it
takes for all the n nodes to receive the signal. If it is impossible for
all n nodes to receive the signal, return -1.

Constraints:
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n, ui != vi
- 0 <= wi <= 100
- No duplicate (ui, vi) pairs
- All the pairs (ui, vi) are unique (no repeated edges)

Examples:
- Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
  Output: 2
  Explanation: 2->1 costs 1, 2->3->4 costs 2; the last node hears at t=2.

- Input: times = [[1,2,1]], n = 2, k = 1
  Output: 1

- Input: times = [[1,2,1]], n = 2, k = 2
  Output: -1
  Explanation: edges are DIRECTED — node 2 can never reach node 1.

Approach: Dijkstra — BFS with the frontier ordered by TIME, not hops
- Level-BFS fails on weighted edges: first-visit settling assumes
  fewest-hops = earliest, broken by a cheap multi-hop route (1->2 direct
  costs 100; 1->3->4->2 costs 3 — BFS settles 2 at t=100 and returns 100)
- Min-heap of (arrival, node), seeded (0, k): each pop is the earliest
  unprocessed arrival in the graph; nonnegative weights make it FINAL —
  that is Dijkstra's entire correctness argument
- Settle-once at pop time: stale entries (an outdated, larger arrival
  pushed before a better route) are skipped via the seen check
- Relaxation accumulates d + w and pushes only improvements; result = d
  at each settle works because pops are nondecreasing — the last settled
  node is the latest arrival, which is the answer
- BFS IS the degenerate case: unit weights make earliest-time equal
  fewest-hops and the heap collapses to FIFO (0994 Rotting Oranges)
- Precondition: weights >= 0; negative edges need Bellman-Ford

Time: O(E log E)   Space: O(N + E)
Complexity derivation: each edge is examined once (settle-once); each
successful relaxation pushes one heap entry, and every entry is popped
once (including stale ones — lazy deletion in place of decrease-key,
which heapq lacks), so <= 2E heap ops at O(log E) each; log E <= 2 log N
makes O(E log E) = O(E log N). Heap holds <= E entries (bounded by edges,
not nodes); adjacency N + E, dist/seen N.
"""

import heapq
from collections import defaultdict


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """
    Return the time at which the last node receives the signal from k.

    Args:
        times: Directed edges [u, v, w] — signal travels u -> v in time w
        n: Number of nodes, labeled 1..n
        k: Source node

    Returns:
        Max shortest-path distance from k over all nodes; -1 if any node
        is unreachable
    """
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    heap: list[tuple[int, int]] = [(0, k)]  # (arrive time, node)
    dist: dict[int, int] = {k: 0}  # best know arrival per node
    seen: set[int] = set()
    result = 0

    while heap:
        d, u = heapq.heappop(heap)  # earliest unprocessed arrival in the graph

        if u in seen:  # stale entry - a cheaper route already settle u
            continue
        seen.add(u)
        result = d  # pops are nondecreasing: last settle = last arrival

        for v, w in adj[u]:
            candidate = d + w
            if v not in seen and candidate < dist.get(v, float("inf")):
                dist[v] = candidate
                heapq.heappush(heap, (candidate, v))

    return result if len(seen) == n else -1


if __name__ == "__main__":
    # Example 1
    result1 = network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2)
    expected1 = 2
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2
    result2 = network_delay_time([[1, 2, 1]], 2, 1)
    expected2 = 1
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    # Example 3: directed edges — unreachable target
    result3 = network_delay_time([[1, 2, 1]], 2, 2)
    expected3 = -1
    assert result3 == expected3, f"Example 3: got {result3}, expected {expected3}"

    # Edge: single node, no edges — the source already has the signal
    result4 = network_delay_time([], 1, 1)
    expected4 = 0
    assert result4 == expected4, f"Single: got {result4}, expected {expected4}"

    # Edge: the classic Dijkstra discriminator — the cheaper route has MORE hops
    # 1 -> 2 (100) vs 1 -> 3 (1) -> 4 (1) -> 2 (1): node 2 hears at t=3, not 100
    result5 = network_delay_time([[1, 2, 100], [1, 3, 1], [3, 4, 1], [4, 2, 1]], 4, 1)
    expected5 = 3
    assert result5 == expected5, f"Multi-hop cheaper: got {result5}, expected {expected5}"

    # Edge: settle-once discipline — a node popped early must not be re-relaxed
    # 1 -> 2 (5), 1 -> 3 (1), 3 -> 2 (1): node 2's answer is 2 via 3, and the
    # stale heap entry (5, 2) must be ignored when popped later
    result6 = network_delay_time([[1, 2, 5], [1, 3, 1], [3, 2, 1]], 3, 1)
    expected6 = 2
    assert result6 == expected6, f"Stale entry: got {result6}, expected {expected6}"

    print("All tests passed.")


# solved: 2026-11-09, medium, 45min, Network Delay Time
