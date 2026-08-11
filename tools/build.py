#!/usr/bin/env python3
"""
Quét cây content/ rồi sinh lại hai file:

  assets/catalog.js       — danh mục kệ + bài (trang chủ và nút bài trước/sau đọc file này)
  assets/search-index.js  — chỉ mục tìm kiếm toàn văn

Chạy lại mỗi khi thêm/sửa/đổi tên bài:  python3 tools/build.py

Nguồn dữ liệu là chính cây thư mục:
  content/<kệ>/category.json          {"name", "note", "books": [thứ tự thư mục bài]}
  content/<kệ>/<bài>/index.html       <article id="art-SLUG" data-title data-tag data-blurb>
Không cần khai báo gì thêm ở chỗ khác.
"""
import re, json, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def text_of(fragment: str) -> str:
    """Bóc thẻ HTML, còn lại chữ thuần để tìm kiếm."""
    s = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def attr(tag: str, name: str) -> str:
    m = re.search(r'%s="(.*?)"' % name, tag, re.S)
    return html.unescape(m.group(1)) if m else ""


def main() -> int:
    catalog, index, problems = [], [], []

    for cat_dir in sorted(p for p in CONTENT.iterdir() if p.is_dir()):
        meta_file = cat_dir / "category.json"
        if not meta_file.exists():
            problems.append(f"{cat_dir.name}/: thiếu category.json")
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        on_disk = sorted(p.name for p in cat_dir.iterdir() if p.is_dir())
        listed = [b for b in meta.get("books", []) if b in on_disk]
        extra = [b for b in on_disk if b not in listed]          # bài mới chưa khai báo thứ tự
        if extra:
            problems.append(f"{cat_dir.name}/category.json: chưa liệt kê {', '.join(extra)} — tạm xếp cuối kệ")
        missing = [b for b in meta.get("books", []) if b not in on_disk]
        if missing:
            problems.append(f"{cat_dir.name}/category.json: liệt kê {', '.join(missing)} nhưng không có thư mục")

        books = []
        for name in listed + extra:
            page = cat_dir / name / "index.html"
            if not page.exists():
                problems.append(f"{cat_dir.name}/{name}/: thiếu index.html — bỏ qua")
                continue
            src = page.read_text(encoding="utf-8")

            m = re.search(r"<article class=\"doc\"[^>]*>", src)
            if not m:
                problems.append(f"{cat_dir.name}/{name}/index.html: không tìm thấy <article class=\"doc\">")
                continue
            tag = m.group(0)
            slug = attr(tag, "id").replace("art-", "")
            title = attr(tag, "data-title")

            secs = re.findall(
                r'<section id="([^"]+)">(.*?)</section>', src[m.end():], re.S)
            rel = f"content/{cat_dir.name}/{name}/index.html"
            for sec_id, body in secs:
                h2 = re.search(r'<div class="sh"><b>(.*?)</b><h2>(.*?)</h2>', body, re.S)
                if not h2:
                    continue
                index.append({
                    "u": f"{rel}#{sec_id}",
                    "b": title,
                    "n": text_of(h2.group(1)),
                    "t": text_of(h2.group(2)),
                    "x": text_of(body),
                })

            books.append({
                "dir": name,
                "slug": slug,
                "title": title,
                "tag": attr(tag, "data-tag"),
                "blurb": attr(tag, "data-blurb"),
                "n": len(secs),
                "path": rel,
            })

        catalog.append({
            "dir": cat_dir.name,
            "name": meta["name"],
            "note": meta.get("note", ""),
            "books": books,
        })

    banner = "/* SINH TỰ ĐỘNG bởi tools/build.py — đừng sửa tay. */\n"
    (ROOT / "assets" / "catalog.js").write_text(
        banner + "window.CATALOG = " + json.dumps(catalog, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    (ROOT / "assets" / "search-index.js").write_text(
        banner + "window.SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")

    nbooks = sum(len(c["books"]) for c in catalog)
    print(f"catalog.js      : {len(catalog)} kệ · {nbooks} bài")
    print(f"search-index.js : {len(index)} mục")
    for p in problems:
        print("  ! " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
