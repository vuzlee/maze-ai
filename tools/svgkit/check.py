# -*- coding: utf-8 -*-
"""Soát chồng lấn trong SVG bằng ước lượng bề rộng chữ.

Sáu phép. Phép 4 là phép quan trọng nhất và cũng là phép sinh sau cùng: ba đợt
đầu áp luật 1, bản kiểm cũ báo 0 lỗi mà ảnh chụp vẫn thấy caption đè lên viền
dưới của hàng ô ngay trên nó — vì nó chỉ so chữ-với-chữ và chữ-tràn-ô-bao.
Chữ cắt ngang viền một ô mà không nằm hẳn trong ô đó là lỗi.

    python3 tools/svgkit/check.py <file.svg>...
"""
import re, sys, html

# (cỡ chữ px, hệ số bề rộng trung bình một ký tự) — đo từ style.css của kho.
# Hai lớp nhãn CHỮ HOA có letter-spacing nên rộng hơn hẳn — hệ số đo lại bằng
# getComputedTextLength() trong chrome, không ước bằng mắt: sv-hv thật là 0,79
# chứ không phải 0,62, nên bản cũ báo lọt mọi nhãn panel dài.
W = {'sv-t': (12.5, 0.55), 'sv-s': (11.5, 0.55), 'sv-d': (10.5, 0.52),
     'sv-l': (11, 0.60), 'sv-h': (9.5, 0.78), 'sv-hv': (9.5, 0.80)}
TOL = 0.5          # px bỏ qua, tránh báo nhầm vì ước lượng bề rộng
PANX = 372         # mép trái panel phải — trùng base.PANX

# Đỉnh chữ tính từ baseline. Chữ có dấu tiếng Việt vươn cao hơn chữ Latin trần
# — mũ + dấu thanh chồng lên nhau. Dùng nhầm hệ số 0.8 cho cả hai là lý do ba
# đợt đầu máy báo sạch mà ảnh chụp vẫn thấy caption cắt vào viền ô bên trên.
ASC_PLAIN, ASC_ACCENT = 0.80, 1.00
ACC = ('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
       'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')


def parse(svg):
    vb = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg)
    VW, VH = float(vb.group(1)), float(vb.group(2))
    texts, rects = [], []
    for m in re.finditer(r'<text class="([\w-]+)"([^>]*)>(.*?)</text>', svg, flags=re.S):
        cls, attrs, body = m.group(1), m.group(2), m.group(3)
        if cls not in W:
            raise SystemExit(f"class chưa đăng ký bề rộng: {cls}")
        x = float(re.search(r'x="([-\d.]+)"', attrs).group(1))
        y = float(re.search(r'y="([-\d.]+)"', attrs).group(1))
        anch = (re.search(r'text-anchor="(\w+)"', attrs) or [None, 'start'])[1]
        s = html.unescape(re.sub(r'<[^>]+>', '', body))
        size, k = W[cls]
        w = len(s) * size * k
        if anch == 'middle': x -= w / 2
        elif anch == 'end':  x -= w
        asc = ASC_ACCENT if any(c in ACC for c in s) else ASC_PLAIN
        texts.append(dict(cls=cls, s=s, x=x, y=y, w=w, h=size,
                          top=y - size * asc, bot=y + size * 0.22))
    # chỉ bắt <rect …> viết đủ bốn thuộc tính theo thứ tự của base.rect
    for m in re.finditer(r'<rect x="([-\d.]+)" y="([-\d.]+)" '
                         r'width="([\d.]+)" height="([\d.]+)"', svg):
        x, y, w, h = map(float, m.groups())
        rects.append(dict(x=x, y=y, w=w, h=h))
    return VW, VH, texts, rects


def check(svg, name=''):
    VW, VH, T, R = parse(svg)
    bad = []

    # 1. chữ tràn khỏi viewBox
    for t in T:
        if t['x'] < -1 or t['x'] + t['w'] > VW + 1:
            bad.append(f"tràn viewBox: {t['s'][:42]!r} "
                       f"x={t['x']:.0f}..{t['x']+t['w']:.0f} / {VW:.0f}")
        if t['bot'] > VH + 1:
            bad.append(f"tràn đáy: {t['s'][:32]!r} y={t['bot']:.0f} / {VH:.0f}")

    # 1b. Ô tràn khỏi viewBox. Phép 1 chỉ soi CHỮ, nên một ô vẽ hụt xuống dưới
    # đáy khung thì máy im lặng — chỉ ảnh chụp mới thấy nó bị cắt ngang. Gặp thật
    # ở hình g08 của gradient-boosting.
    for r in R:
        if r['y'] + r['h'] > VH + 1:
            bad.append(f"ô tràn đáy: y={r['y']:.0f}..{r['y']+r['h']:.0f} / {VH:.0f}")
        if r['x'] + r['w'] > VW + 1 or r['x'] < -1:
            bad.append(f"ô tràn ngang: x={r['x']:.0f}..{r['x']+r['w']:.0f} / {VW:.0f}")

    # 2. chữ đè chữ
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            a, b = T[i], T[j]
            if (a['top'] < b['bot'] and b['top'] < a['bot']
                    and a['x'] < b['x'] + b['w'] - 1 and b['x'] < a['x'] + a['w'] - 1):
                bad.append(f"chữ đè chữ: {a['s'][:26]!r} × {b['s'][:26]!r} (y≈{a['y']:.0f})")

    # 3. chữ thò ngang khỏi ô bao nó
    for t in T:
        cands = [r for r in R if r['x'] - 2 <= t['x'] <= r['x'] + r['w']
                 and r['y'] <= t['y'] <= r['y'] + r['h']]
        if not cands:
            continue
        r = min(cands, key=lambda r: r['w'] * r['h'])
        if t['x'] + t['w'] > r['x'] + r['w'] - 3:
            bad.append(f"chữ thò khỏi ô: {t['s'][:40]!r} rộng {t['w']:.0f} "
                       f"> còn {r['x']+r['w']-t['x']-3:.0f}px")

    # 5. chữ SÁT chữ — không đè nhau nên phép 2 im, mà mắt đọc ra dính liền
    # ("0,50lẫn nhất"). Gặp thật ở hình d04 của decision-tree: cột chú thích đặt
    # ngay sau con số, cách 2px. Dưới 5px là dính.
    for i in range(len(T)):
        for j in range(len(T)):
            a, b = T[i], T[j]
            if i == j or not (a['top'] < b['bot'] and b['top'] < a['bot']):
                continue
            gap = b['x'] - (a['x'] + a['w'])
            # bỏ qua cặp nằm hai bên ranh giới bản đồ | panel (x = PANX): chúng
            # cách nhau bằng chính máng 32px, dính là do ƯỚC bề rộng dư ra.
            if a['x'] + a['w'] <= PANX + 2 <= b['x'] + 2:
                continue
            if -1 < gap < 5:
                bad.append(f"chữ sát chữ {gap:.0f}px: {a['s'][:24]!r} | {b['s'][:24]!r} "
                           f"(y≈{a['y']:.0f})")

    # 4. chữ cắt ngang viền một ô — hoặc nằm hẳn trong, hoặc nằm hẳn ngoài
    for t in T:
        tx1, tx2, ty1, ty2 = t['x'], t['x'] + t['w'], t['top'], t['bot']
        for r in R:
            rx1, rx2, ry1, ry2 = r['x'], r['x'] + r['w'], r['y'], r['y'] + r['h']
            if tx1 >= rx2 - TOL or tx2 <= rx1 + TOL:   # không giao theo trục x
                continue
            if ty1 >= ry2 - TOL or ty2 <= ry1 + TOL:   # không giao theo trục y
                continue
            inside = (tx1 >= rx1 - TOL and tx2 <= rx2 + TOL
                      and ty1 >= ry1 - TOL and ty2 <= ry2 + TOL)
            if inside:
                continue
            side = ('viền trên' if ty1 < ry1 < ty2 else
                    'viền dưới' if ty1 < ry2 < ty2 else 'viền cạnh')
            bad.append(f"chữ đè {side} ô: {t['s'][:38]!r} y={t['y']:.0f} "
                       f"× ô y={ry1:.0f}..{ry2:.0f}")
            break
    return bad


if __name__ == '__main__':
    tot = 0
    for p in sys.argv[1:]:
        b = check(open(p, encoding='utf-8').read(), p)
        tot += len(b)
        print(f"== {p}: {len(b)} lỗi")
        for x in b:
            print("   ", x)
    sys.exit(1 if tot else 0)
