# MazeAI memory

**Current standard (since 2026-10-04): everything in the repo is English — lessons, UI, docs and
these notes. Talk to the user in Vietnamese. No Q&A; learning happens through animated figures,
text only supports them.** Reference lessons: the whole `content/05-sql/` shelf — open it in a
browser before writing a new lesson.

## standards/ — how to write

| Note | Contents |
|---|---|
| [Lesson standard](standards/lesson-standard.md) | **read first.** Language rule (repo English, chat Vietnamese) + seven rules: no Q&A · every section and subsection animated · text supports figures · sections → subsections · minimal common knowledge · one lesson one topic. Figure traps from the SQL shelf and how to check |
| [Animated figures](standards/animated-figures.md) | cover-the-text test, nine construction rules, technical traps, four-layer check |
| [Equations](standards/equations.md) | LaTeX-looking formulas in HTML/CSS, no library |
| [Tools and checks](standards/tools-and-checks.md) | `soat.py`, svgkit, what machines miss, how many review rounds |

## log/ — where things stand

| Note | Contents |
|---|---|
| [Repo status](log/repo-status.md) | which shelves are migrated · shared UI · what is still out of sync |

## How to use

Read this file at the start of a session. Record **why** and **where things stand**; do not record
what `CLAUDE.md`, the folder tree or git already says. Delete wrong notes instead of appending
corrections. Keep it under six notes.
Frontmatter: `name` · `description` · `metadata.type` · `updated: YYYY-MM-DD`. Notes are English.
