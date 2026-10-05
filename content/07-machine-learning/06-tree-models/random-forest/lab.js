/* Lab bootstrap → tree → forest.
   Original table of 8 customers → draw one row, the row flies down to the sample table → when the sample is full a tree grows → the forest votes. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("bootlab")) return;

  /* data: customer · income (k) · age · visits · bought */
  var DATA = [
    [12, 24, 2, 0], [31, 38, 6, 1], [9, 22, 1, 0], [45, 41, 9, 1],
    [18, 29, 3, 0], [52, 47, 7, 1], [27, 35, 5, 1], [15, 26, 2, 0]
  ];
  var N = DATA.length;
  var COLS = ["income > 25 ?", "age > 35 ?", "visits > 4 ?"];
  var draws = [], forest = [], timer = null, flying = false, growing = false;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function count(k) { var c = 0; draws.forEach(function (v) { if (v === k) c++; }); return c; }
  function rnd(n) { return Math.floor(Math.random() * n); }
  function head() {
    return '<thead><tr><th>customer</th><th>income</th><th>age</th><th>visits</th>' +
      '<th class="y">bought</th><th class="note"></th></tr></thead>';
  }
  function cells(k) {
    var d = DATA[k - 1];
    return '<td class="id">customer ' + k + '</td><td>' + d[0] + 'k</td><td>' + d[1] + '</td>' +
      '<td>' + d[2] + ' visits</td>' +
      '<td class="y ' + (d[3] ? "yes" : "no") + '">' + (d[3] ? "yes" : "no") + '</td>';
  }
  var BLANK = '<td class="id">—</td><td>—</td><td>—</td><td>—</td><td class="y">—</td>';

  /* ---------- khung ---------- */
  el("bview").innerHTML =
    '<p class="labrow"><b>1.</b> Original dataset — 8 customers. After a draw <b>the customer stays right here in this table</b></p>' +
    '<div class="dtwrap"><table class="dt" id="bsrcT">' + head() + '<tbody>' +
      DATA.map(function (_, k) { return '<tr id="bs' + (k + 1) + '">' + cells(k + 1) + '<td class="cnt"></td></tr>'; }).join("") +
    '</tbody></table></div>' +

    '<p class="labrow"><b>2.</b> Bootstrap sample of tree <span id="bno">1</span> — also 8 rows, but some rows repeat and some are missing</p>' +
    '<div class="dtwrap"><table class="dt" id="bdstT">' + head() + '<tbody>' +
      DATA.map(function (_, i) { return '<tr id="bd' + i + '" class="empty">' + BLANK + '<td class="cnt"></td></tr>'; }).join("") +
    '</tbody></table></div>' +

    '<p class="labrow"><b>3.</b> Forest — each tree learns a different sample, so it asks a different question</p>' +
    '<div class="forest" id="bforest"></div>';

  /* ---------- one mini tree ---------- */
  function treeSVG(q, vote) {
    var leaf = vote === "buy" ? [1, 1, 0, 1] : [0, 0, 1, 0];
    var dot = leaf.map(function (g, i) {
      var x = [28, 48, 72, 92][i];
      return '<circle cx="' + x + '" cy="70" r="5" fill="' + (g ? "rgba(var(--green-a),.25)" : "rgba(var(--red-a),.22)") +
        '" stroke="' + (g ? "var(--ok)" : "var(--tomb)") + '"></circle>';
    }).join("");
    return '<svg viewBox="0 0 120 94" aria-hidden="true">' +
      '<rect x="8" y="4" width="104" height="18" rx="5" fill="rgba(var(--blue-a),.18)" stroke="var(--filled)" stroke-width="2"></rect>' +
      '<text class="sv-l" x="60" y="17" text-anchor="middle" fill="var(--filled-lo)" font-size="8.5">' + q + '</text>' +
      '<line x1="60" y1="22" x2="38" y2="38" stroke="var(--rule)"></line><line x1="60" y1="22" x2="82" y2="38" stroke="var(--rule)"></line>' +
      '<rect x="20" y="38" width="36" height="14" rx="4" class="sv-b"></rect>' +
      '<rect x="64" y="38" width="36" height="14" rx="4" class="sv-b"></rect>' +
      '<line x1="38" y1="52" x2="28" y2="64" stroke="var(--rule)"></line><line x1="38" y1="52" x2="48" y2="64" stroke="var(--rule)"></line>' +
      '<line x1="82" y1="52" x2="72" y2="64" stroke="var(--rule)"></line><line x1="82" y1="52" x2="92" y2="64" stroke="var(--rule)"></line>' +
      dot +
      '<text class="sv-l" x="60" y="90" text-anchor="middle" font-size="10" fill="' +
        (vote === "buy" ? "var(--ok)" : "var(--tomb)") + '">vote: ' + vote + '</text></svg>';
  }

  function paintForest() {
    el("bforest").innerHTML = forest.length
      ? forest.map(function (t, i) {
          return '<div class="tree' + (i === forest.length - 1 ? " new" : "") + '">' +
            '<span class="tag">tree ' + (i + 1) + '</span>' + treeSVG(t.q, t.vote) + '</div>';
        }).join("")
      : '<p class="empty">No trees yet — draw all 8 rows in the table above and the first tree grows.</p>';
  }

  /* ---------- state ---------- */
  function paint() {
    var full = draws.length >= N, k, i;

    for (k = 1; k <= N; k++) {
      var c = count(k), r = el("bs" + k);
      r.className = c >= 2 ? "dup" : (full && c === 0 ? "oob" : "");
      r.querySelector(".cnt").innerHTML = c >= 2 ? "drawn " + c + "×"
        : (full && c === 0 ? "out-of-bag" : "");
    }
    for (i = 0; i < N; i++) {
      var d = el("bd" + i), v = draws[i];
      var again = v !== undefined && draws.slice(0, i).indexOf(v) >= 0;
      d.className = v === undefined ? "empty" : (again ? "dup" : "");
      d.innerHTML = (v === undefined ? BLANK : cells(v)) +
        '<td class="cnt">' + (again ? "repeat" : "") + "</td>";
    }
    el("bno").textContent = forest.length + 1;
    el("bslider").innerHTML = '<i style="width:' + (100 * draws.length / N) + '%"></i>';

    var oob = [];
    for (k = 1; k <= N; k++) if (!count(k)) oob.push(k);
    var line;
    if (!draws.length) line = "Press <b>Draw a row</b>: a customer is copied to the table below, while they themselves <b>stay in the table above</b> — so they can be drawn again next time.";
    else if (!full) line = "<b>" + (N - draws.length) + "</b> empty rows left. A customer drawn twice appears as <b>two rows</b> in the table below.";
    else line = "The sample has 8 rows but is missing <b>customer " + (oob.length ? oob.join(", ") : "—") + "</b> — this tree has never learned them. They are this tree's <b>out-of-bag</b> rows. <b>Tree growing…</b>";
    el("bexp").innerHTML = line;

    el("bstat").textContent = "forest " + forest.length + " trees · sample " + draws.length + "/" + N +
      (full ? " · out-of-bag " + oob.length : "");

    var buy = 0;
    forest.forEach(function (t) { if (t.vote === "buy") buy++; });
    var v2 = el("bverdict");
    v2.hidden = forest.length < 3;
    if (forest.length >= 3) {
      v2.innerHTML = "Forest of <b>" + forest.length + " trees</b>: <b>" + buy + "</b> votes <em>buy</em> · <b>" +
        (forest.length - buy) + "</b> votes <em>no</em> → random forest answers <b>" +
        (buy * 2 > forest.length ? "buy" : "no") + "</b>. " +
        "Each tree learns a different sample table, so it asks different questions and can be wrong in different ways — <b>combined, the wrong votes end up in the minority</b>.";
    }
    el("bstep").disabled = full;
    el("bauto").disabled = full;

    /* once 8 rows are drawn the tree grows by itself — wait a beat so the out-of-bag line can be read */
    if (full && !growing) {
      growing = true;
      setTimeout(function () { growing = false; grow(); }, slow ? 1100 : 60);
    }
  }

  /* ---------- row flies from the original table to the sample table ---------- */
  function fly(v, slot, after) {
    if (!slow) return after();
    var src = el("bs" + v), dst = el("bd" + slot);
    var a = src.getBoundingClientRect(), b = dst.getBoundingClientRect();
    var box = el("bootlab").getBoundingClientRect();
    var g = document.createElement("div");
    g.className = "flyrow";
    g.textContent = "customer " + v + " · " + DATA[v - 1][0] + "k · age " + DATA[v - 1][1];
    g.style.left = (a.left - box.left) + "px";
    g.style.top = (a.top - box.top) + "px";
    g.style.width = a.width + "px";
    g.style.height = a.height + "px";
    el("bootlab").appendChild(g);
    src.classList.add("pick");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        g.style.transform = "translate(" + (b.left - a.left) + "px," + (b.top - a.top) + "px)";
      });
    });
    setTimeout(function () {
      g.remove();
      src.classList.remove("pick");
      after();
    }, 500);
  }

  function step() {
    if (flying || draws.length >= N) return;
    var v = 1 + rnd(N), slot = draws.length;
    flying = true;
    fly(v, slot, function () {
      draws.push(v);
      paint();
      var row = el("bd" + slot);
      row.classList.add("land");
      setTimeout(function () { row.classList.remove("land"); }, 460);
      flying = false;
    });
  }

  function grow() {
    if (draws.length < N) return;
    forest.push({ q: COLS[rnd(COLS.length)], vote: Math.random() < 0.66 ? "buy" : "no" });
    draws = [];
    paintForest();
    paint();
  }

  el("bstep").onclick = step;
  el("bauto").onclick = function () {
    if (timer) return;
    timer = setInterval(function () {
      step();
      if (draws.length >= N) { clearInterval(timer); timer = null; }
    }, slow ? 640 : 40);
  };
  el("brst").onclick = function () {
    if (timer) { clearInterval(timer); timer = null; }
    draws = []; forest = []; flying = false; growing = false;
    paintForest(); paint();
  };

  paintForest();
  paint();
})();
