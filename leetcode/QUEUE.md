# LeetCode Problem Queue

Following [labuladong's algorithm roadmap](https://labuladong.online/zh/roadmap/algo/) for systematic pattern-based learning.

Work through in order. Check off as completed.

| # | LC | Problem | Diff | Pattern |
|---|-----|---------|------|---------|
| 1 | 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | E | Hash map complement |
| 2 | 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | E | One pass, running min |
| 3 | 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | E | Set membership |
| 4 | 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | E | Frequency map / Counter |
| 5 | 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | M | Hash key from sorted tuple |
| 6 | 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | M | Prefix/suffix |
| 7 | 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | E | Two pointers |
| 8 | 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | E | Read/write two pointers |
| 9 | 15 | [3Sum](https://leetcode.com/problems/3sum/) | M | Sort + two pointers + dedupe |
| 10 | 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | E | Stack matching |
| 11 | 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | E | Bisect template |
| 12 | 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | M | Modified binary search |
| 13 | 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | E | Iterative pointer flip |
| 14 | 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | E | Dummy head merge |
| 15 | 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | E | Floyd slow/fast |
| 16 | 104 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | E | Recursive DFS |
| 17 | 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | M | BFS with deque |
| 18 | 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | E | DFS swap children |
| 19 | 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | M | Grid flood fill |
| 20 | 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | M | Graph cycle / topo BFS |
| 21 | 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | M | Sliding window |
| 22 | 567 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | M | Fixed-size sliding window |
| 23 | 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | M | Monotonic stack |
| 24 | 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | M | heapq size-k |
| 25 | 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | M | Kadane |
| 26 | 198 | [House Robber](https://leetcode.com/problems/house-robber/) | M | 1D DP take/skip |
| 27 | 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | E | Fibonacci-style DP |
| 28 | 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | M | Unbounded knapsack DP |
| 29 | 133 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | M | BFS/DFS + clone map |
| 30 | 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | M | Counter + heap/bucket |
| 31 | 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | M | Two pointers |
| 32 | 167 | [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | M | Two pointers |
| 33 | 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | H | Two pointers |
| 34 | 16 | [3Sum Closest](https://leetcode.com/problems/3sum-closest/) | M | Two pointers |
| 35 | 18 | [4Sum](https://leetcode.com/problems/4sum/) | M | Two pointers + dedupe |
| 36 | 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | M | Sliding window |
| 37 | 763 | [Partition Labels](https://leetcode.com/problems/partition-labels/) | M | Sliding window |
| 38 | 340 | [Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) | M | Sliding window |
| 39 | 438 | [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | M | Sliding window |
| 40 | 81 | [Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | M | Modified binary search |
| 41 | 154 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | M | Modified binary search |
| 42 | 162 | [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | M | Binary search |
| 43 | 82 | [Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) | M | Linked list pointers |
| 44 | 86 | [Partition List](https://leetcode.com/problems/partition-list/) | M | Linked list pointers |
| 45 | 143 | [Reorder List](https://leetcode.com/problems/reorder-list/) | M | Linked list pointers |
| 46 | 148 | [Sort List](https://leetcode.com/problems/sort-list/) | M | Merge sort on list |
| 47 | 234 | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | M | Linked list reverse |
| 48 | 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | H | Linked list reverse |
| 49 | 61 | [Rotate List](https://leetcode.com/problems/rotate-list/) | M | Linked list pointers |
| 50 | 138 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | M | Hash map clone |
| 51 | 94 | [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) | E | Recursive DFS |
| 52 | 98 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | M | BST properties |
| 53 | 100 | [Same Tree](https://leetcode.com/problems/same-tree/) | E | Recursive DFS |
| 54 | 101 | [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | E | Recursive DFS |
| 55 | 105 | [Construct from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | M | Tree construction |
| 56 | 106 | [Construct from Inorder and Postorder](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | M | Tree construction |
| 57 | 572 | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | E | Tree comparison |
| 58 | 210 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | M | Graph topo BFS |
| 59 | 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | M | BFS on grid |
| 60 | 1306 | [Jump Game III](https://leetcode.com/problems/jump-game-iii/) | M | BFS on graph |
| 61 | 64 | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | M | 2D DP |
| 62 | 62 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | M | 2D DP |
| 63 | 1143 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | M | 2D DP |
| 64 | 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | M | DP on strings |
| 65 | 72 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | M | DP on strings |
| 66 | 55 | [Jump Game](https://leetcode.com/problems/jump-game/) | M | Greedy |
| 67 | 45 | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | M | Greedy |
| 68 | 122 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | M | Greedy |
| 69 | 406 | [Queue Reconstruction by Height](https://leetcode.com/problems/queue-reconstruction-by-height/) | M | Greedy |
| 70 | 46 | [Permutations](https://leetcode.com/problems/permutations/) | M | Backtracking |
| 71 | 78 | [Subsets](https://leetcode.com/problems/subsets/) | M | Backtracking |
| 72 | 39 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | M | Backtracking |
| 73 | 208 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | M | Trie data structure |
| 74 | 211 | [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | M | Trie data structure |
| 75 | 190 | [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | E | Bit manipulation |
| 76 | 191 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | E | Bit manipulation |
| 77 | 231 | [Power of Two](https://leetcode.com/problems/power-of-two/) | E | Bit manipulation |
| 78 | 145 | [Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/) | E | Recursive DFS |
| 79 | 450 | [Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) | M | BST operations |
| 80 | 701 | [Insert into a BST](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | M | BST operations |
| 81 | 236 | [Lowest Common Ancestor of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | M | Tree traversal |
| 82 | 323 | [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | M | Graph traversal |
| 83 | 63 | [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | M | 2D DP with obstacles |
| 84 | 97 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | M | 2D DP |
| 85 | 300 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | M | 1D DP + binary search |
| 86 | 309 | [Best Time with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | M | DP with states |
| 87 | 123 | [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) | M | DP with states |
| 88 | 47 | [Permutations II](https://leetcode.com/problems/permutations-ii/) | M | Backtracking + dedupe |
| 89 | 90 | [Subsets II](https://leetcode.com/problems/subsets-ii/) | M | Backtracking + dedupe |
| 90 | 40 | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | M | Backtracking + dedupe |
| 91 | 352 | [Data Stream as Disjoint Intervals](https://leetcode.com/problems/data-stream-as-disjoint-intervals/) | H | Heap with lazy deletion |
| 92 | 480 | [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) | H | Two heaps |
| 93 | 212 | [Word Search II](https://leetcode.com/problems/word-search-ii/) | H | Trie + DFS |
| 94 | 201 | [Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | M | Bit manipulation |
| 95 | 847 | [Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | H | BFS + bitmask |
| 96 | 23 | [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | H | Divide & conquer / heap |

**Hard problems:** 33, 48, 91, 92, 93, 95, 96 (7 problems)
