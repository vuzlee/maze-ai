"""OS group overview as a map (2026-10-09): kernel (kept, no lesson owns system calls) · lessons by resource · that's it.
CPU time / memory / synchronisation subsections dropped: thread-process-gil (scheduling, context switch),
memory-virtual-paging (isolation, page table) and lock-deadlock-race (mutex) already cover them.
Run: python3 tools/svgkit/03-cs-fundamentals/os_overview.py  (re-runnable)"""
# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from groupmap import rewrite, sec, gist, table, order, keep_figure
from overview import Fig, text
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
L = lambda d: "../%s/index.html" % d

PAGE = os.path.join(ROOT, "content/03-cs-fundamentals/02-os/os-overview/index.html")
src = open(PAGE, encoding="utf-8").read()
K = keep_figure(src, "Programs sit on top, hardware at the bottom")
a = src.index("</figure>", src.index("Programs sit on top")) + 9
b = src.index("</ul>", a) + 5
KAFTER = src[a:b]
T = table("osmap", "WHAT THE KERNEL SHARES · ONE LESSON EACH · READ TOP TO BOTTOM",
  "A table of three shared resources, in reading order, each linking to its lesson. CPU time: the scheduler gives each process or thread a short turn, lesson Process, thread and GIL. "
  "Memory: each process sees its own virtual addresses, mapped to RAM by page tables, lesson Virtual memory and paging. "
  "Shared data: threads that touch the same value must take turns, lesson Lock, deadlock and race condition.",
  [(0, "RESOURCE"), (130, "THE KERNEL’S ANSWER"), (420, "LESSON")],
  [("1 · CPU time", "scheduler · time slice · context switch", "Process, thread & GIL", "../../../02-python/04-concurrency/thread-process-gil/index.html"),
   ("2 · Memory", "virtual addresses · page table · TLB", "Virtual memory & paging", L("memory-virtual-paging")),
   ("3 · Shared data", "mutex · semaphore · lock order", "Lock, deadlock & race", L("lock-deadlock-race"))], rowh=36)
BODY = """<header class="hero">
  <p class="eyebrow">CS fundamentals · operating system</p>
  <h1>Operating system <em>overview</em></h1>
  <p class="lede">One machine, many programs: the <b>kernel</b> stands between them and the hardware, and shares out CPU time, memory and access to shared data.</p>
</header>

""" + sec("osov", 1, "Kernel", "Programs never touch hardware directly — they <em>ask the kernel</em>.", K, after=KAFTER) + "\n"  + sec("osov", 2, "Lessons by resource", "Three things many programs want at once; <em>each has its own lesson</em>.", gist(T),
   ["CPU scheduling is taught from the Python side, where threads, processes and the GIL meet it."])
rewrite(PAGE, BODY, "The operating system on one page: the kernel between programs and hardware, and the three things it shares — CPU time, memory, shared data — each with its lesson.",
  "CS fundamentals · operating system · first lesson: <a href=\"../memory-virtual-paging/index.html\">Virtual memory &amp; paging</a>.")
print("ok")
