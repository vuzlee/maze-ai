/* Lab binary search — a story instead of a control panel.
   Three parts: scenario → step-by-step run with the code line highlighted → takeaway. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("bslab")) return;

  /* ---------- scenarios ---------- */
  var A = [1, 3, 4, 4, 4, 7, 9, 11, 15, 20];

  var CODE = {
    lower: [
      { t: 'lo, hi = 0, len(a)', k: 'init' },
      { t: 'while lo < hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] < t:', k: 'cmp' },
      { t: '        lo = mid + 1', k: 'left' },
      { t: '    else:', k: 'cmp2' },
      { t: '        hi = mid', k: 'right' },
      { t: 'return lo', k: 'done' }
    ],
    upper: [
      { t: 'lo, hi = 0, len(a)', k: 'init' },
      { t: 'while lo < hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] <= t:', k: 'cmp' },
      { t: '        lo = mid + 1', k: 'left' },
      { t: '    else:', k: 'cmp2' },
      { t: '        hi = mid', k: 'right' },
      { t: 'return lo', k: 'done' }
    ],
    exact: [
      { t: 'lo, hi = 0, len(a) - 1', k: 'init' },
      { t: 'while lo <= hi:', k: 'loop' },
      { t: '    mid = lo + (hi - lo) // 2', k: 'mid' },
      { t: '    if a[mid] == t: return mid', k: 'cmp' },
      { t: '    elif a[mid] < t: lo = mid + 1', k: 'left' },
      { t: '    else:            hi = mid - 1', k: 'right' },
      { t: 'return -1', k: 'done' }
    ]
  };

  var SCEN = [
    { id: "lower", t: 4, mode: "lower", label: "find the LEFT edge of 4",
      ask: "The three 4s sit at indices 2, 3, 4. lower_bound must stop exactly at 2.",
      end: function (r) { return "Returns <b>" + r + "</b> — the first index with a[i] ≥ 4. This is the <b>left edge</b> of the duplicate group, used for “first occurrence” questions."; } },
    { id: "upper", t: 4, mode: "upper", label: "find the RIGHT edge of 4",
      ask: "Same array, same target, only one = sign changes in the comparison.",
      end: function (r) { return "Returns <b>" + r + "</b> — the first index with a[i] > 4. The number of 4s = 5 − 2 = <b>3</b>."; } },
    { id: "miss", t: 5, mode: "lower", label: "find a MISSING number (5)",
      ask: "5 is not in the array. Guess what the function returns instead of an error?",
      end: function (r) { return "Returns <b>" + r + "</b> — the position <b>where it would be inserted</b>, not −1. That is why you must always check <code>i &lt; len(a) and a[i] == t</code> before using it."; } },
    { id: "exact", t: 4, mode: "exact", label: "template 1 finds 4",
      ask: "The same array has three 4s. Which of the three will template 1 stop at?",
      end: function (r) { return "Returns <b>" + r + "</b> — <b>some</b> position in the duplicate group, not the left edge. That is why template 1 cannot answer boundary questions."; } }
  ];

  /* ---------- state machine ---------- */
  var cur, lo, hi, mid, step, phase, result, timer = null;

  function build(sc) {
    stopAuto();
    cur = sc;
    var closed = sc.mode === "exact";
    lo = 0; hi = closed ? A.length - 1 : A.length;
    mid = null; step = 0; result = null; phase = "init";
    el("bverdict").hidden = true;
    el("bstep").disabled = false;
    draw();
    say("Initial state", sc.ask);
  }

  function alive() {
    return cur.mode === "exact" ? lo <= hi : lo < hi;
  }

  function next() {
    if (result !== null) return;
    if (phase === "init" || phase === "move") {
      if (!alive()) { finish(cur.mode === "exact" ? -1 : lo); return; }
      phase = "mid";
      mid = lo + Math.floor((hi - lo) / 2);
      step++;
      draw();
      say("Step " + step + " — take the midpoint",
        "mid = " + lo + " + (" + hi + " − " + lo + ") // 2 = <b>" + mid + "</b>, value a[" + mid + "] = <b>" + A[mid] + "</b>.");
      return;
    }
    if (phase === "mid") {
      var v = A[mid], t = cur.t, goRight;
      if (cur.mode === "exact") {
        if (v === t) { phase = "cmp"; draw(); finish(mid); return; }
        goRight = v < t;
      } else if (cur.mode === "lower") {
        goRight = v < t;
      } else {
        goRight = v <= t;
      }
      phase = goRight ? "left" : "right";
      var why;
      if (goRight) {
        why = "a[" + mid + "] = " + v + (cur.mode === "upper" ? " ≤ " : " < ") + t +
          " → mid is <b>surely not</b> the answer, drop it too: <code>lo = mid + 1</code>.";
        lo = mid + 1;
      } else {
        why = "a[" + mid + "] = " + v + (cur.mode === "upper" ? " > " : " ≥ ") + t +
          " → mid <b>may be</b> the answer, so keep it: <code>hi = mid</code>.";
        hi = cur.mode === "exact" ? mid - 1 : mid;
      }
      if (cur.mode === "exact") {
        why = goRight
          ? "a[" + mid + "] = " + v + " < " + t + " → the answer is to the right: <code>lo = mid + 1</code>."
          : "a[" + mid + "] = " + v + " > " + t + " → the answer is to the left: <code>hi = mid - 1</code>.";
      }
      draw();
      say("Step " + step + " — compare, then narrow", why);
      phase = "move";
      return;
    }
  }

  function finish(r) {
    result = r;
    phase = "done";
    mid = null;
    el("bstep").disabled = true;
    stopAuto();
    draw();
    say("Done after " + step + " steps", "The loop stops because the range is empty." +
      (cur.mode === "exact" ? "" : " Now <b>lo == hi == " + lo + "</b> — exactly the boundary we were looking for."));
    var v = el("bverdict");
    v.hidden = false;
    v.innerHTML = cur.end(r) + " A 10-element array, done in <b>" + step + " steps</b> — log₂(10) ≈ 3.3.";
  }

  /* ---------- drawing ---------- */
  function draw() {
    var closed = cur.mode === "exact";
    var hiIx = closed ? hi : hi - 1;      /* last cell still in range */
    var h = '<div class="strip">';
    for (var i = 0; i < A.length; i++) {
      var out = result === null ? (i < lo || i > hiIx) : (i !== result);
      var mk = "";
      if (i === lo && result === null) mk += "lo";
      if (i === mid) mk += (mk ? " " : "") + "mid";
      if (i === hiIx && result === null) mk += (mk ? " " : "") + "hi";
      if (result !== null && i === result) mk = "result";
      h += '<div class="c' + (i === mid ? " on" : "") + (out ? " out" : "") + '">' +
        "<i>" + i + "</i><b>" + A[i] + "</b><u>" + mk + "</u></div>";
    }
    el("bview").innerHTML = h + "</div>";

    var note = el("bnote");
    note.innerHTML = "<span>target = <em>" + cur.t + "</em> · remaining range <em>" +
      (result !== null ? "empty" : (closed ? "[" + lo + ", " + hi + "]" : "[" + lo + ", " + hi + ")")) +
      "</em> · <em>" + Math.max(0, hiIx - lo + 1) + "</em> cells not yet ruled out</span>" +
      "<span>step <em>" + step + "</em></span>";

    /* code + the line now running */
    var lines = CODE[cur.mode];
    var active = { init: "init", mid: "mid", left: "left", right: "right", move: "loop", done: "done" }[phase] || "loop";
    el("bcode").innerHTML = lines.map(function (l) {
      var txt = l.t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      txt = txt.replace(/\b(while|if|elif|else|return|len)\b/g, '<span class="kw">$1</span>');
      return '<div class="ln' + (l.k === active ? " on" : "") + '">' + txt + "</div>";
    }).join("");

    el("bstat").textContent = result !== null
      ? "done · " + step + " steps"
      : step + " steps so far";
  }

  function say(head, body) {
    el("bexp").innerHTML = "<h6>" + head + "</h6><p>" + body + "</p>" +
      '<p class="vals">lo = <b>' + lo + "</b> · mid = <b>" + (mid === null ? "–" : mid) +
      "</b> · hi = <b>" + hi + "</b></p>";
  }

  /* ---------- controls ---------- */
  function stopAuto() {
    if (timer) { clearInterval(timer); timer = null; el("bauto").textContent = "Auto run"; }
  }
  el("bstep").onclick = function () { stopAuto(); next(); };
  el("bauto").onclick = function () {
    if (timer) { stopAuto(); return; }
    el("bauto").textContent = "Stop";
    timer = setInterval(function () {
      if (result !== null) { stopAuto(); return; }
      next();
    }, 900);
  };
  el("brst").onclick = function () { build(cur); };

  el("bscen").innerHTML = SCEN.map(function (s, i) {
    return '<button data-i="' + i + '"' + (i === 0 ? ' class="on"' : "") + ">" + s.label + "</button>";
  }).join("");
  [].slice.call(el("bscen").querySelectorAll("button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(el("bscen").querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      build(SCEN[+b.getAttribute("data-i")]);
    };
  });

  build(SCEN[0]);
})();
