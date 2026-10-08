---
name: lesson-standard
description: "Current lesson standard (set 2026-10-04): English only, no Q&A, learn through animated figures, sections with subsections, minimal common knowledge. Reference: shelf 05-sql."
metadata:
  type: feedback
updated: 2026-10-04
---

Replaces every older template (layouts A/B/C, Vietnamese prose, Q&A, labs). The user set it while
reworking the SQL shelf on 2026-10-04: everything in English, no Q&A, mostly easy-to-read
animations — learning happens through the figures, text only supports them.

**Reference lessons: the whole `content/05-sql/` shelf (12 lessons).** Open
`02-relational-basics/db-normalization/` and `03-sql-basics/sql-join/` in a browser before
writing a new lesson.

## Language

- **Repo content is English only**: lessons, figure text, `aria-label`, `data-blurb`, footers,
  `category.json`, UI strings, `CLAUDE.md`, and these memory notes.
- **Talk to the user in Vietnamese.** Only the conversation is Vietnamese.
- Example names are English (Alice, Bob, Carol, Dan); cities Paris / Rome / Oslo.

**Why:** the user is migrating the whole site to English; they said so twice on 2026-10-04.
**How to apply:** never write Vietnamese into a file in this repo; reply in chat in Vietnamese.

## Seven rules

1. **English only** — see above.
2. **No Q&A section**, no lab, no `.note`.
3. **Every section and every subsection has one animated figure.** Tables and bullets go *with*
   a figure, never instead of one. The user repeated this twice — a table on its own is a defect.
4. **Text supports the figure**: each section = one-line `.key` + figure + at most one line of
   syntax + up to 3 bullets.
5. **Sections hold subsections** when there are several peer parts: 1NF/2NF/3NF are subsections
   of *Normalization*, not top-level sections. Markup is in `CLAUDE.md`.
   The first section is `Mental model` unless the problem name is clearer (e.g. `Anomalies`).
   **Split down to one item per figure**: when a section lists several variants (INNER/LEFT/RIGHT/FULL,
   NOT NULL/UNIQUE/CHECK/DEFAULT, RANK/DENSE_RANK, each anomaly, each isolation anomaly), each one is
   its own subsection with its own figure — never one combined figure for all of them. The user
   asked for this on 2026-10-05.
   **Up to 4 levels** (user, 2026-10-07): section `03` → `3.1` → `3.1.2` → `3.1.2.1`. Nest a
   `.subsec` inside a `.subsec`; numbering lives in `h3.ssh b`. Figures sit only on leaf levels; a
   middle level carries one `.skey` line. Open a level only when it has ≥2 children, and use depth
   only where the topic needs it — a lesson should stay **minimal** (the user cut the decision-tree
   3-level plan back to a simpler one the same day). **Symmetric pairs** (classification ↔
   regression) get the same children, same order, same figure kind.
6. **Minimal but complete common knowledge** — what a beginner will certainly meet. The SQL shelf
   needed DDL/DML/DCL, data types, composite/surrogate keys, self join, CASE/COALESCE, UNION,
   locks/deadlock. Drop deep material (MVCC, N+1, formal functional dependencies).
7. **One lesson, one topic, no overlap.** Keep a group overview only when the group's lessons are
   competing variants; for a sequential group (like SQL) drop it and state the learning order in
   exactly one place, the shelf overview.

## Figures

**Pick the visual vocabulary the field already uses** (user, 2026-10-05): SQL lessons draw tables;
distributed-systems lessons draw **HLD diagrams** — icons for user, browser, server, database,
cache, load balancer, queue, CDN, worker, joined by arrows. The reader should recognise the picture
from real architecture diagrams. Classic concepts keep their classic picture: CAP is a three-circle
Venn diagram first, then one figure per basic case (normal, CP, AP, CA).

**Figure quality bar = the classical-ML lessons** (`content/07-machine-learning/05-classical-ml/`,
e.g. `knn`), user 2026-10-05. Copy their notation and animation, not their content:
caption line in muted caps · centred table cells with a muted header (second line for type/formula)
and a rule under it · amber outline on what is being looked at *now* · results as tinted pills or
cells · dashed leader lines to short coloured notes · the SQL being run in a box with an amber bar
on the executing line · an execution-order strip of boxes along the bottom, last box amber · steps
revealed in execution order, rows sliding into the result table. Table-shaped topics use
`tools/svgkit/tablefig.py`; architecture topics use `tools/svgkit/hldfig.py` (HLD icons + `send()`:
an arrow draws in and a labelled packet rides along it, so every message visibly travels). Overlapping
states of one node must hide the earlier one (`hide=`) — two labels never show at once. (`Fig`, `Table`, `Query`, `strip`, `pill`, `leader`, `callout`).
Size the `viewBox` to the content (640–720 wide) so text stays readable; never leave empty space.
To see the animation, pause it at chosen times with `/tmp/frames.py`-style CDP screenshots —
a reduced-motion screenshot only shows the end state.

**Common knowledge only** — basic cases, not internals. The user rejected a first distributed shelf
that went into Raft terms, PACELC and log replication: "common thôi, k cần quá kĩ".


Animation technique follows [[animated-figures]] (keyframes inside each `<svg>`'s `<style>`,
`opacity`+`transform` only, wrapped in `prefers-reduced-motion`, plays once when scrolled into view).
Learned on the SQL shelf:
- when a new state is drawn over an old cell, **paint a `var(--bg)` backing first** — otherwise the
  old text shows through (hit in DML, surrogate key, deadlock);
- lines between two tables stop at **the table edge**, never cross a text column — put the key
  column next to the connecting edge;
- labels beside a figure need room: check at 1000px, long labels collide.

## How to check

`python3 tools/build.py` with no warnings, `python3 tools/soat.py` with no line for the shelf you
touched, then **screenshot with headless Chrome** (`--force-prefers-reduced-motion` shows the end
state) and look at every figure. The SQL figure generator script is not in the repo — rebuild from
the existing HTML.

DSA lessons follow [[dsa-lesson-prompt]] on top of these rules.

## Shelf overviews

No Mental model section (user, 2026-10-08). A shelf overview answers four learner questions —
what is it · where am I / what is in this shelf · how did it grow · in what order to learn — but
**each shelf draws them with the picture its own field uses**. Do not stamp one template (rings +
building + generic timeline) on every shelf: the user rejected that on 2026-10-08 ("dập khuôn quá";
DSA history should be a family tree of structures, not a dated timeline).
History is drawn only when it explains why things look the way they do.

**How to work (user, 2026-10-08):** act as a design pair. Before building, look at outside sources
(roadmaps, textbooks, classic diagrams of the field), then **propose first** — a table per overview
with sections and the figure for each — and wait for approval. The user liked this flexible
proposal style.

Applied to shelves 01–08 on 2026-10-09 (user: "apply hết đi"). Shape of every overview now:
**01 = gallery of the field's real pictures** (tiles drawing each concept's classic shape, each a
link — `gallery()` in `tools/svgkit/overview.py`), then 1–2 field-specific figures (DSA family tree
+ problem→technique; Python life of a line + lineage; CS type-a-URL; Distributed growing with load
+ what becomes hard; SQL pendulum + types + commands; NoSQL one data system; ML taxonomy + AI
summers/winters; DL learned features + timeline), then Learning order. Trees read top-down
(NeetCode style). One script per page in `tools/svgkit/<shelf>/<slug>_overview*.py`.
Content with no owning lesson stays in the overview: SQL commands (DDL/DML/DCL), RL subsection in ML.

Accent colours (user, 2026-10-08): the palette is blue-periwinkle, so figures use only its
neighbours — `--brand`, `--filled`, `--violet` (pointer/highlight), `--rose` (wall/wrong). No
amber/brown `--probe` and no green `--ok` in new figures.

**Group overviews (2026-10-09, pilot Optimizer):** a group overview must not teach its lessons.
The old Optimizer overview held all content while its five lessons were skeletons; it was split
(`tools/svgkit/08-deep-learning/optimizer_split.py`, sections moved verbatim) and rebuilt as family
tree (top-down, arrows labelled "what it fixes") · same-valley race · comparison table · learning
order (`optimizer_overview_v2.py`). Applied the same day to every written group overview
(variant groups: tree + side-by-side + table; sequential groups: short map, `tools/svgkit/groupmap.py`).
Known gaps with no owning lesson: agglomerative + GMM clustering, ranking metrics (MAP/NDCG), RL, SQL DDL/DCL.
