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

BG = (20, 17, 14, 255)          # --bg   #14110E
CLAY_HI = (238, 158, 122)       # --clay-hi #EE9E7A
CLAY_LO = (201, 106, 68)        # nhánh tối của gradient .mk

SS = 8                          # khử răng cưa bằng cách vẽ to rồi thu nhỏ

# toạ độ theo khung 32 đơn vị, đúng bằng assets/favicon.svg
RADIUS = 9
BARS = [(7, 8, 18, 3), (7, 14.5, 10, 3), (14, 21, 11, 3)]


def gradient(size):
    """Chéo 145° từ --clay-hi xuống nhánh tối, xấp xỉ bằng nội suy theo (x+y)."""
    g = Image.new("RGB", (size, size))
    px = g.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size - 2)
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(CLAY_HI, CLAY_LO))
    return g


def mark(px, pad_ratio=0.0, opaque=False):
    """Một icon vuông cạnh `px`. pad_ratio > 0 thì chừa lề để iOS bo góc không cắt vào nét."""
    side = px * SS
    pad = round(side * pad_ratio)
    inner = side - 2 * pad
    u = inner / 32.0                                   # 1 đơn vị khung 32

    tile = gradient(inner)
    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner - 1, inner - 1], radius=round(RADIUS * u), fill=255)

    plate = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    plate.paste(tile, (0, 0), mask)

    d = ImageDraw.Draw(plate)
    for x, y, w, h in BARS:
        d.rounded_rectangle([x * u, y * u, (x + w) * u, (y + h) * u], radius=1.5 * u, fill=BG)

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
