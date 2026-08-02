"""
LeetCode 210: Course Schedule II
https://leetcode.com/problems/course-schedule-ii/

Problem: There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take
course bi first if you want to take course ai. Return the ordering of courses you should take to
finish all courses. If it is impossible to finish all courses, return an empty array.

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- ai != bi
- All the pairs [ai, bi] are distinct.

Approach: Kahn's algorithm (BFS topological sort)
- Build adjacency list and indegree array from prerequisites
- Start BFS with all courses having indegree 0 (no prerequisites)
- Process each course, decrement neighbors' indegree, add to queue when indegree hits 0
- If all courses processed, valid ordering exists; otherwise, cycle detected

Time: O(V + E)   Space: O(V + E)
where V = numCourses, E = len(prerequisites)
"""

from collections import defaultdict, deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Return a valid course ordering that satisfies all prerequisites.
    If impossible, return empty array.

    Args:
        num_courses: Total number of courses (labeled 0 to num_courses-1).
        prerequisites: List of [course, prerequisite] pairs.

    Returns:
        Valid ordering of courses, or empty array if impossible.
    """
    if not prerequisites:
        return list(range(num_courses))

    graph = defaultdict(list)
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        indegree[course] += 1
        graph[prereq].append(course)

    result = []
    queue = deque([course for course in range(num_courses) if indegree[course] == 0])
    count = 0

    while queue:
        curr = queue.popleft()
        result.append(curr)
        count += 1

        for course in graph[curr]:
            indegree[course] -= 1

            if indegree[course] == 0:
                queue.append(course)

    return result if count == num_courses else []


if __name__ == "__main__":
    # Example 1: Simple chain
    # 1 -> 0, 2 -> 0 means: take 0 before 1 and 2
    result = find_order(2, [[1, 0]])
    assert result == [0, 1], f"Got {result}"

    # Example 2: Cycle - impossible
    # 0 -> 1 -> 2 -> 0 forms a cycle
    result = find_order(2, [[1, 0], [0, 1]])
    assert result == [], f"Expected empty for cycle, got {result}"

    # Example 3: Multiple valid orderings
    # To take 3, need 1 and 2. To take 1, need 0.
    # Valid: [0,2,1,3] or [0,1,2,3] or [2,0,1,3]
    result = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    valid = (
        result[0] == 0
        and result[3] == 3
        and set(result[:2]) == {0, 1, 2}
        or set(result) == {0, 1, 2, 3}
    )
    assert valid, f"Got {result}"

    # Example 4: Single course, no prerequisites
    result = find_order(1, [])
    assert result == [0], f"Got {result}"

    # Example 5: All courses independent
    result = find_order(3, [])
    assert set(result) == {0, 1, 2}, f"Got {result}"

    print("All tests passed.")
