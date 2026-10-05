/* Lab: adding trees on the residuals.
   Table of 8 houses → each click grows a shallow tree on the residual column → add it with η → the residuals shrink. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("gblab")) return;

  /* area (×10 m²) · true price (×100k) — has a step jump so a shallow tree can learn it */
  var X = [1, 2, 3, 4, 5, 6, 7, 8];
  var Y = [2, 3, 4, 9, 10, 11, 17, 18];
  var THR = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5];
  var N = X.length;

  var eta = 0.3, F = [], trees = [], hist = [], timer = null;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function mean(a) { var s = 0; a.forEach(function (v) { s += v; }); return a.length ? s / a.length : 0; }
  function resid() { return Y.map(function (y, i) { return y - F[i]; }); }
  function mse() { var r = resid(), s = 0; r.forEach(function (v) { s += v * v; }); return s / N; }
  function fmt(x) { return (Math.round(x * 100) / 100).toFixed(2); }
  function sgn(x) { return (x >= 0 ? "+" : "−") + fmt(Math.abs(x)); }

  /* the shallowest tree possible: one question, two leaves — fit on the residuals */
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
    '<p class="labrow"><b>1.</b> Start: <b>every house is predicted as the mean of y</b> — wrong on almost every row</p>' +
    '<div class="dtwrap"><table class="dt" id="gbT"><thead><tr>' +
      '<th>house</th><th>area</th><th class="y">true price y</th><th>prediction F</th>' +
      '<th>residual r</th><th class="note">how far off</th></tr></thead><tbody>' +
      X.map(function (_, i) { return '<tr id="gr' + i + '"></tr>'; }).join("") +
    "</tbody></table></div>" +
    '<p class="labrow"><b>2.</b> The tree just added — it learns the <b>residual column</b>, not the y column</p>' +
    '<div class="forest" id="gbforest"></div>';

  function stumpSVG(s, k) {
    var q = "area &lt; " + fmt(s.t) + " ?";
    function leaf(v, x) {
      var g = v >= 0;
      return '<rect x="' + x + '" y="46" width="44" height="20" rx="4" fill="' +
        (g ? "rgba(var(--green-a),.16)" : "rgba(var(--red-a),.16)") + '" stroke="' + (g ? "var(--ok)" : "var(--tomb)") + '"></rect>' +
        '<text class="sv-l" x="' + (x + 22) + '" y="60" text-anchor="middle" font-size="9" fill="' +
        (g ? "var(--ok)" : "var(--tomb)") + '">' + sgn(v * eta) + "</text>";
    }
    return '<svg viewBox="0 0 120 84" aria-hidden="true">' +
      '<rect x="6" y="4" width="108" height="18" rx="5" fill="rgba(var(--blue-a),.18)" stroke="var(--filled)" stroke-width="2"></rect>' +
      '<text class="sv-l" x="60" y="17" text-anchor="middle" fill="var(--filled-lo)" font-size="8.5">' + q + "</text>" +
      '<line x1="60" y1="22" x2="30" y2="46" stroke="var(--rule)"></line>' +
      '<line x1="60" y1="22" x2="90" y2="46" stroke="var(--rule)"></line>' +
      leaf(s.L, 8) + leaf(s.R, 68) +
      '<text class="sv-l" x="60" y="80" text-anchor="middle" font-size="9" fill="var(--faint)">tree ' + k + " · times η</text></svg>";
  }

  function paintForest() {
    el("gbforest").innerHTML = trees.length
      ? trees.slice(-6).map(function (s, i, a) {
          var k = trees.length - a.length + i + 1;
          return '<div class="tree' + (k === trees.length ? " new" : "") + '">' + stumpSVG(s, k) + "</div>";
        }).join("")
      : '<p class="empty">No trees added yet — press <b>Add a tree</b> to grow the first tree on the residual column.</p>';
  }

  function paint(first) {
    var r = resid(), mx = 0;
    r.forEach(function (v) { mx = Math.max(mx, Math.abs(v)); });
    var base = Math.max(mx, 8);

    X.forEach(function (x, i) {
      var v = r[i], w = Math.min(100, 100 * Math.abs(v) / base);
      var small = Math.abs(v) < 0.6;
      el("gr" + i).innerHTML =
        '<td class="id">house ' + (i + 1) + "</td>" +
        "<td>" + x * 10 + " m²</td>" +
        '<td class="y">' + Y[i] + "</td>" +
        "<td>" + fmt(F[i]) + "</td>" +
        '<td class="' + (small ? "gz" : "gr") + '">' + sgn(v) + "</td>" +
        '<td class="rbar"><u class="' + (small ? "ok" : "") + '" style="width:' + w.toFixed(1) + '%"></u></td>';
    });

    el("gbslider").innerHTML = '<i style="width:' + (100 * Math.min(1, hist[0] ? 1 - mse() / hist[0] : 0)) + '%"></i>';
    paintForest();

    var line;
    if (!trees.length) line = "The <b>residual</b> column is the dataset for the next tree: the feature column stays the same, the new label is <b>how much is still missing</b>.";
    else line = "The last tree asked <b>area &lt; " + fmt(trees[trees.length - 1].t) + "</b> and returns two leaf values. Added in (times η = " +
      fmt(eta) + "), <b>the residuals shrink</b> — and the new residual table is the data for the next tree.";
    el("gbexp").innerHTML = line;

    el("gbstat").textContent = "η = " + fmt(eta) + " · " + trees.length + " trees · MSE " + fmt(mse());

    var v2 = el("gbverdict");
    v2.hidden = trees.length < 4;
    if (trees.length >= 4) {
      v2.innerHTML = "After <b>" + trees.length + " trees</b>, MSE went from <b>" + fmt(hist[0]) + "</b> down to <b>" + fmt(mse()) + "</b>. " +
        "None of those trees learned <em>house prices</em> — they only learned <b>the part the previous trees' sum still got wrong</b>. " +
        "Lower η and each tree moves more slowly, so more trees are needed to reach the same place.";
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
