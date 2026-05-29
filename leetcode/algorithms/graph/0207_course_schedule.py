"""
LeetCode 207: Course Schedule
https://leetcode.com/problems/course-schedule/

Problem: Given numCourses and prerequisites, determine if you can finish all courses.
Return false if there's a cycle (impossible to complete).

Approach: Kahn's algorithm (BFS topological sort)
- Build graph, prereq -> dependent courses, count in_degrees
- Start with course having 0 prerequisites (in_degree = 0)
- Process each course, remove its outgoing edges, decrement neighbors' in_degrees
- If neighbor's in_degree becomes 0, add to queue
- If processed count < total courses, there's a cycle

Time: O(V + E)   Space: O(V + E) V = num_courses, E = len(prerequisites)
"""

from collections import defaultdict, deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determine if all courses can be finished given prerequisites.

    Args:
        num_courses: Total number of courses (labeled 0 to num_courses-1)
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        True if all courses can be finished (no cycle), False otherwise
    """
    """
    Recursion solution:
    def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
        # Build graph: course -> [prerequisites]
        graph = {i: [] for i in range(num_courses)}
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        # 0=unvisited, 1=visiting, 2=visited
        state = [0] * num_courses
        def has_cycle(node: int) -> bool:
            if state[node] == 1:  # currently in path → cycle!
                return True
            if state[node] == 2:  # already processed
                return False
            state[node] = 1  # mark as visiting
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True
            state[node] = 2  # mark as visited
            return False
        for course in range(num_courses):
            if has_cycle(course):
                return False
        return True
    """
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Initialize queue with courses having no prerequisites
    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    count = 0

    while queue:
        course = queue.popleft()
        count += 1
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return count == num_courses


if __name__ == "__main__":
    # Example 1: Simple chain, no cycle
    assert can_finish(2, [[1, 0]])

    # Example 2: Cycle between two courses
    assert not can_finish(2, [[1, 0], [0, 1]])

    # Example 3: Multiple valid courses
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])

    # Example 4: No prerequisites
    assert can_finish(1, [])

    print("All tests passed.")
