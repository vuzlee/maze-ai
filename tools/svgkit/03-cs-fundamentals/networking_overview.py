"""Networking group overview as a map (2026-10-09): opening a URL (kept sequence = connecting structure) · round trips (kept, spans lessons) · learning order (kept).
Only change: 'Mental model' renamed, ledelist dropped. Run: python3 tools/svgkit/03-cs-fundamentals/networking_overview.py"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
from overview import Fig, text
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
L = lambda d: "../%s/index.html" % d

import re
PAGE = os.path.join(ROOT, "content/03-cs-fundamentals/03-networking/networking-overview/index.html")
s = open(PAGE, encoding="utf-8").read()
s = s.replace('<h2>Mental model</h2>', '<h2>Opening a URL</h2>')
s = re.sub(r'\s*<ul class="ledelist">.*?</ul>', '', s, count=1, flags=re.S)
s = s.replace('<p class="lede">Two machines talking over an unreliable wire.</p>',
  '<p class="lede">Two machines talking over an unreliable wire. Opening a URL takes four steps — DNS, TCP, TLS, HTTP — and each has its lesson.</p>')
s = re.sub(r'<footer>.*?</footer>', '<footer>CS fundamentals · networking · first lesson: <a href="../osi-model/index.html">OSI model</a>.</footer>', s, count=1, flags=re.S)
open(PAGE, "w", encoding="utf-8").write(s)
print("ok")
