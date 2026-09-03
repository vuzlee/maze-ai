/* Lab bootstrap → cây → rừng.
   Rút mẫu (chấm bay xuống ô chứa) → mẫu đầy thì mọc một cây → cây vào rừng → rừng bỏ phiếu. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("bootlab")) return;

  var N = 8;
  var COLS = ["thu nhập ?", "tuổi ?", "đã mua ?", "số lần ghé ?"];
  var draws = [], forest = [], timer = null, flying = false;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function count(k) { var c = 0; draws.forEach(function (v) { if (v === k) c++; }); return c; }
  function rnd(n) { return Math.floor(Math.random() * n); }

  /* ---------- khung ---------- */
  el("bview").innerHTML =
    '<p class="labrow"><b>1.</b> Bộ dữ liệu gốc — 8 khách, rút xong vẫn ở lại đây</p>' +
    '<div class="strip" id="bsrc">' +
      Array.apply(null, Array(N)).map(function (_, k) {
        return '<div class="c" id="bs' + (k + 1) + '"><b>' + (k + 1) + '</b><u></u></div>';
      }).join("") + '</div>' +
    '<p class="labrow"><b>2.</b> Mẫu bootstrap của cây <span id="bno">1</span> — 8 ô chứa</p>' +
    '<div class="strip" id="bdst">' +
      Array.apply(null, Array(N)).map(function (_, i) {
        return '<div class="c slot" id="bd' + i + '"><b>—</b><u></u></div>';
      }).join("") + '</div>' +
    '<p class="labrow"><b>3.</b> Rừng — mỗi cây một mẫu khác nhau nên hỏi câu khác nhau</p>' +
    '<div class="forest" id="bforest"></div>';

  /* ---------- một cây mini ---------- */
  function treeSVG(q, vote) {
    var leaf = vote === "mua" ? [1, 1, 0, 1] : [0, 0, 1, 0];
    var dot = leaf.map(function (g, i) {
      var x = [28, 48, 72, 92][i];
      return '<circle cx="' + x + '" cy="70" r="5" fill="' + (g ? "rgba(91,207,160,.25)" : "rgba(242,113,138,.22)") +
        '" stroke="' + (g ? "#5BCFA0" : "#F2718A") + '"></circle>';
    }).join("");
    return '<svg viewBox="0 0 120 94" aria-hidden="true">' +
      '<rect x="20" y="4" width="80" height="18" rx="5" fill="rgba(140,169,242,.18)" stroke="#8CA9F2" stroke-width="2"></rect>' +
      '<text class="sv-l" x="60" y="17" text-anchor="middle" fill="#A8BEF6" font-size="9">' + q + '</text>' +
      '<line x1="60" y1="22" x2="38" y2="38" stroke="#2E2822"></line><line x1="60" y1="22" x2="82" y2="38" stroke="#2E2822"></line>' +
      '<rect x="20" y="38" width="36" height="14" rx="4" class="sv-b"></rect>' +
      '<rect x="64" y="38" width="36" height="14" rx="4" class="sv-b"></rect>' +
      '<line x1="38" y1="52" x2="28" y2="64" stroke="#2E2822"></line><line x1="38" y1="52" x2="48" y2="64" stroke="#2E2822"></line>' +
      '<line x1="82" y1="52" x2="72" y2="64" stroke="#2E2822"></line><line x1="82" y1="52" x2="92" y2="64" stroke="#2E2822"></line>' +
      dot +
      '<text class="sv-l" x="60" y="90" text-anchor="middle" font-size="10" fill="' +
        (vote === "mua" ? "#8EE0BE" : "#F79BAB") + '">phiếu: ' + vote + '</text></svg>';
  }

  function paintForest() {
    el("bforest").innerHTML = forest.length
      ? forest.map(function (t, i) {
          return '<div class="tree' + (i === forest.length - 1 ? " new" : "") + '">' +
            '<span class="tag">cây ' + (i + 1) + '</span>' + treeSVG(t.q, t.vote) + '</div>';
        }).join("")
      : '<p class="empty">Chưa có cây nào — rút đủ 8 ô ở trên thì cây đầu tiên mọc lên.</p>';
  }

  /* ---------- trạng thái ---------- */
  function paint() {
    var full = draws.length >= N;
    for (var k = 1; k <= N; k++) {
      var c = count(k), n = el("bs" + k);
      n.className = "c" + (full && c === 0 ? " f" : (c >= 2 ? " t" : ""));
      n.querySelector("u").textContent = c >= 2 ? "×" + c : (full && c === 0 ? "bỏ ngoài" : "");
    }
    for (var i = 0; i < N; i++) {
      var d = el("bd" + i), v = draws[i];
      d.className = "c" + (v === undefined ? " slot" : (draws.slice(0, i).indexOf(v) >= 0 ? " t" : ""));
      d.querySelector("b").textContent = v === undefined ? "—" : v;
      d.querySelector("u").textContent = "";
    }
    el("bno").textContent = forest.length + 1;
    el("bslider").innerHTML = '<i style="width:' + (100 * draws.length / N) + '%"></i>';

    var oob = [];
    for (var j = 1; j <= N; j++) if (!count(j)) oob.push(j);
    var line;
    if (!draws.length) line = "Bấm <b>Rút một lần</b>: một khách rơi xuống ô chứa, bản thân họ vẫn ở lại bộ gốc — nên lần sau vẫn rút trúng được.";
    else if (!full) line = "Còn <b>" + (N - draws.length) + "</b> ô trống. Số vàng ở trên là khách đã bị rút trúng <b>hơn một lần</b>.";
    else line = "Mẫu đủ 8 dòng nhưng thiếu <b>khách " + (oob.length ? oob.join(", ") : "—") + "</b> — cây này chưa từng thấy họ. Đó là <b>out-of-bag</b>.";
    el("bexp").innerHTML = line;

    el("bstat").textContent = "rừng " + forest.length + " cây · mẫu " + draws.length + "/" + N +
      (full ? " · bỏ ngoài " + oob.length : "");

    var buy = 0;
    forest.forEach(function (t) { if (t.vote === "mua") buy++; });
    var v2 = el("bverdict");
    v2.hidden = forest.length < 3;
    if (forest.length >= 3) {
      v2.innerHTML = "Rừng <b>" + forest.length + " cây</b>: <b>" + buy + "</b> phiếu <em>mua</em> · <b>" +
        (forest.length - buy) + "</b> phiếu <em>không</em> → random forest trả lời <b>" +
        (buy * 2 > forest.length ? "mua" : "không") + "</b>. " +
        "Mỗi cây học một mẫu khác nên hỏi câu khác và có thể sai khác nhau — <b>gộp lại thì phiếu sai bị thiểu số</b>.";
    }
    el("bstep").disabled = full;
    el("bauto").disabled = full;
    el("bgrow").disabled = !full;
  }

  /* ---------- chấm bay xuống ô chứa ---------- */
  function fly(v, slot, after) {
    if (!slow) return after();
    var a = el("bs" + v).getBoundingClientRect();
    var b = el("bd" + slot).getBoundingClientRect();
    var box = el("bootlab").getBoundingClientRect();
    var g = document.createElement("i");
    g.className = "flydot";
    g.style.left = (a.left - box.left + a.width / 2 - 7) + "px";
    g.style.top = (a.top - box.top + a.height / 2 - 7) + "px";
    el("bootlab").appendChild(g);
    el("bs" + v).classList.add("pick");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        g.style.transform = "translate(" + (b.left - a.left) + "px," + (b.top - a.top) + "px)";
      });
    });
    setTimeout(function () {
      g.remove();
      el("bs" + v).classList.remove("pick");
      after();
    }, 480);
  }

  function step() {
    if (flying || draws.length >= N) return;
    var v = 1 + rnd(N), slot = draws.length;
    flying = true;
    fly(v, slot, function () {
      draws.push(v);
      el("bd" + slot).classList.add("land");
      setTimeout(function () { el("bd" + slot).classList.remove("land"); }, 400);
      flying = false;
      paint();
    });
  }

  function grow() {
    if (draws.length < N) return;
    forest.push({ q: COLS[rnd(COLS.length)], vote: Math.random() < 0.66 ? "mua" : "không" });
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
    }, slow ? 620 : 40);
  };
  el("bgrow").onclick = grow;
  el("brst").onclick = function () {
    if (timer) { clearInterval(timer); timer = null; }
    draws = []; forest = []; flying = false;
    paintForest(); paint();
  };

  paintForest();
  paint();
})();
