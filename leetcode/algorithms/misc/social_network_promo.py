"""
Optimal Promo Starter in Social Network

Problem: Find the starting user ID such that a message reaches the maximum number of users.
Friendship is directed (if A follows B, B may not follow A). A user can only share with friends
who haven't received the message yet.

Approach: Graph traversal
- For each node, run BFS/DFS to count reachable nodes
- Return the node with maximum reach

Time: O(N * (V + E))   Space: O(V + E)
"""

from collections import defaultdict, deque


def social_network_promo(users: int, edges: list[tuple[int, int]]) -> int:
    """
    Find the starting user ID that reaches maximum users via directed sharing.

    Args:
        users: Number of users (user IDs are 0 to users-1).
        edges: List of directed friendship pairs (follower, followee).

    Returns:
        User ID that reaches the most users when starting the message.
    """
    if users == 1:
        return 0

    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)

    def bfs_count(start: int) -> int:
        visited = set()
        visited.add(start)
        queue = deque([start])
        count = 0

        while queue:
            curr = queue.popleft()
            count += 1
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return count

    max_reach = -1
    best_user = 0
    for user in range(users):
        reach = bfs_count(user)
        if reach > max_reach:
            max_reach = reach
            best_user = user

    return best_user


if __name__ == "__main__":
    # Test cases from the problem description
    test_cases = [
        (4, [(0, 1), (1, 2), (2, 1)], 0),  # Starting from 0 reaches most users
        (3, [(0, 1), (1, 2)], 0),  # Linear chain: 0 -> 1 -> 2, so start from 0
        (5, [(0, 1), (0, 2), (1, 3), (2, 4)], 0),  # Star: 0 reaches all
        (4, [(0, 1), (2, 3)], 0),  # Two disconnected pairs, both reach 2 users
        (1, [], 0),  # Single user, no edges
    ]

    for users, edges, expected in test_cases:
        result = social_network_promo(users, edges)
        assert result == expected, (
            f"users={users}, edges={edges}: got {result}, expected {expected}"
        )

    print("All tests passed.")

# solved: YYYY-MM-DD, difficulty, minutes, Social Network Promo
