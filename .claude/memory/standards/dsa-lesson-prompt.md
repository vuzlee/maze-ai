---
name: dsa-lesson-prompt
description: "The prompt for writing or rewriting one DSA lesson visual-first — three parts, figure script, colours, layout, checks. Pilot: binary-search, approved 2026-10-05."
metadata:
  type: feedback
updated: 2026-10-05
---

The user approved `content/01-dsa/04-algorithms/binary-search/` on 2026-10-05 after four review
rounds ("oke rồi đấy"). Everything below was learned from those rounds. Hand the block under
**Prompt** to an agent as-is, with `<SLUG>` filled in. It overrides the old DSA template in
`CLAUDE.md` (Lab · Common mistakes · Q&A) and adds to [[lesson-standard]].

## Prompt

> Rewrite the DSA lesson `content/01-dsa/<GROUP>/<SLUG>/index.html` **visual-first**. You learn it
> by watching the animations; text only labels what the figure shows. The pilot to copy is
> `content/01-dsa/04-algorithms/binary-search/`. Open it in a browser and click each figure to
> replay it before you start.
>
> **Structure.** Three parts only, and no Lab, Common mistakes, Q&A, `.note` or long code block:
> 1. `Mental model`: what the thing *is* and how to picture it.
> 2. `Properties`
>    - Data-structure lessons: the cost of each operation (index, search, insert, delete, append…),
>      one subsection and one figure per operation.
>    - Algorithm lessons: drop this part and fold the one or two properties that explain the
>      algorithm into Mental model (binary search: *why the list must be sorted*, *O(log n)*).
> 3. `Patterns`: one subsection per pattern, each with figure → `.sig` signals line → the existing
>    `.probs` LeetCode list kept unchanged.
>
> Every subsection has **exactly one animated figure** with a one-line `.skey` above it. Headings
> are plain English nouns that a beginner understands at once. "Why the list must be sorted" beat
> "Monotonic predicate".
>
> **Figure script.** Play the story in order and never show a result before it happens:
> 1. Draw the data (cells fade in left to right, index under each cell).
> 2. Show the goal *on the data itself*. For a known target: dashed ring on its cell and a chip
>    born there that floats to the corner, so the eye never hunts for it. For an unknown answer:
>    the chip sits in the corner.
> 3. Place the pointers at their start positions.
> 4. Run the steps. Each one:
>    - a status line shows the arithmetic (`mid = (0 + 10) // 2 = 5`);
>    - a ring marks the cell being looked at, with a one-line verdict (`a[5] = 31 > 23 → go left`);
>    - discarded cells turn grey;
>    - pointers **slide** to their new index.
> 5. Finish: the answer cell turns solid indigo with `✓ found` under it, plus one summary line
>    (`found at index 4 · 4 steps for 11 cells`). No expanding rings or other celebration.
>
> When the lesson has code: the code box sits **on the left**, the data on the right. One violet
> bar **slides from line to line** in step with the animation, and only the running line is
> highlighted.
>
> Complexity is shown, not stated. Play a concrete case (16 → 8 → 4 → 2 → 1), then turn it into a
> real math graph (axes, ticks, the O(n) line vs the curve drawing itself, dots on sample points).
>
> **Notation.** Short, plain names: `l`, `r`, `mid`, `i`, `j`, `ans`. Not `lo`/`hi`. Use the same
> names in the code, the pointer labels and the status line.
>
> **Colours.** One analogous blue–violet family, always through tokens:
>
> | Token | Means |
> |---|---|
> | `--brand` | pointers (`l`, `r`) |
> | `--violet` | the cell being probed, and the running code line |
> | `--filled` | the goal and the found answer |
> | `--sunk` + `--ghost` text | discarded |
> | `--bg` cells, `--rule-hi` border | untouched data |
>
> No amber, green or red in DSA figures. Every cell looks the same until it has been checked: no
> pre-coloured cells and no phantom slots (e.g. a dashed cell at index `n`).
>
> **Build.**
> - Use the engine in `tools/svgkit/dsa/`: `engine.py` (`Anim` timeline: `show`, `path` for
>   sliding, `static`; `Code`, `cell`, `grey`…) and `binary_search.py` as the worked example.
> - Write one `<slug>.py` per lesson next to them. It writes a JSON of figures that you splice
>   into the page.
> - Keyframe/class prefixes are unique per figure (`m1-`, `q2-`…), since one page shares one
>   style scope.
> - Copy the click-to-replay `<script>` block from the bottom of the binary-search page.
>
> **Check before calling it done.**
> - `python3 tools/build.py` prints no warnings.
> - `python3 tools/soat.py` prints no line for this lesson.
> - Screenshot every figure **mid-animation and at the end** with
>   `python3 tools/svgkit/frames.py <page> <fig-index> <out> <t1> <t2>…`, and look for text
>   overlapping text, text crossing a box edge, and code spilling out of its box.
> - Report which figures you looked at and which you did not.

## Why each rule exists

| Rule | Review round that produced it |
|---|---|
| three parts, no lab / mistakes | the original request |
| algorithms fold Properties into Mental model | round 2: "algo k cần properties cũng đc" |
| ordered story, goal shown first, no phantom cells | round 3: "nhìn k hiểu đang làm gì… mờ phần tử cuối" |
| goal born on its own cell, code left, sliding bar, log graph | round 4 |
| analogous blue–violet palette | round 4: "khoảng màu lân cận như xanh tím" |
| `l`/`r` not `lo`/`hi` · plain finish | round 5 |

## Open

- At ~490px the figures (~760 wide) are cut off or scroll sideways. Not yet decided whether to
  stack code under the data on mobile.
- All 24 DSA lessons follow this prompt (2026-10-05); only `binary-search` is user-approved so far.

## Same palette on the Python and CS shelves (2026-10-05/06)

The user asked for the analogous palette there too. Done by a token swap in figures only:
`--probe`→`--violet`, `--ok`→`--filled`, `--tomb`→`--rose` (new token, `#B83A86`), old
`--filled` data→`--brand`, with the matching `*-a` rgb tokens. Wrong/error keeps its own hue
(rose) because Python figures need a "bad" state; DSA figures do not.
