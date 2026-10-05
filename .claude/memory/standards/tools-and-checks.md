---
name: tools-and-checks
description: "Checking tools (soat.py 8 checks, svgkit), checking the ruler itself, what machines cannot catch, how many review rounds per kind of edit, .eq editing traps"
metadata:
  type: reference
updated: 2026-10-04
---

## Root rule: machine-checkable rules live in `tools/`, not in throwaway scripts

Rewriting the same counting script from scratch each session made numbers incomparable between
sessions. `tools/soat.py` prints 8 groups + a total; `tools/svgkit/` is the shared figure builder
and checker — `anim.py` is the template for **step-by-step animated figures** (one `<g>` per step,
held to 100%, no fade-out). **Do not copy it to `/tmp`**: a fix in `/tmp/A` never reaches `/tmp/B`.
Only a lesson's own generator belongs in `/tmp/<slug>/`. A geometry bug that can recur gets
**patched into `check.py`**, then every finished `.svg` is re-run to make sure the patch adds no
false alarms.

## `tools/soat.py` — 8 checks

| # | Check | Threshold / how it catches |
|---|---|---|
| 1 | Link to a lesson that is still a skeleton | `data-skeleton="1"` |
| 2 | Hard-coded colour in a lesson | **any** hex in `content/` (incl. `lab.js`), except `theme-color` |
| 3 | Brand colour filling a cell in a figure | only `<rect fill="var(--brand\|--clay)">` |
| 4 | Heading that counts ("Three traps") | — |
| 5 | Code line over 92 characters | overflows on mobile |
| 6 | Term translated to Vietnamese | `DICH` + `MIEN` + `KE_RIENG` tables — irrelevant for English lessons |
| 7 | `<title>` differs from `data-title` | must **start** with `data-title` |
| 8 | Missing figures | >2500 words **or** >10 sections without `figure.gist`, or `nsvg < nsec-2` |

Check 7 allows a subtitle after a dash; only a different **name** is an error. **Check 8 is a to-do
list, not pass/fail** — sorted by word count, work from the longest down. Removing a figure can
break check 8; fix it by adding a small figure, not by restoring prose.

Checks 2 and 3 were rewritten on 2026-10-04 for the white palette: before that they compared
against **old hex codes** and stayed at 0 for an empty reason. Check 3 does **not** prove brand
colour is used correctly ([[animated-figures]]).

## Check the ruler itself — more important than the result

A report of all zeros **proves nothing** until the ruler producing it is checked: a broken ruler
and a clean lesson print **the same line**. On 2026-09-07 an over-counting ruler led to acting on
it and **corrupting 81 files**.

1. **A ruler that takes a file list must print how many files it read.** `TOTAL 0` without
   `128 lessons` is meaningless — `sys.argv[1:]` may be empty.
2. **Copy regexes from this file; never retype them from memory.** One missing lookahead turned
   10 violations into 144.
3. **Run it on a known-bad case first.** A ruler that misses a known defect is broken.
4. **An unusually high count = suspect the ruler first, the lessons second.**
5. **Back up before any bulk edit**; restore file by file — never `rm -rf` the tree.
6. Known measuring traps: forgetting to strip `<details>`/`<figure>` inflates counts 7×;
   `s.count('</b>')` also matches `</body>` — **string counting does not replace `html.parser`**.

> **`check.py` is the SIEVE, `getBBox` is the REFEREE.** Fix a figure only when the real bbox also
> complains. When both point at the same spot, it is real.

`check.py` follows `<g transform="translate(…)">` but only `translate` — figures with `scale`/`rotate`
still need a screenshot. Never pass a whole HTML file to `check()` (it takes ONE `<svg>`; it will grab
the 24×24 search icon). **Text-width factors must be MEASURED**: build a sample page, headless Chrome,
`getComputedTextLength()/(len×font-size)` — currently `0.78`/`0.80`. Re-measure after any font/CSS change.

## Seven things machines do NOT catch

1. **Geometrically right, semantically wrong.** SVG y grows **downward**, so "error decreases"
   gets drawn going up. Write an axis-flip function and send every point through it.
2. **Invented numbers in a figure.** Pin them with an `assert` inside the drawing function.
3. **Text touching text** (not overlapping) — every intersection test is blind to adjacency.
4. **A line crossing text.** No check compares text with `<line>`/`<path>`; only a screenshot does.
5. **`check.py` on a whole `index.html`** — ten figures, ten coordinate systems, phantom overlaps.
   **Run per `.svg`.**
6. **HTML template geometry contradicting the prose.** `.cmp two` means "choose A or B"; using it
   for "A runs on B" says the opposite. Read the figure first, the text second.
7. **One colour, one meaning — within each figure.** `--tomb` cannot be both accent and "wrong".

Python trap: `hl=()` is **falsy**, so `keys and not (…)` short-circuits; write `keys is not None and not (…)`.

## How many rounds — do not screenshot every edit

The user once asked why every edit took so long. Screenshots only catch **meaning** errors; text
edits do not create those.

| Kind of edit | Run |
|---|---|
| Text only (lede, captions, bullets) | generate → `tools/build.py`. **No screenshot.** |
| Colour / class / CSS token | add `check.py`. Screenshot **one** representative figure. |
| Coordinates, cells added/removed | all three stages — screenshot **one** figure + **one** top of page. |
| New lesson / new figures | all three stages, screenshot everything. |

**Batch commands**: generate several lessons + `tools/build.py` in one bash call. Headless Chrome at
430px crops every page, even untouched ones — a tool quirk, not a layout bug. When comparing many
`.eq` blocks on one page in `/tmp`, **inline `assets/style.css` freshly from disk**, or the
screenshot lies with stale CSS.

## `.eq` editing traps

- `display:inline-flex` on `.eq .t>span:first-child` trims spaces around text nodes — keep `inline`.
- A regex that wraps `<var>` must run **around** tags, not through them; a second pass produces
  `<var><var>x</var></var>`.
- Inserting via `s.index('  </div>\n', …)` **lands in another section's `.eq`** — anchor on a long
  unique string from the section being edited.
- Square roots need a vinculum: `.eq .ov{border-top:1px solid currentColor}`. Colour classes are
  only `.t.b` `.t.p` `.t.g` `.t.r` — **there is no `.t.a`**.

## Animated figures

Animation lives in each `<svg>`'s `<style>`, so `check.py` and `getBBox` **cannot see it** — they
measure the end state. That is why animated figures need the **four-layer check** in
[[animated-figures]], the last two layers by eye.

## Three manual measurements — copy verbatim

```python
# 1 · words per figure
v = len(re.findall(r'<figure|<svg |class="(?:strip|flow|cmp|stack|mtx|axis|seq|bars|eq|cellrow|cells)\b', s))
t = re.sub(r'<svg.*?</svg>', '', s, flags=re.S); t = re.sub(r'<[^>]+>', ' ', t)
ratio = len(t.split()) / max(v, 1)

# 2 · paragraphs over 33 words on the page — strip <details> and <figure> first,
#     or SVG <text> counts as prose. (?!re\b) is required, or <pre> matches <p...>.
mat = re.sub(r'<details.*?</details>|<figure.*?</figure>', '', s, flags=re.S)
doan = [re.sub(r'<[^>]+>', ' ', p) for p in re.findall(r'<p(?!re\b)[^>]*>(.*?)</p>', mat, re.S)]

# 3 · text inside figures — measure per <br> line, not per block
```
