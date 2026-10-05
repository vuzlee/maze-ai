/* Lab linked list — reverse the list step by step, highlighting the running code line. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("lllab")) return;

  var CODE = [
    { t: "prev, cur = None, head", k: "init" },
    { t: "while cur:", k: "loop" },
    { t: "    nxt = cur.next", k: "save" },
    { t: "    cur.next = prev", k: "flip" },
    { t: "    prev, cur = cur, nxt", k: "move" },
    { t: "return prev", k: "done" }
  ];

  var vals, next, prev, cur, nxt, phase, step, timer = null;

  function build() {
    stopAuto();
    vals = (el("lvals").value || "3 7 1 9").trim().split(/\s+/).slice(0, 7);
    next = vals.map(function (_, i) { return i + 1 < vals.length ? i + 1 : null; });
    prev = null; cur = vals.length ? 0 : null; nxt = null;
    phase = "init"; step = 0;
    el("lverdict").hidden = true;
    draw();
    say("Initial state", "<code>prev = None</code>, <code>cur</code> sits at the first node. Each loop will flip exactly one arrow.");
  }

  function next_() {
    if (phase === "done") return;
    if (phase === "init" || phase === "move") {
      if (cur === null) { finish(); return; }
      phase = "save"; step++;
      nxt = next[cur];
      draw();
      say("Step " + step + " — save the next node",
        "<code>nxt = cur.next</code> → saves <b>" + (nxt === null ? "∅" : vals[nxt]) +
        "</b>. Without saving it first, the whole tail is lost.");
      return;
    }
    if (phase === "save") {
      phase = "flip";
      next[cur] = prev;
      draw();
      say("Step " + step + " — flip the arrow",
        "<code>cur.next = prev</code> → node <b>" + vals[cur] + "</b> now points back to <b>" +
        (prev === null ? "∅" : vals[prev]) + "</b>.");
      return;
    }
    if (phase === "flip") {
      phase = "move";
      prev = cur; cur = nxt; nxt = null;
      draw();
      say("Step " + step + " — advance",
        "<code>prev, cur = cur, nxt</code>. The left part is reversed, the right part is untouched.");
    }
  }

  function finish() {
    phase = "done";
    draw();
    say("Done after " + step + " loops", "<code>cur</code> has left the list, so the loop stops.");
    var v = el("lverdict");
    v.hidden = false;
    v.innerHTML = "Return <b>prev</b>, not <code>cur</code> — by now <code>cur</code> is <code>None</code>. " +
      "Each node is touched <b>exactly once</b>: O(n) time, O(1) memory.";
  }

  function draw() {
    var h = '<div class="strip">';
    vals.forEach(function (v, i) {
      var mk = [];
      if (i === prev) mk.push("prev");
      if (i === cur) mk.push("cur");
      if (i === nxt) mk.push("nxt");
      var done = next[i] !== (i + 1 < vals.length ? i + 1 : null);
      h += '<div class="c' + (i === cur ? " on" : (done ? " t" : "")) + '">' +
        "<i>" + (next[i] === null ? "∅" : vals[next[i]]) + "</i><b>" + v + "</b><u>" + mk.join(" ") + "</u></div>";
    });
    el("lview").innerHTML = h + "</div>";
    el("lnote").innerHTML =
      "<span>small number above each cell = <em>the node it points to</em></span>" +
      "<span>green cell = <em>already flipped</em></span>";

    var active = { init: "init", save: "save", flip: "flip", move: "move", done: "done" }[phase] || "loop";
    el("lcode").innerHTML = CODE.map(function (l) {
      var txt = l.t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/\b(while|return|None)\b/g, '<span class="kw">$1</span>');
      return '<div class="ln' + (l.k === active ? " on" : "") + '">' + txt + "</div>";
    }).join("");

    el("lstat").textContent = phase === "done" ? "done · " + step + " loops" : "loop " + step;
  }

  function say(head, body) {
    el("lexp").innerHTML = "<h6>" + head + "</h6><p>" + body + "</p>" +
      '<p class="vals">prev = <b>' + (prev === null ? "None" : vals[prev]) +
      "</b> · cur = <b>" + (cur === null ? "None" : vals[cur]) +
      "</b> · nxt = <b>" + (nxt === null || nxt === undefined ? "–" : vals[nxt]) + "</b></p>";
  }

  function stopAuto() { if (timer) { clearInterval(timer); timer = null; el("lauto").textContent = "Auto run"; } }
  el("lstep").onclick = function () { stopAuto(); next_(); };
  el("lauto").onclick = function () {
    if (timer) { stopAuto(); return; }
    el("lauto").textContent = "Stop";
    timer = setInterval(function () { if (phase === "done") { stopAuto(); return; } next_(); }, 800);
  };
  el("lrst").onclick = build;
  el("lvals").addEventListener("change", build);

  build();
})();
