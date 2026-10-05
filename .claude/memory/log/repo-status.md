---
name: repo-status
description: "Migration to the English standard — which shelves are done, which are not, and what is still out of sync"
metadata:
  type: project
updated: 2026-10-04
---

Take real lesson/skeleton counts from the `python3 tools/build.py` log; do not copy numbers here.

## Migration to the new standard (started 2026-10-04)

Standard: [[lesson-standard]]. Work **one shelf at a time**; the user approves a shelf before the
next one starts.

| Shelf | Status |
|---|---|
| 04 Distributed systems | ✅ done 2026-10-05 — 6 lessons, HLD icon figures |
| 05 SQL & relational | ✅ done — 12 lessons, English, subsections, every section animated |
| 01–03, 06–12 | ⏳ still Vietnamese, old template (Q&A, labs) |

## Shared UI

- `app.js`, search box, table of contents, home hero: English.
- Removed the "mark as done" button, the `m` shortcut and the home progress bar (user request).
- Subsections (`.subsec` / `h3.ssh`) show in the table of contents. **Not** in `search-index.js`
  yet — searching "2NF" lands on the parent section.

## Still out of sync

- `CLAUDE.md` still describes the old template: Vietnamese prose, layouts A/B/C, Q&A, DSA labs —
  and is itself in Vietnamese. Rewrite only once the user agrees.
- `note` in the other shelves' `category.json`, and `<title>`/meta of `index.html`, are Vietnamese.
- Three old `lab.js` files in `content/05-sql/04-sql-advanced/` are unused but could not be
  deleted (staged changes in git — the user must run `git rm -f`).
- `quiz.html` (Flashcards) is built from Q&A sections; a shelf that drops Q&A loses its cards.

- Figures on one page share one `<style>` scope, so class and keyframe names must be unique per
  figure. Both migrated shelves were namespaced (`f1-`, `f2-` …) after a collision on 2026-10-05; any
  new page needs the same treatment.
