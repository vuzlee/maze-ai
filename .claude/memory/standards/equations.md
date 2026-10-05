---
name: equations
description: "Why MazeAI uses the .eq template instead of KaTeX; LaTeX look must cover all three places (.eq display, .mth inline, sv-m in SVG); .eq vs <pre> and <code> vs .mth boundaries; drawing curves with SVG"
metadata:
  type: feedback
updated: 2026-10-04
---

Decided 2026-09-03: display equations use the HTML `.eq` template (template 9 in `kit.html`),
**not** KaTeX/MathJax.

**Why not KaTeX.** Of 58 `<pre>` blocks with math symbols, only ~12 were real display equations;
the rest were *derivations* — annotations, tables of numbers, multi-line reasoning — which KaTeX
would break. Bundling KaTeX offline costs ~1.3 MB to serve 12 blocks, leaving two parallel systems.
The real pattern in this repo is **one formula + a note per symbol**, which `.eq` covers. KaTeX
would also break the "opens from `file://`" property.

**Deciding reason.** Aligning ASCII math by eye is wrong: `f̂` is two code points but one display
cell, so brackets drift 1–2 columns. `.eq` lets the browser align.

**Boundary.** `.eq` is only for a standalone formula; derivations stay in `<pre><code>`. Known
limit: no integrals, matrices or nested fractions — if that need appears, reconsider KaTeX.
Usage details live in section 09 of `kit.html` and in `CLAUDE.md`.

## Curves are drawn in SVG, never with characters

Characters cannot draw a curve, only hint at one. Conventions so every line chart looks like a set:

- `viewBox="0 0 900 NNN"`, plot area **x from 96 to 730**, labels at **x=744**.
- **Compute coordinates from a formula and print them**, never type them by hand — only then do
  curves cross at the right place.
- Each label gets **its own y**, spaced out manually; the browser will not do it.
- Use the four semantic colours, not brand colour.

## LaTeX look — built with CSS, no library (2026-09-07)

What was missing was the **typeface**, not the layout. Follow TeX typesetting rules:

| Thing | Markup | Rule |
|---|---|---|
| font | `--math` = Newsreader → Georgia → Times | Newsreader lacks `‖ √ Σ ∇`, the fallbacks cover them |
| variable | `<var>x</var>` | **variables italic** |
| function name | `<b class="fn">min</b>` | **functions upright**: min, max, log, exp, softmax |
| fraction | `<span class="frac"><i>num</i><i>den</i></span>` | a real bar, not `/` |
| term note | `<em>` inside `.t` | not in LaTeX; keep it |

Digits stay upright — never wrap them in `<var>`.

**A fraction always becomes `.frac`, even if one line would be readable.** A `/` between two terms
(`<span class="op">/</span>`) is always unpaid `.frac` debt.

`.frac` uses `vertical-align:middle`, `.eq .line` uses `align-items:center`; baseline alignment
makes `max` float up and fractions sink. In SVG there is no `.frac`: numerator at `y-7`, `<line>`
at `y`, denominator at `y+11`.

## The LaTeX look must cover ALL THREE places

| Place | Wrong | Right |
|---|---|---|
| display formula | — | `.eq` |
| symbol **in running text** | `<code>λ</code>` — monospace says "type this" | `.mth` = `<span class="mth"><var>λ</var></span>` |
| formula **inside `<svg>`** | `class="sv-h"` — spaced monospace capitals | `class="sv-m"`, variables in `<tspan class="v">` |

**`<code>` vs `.mth`** — ask: *can you type this into a machine?* `reg_lambda`, `RidgeCV` →
`<code>`. `λ`, `‖w‖²`, `Σ|w|` → `.mth`.

**Trap:** `<tspan>` is valid **only in SVG**; in HTML use `<var>`. Register `sv-m` in the `W` table
of `check.py` **and** `CW` in `base.py`, or `check.py` stops with "unregistered class width".

## Term notes on one row — built with grid

`.eq .line` is a **two-row grid**: row 1 formula, row 2 notes; `.eq .t` is `display:contents` so its
two children fall into those rows. With flex, taller terms (with `.frac`) pushed their notes down.
`.eq{overflow-x:auto}` for long formulas on narrow screens.

**Never set `display:inline-flex` on `.eq .t>span:first-child`** — flex trims spaces at both ends of
each text node ("from <var>a</var> to" becomes "froma to"). Keep `display:inline`.
