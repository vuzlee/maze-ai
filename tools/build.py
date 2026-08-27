#!/usr/bin/env python3
"""
Quét cây content/ rồi sinh lại hai file:

  assets/catalog.js       — danh mục kệ → nhóm → bài (trang chủ và nút bài trước/sau đọc file này)
  assets/search-index.js  — chỉ mục tìm kiếm toàn văn

đồng thời ghi lại khối meta chuẩn trong <head> của mọi trang (mô tả, favicon, thẻ chia sẻ)
— xem sync_head(). Khối này sinh từ data-title/data-blurb nên sửa bài là nó tự khớp theo.

Chạy lại mỗi khi thêm/sửa/đổi tên bài:  python3 tools/build.py

Nguồn dữ liệu là chính cây thư mục:
  content/<kệ>/category.json                 {"name", "note", "groups": [{"dir", "name", "books"}]}
  content/<kệ>/<nhóm>/<bài>/index.html       <article id="art-SLUG" data-title data-tag data-blurb>
Không cần khai báo gì thêm ở chỗ khác.
"""
import re, json, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


SITE = "MazeAI"
THEME = "#14110E"          # --bg, để thanh trình duyệt trên mobile không lệch màu trang

HOME_DESC = ("Kiến thức nền cho kỹ sư data, machine learning và AI, viết bằng tiếng Việt: "
             "mười kệ từ cấu trúc dữ liệu và SQL tới Transformer, LLM và MLOps. Mỗi bài đi từ "
             "cơ chế bên dưới tới hệ quả thực tế, kèm code, sơ đồ và lab bấm được.")
KIT_DESC = ("Bộ khuôn hình dùng chung của MazeAI — chép đoạn HTML, thay chữ, "
            "tự co giãn và tự đúng bảng màu.")

# Khối meta nằm gọn giữa </title> và dòng preconnect, nên thay lại được mà không đụng
# tới <title> viết tay hay phần font/stylesheet phía dưới.
HEAD_SLOT = re.compile(
    r'(</title>\n).*?(<link rel="preconnect" href="https://fonts\.googleapis\.com">)', re.S)


def head_meta(base: str, title: str, desc: str, og_type: str, manifest: bool) -> str:
    """Khối meta chuẩn của một trang. `base` là số cấp ../ để về gốc kho."""
    e = lambda v: html.escape(v, quote=True)
    lines = [
        f'<meta name="description" content="{e(desc)}">',
        '<meta name="color-scheme" content="dark">',
        f'<meta name="theme-color" content="{THEME}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{SITE}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:image" content="{base}assets/icon-512.png">',
        '<meta name="twitter:card" content="summary">',
        f'<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">',
        f'<link rel="alternate icon" href="{base}assets/favicon.ico" sizes="any">',
        f'<link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">',
    ]
    if manifest:
        # chỉ trang chủ mới khai báo manifest: mở bằng file:// thì trình duyệt
        # không nạp được manifest và sẽ kêu ở console, không cần lặp ở 171 trang bài.
        lines.append('<link rel="manifest" href="site.webmanifest">')
    return "\n".join(lines)


def sync_head(page: pathlib.Path, src: str, base: str, title: str, desc: str,
              og_type: str, manifest: bool, problems: list) -> bool:
    """Ghi lại khối meta cho một trang. Chạy lại nhiều lần vẫn ra đúng một kết quả."""
    if not HEAD_SLOT.search(src):
        problems.append(f"{page}: <head> không theo khuôn (thiếu </title> hoặc dòng preconnect) — bỏ qua meta")
        return False
    out = HEAD_SLOT.sub(
        lambda m: m.group(1) + head_meta(base, title, desc, og_type, manifest) + "\n" + m.group(2),
        src, count=1)
    if out == src:
        return False
    page.write_text(out, encoding="utf-8")
    return True


def text_of(fragment: str) -> str:
    """Bóc thẻ HTML, còn lại chữ thuần để tìm kiếm."""
    s = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def attr(tag: str, name: str) -> str:
    m = re.search(r'%s="(.*?)"' % name, tag, re.S)
    return html.unescape(m.group(1)) if m else ""


def read_book(page: pathlib.Path, rel: str, index: list, problems: list, touched: list):
    """Đọc một bài: trả về metadata cho catalog, đồng thời nạp các mục vào chỉ mục tìm kiếm."""
    src = page.read_text(encoding="utf-8")
    m = re.search(r"<article class=\"doc\"[^>]*>", src)
    if not m:
        problems.append(f"{rel}: không tìm thấy <article class=\"doc\">")
        return None
    tag = m.group(0)
    title = attr(tag, "data-title")
    blurb = attr(tag, "data-blurb")

    # data-base phải đúng số cấp ../ để về gốc kho, sai là gãy hết assets/ và link chéo
    depth = rel.count("/")
    want = "../" * depth
    got = attr(re.search(r"<html[^>]*>", src).group(0), "data-base")
    if got != want:
        problems.append(f'{rel}: data-base="{got}" — phải là "{want}"')
    if sync_head(page, src, want, title, blurb or title, "article", False, problems):
        touched.append(rel)

    secs = re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>', src[m.end():], re.S)
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

    return {
        "dir": page.parent.name,
        "slug": attr(tag, "id").replace("art-", ""),
        "title": title,
        "tag": attr(tag, "data-tag"),
        "blurb": blurb,
        "n": len(secs),
        "path": rel,
        "skeleton": bool(attr(tag, "data-skeleton")),
    }


def main() -> int:
    catalog, index, problems, touched = [], [], [], []

    for cat_dir in sorted(p for p in CONTENT.iterdir() if p.is_dir()):
        meta_file = cat_dir / "category.json"
        if not meta_file.exists():
            problems.append(f"{cat_dir.name}/: thiếu category.json")
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        declared_groups = meta.get("groups", [])
        on_disk = sorted(p.name for p in cat_dir.iterdir() if p.is_dir())
        listed = [g["dir"] for g in declared_groups]
        for extra in [g for g in on_disk if g not in listed]:
            problems.append(f"{cat_dir.name}/category.json: chưa khai báo nhóm {extra} — bỏ qua")
        for miss in [g for g in listed if g not in on_disk]:
            problems.append(f"{cat_dir.name}/category.json: khai báo nhóm {miss} nhưng không có thư mục")

        groups = []
        for g in declared_groups:
            grp_dir = cat_dir / g["dir"]
            if not grp_dir.is_dir():
                continue
            books_on_disk = sorted(p.name for p in grp_dir.iterdir() if p.is_dir())
            order = [b for b in g.get("books", []) if b in books_on_disk]
            tail = [b for b in books_on_disk if b not in order]
            if tail:
                problems.append(f"{cat_dir.name}/{g['dir']}: chưa liệt kê {', '.join(tail)} — tạm xếp cuối nhóm")
            for miss in [b for b in g.get("books", []) if b not in books_on_disk]:
                problems.append(f"{cat_dir.name}/{g['dir']}: liệt kê {miss} nhưng không có thư mục")

            books = []
            for name in order + tail:
                page = grp_dir / name / "index.html"
                if not page.exists():
                    problems.append(f"{cat_dir.name}/{g['dir']}/{name}/: thiếu index.html — bỏ qua")
                    continue
                book = read_book(page, f"content/{cat_dir.name}/{g['dir']}/{name}/index.html",
                                 index, problems, touched)
                if book:
                    books.append(book)
            groups.append({"dir": g["dir"], "name": g["name"], "books": books})

        catalog.append({
            "dir": cat_dir.name,
            "name": meta["name"],
            "note": meta.get("note", ""),
            "groups": groups,
        })

    for name, desc, manifest in (("index.html", HOME_DESC, True), ("kit.html", KIT_DESC, False)):
        f = ROOT / name
        if not f.exists():
            problems.append(f"{name}: không có file")
            continue
        src = f.read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", src, re.S).group(1)
        if sync_head(f, src, "", html.unescape(title), desc, "website", manifest, problems):
            touched.append(name)

    banner = "/* SINH TỰ ĐỘNG bởi tools/build.py — đừng sửa tay. */\n"
    (ROOT / "assets" / "catalog.js").write_text(
        banner + "window.CATALOG = " + json.dumps(catalog, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    (ROOT / "assets" / "search-index.js").write_text(
        banner + "window.SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")

    ngroups = sum(len(c["groups"]) for c in catalog)
    nbooks = sum(len(g["books"]) for c in catalog for g in c["groups"])
    print(f"catalog.js      : {len(catalog)} kệ · {ngroups} nhóm · {nbooks} bài")
    print(f"search-index.js : {len(index)} mục")
    print(f"meta trong head : {len(touched)} trang được ghi lại" if touched else "meta trong head : đã khớp")
    for p in problems:
        print("  ! " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
