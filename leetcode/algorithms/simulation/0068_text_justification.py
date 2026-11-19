"""
LeetCode 68: Text Justification
https://leetcode.com/problems/text-justification/

Problem: Given an array of strings words and a width maxWidth, format
the text such that each line has exactly maxWidth characters and is
fully (left and right) justified. Pack words greedily — as many as fit
per line. Extra spaces go between words, distributed as evenly as
possible; if they don't divide evenly, leftmost slots get more. The
last line is left-justified with single spaces (padded on the right),
and a line holding a single word is left-justified too. Every word is
guaranteed to fit within maxWidth.

Constraints:
- 1 <= words.length <= 300
- 1 <= words[i].length <= 20
- words[i] consists of only uppercase/lowercase letters and symbols
- 1 <= maxWidth <= 100
- words[i].length <= maxWidth

Examples:
- Input: words = ["This","is","an","example","of","text","justification."],
  maxWidth = 16
  Output: ["This    is    an","example  of text","justification.  "]

- Input: words = ["What","must","be","acknowledgment","shall","be"],
  maxWidth = 16
  Output: ["What   must   be","acknowledgment  ","shall be        "]
  Explanation: the last line is left-justified ("shall be" + padding);
    the middle line holds a single word, so left-justified as well.

- Input: words = ["Science","is","what","we","understand","well","enough",
  "to","explain","to","a","computer.","Art","is","everything","else",
  "we","do"], maxWidth = 20
  Output: ["Science  is  what we","understand      well","enough to explain to",
    "a  computer.  Art is","everything  else  we","do                  "]

Approach: Greedy line packing + per-rule flush (simulation)
- Pack: appending a word to a k-word line costs len(line) spaces (k-1 old
  gaps + 1 new), so the overflow test is line_len + len(line) + len(word)
  > max_width — a bare +1 under-counts for k >= 2 and fuses words into
  width-exact but invalid lines
- Flush interior lines BEFORE inserting the overflowing word: divmod the
  free spaces over the gaps, leftmost gaps take the remainder (i < extra);
  gaps == 0 means a single word — pad it on the right
- The last line survives the loop unflushed, so the left-justified rule
  (" ".join + right pad) lives in one epilogue — no last-line flag needed

Time: O(total characters)   Space: O(max_width) per line buffer
"""


def full_justify(words: list[str], max_width: int) -> list[str]:
    """
    Return the words formatted into fully justified lines of max_width.

    Args:
        words: Words to lay out (each guaranteed to fit max_width)
        max_width: Exact character width every output line must have

    Returns:
        List of lines, each exactly max_width characters: interior lines
        fully justified with even space distribution (left slots get the
        remainder), last line and single-word lines left-justified
    """
    result: list[str] = []
    line: list[str] = []  # words packed into the current line
    line_len = 0  # their total character count, no spaces

    for word in words:
        # does `word` overflow? cost = len(line) spaces: k existing words
        # mean k gaps once the new word lands (k-1 old + 1 new)
        if line and line_len + len(line) + len(word) > max_width:
            spaces = max_width - line_len
            gaps = len(line) - 1
            if gaps == 0:
                # single-word interior line: all padding on the right
                result.append(line[0] + " " * spaces)
            else:
                base, extra = divmod(spaces, gaps)  # leftmost gaps get the remainder
                pieces: list[str] = []
                for i, w in enumerate(line):
                    pieces.append(w)
                    if i < gaps:
                        pieces.append(" " * (base + (1 if i < extra else 0)))
                result.append("".join(pieces))
            line, line_len = [], 0
        line.append(word)
        line_len += len(word)

    # last line: single spaces, pad right - flush it directly
    # line holds >= 1 word here: every flush is immediately followed by
    # an insert, and words is non-empty by contract
    last = " ".join(line)
    result.append(last + " " * (max_width - len(last)))
    return result


if __name__ == "__main__":
    # Example 1: classic full justification with uneven space split
    result1 = full_justify(["This", "is", "an", "example", "of", "text", "justification."], 16)
    expected1 = ["This    is    an", "example  of text", "justification.  "]
    assert result1 == expected1, f"Example 1: got {result1}"

    # Example 2: single-word line and last line are left-justified
    result2 = full_justify(["What", "must", "be", "acknowledgment", "shall", "be"], 16)
    expected2 = ["What   must   be", "acknowledgment  ", "shall be        "]
    assert result2 == expected2, f"Example 2: got {result2}"

    # Example 3: long flowing text
    result3 = full_justify(
        [
            "Science",
            "is",
            "what",
            "we",
            "understand",
            "well",
            "enough",
            "to",
            "explain",
            "to",
            "a",
            "computer.",
            "Art",
            "is",
            "everything",
            "else",
            "we",
            "do",
        ],
        20,
    )
    expected3 = [
        "Science  is  what we",
        "understand      well",
        "enough to explain to",
        "a  computer.  Art is",
        "everything  else  we",
        "do                  ",
    ]
    assert result3 == expected3, f"Example 3: got {result3}"

    # Edge: single word shorter than width — one padded line
    assert full_justify(["hello"], 10) == ["hello     "], (
        f"Single: got {full_justify(['hello'], 10)}"
    )

    # Edge: word exactly the width — no padding possible
    assert full_justify(["0123456789"], 10) == ["0123456789"], (
        f"Exact: got {full_justify(['0123456789'], 10)}"
    )

    # Edge: a lone line is also the last line — left-justified, not full
    assert full_justify(["ab", "cd"], 7) == ["ab cd  "], (
        f"Two words: got {full_justify(['ab', 'cd'], 7)}"
    )

    # Edge: spaces don't divide evenly on an INTERIOR line — left slot
    # gets the remainder: width 9, chars 6, 3 spaces over 2 gaps -> 2 then 1
    assert full_justify(["ab", "cd", "ef", "xxxxx"], 9) == ["ab  cd ef", "xxxxx    "], (
        f"Remainder: got {full_justify(['ab', 'cd', 'ef', 'xxxxx'], 9)}"
    )

    print("All tests passed.")


# solved: 2026-11-19, hard, 60min, Text Justification
