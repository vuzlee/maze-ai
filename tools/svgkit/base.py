# -*- coding: utf-8 -*-
"""Nguyên liệu vẽ hình luật 1: primitive SVG + ba khuôn hàng dùng đi dùng lại.

Mỗi bài chỉ cần viết `map.py` (bản đồ riêng của bài) và `gen.py` (phần bóc ô),
import từ đây. Xem tools/svgkit/README.md.
"""

# Ba con số cố định cho mọi hình luật 1 — bản đồ trái, panel phóng to phải.
MAPW, PANX, PANW = 340, 372, 488
VBW = 860

ACC = ('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
       'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')

# Bốn màu ngữ nghĩa của kho, cặp (stroke, biến rgb để pha nền mờ).
BLUE  = ('var(--filled)', 'blue-a')    # dữ liệu, thứ đang xét
AMBER = ('var(--probe)',  'amber-a')   # con trỏ, điểm nhấn, đáp án
RED   = ('var(--tomb)',   'red-a')     # sai, bị loại, chưa thoả
GREEN = ('var(--ok)',     'green-a')   # đúng, kết quả, đã thoả
GREY_S, GREY_T = 'var(--rule-hi)', 'var(--faint)'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def txt(x, y, s, cls='sv-t', fill=None, anchor=None):
    """Chữ. sv-l/sv-h là font mono không có dấu tiếng Việt — tự đổi sang sv-d/sv-hv."""
    if cls in ('sv-l', 'sv-h') and any(c in s for c in ACC):
        cls = {'sv-l': 'sv-d', 'sv-h': 'sv-hv'}[cls]
    a = f' text-anchor="{anchor}"' if anchor else ''
    f = f' fill="{fill}"' if fill else ''
    return f'<text class="{cls}" x="{x}" y="{y}"{f}{a}>{esc(s)}</text>'


# Bề rộng trung bình một ký tự, khớp bảng W của check.py — dùng để ngắt dòng.
CW = {'sv-t': 12.5*0.55, 'sv-s': 11.5*0.55, 'sv-d': 10.5*0.52,
      'sv-l': 11*0.60, 'sv-h': 9.5*0.72, 'sv-hv': 9.5*0.62}

def wrap(s, px, cls='sv-d'):
    """Ngắt chuỗi theo BỀ RỘNG px, cắt ở khoảng trắng.

    Cắt theo số ký tự (s[:44], s[44:]) thì chữ bị đứt giữa từ — 'CHÍNH LÀ B /
    ƯỚC 2'. check.py không bắt được lỗi đó vì hai dòng vẫn nằm gọn trong khung;
    chỉ ảnh chụp mới thấy. Nên mọi chú thích dài phải qua hàm này.
    """
    n = max(1, int(px / CW[cls]))
    lines, cur = [], ''
    for w in s.split(' '):
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= n:
            cur += ' ' + w
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def para(e, x, y, s, px, cls='sv-d', fill='var(--muted)', lh=16):
    """Đoạn chữ nhiều dòng, trả về y của dòng cuối + lh."""
    for ln in wrap(s, px, cls):
        e.append(txt(x, y, ln, cls, fill))
        y += lh
    return y

def rect(x, y, w, h, stroke, rgb=None, alpha='.10', sw='1.6', rx=6, dash=None):
    fl = f'rgba(var(--{rgb}),{alpha})' if rgb else 'none'
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fl}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def vline(x, y1, y2, c, sw='1.2'):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-8}" stroke="{c}" stroke-width="{sw}"/>'
            f'<polygon points="{x},{y2} {x-4.2},{y2-8} {x+4.2},{y2-8}" fill="{c}"/>')


def aline(x1, y, x2, c, sw='1.2'):
    d = 1 if x2 > x1 else -1
    return (f'<line x1="{x1}" y1="{y}" x2="{x2-8*d}" y2="{y}" stroke="{c}" stroke-width="{sw}"/>'
            f'<polygon points="{x2},{y} {x2-8*d},{y-4.2} {x2-8*d},{y+4.2}" fill="{c}"/>')


def hline(x1, y, x2, c='var(--rule)', dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="1"{d}/>'


def dot(x, y, c, r=4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def lens(y_from, y_to, x_from=MAPW+2, x_to=PANX-6):
    """Đường cong đứt nối ô đang sáng bên trái sang panel phóng to bên phải."""
    return (f'<path d="M{x_from} {y_from} C {x_from+14} {y_from}, {x_to-14} {y_to}, {x_to} {y_to}" '
            f'fill="none" stroke="var(--rule-hi)" stroke-width="1" stroke-dasharray="4 4"/>'
            f'<circle cx="{x_to}" cy="{y_to}" r="2.4" fill="var(--rule-hi)"/>')


def panel(title, y=18):
    return txt(PANX, y, title, 'sv-hv')


# ── ba khuôn hàng của panel phải ────────────────────────────────────────────
# Bước y của cả ba đã cộng sẵn khoảng hở an toàn: hàng ô cao H thì trả về
# y + H + GAP, đủ để dòng chữ kế tiếp không đè lên viền dưới của ô.
GAP = 18


def band(e, y, w, col, rgb, head, sub, x=PANX, h=54, alpha='.10', sw='1'):
    """Dải ngang: một câu đậm + một câu nhỏ bên dưới, cả hai NẰM TRONG ô."""
    e.append(rect(x, y, w, h, col, rgb, alpha, sw=sw, rx=5))
    e.append(txt(x+16, y+22, head, 'sv-t', col))
    if sub:
        e.append(txt(x+16, y+40, sub, 'sv-s', 'var(--dim)'))
    return y + h


def row(e, y, left, right, col, rgb, lw=176, h=32, cls='sv-d', x=PANX):
    """Hàng hai cột: ô có viền bên trái, chú thích trần bên phải — cùng một dòng."""
    e.append(rect(x, y, lw, h, col, rgb, '.08', sw='1.2', rx=4))
    e.append(txt(x+12, y+h/2+5, left, cls, col))
    e.append(txt(x+lw+14, y+h/2+5, right, 'sv-d', 'var(--muted)'))
    return y + h + 8


def stack(e, y, head, note, col, rgb, w=None, h=30, x=PANX):
    """Ô có viền, chú thích nằm DƯỚI ô — bước y phải vượt qua viền dưới."""
    w = w or PANW
    e.append(rect(x, y, w, h, col, rgb, '.10', sw='1.3', rx=4))
    e.append(txt(x+12, y+h/2+5, head, 'sv-l', col))
    if note:
        e.append(txt(x+12, y+h+14, note, 'sv-d', 'var(--muted)'))
        return y + h + GAP + 6
    return y + h + 8


def foot(e, y, s, col='var(--dim)', x=PANX):
    e.append(txt(x, y+14, s, 'sv-s', col))
    return y + 20


def title(e, s, col='var(--text)', y=40, x=PANX):
    e.append(txt(x, y, s, 'sv-t', col))
    return y + 14


def build(elems, bottom, name, aria, outdir, pad=8):
    """Ghi ra file .svg, cao vừa đủ phần dài hơn giữa bản đồ và panel."""
    H = bottom + pad
    svg = (f'<svg viewBox="0 0 {VBW} {H}" role="img" aria-label="{aria}">\n'
           + '\n'.join(elems) + '\n</svg>')
    open(f'{outdir}/{name}.svg', 'w', encoding='utf-8').write(svg)
    return H
