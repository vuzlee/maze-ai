# Figure tooling (2026-10 English standard)

| Tool | Use |
|---|---|
| `tablefig.py` | build table-shaped animated figures (`Fig`, `Table`, `Query`, `strip`, `pill`, `leader`, `callout`) |
| `hldfig.py` | build HLD / architecture figures (`icon`, `send`, `ring`, `steps`, `frame`, `cut`) on top of tablefig |
| `figns.py page.html …` | give every animated `<svg>` on a page its own class/keyframe prefix (`f1-`, `f2-` …). Run after editing figures. |
| `figfit.py page.html …` | play every figure, measure everything drawn over time, rewrite each `viewBox` to fit (no clipping, no dead space). Idempotent. |
| `figcheck.py page.html …` | play every figure at ~40 moments; report text that overlaps other visible text, or spills outside the svg. Must print `clean`. |
| `frames.py page.html IDX out t1 t2 …` | screenshot figure IDX paused at chosen times (seconds) — the only way to *see* an animation mid-run. |

Order after editing a page: `figns.py` → `figfit.py` → `figcheck.py` → `python3 tools/build.py`.
Run several checks in parallel with different `CDP_PORT=93xx` values.
