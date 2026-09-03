/* Lab bootstrap → cây → rừng.
   Bảng gốc 8 khách → rút một dòng, dòng bay xuống bảng mẫu → mẫu đầy thì mọc một cây → rừng bỏ phiếu. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("bootlab")) return;

  /* dữ liệu: khách · thu nhập (triệu) · tuổi · số lần ghé · đã mua */
  var DATA = [
    [12, 24, 2, 0], [31, 38, 6, 1], [9, 22, 1, 0], [45, 41, 9, 1],
    [18, 29, 3, 0], [52, 47, 7, 1], [27, 35, 5, 1], [15, 26, 2, 0]
  ];
  var N = DATA.length;
  var COLS = ["thu nhập > 25 ?", "tuổi > 35 ?", "ghé > 4 lần ?"];
  var draws = [], forest = [], timer = null, flying = false, growing = false;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function count(k) { var c = 0; draws.forEach(function (v) { if (v === k) c++; }); return c; }
  function rnd(n) { return Math.floor(Math.random() * n); }
  function head() {
    return '<thead><tr><th>khách</th><th>thu nhập</th><th>tuổi</th><th>số lần ghé</th>' +
      '<th class="y">đã mua</th><th class="note"></th></tr></thead>';
  }
  function cells(k) {
    var d = DATA[k - 1];
    return '<td class="id">khách ' + k + '</td><td>' + d[0] + ' triệu</td><td>' + d[1] + '</td>' +
      '<td>' + d[2] + ' lần</td>' +
      '<td class="y ' + (d[3] ? "yes" : "no") + '">' + (d[3] ? "có" : "không") + '</td>';
  }
  var BLANK = '<td class="id">—</td><td>—</td><td>—</td><td>—</td><td class="y">—</td>';

  /* ---------- khung ---------- */
  el("bview").innerHTML =
    '<p class="labrow"><b>1.</b> Bộ dữ liệu gốc — 8 khách. Rút xong <b>khách vẫn nằm nguyên ở bảng này</b></p>' +
    '<div class="dtwrap"><table class="dt" id="bsrcT">' + head() + '<tbody>' +
      DATA.map(function (_, k) { return '<tr id="bs' + (k + 1) + '">' + cells(k + 1) + '<td class="cnt"></td></tr>'; }).join("") +
    '</tbody></table></div>' +

    '<p class="labrow"><b>2.</b> Mẫu bootstrap của cây <span id="bno">1</span> — cũng 8 dòng, nhưng có dòng lặp có dòng thiếu</p>' +
    '<div class="dtwrap"><table class="dt" id="bdstT">' + head() + '<tbody>' +
      DATA.map(function (_, i) { return '<tr id="bd' + i + '" class="empty">' + BLANK + '<td class="cnt"></td></tr>'; }).join("") +
    '</tbody></table></div>' +

    '<p class="labrow"><b>3.</b> Rừng — mỗi cây học một mẫu khác nên hỏi câu khác</p>' +
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
      '<rect x="8" y="4" width="104" height="18" rx="5" fill="rgba(140,169,242,.18)" stroke="#8CA9F2" stroke-width="2"></rect>' +
      '<text class="sv-l" x="60" y="17" text-anchor="middle" fill="#A8BEF6" font-size="8.5">' + q + '</text>' +
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
      : '<p class="empty">Chưa có cây nào — rút đủ 8 dòng ở bảng trên thì cây đầu tiên mọc lên.</p>';
  }

  /* ---------- trạng thái ---------- */
  function paint() {
    var full = draws.length >= N, k, i;

    for (k = 1; k <= N; k++) {
      var c = count(k), r = el("bs" + k);
      r.className = c >= 2 ? "dup" : (full && c === 0 ? "oob" : "");
      r.querySelector(".cnt").innerHTML = c >= 2 ? "rút " + c + " lần"
        : (full && c === 0 ? "out-of-bag" : "");
    }
    for (i = 0; i < N; i++) {
      var d = el("bd" + i), v = draws[i];
      var again = v !== undefined && draws.slice(0, i).indexOf(v) >= 0;
      d.className = v === undefined ? "empty" : (again ? "dup" : "");
      d.innerHTML = (v === undefined ? BLANK : cells(v)) +
        '<td class="cnt">' + (again ? "lặp lại" : "") + "</td>";
    }
    el("bno").textContent = forest.length + 1;
    el("bslider").innerHTML = '<i style="width:' + (100 * draws.length / N) + '%"></i>';

    var oob = [];
    for (k = 1; k <= N; k++) if (!count(k)) oob.push(k);
    var line;
    if (!draws.length) line = "Bấm <b>Rút một dòng</b>: một khách được chép xuống bảng dưới, còn bản thân họ <b>vẫn ở lại bảng trên</b> — nên lần sau vẫn rút trúng được.";
    else if (!full) line = "Còn <b>" + (N - draws.length) + "</b> dòng trống. Khách nào bị rút trúng hai lần thì bảng dưới có họ <b>hai dòng</b>.";
    else line = "Mẫu đủ 8 dòng nhưng vắng <b>khách " + (oob.length ? oob.join(", ") : "—") + "</b> — cây này chưa từng học họ. Họ là <b>out-of-bag</b> của cây này. <b>Cây đang mọc…</b>";
    el("bexp").innerHTML = line;

    el("bstat").textContent = "rừng " + forest.length + " cây · mẫu " + draws.length + "/" + N +
      (full ? " · out-of-bag " + oob.length : "");

    var buy = 0;
    forest.forEach(function (t) { if (t.vote === "mua") buy++; });
    var v2 = el("bverdict");
    v2.hidden = forest.length < 3;
    if (forest.length >= 3) {
      v2.innerHTML = "Rừng <b>" + forest.length + " cây</b>: <b>" + buy + "</b> phiếu <em>mua</em> · <b>" +
        (forest.length - buy) + "</b> phiếu <em>không</em> → random forest trả lời <b>" +
        (buy * 2 > forest.length ? "mua" : "không") + "</b>. " +
        "Mỗi cây học một bảng mẫu khác nên hỏi câu khác và có thể sai khác nhau — <b>gộp lại thì phiếu sai bị thiểu số</b>.";
    }
    el("bstep").disabled = full;
    el("bauto").disabled = full;

    /* rút đủ 8 dòng thì cây tự mọc — chờ một nhịp cho kịp đọc dòng out-of-bag */
    if (full && !growing) {
      growing = true;
      setTimeout(function () { growing = false; grow(); }, slow ? 1100 : 60);
    }
  }

  /* ---------- dòng bay từ bảng gốc xuống bảng mẫu ---------- */
  function fly(v, slot, after) {
    if (!slow) return after();
    var src = el("bs" + v), dst = el("bd" + slot);
    var a = src.getBoundingClientRect(), b = dst.getBoundingClientRect();
    var box = el("bootlab").getBoundingClientRect();
    var g = document.createElement("div");
    g.className = "flyrow";
    g.textContent = "khách " + v + " · " + DATA[v - 1][0] + " triệu · " + DATA[v - 1][1] + " tuổi";
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
