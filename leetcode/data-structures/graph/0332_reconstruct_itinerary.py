"""
LeetCode 332: Reconstruct Itinerary
https://leetcode.com/problems/reconstruct-itinerary/

Problem: You are given a list of airline tickets where tickets[i] = [from_i, to_i]
represent the departure and the arrival airports of one flight. Reconstruct the
itinerary in order and return it.

All of the tickets belong to a man who departs from "JFK", thus, the itinerary must
begin with "JFK". If there are multiple valid itineraries, you should return the
itinerary that has the smallest lexical order when read as a single string.

You may assume all tickets form at least one valid itinerary. You must use all the
tickets once and only once.

Constraints:
- 1 <= tickets.length <= 300
- tickets[i].length == 2
- from_i.length == 3, to_i.length == 3
- from_i and to_i consist of uppercase English letters.
- from_i != to_i

Examples:
- Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
  Output: ["JFK","MUC","LHR","SFO","SJC"]
  Explanation: The itinerary is a single chain: JFK -> MUC -> LHR -> SFO -> SJC.

- Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
  Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
  Explanation: Another reconstruction ["JFK","SFO","ATL","JFK","ATL","SFO"] is also
    valid but it is larger in lexical order (SFO > ATL at index 1).

Approach: Hierholzer's algorithm (Eulerian path on directed graph)
- Build adjacency with reverse-sorted destinations (pop smallest via O(1) from end)
- DFS from JFK: while outgoing edges exist, pop and recurse
- Post-order append (all edges consumed → dead end), then reverse

Time: O(n log n)   Space: O(n)
"""

from collections import defaultdict


def find_itinerary(tickets: list[list[str]]) -> list[str]:
    """
    Reconstruct the itinerary starting from "JFK" using all tickets exactly once.

    Args:
        tickets: List of [from, to] airport pairs

    Returns:
        Itinerary as a list of airport codes
    """
    # Collect edges
    adjacent = defaultdict(list)
    for origin, destination in tickets:
        adjacent[origin].append(destination)

    # Sort each list in reverse so smallest is at the end (O(1) pop)
    for destinations in adjacent.values():
        destinations.sort(reverse=True)

    result: list[str] = []

    def dfs(airport: str) -> None:
        while adjacent[airport]:
            dfs(adjacent[airport].pop())  # visit smallest available destination
        result.append(airport)  # all edges consumed - dead end

    dfs("JFK")
    return result[::-1]


if __name__ == "__main__":
    # Example 1: single chain
    result1 = find_itinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]])
    expected1 = ["JFK", "MUC", "LHR", "SFO", "SJC"]
    assert result1 == expected1, f"Example 1: got {result1}, expected {expected1}"

    # Example 2: multiple valid, must pick lexicographically smallest
    result2 = find_itinerary(
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    )
    expected2 = ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
    assert result2 == expected2, f"Example 2: got {result2}, expected {expected2}"

    print("All tests passed.")
