---
name: animated-figures
description: "How to build ANIMATED figures — the cover-the-text test, nine construction rules, technical traps already hit, four-layer check, seven-step workflow. Reference: shelf 05-sql"
metadata:
  type: feedback
updated: 2026-10-04
---

This note says **how a figure runs**; [[lesson-standard]] says **what a lesson contains**.

**Reference: the `content/05-sql/` shelf.**

## Root principle: cover all the text and it must still make sense

Cover every `<text>` in the figure. What remains — boxes, arrows, colour, motion — **must be enough
to understand what is happening**. If not, the figure illustrates the text instead of replacing it.
Every rule below follows from this test.

## Nine rules

**1 · One figure, one idea — if the title needs "and", split it.** "Append and concat" is two figures.

**2 · Animate in execution order, with a "now running" badge.** The running line of code sits in a
badge at the top edge and changes per step (`a = [1, 2]` → `b = a` → `b.append(3)`). The reader
always knows which line they are on.

**3 · Map the operation onto the data: connector + outline of the exact scope.** A `b[0] = 9` badge
needs a dashed line down to **the exact cell** it changes, and that cell is outlined. A floating
badge the reader has to match up is where the cover-the-text test fails first.

**4 · Values change gradually; write the timeline before the code.** Cell `1` does not jump to `9`;
it is outlined, then changes. **Write the timeline in words before any Python** — which step shows
when, how long it holds. Encoding an agreed timeline is cheap; moving timings inside written code is
expensive.

**5 · Colour shows relationships: together means same colour.** Everything belonging to one object
shares a colour; the wrong branch is `--tomb`, the right one `--ok`. Colour here is **relationship**,
not decoration — the four semantic colours in `CLAUDE.md` keep their meaning.

**Brand colour in figures — allowed only as a neutral surface.** Memory cells, scope frames, stack
slots are **neutral containers**; brand colour there means "plain cell, nothing has happened yet",
and the semantic colours mark what changes.

> Brand colour may be used for **neutral surfaces**. It must **never** carry meaning —
> right/wrong/pointer/result stay `--ok`/`--tomb`/`--probe`/`--filled`.

Use `--brand`; `--clay`/`--clay-a` are old aliases that still work. `soat.py` check 3 only catches a
`<rect>` **filled solid** with brand colour; a 0 there does **not** prove correct use — still look.

**6 · Fewer connectors — let behaviour replace arrows.** Two cells lighting up together already say
they are related; an arrow adds clutter. Show a shallow copy by **changing two cells in two matrices
at once**, with no arrow between them.

**7 · Draw the real structure, outline only what matters.** Stack is a frame, heap is a frame, names
live in the stack, objects in the heap — as in the machine. Outline in bold only what this section
is about; outline everything and nothing stands out.

**8 · Numbers come from code, and say so when a request is untrue.** Every number in a figure must
be reproducible, never estimated. If asked to draw something that does not match real behaviour,
**say so** instead of drawing it anyway.

**9 · One figure, one cycle, played once when scrolled into view.** `linear 1 forwards` + the
`IntersectionObserver` block at the end of the lesson, threshold 0.4, click to replay. Hold at 100%,
no `infinite`, no fade-out keyframe. The whole `animation:` block lives inside
`@media (prefers-reduced-motion:no-preference)`; animate only `opacity` and `transform`.

## Technical traps already hit

| # | Trap | Symptom | Fix |
|---|---|---|---|
| 1 | **`fly` exists only in the keyframe, no static copy** | element disappears with animation off | the moving element must already sit at its final spot in `<g transform="translate(...)">`; the keyframe only *brings it there* |
| 2 | **`loop=True` together with `window`** | figure loops but the viewport is cropped | drop `loop`; play once and stop is the default |
| 3 | **`window` crops too early** | last step falls outside `viewBox` | compute height from the lowest element **after** adding every `translate` |
| 4 | **`str.replace` corrupts the file** | fixes one spot, breaks another, or hits a duplicate string | regenerate the whole `<svg>` block; do not patch strings in generated HTML |
| 5 | **`check.py` reports false "text overlap"** | two labels share coordinates but **not time** | not a bug — `check.py` sees only the end state; compare each `<g>`'s visible window first |
| 6 | **bare `<` inside `<text>` of an `<svg>`** | HTML renders, but every SVG parser fails | escape as `&lt;` |
| 7 | **every step drawn ON TOP of the same spot** | the final frame shows only a few groups; reduced-motion version nearly empty | give each step its own row/column; count groups still at `opacity:1` at 100% |
| 8 | **`opacity="0"` on the `<g>` itself** | with animation off the group vanishes | the hidden initial state belongs INSIDE the reduced-motion media query: `.k3{opacity:0;animation:…}`; `tools/svgkit/anim.py` does this |
| 9 | **new state drawn over an old cell without a backing** | old text shows through the new cell | paint a `var(--bg)` rect first (SQL shelf, 2026-10-04) |

Hit a new trap? Add it here so it does not repeat — and if a machine can catch it, patch
`tools/svgkit/check.py` ([[tools-and-checks]]).

## Four-layer check

In order; a layer must be clean before the next:

1. **Numbers** — every number comes from the generator, with an `assert` against the source.
2. **Geometry** — `tools/svgkit/check.py` is the sieve (overflowing `viewBox`, overlapping text);
   `getBBox` in a browser is the referee. For animated figures the overlap check **false-alarms
   systematically** (trap #5): run it on the **static version** for the real number.
3. **Static version** — turn on reduced motion and read again: the figure must be complete. Catches
   trap #1; no machine does this for you.
4. **Animated version** — watch one full run: step order matches execution order, and the badge
   changes at the right moment.

## Seven-step workflow

1. **Write the timeline in words** — step, when it shows, how long it holds.
2. **Fix the numbers** and write `assert`s for them.
3. **Build the static version first** — fully readable without a single keyframe.
4. **Add keyframes** following step 1, `opacity` and `transform` only.
5. **Run `check.py`**, fix geometry.
6. **Run the four-layer check.**
7. `python3 tools/build.py`, then open in a browser — [[tools-and-checks]].

## Traps found reviewing the ML shelf (2026-10-06)

- **Splice must replace, never wrap.** Several splice scripts wrapped a new `<figure class="gist">` around an
  existing one, so the figure showed 2–4 nested grey frames. Replace the whole old `<figure>…</figure>`.
  Check: `<figure` and `</figure>` counts match and no `<figure…>\s*<figure` on the page.
- **Measure the viewBox in a browser, not by guessing.** `python3 tools/svgkit/clipcheck.py <pages>` renders
  each figure's final state and lists content spilling past the viewBox; `tools/svgkit/fitviewbox.py` grows
  the viewBox to fit. Regex checks missed every case (moved `<g transform>` groups).
- **Math is always LaTeX-looking**: in SVG use `class="sv-m"` with variables in `<tspan class="v">`, never a
  monospace font; in HTML use `.eq` / `span.mth`. `x_i^2` must stack: `<var>x</var><span class="ss"><sup>2</sup><sub>i</sub></span>`.
  Monospace stays only for real code (`JOIN … ON`, `x = "local"`).
- **Worked math beats labels**: the chain rule reads best as stacked fractions filled in step by step
  (dy/du = 2u = 14, × du/dx = 2 → 28); growth/decay as small plots of cⁿ with one word each, not a legend.
- **General notation first**: column heads `x₁, x₂` with the domain name small under them; end with the
  general form (`x′ = f(x₁, x₂)`).
- **Highlight rings sit outside the cells they ring** (e.g. `R(x-3, …)` around a row starting at x=0), so they
  poke past the viewBox and get sliced on the left. Two fixes, both in place since 2026-10-06:
  `figure.gist svg{overflow:visible}` in style.css, and `python3 tools/svgkit/padviewbox.py <pages>` which
  measures every element with all opacity forced on (mid-animation rings included) and widens the viewBox by
  8px where needed. **Run padviewbox on every page after generating figures.** clipcheck only sees the final frame.
