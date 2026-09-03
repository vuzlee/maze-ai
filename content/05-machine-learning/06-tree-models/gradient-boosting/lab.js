/* Lab cộng cây theo phần dư.
   Bảng 8 căn nhà → mỗi lần bấm mọc một cây nông trên cột phần dư → cộng vào với η → phần dư co lại. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("gblab")) return;

  /* diện tích (chục m²) · giá thật (trăm triệu) — có bậc nhảy nên cây nông học được */
  var X = [1, 2, 3, 4, 5, 6, 7, 8];
  var Y = [2, 3, 4, 9, 10, 11, 17, 18];
  var THR = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5];
  var N = X.length;

  var eta = 0.3, F = [], trees = [], hist = [], timer = null;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function mean(a) { var s = 0; a.forEach(function (v) { s += v; }); return a.length ? s / a.length : 0; }
  function resid() { return Y.map(function (y, i) { return y - F[i]; }); }
  function mse() { var r = resid(), s = 0; r.forEach(function (v) { s += v * v; }); return s / N; }
  function fmt(x) { return (Math.round(x * 100) / 100).toFixed(2).replace(".", ","); }
  function sgn(x) { return (x >= 0 ? "+" : "−") + fmt(Math.abs(x)); }

  /* cây nông nhất có thể: một câu hỏi, hai lá — fit trên phần dư */
  function stump(r) {
    var best = null;
    THR.forEach(function (t) {
      var L = [], R = [];
      X.forEach(function (x, i) { (x < t ? L : R).push(r[i]); });
      var mL = mean(L), mR = mean(R), sse = 0;
      X.forEach(function (x, i) { var d = r[i] - (x < t ? mL : mR); sse += d * d; });
      if (!best || sse < best.sse) best = { t: t, L: mL, R: mR, sse: sse };
    });
    return best;
  }

  function reset() {
    F = Y.map(function () { return mean(Y); });
    trees = []; hist = [mse()];
    paint(true);
  }

  /* ---------- khung ---------- */
  el("gbview").innerHTML =
    '<p class="labrow"><b>1.</b> Khởi tạo: <b>mọi căn đều đoán bằng trung bình của y</b> — sai gần như ở mọi dòng</p>' +
    '<div class="dtwrap"><table class="dt" id="gbT"><thead><tr>' +
      '<th>căn</th><th>diện tích</th><th class="y">giá thật y</th><th>dự đoán F</th>' +
      '<th>phần dư r</th><th class="note">còn sai bao nhiêu</th></tr></thead><tbody>' +
      X.map(function (_, i) { return '<tr id="gr' + i + '"></tr>'; }).join("") +
    "</tbody></table></div>" +
    '<p class="labrow"><b>2.</b> Cây vừa cộng vào — nó học <b>cột phần dư</b>, không học cột y</p>' +
    '<div class="forest" id="gbforest"></div>';

  function stumpSVG(s, k) {
    var q = "diện tích &lt; " + fmt(s.t) + " ?";
    function leaf(v, x) {
      var g = v >= 0;
      return '<rect x="' + x + '" y="46" width="44" height="20" rx="4" fill="' +
        (g ? "rgba(91,207,160,.16)" : "rgba(242,113,138,.16)") + '" stroke="' + (g ? "#5BCFA0" : "#F2718A") + '"></rect>' +
        '<text class="sv-l" x="' + (x + 22) + '" y="60" text-anchor="middle" font-size="9" fill="' +
        (g ? "#8EE0BE" : "#F79BAB") + '">' + sgn(v * eta) + "</text>";
    }
    return '<svg viewBox="0 0 120 84" aria-hidden="true">' +
      '<rect x="6" y="4" width="108" height="18" rx="5" fill="rgba(140,169,242,.18)" stroke="#8CA9F2" stroke-width="2"></rect>' +
      '<text class="sv-l" x="60" y="17" text-anchor="middle" fill="#A8BEF6" font-size="8.5">' + q + "</text>" +
      '<line x1="60" y1="22" x2="30" y2="46" stroke="#2E2822"></line>' +
      '<line x1="60" y1="22" x2="90" y2="46" stroke="#2E2822"></line>' +
      leaf(s.L, 8) + leaf(s.R, 68) +
      '<text class="sv-l" x="60" y="80" text-anchor="middle" font-size="9" fill="#7A6F63">cây ' + k + " · nhân η</text></svg>";
  }

  function paintForest() {
    el("gbforest").innerHTML = trees.length
      ? trees.slice(-6).map(function (s, i, a) {
          var k = trees.length - a.length + i + 1;
          return '<div class="tree' + (k === trees.length ? " new" : "") + '">' + stumpSVG(s, k) + "</div>";
        }).join("")
      : '<p class="empty">Chưa cộng cây nào — bấm <b>Cộng một cây</b> để mọc cây đầu tiên trên cột phần dư.</p>';
  }

  function paint(first) {
    var r = resid(), mx = 0;
    r.forEach(function (v) { mx = Math.max(mx, Math.abs(v)); });
    var base = Math.max(mx, 8);

    X.forEach(function (x, i) {
      var v = r[i], w = Math.min(100, 100 * Math.abs(v) / base);
      var small = Math.abs(v) < 0.6;
      el("gr" + i).innerHTML =
        '<td class="id">căn ' + (i + 1) + "</td>" +
        "<td>" + x * 10 + " m²</td>" +
        '<td class="y">' + Y[i] + "</td>" +
        "<td>" + fmt(F[i]) + "</td>" +
        '<td class="' + (small ? "gz" : "gr") + '">' + sgn(v) + "</td>" +
        '<td class="rbar"><u class="' + (small ? "ok" : "") + '" style="width:' + w.toFixed(1) + '%"></u></td>';
    });

    el("gbslider").innerHTML = '<i style="width:' + (100 * Math.min(1, hist[0] ? 1 - mse() / hist[0] : 0)) + '%"></i>';
    paintForest();

    var line;
    if (!trees.length) line = "Cột <b>phần dư</b> chính là bộ dữ liệu của cây tiếp theo: cột đặc trưng giữ nguyên, nhãn mới là <b>còn thiếu bao nhiêu</b>.";
    else line = "Cây vừa rồi hỏi <b>diện tích &lt; " + fmt(trees[trees.length - 1].t) + "</b>, trả về hai giá trị lá. Cộng vào (đã nhân η = " +
      fmt(eta) + ") thì <b>phần dư co lại</b> — và bảng dư mới là dữ liệu cho cây sau.";
    el("gbexp").innerHTML = line;

    el("gbstat").textContent = "η = " + fmt(eta) + " · " + trees.length + " cây · MSE " + fmt(mse());

    var v2 = el("gbverdict");
    v2.hidden = trees.length < 4;
    if (trees.length >= 4) {
      v2.innerHTML = "Sau <b>" + trees.length + " cây</b>, MSE từ <b>" + fmt(hist[0]) + "</b> xuống <b>" + fmt(mse()) + "</b>. " +
        "Không cây nào trong số đó học <em>giá nhà</em> — chúng chỉ học <b>phần mà tổng các cây trước còn sai</b>. " +
        "Hạ η xuống thì mỗi cây đi chậm hơn, và cần nhiều cây hơn để tới cùng chỗ.";
    }
    if (!first && slow) {
      var t = el("gbT");
      t.classList.add("pulse");
      setTimeout(function () { t.classList.remove("pulse"); }, 420);
    }
  }

  function step() {
    if (trees.length >= 40) return;
    var s = stump(resid());
    X.forEach(function (x, i) { F[i] += eta * (x < s.t ? s.L : s.R); });
    trees.push(s); hist.push(mse());
    paint();
  }

  el("gbeta").innerHTML = [0.1, 0.3, 1].map(function (v) {
    return '<button data-e="' + v + '"' + (v === eta ? ' class="on"' : "") + ">η = " + fmt(v) + "</button>";
  }).join("");
  [].slice.call(el("gbeta").querySelectorAll("button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(el("gbeta").querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      eta = parseFloat(b.getAttribute("data-e"));
      if (timer) { clearInterval(timer); timer = null; }
      reset();
    };
  });

  el("gbstep").onclick = step;
  el("gbauto").onclick = function () {
    if (timer) { clearInterval(timer); timer = null; return; }
    timer = setInterval(function () {
      step();
      if (trees.length >= 12) { clearInterval(timer); timer = null; }
    }, slow ? 560 : 40);
  };
  el("gbrst").onclick = function () {
    if (timer) { clearInterval(timer); timer = null; }
    reset();
  };

  reset();
})();
