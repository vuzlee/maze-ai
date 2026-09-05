# -*- coding: utf-8 -*-
"""Chụp ảnh hình để soát bằng mắt — check.py không thay được bước này.

    python3 tools/svgkit/shot.py <thumuc> <ten>...     # mỗi hình một ảnh
    python3 tools/svgkit/shot.py <thumuc> --page <file.html> [rộng]

Cần google-chrome. Ảnh ra cùng thư mục với .svg.
"""
import subprocess, sys, os

CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                   'assets', 'style.css')
CSS = os.path.abspath(CSS)
CHROME = ['google-chrome', '--headless', '--disable-gpu', '--no-sandbox',
          '--hide-scrollbars', '--virtual-time-budget=3000']


def shoot(d, name, width=920, height=540, scale=2):
    svg = open(f'{d}/{name}.svg', encoding='utf-8').read()
    html = (f'<html><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="file://{CSS}">'
            f'<style>body{{background:var(--bg);margin:0;padding:18px}}'
            f'figure{{margin:0}}svg{{width:100%;height:auto}}</style>'
            f'</head><body><figure class="scrollx">{svg}</figure></body></html>')
    open(f'{d}/{name}.html', 'w', encoding='utf-8').write(html)
    subprocess.run(CHROME + [f'--force-device-scale-factor={scale}',
                             f'--window-size={width},{height}',
                             f'--screenshot={d}/{name}.png', f'{d}/{name}.html'],
                   capture_output=True)
    return f'{d}/{name}.png'


def page(d, path, width=1180, out='page'):
    """Chụp cả trang bài thật — bước cuối, để thấy hình nằm giữa chữ ra sao."""
    subprocess.run(CHROME + ['--force-device-scale-factor=1',
                             f'--window-size={width},2000',
                             '--screenshot=%s/%s.png' % (d, out),
                             f'file://{os.path.abspath(path)}'], capture_output=True)
    return f'{d}/{out}.png'


if __name__ == '__main__':
    d = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == '--page':
        w = int(sys.argv[4]) if len(sys.argv) > 4 else 1180
        print(page(d, sys.argv[3], w))
    else:
        for n in sys.argv[2:]:
            print(shoot(d, n))
