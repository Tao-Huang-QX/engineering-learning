"""
LeetCode 406: Queue Reconstruction by Height
https://leetcode.com/problems/queue-reconstruction-by-height/

Problem: You are given an array of people where people[i] = [hi, ki] represents the ith
person of height hi with exactly ki other people who have a height greater than or equal
to hi in front. Return the queue reconstructed by the [h, k] attributes.

Constraints:
- 1 <= people.length <= 2000
- 0 <= hi <= 10^6
- 0 <= ki < people.length
- It is guaranteed that the queue can be reconstructed

Examples:
- Input: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
  Output: [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
- Input: people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]
  Output: [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]

Approach: Greedy insertion
- Sort by height descending, then by k ascending
- Insert each person at index k (all taller people already placed)

Time: O(n²) due to list.insert operations   Space: O(n)
"""


def reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
    """
    Return the queue reconstructed by height and k attribute.

    Args:
        people: Array of [height, k] where k is number of people with height >= in front

    Returns:
        Reconstructed queue satisfying all [h, k] constraints
    """
    if len(people) == 1:
        return people

    people.sort(key=lambda x: (-x[0], x[1]))
    queue = []
    for person in people:
        queue.insert(person[1], person)
    return queue


if __name__ == "__main__":
    # Example 1: Mixed heights with varying k values
    result = reconstruct_queue([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]])
    expected = [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]
    assert result == expected, f"Example 1 failed: got {result}, expected {expected}"

    # Example 2: Sorted by height descending
    result = reconstruct_queue([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]])
    expected = [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]]
    assert result == expected, f"Example 2 failed: got {result}, expected {expected}"

    # Eample 3: Single person
    result = reconstruct_queue([[5, 0]])
    assert result == [[5, 0]], ...

    # Example 4: Same height, different k values
    result = reconstruct_queue([[5, 2], [5, 0], [5, 1]])
    assert result == [[5, 0], [5, 1], [5, 2]], ...

    print("All tests passed.")
