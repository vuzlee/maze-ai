#!/usr/bin/env python3
"""
Vẽ lại bộ icon từ dấu ◆ thương hiệu (cùng hình với `.brand .mk` trong assets/style.css).

  python3 tools/make-icons.py

Sinh: assets/favicon.ico · assets/icon-192.png · assets/icon-512.png · assets/apple-touch-icon.png
Nguồn hình duy nhất là assets/favicon.svg — sửa hình thì sửa cả hai cho khớp.
Chỉ chạy khi đổi logo, không phải sau mỗi lần sửa bài.
"""
import pathlib, sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("cần Pillow:  pip install Pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

BG = (253, 253, 255, 255)       # --bg, only behind the iOS icon
LO = (64, 69, 106)              # --brand-ink #40456A, bottom-left
HI = (133, 147, 216)            # --brand-lt #8593D8, top-right

SS = 8                          # supersample, then downscale

# coordinates on the 32-unit grid of assets/favicon.svg — no tile, just the mark
# the soft M: straight points and ("Q", control, end) quadratic curves, as in the SVG path
PATH = [(5, 26), (5, 10), ("Q", (5, 7), (8, 7)), ("Q", (11, 7), (11, 10)), (11, 15),
        ("Q", (11, 18), (13.5, 18)), ("Q", (16, 18), (16, 15)), (16, 14),
        ("Q", (16, 11), (18.5, 11)), ("Q", (21, 11), (21, 9)), ("Q", (21, 7), (24, 7)),
        ("Q", (27, 7), (27, 10)), (27, 26)]
STROKE = 3
GOAL = [(16, 22), (18.5, 24.5), (16, 27), (13.5, 24.5)]   # the ◆

def flatten(path, n=24):
    """Turn PATH into a polyline, sampling each quadratic curve into n segments."""
    pts = [path[0]]
    for seg in path[1:]:
        if seg[0] == "Q":
            (x0, y0), (cx, cy), (x1, y1) = pts[-1], seg[1], seg[2]
            for i in range(1, n + 1):
                t = i / n
                pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                            (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
        else:
            pts.append(seg)
    return pts

def gradient(size):
    """Chéo từ góc dưới-trái (tối) lên góc trên-phải (sáng), như x1=0 y1=1 → x2=1 y2=0 trong SVG."""
    g = Image.new("RGB", (size, size))
    px = g.load()
    for y in range(size):
        for x in range(size):
            t = (x + (size - 1 - y)) / (2 * size - 2)
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(LO, HI))
    return g

def mark(px, pad_ratio=0.0, opaque=False):
    """Một icon vuông cạnh `px`. pad_ratio > 0 thì chừa lề để iOS bo góc không cắt vào nét."""
    side = px * SS
    pad = round(side * pad_ratio)
    inner = side - 2 * pad
    u = inner / 32.0

    mask = Image.new("L", (inner, inner), 0)
    d = ImageDraw.Draw(mask)
    w = max(1, round(STROKE * u))
    pts = [(x * u, y * u) for x, y in flatten(PATH)]
    d.line(pts, fill=255, width=w, joint="curve")
    for x, y in pts:                                       # round caps + joins (no gaps on curves)
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=255)
    d.polygon([(x * u, y * u) for x, y in GOAL], fill=255)

    plate = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    plate.paste(gradient(inner), (0, 0), mask)

    canvas = Image.new("RGBA", (side, side), BG if opaque else (0, 0, 0, 0))
    canvas.paste(plate, (pad, pad), plate)
    return canvas.resize((px, px), Image.LANCZOS)

def main():
    mark(512).save(OUT / "icon-512.png")
    mark(192).save(OUT / "icon-192.png")
    # iOS tự bo góc và tự đắp nền, nên bản này để đặc và chừa lề
    mark(180, pad_ratio=0.10, opaque=True).convert("RGB").save(OUT / "apple-touch-icon.png")
    # .ico gói nhiều cỡ: trình duyệt cũ và thanh tab hẹp lấy bản 16
    mark(64).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    for f in ("favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        print(f"assets/{f:<22} {(OUT / f).stat().st_size:>7,} B")


if __name__ == "__main__":
    main()
