/* Lab linked list — đảo danh sách từng bước, tô dòng code đang chạy. */
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
    say("Trạng thái ban đầu", "<code>prev = None</code>, <code>cur</code> đứng ở nút đầu. Mỗi vòng sẽ quay đúng một mũi tên.");
  }

  function next_() {
    if (phase === "done") return;
    if (phase === "init" || phase === "move") {
      if (cur === null) { finish(); return; }
      phase = "save"; step++;
      nxt = next[cur];
      draw();
      say("Bước " + step + " — giữ lại nút sau",
        "<code>nxt = cur.next</code> → giữ <b>" + (nxt === null ? "∅" : vals[nxt]) +
        "</b>. Không giữ trước là mất sạch phần đuôi.");
      return;
    }
    if (phase === "save") {
      phase = "flip";
      next[cur] = prev;
      draw();
      say("Bước " + step + " — quay mũi tên",
        "<code>cur.next = prev</code> → nút <b>" + vals[cur] + "</b> giờ trỏ ngược về <b>" +
        (prev === null ? "∅" : vals[prev]) + "</b>.");
      return;
    }
    if (phase === "flip") {
      phase = "move";
      prev = cur; cur = nxt; nxt = null;
      draw();
      say("Bước " + step + " — đi tiếp",
        "<code>prev, cur = cur, nxt</code>. Phần bên trái đã đảo xong, phần bên phải còn nguyên.");
    }
  }

  function finish() {
    phase = "done";
    draw();
    say("Xong sau " + step + " vòng", "<code>cur</code> đã ra khỏi danh sách nên vòng lặp dừng.");
    var v = el("lverdict");
    v.hidden = false;
    v.innerHTML = "Trả về <b>prev</b>, không phải <code>cur</code> — lúc này <code>cur</code> đã là <code>None</code>. " +
      "Mỗi nút được chạm <b>đúng một lần</b>: O(n) thời gian, O(1) bộ nhớ.";
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
      "<span>số nhỏ phía trên mỗi ô = <em>nút mà nó đang trỏ tới</em></span>" +
      "<span>ô xanh = <em>đã quay xong</em></span>";

    var active = { init: "init", save: "save", flip: "flip", move: "move", done: "done" }[phase] || "loop";
    el("lcode").innerHTML = CODE.map(function (l) {
      var txt = l.t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/\b(while|return|None)\b/g, '<span class="kw">$1</span>');
      return '<div class="ln' + (l.k === active ? " on" : "") + '">' + txt + "</div>";
    }).join("");

    el("lstat").textContent = phase === "done" ? "đã xong · " + step + " vòng" : "vòng " + step;
  }

  function say(head, body) {
    el("lexp").innerHTML = "<h6>" + head + "</h6><p>" + body + "</p>" +
      '<p class="vals">prev = <b>' + (prev === null ? "None" : vals[prev]) +
      "</b> · cur = <b>" + (cur === null ? "None" : vals[cur]) +
      "</b> · nxt = <b>" + (nxt === null || nxt === undefined ? "–" : vals[nxt]) + "</b></p>";
  }

  function stopAuto() { if (timer) { clearInterval(timer); timer = null; el("lauto").textContent = "Tự chạy"; } }
  el("lstep").onclick = function () { stopAuto(); next_(); };
  el("lauto").onclick = function () {
    if (timer) { stopAuto(); return; }
    el("lauto").textContent = "Dừng";
    timer = setInterval(function () { if (phase === "done") { stopAuto(); return; } next_(); }, 800);
  };
  el("lrst").onclick = build;
  el("lvals").addEventListener("change", build);

  build();
})();
