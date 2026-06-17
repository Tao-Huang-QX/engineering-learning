"""
Prime Numbers from 2 to N

Problem: Find all prime numbers from 2 to a given positive integer n.

Approach: Sieve of Eratosthenes
- Create boolean array of size n+1, initially all True
- Mark multiples of each prime starting from 2 as False
- Collect indices that remain True (these are primes)

Time: O(n log log n)   Space: O(n)
"""


def solve(num: int) -> list[int]:
    """Return all prime numbers from 2 to num inclusive."""
    if num < 2:
        return []

    # Sieve of Eratosthenes
    is_prime = [True] * (num + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(num ** 0.5) + 1):
        if is_prime[i]:
            # Mark all multiples of i as non-prime
            for j in range(i * i, num + 1, i):
                is_prime[j] = False

    return [i for i in range(2, num + 1) if is_prime[i]]


if __name__ == "__main__":
    test_cases = [
        (11, [2, 3, 5, 7, 11]),
        (2, [2]),
        (1, []),
        (20, [2, 3, 5, 7, 11, 13, 17, 19]),
        (3, [2, 3]),
    ]

    for num, expected in test_cases:
        result = solve(num)
        assert result == expected, f"{num}: got {result}, expected {expected}"

    print("All tests passed.")

    # Print output for example
    print("Example output for 11:", " ".join(map(str, solve(11))))

# solved: 2026-06-17, easy, 10min, Prime Numbers Sieve
