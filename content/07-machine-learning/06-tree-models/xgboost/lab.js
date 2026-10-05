/* Gain lab — drag λ and γ, watch the formula decide on its own whether to split or stop.
   8 samples, each a pair (g, h); try every threshold, compute Obj* before and after, the gain decides. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("xgblab")) return;

  /* EXACTLY the six samples A–F of the two figures above — change them here and you must fix the figures too, or the lab and the figures
     tell two different stories. g is the slope, h is the curvature. */
  var NAME = ["A", "B", "C", "D", "E", "F"];
  var G = [-2.4, -2.1, -1.8, -0.4, 0.6, 3.2];
  var H = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4];
  var X = [1, 2, 3, 4, 5, 6];
  var THR = [1.5, 2.5, 3.5, 4.5, 5.5];
  var N = X.length;

  /* λ fixed = 1: that belongs to the previous section; this lab asks ONE question only — split or stop.
     Adding a λ knob here would make the reader weigh two things at once. */
  var lam = 1, gam = 0.5, cut = 4.5;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function fmt(x) { return (Math.round(x * 100) / 100).toFixed(2).replace("-", "−"); }
  function sum(a, f) { var s = 0; a.forEach(function (v, i) { s += f(v, i); }); return s; }
  function score(idx) {                    /* − ½ G²/(H+λ), a leaf's share of the score */
    var g = sum(idx, function (i) { return G[i]; });
    var h = sum(idx, function (i) { return H[i]; });
    return { g: g, h: h, s: g * g / (h + lam), w: -g / (h + lam) };
  }
  function all() { return X.map(function (_, i) { return i; }); }
  function sides(t) {
    var L = [], R = [];
    X.forEach(function (x, i) { (x < t ? L : R).push(i); });
    return { L: L, R: R };
  }
  function gainAt(t) {
    var s = sides(t);
    if (!s.L.length || !s.R.length) return -Infinity;
    return 0.5 * (score(s.L).s + score(s.R).s - score(all()).s) - gam;
  }

  /* ---------- khung ---------- */
  el("xview").innerHTML =
    '<p class="labrow"><b>1.</b> Still the six samples A–F from the figure above — each carries a ready-made pair <b>(g, h)</b> computed from the loss</p>' +
    '<div id="xstrip"></div>' +
    '<p class="stripnote" id="xnote"><span></span><span></span></p>' +
    '<p class="labrow"><b>2.</b> Gain of every threshold — click a bar to see the details</p>' +
    '<div id="xbars"></div>';

  function draw() {
    var s = sides(cut), root = score(all()), L = score(s.L), R = score(s.R), g = gainAt(cut);

    /* sample strip, cut line at the exact threshold */
    var h = '<div class="strip">';
    X.forEach(function (x, i) {
      if (x > cut && X[i - 1] < cut) h += '<div class="cut"></div>';
      h += '<div class="c ' + (G[i] < 0 ? "t" : "f") + '"><i>' + NAME[i] + "</i><b>" +
        (G[i] > 0 ? "+" : "−") + fmt(Math.abs(G[i])) + "</b><u>h " + fmt(H[i]) + "</u></div>";
    });
    el("xstrip").innerHTML = h + "</div>";

    el("xnote").innerHTML =
      "<span>left leaf: G " + fmt(L.g) + " · H " + fmt(L.h) + " → w* <em>" + fmt(L.w) + "</em></span>" +
      "<span>threshold <em>" + fmt(cut) + "</em></span>" +
      "<span>right leaf: G " + fmt(R.g) + " · H " + fmt(R.h) + " → w* <em>" + fmt(R.w) + "</em></span>";

    /* every threshold */
    var best = THR.reduce(function (a, b) { return gainAt(b) > gainAt(a) ? b : a; });
    var mx = Math.max(0.01, gainAt(best));
    el("xbars").innerHTML = '<div class="bars">' + THR.map(function (t) {
      var v = gainAt(t), pos = v > 0;
      return '<div class="b' + (t === cut ? " hi" : (pos ? "" : " bad")) + '" data-t="' + t +
        '" style="cursor:pointer;margin:5px 0"><i>threshold ' + fmt(t) + "</i>" +
        '<u style="width:' + Math.max(1, 100 * Math.abs(v) / mx).toFixed(1) + '%"></u>' +
        "<b>" + (v > 0 ? "+" : "−") + fmt(Math.abs(v)) + (t === best ? " ★" : "") + "</b></div>";
    }).join("") + "</div>";
    [].slice.call(el("xbars").querySelectorAll(".b")).forEach(function (b) {
      b.onclick = function () { cut = parseFloat(b.getAttribute("data-t")); draw(); };
    });

    el("xexp").innerHTML = g > 0
      ? "Gain <b>" + fmt(g) + " &gt; 0</b> → <b>split</b>. The two leaves return <b>" + fmt(L.w) + "</b> and <b>" + fmt(R.w) +
        "</b> — no searching, computed directly as <span class=\"mth\">−<var>G</var>/(<var>H</var>+<var>λ</var>)</span>."
      : "Gain <b>" + fmt(g) + " ≤ 0</b> → <b>no split</b>, this node becomes a leaf returning <b>" + fmt(root.w) +
        "</b>. The price γ = " + fmt(gam) + " of a new leaf is larger than the benefit gained.";

    el("xstat").textContent = "γ = " + fmt(gam) + " · best threshold " + fmt(best) +
      " (gain " + fmt(gainAt(best)) + ")";

    var v = el("xverdict"), pos = 0;
    THR.forEach(function (t) { if (gainAt(t) > 0) pos++; });
    v.hidden = false;
    v.innerHTML = pos
      ? "<b>" + pos + "/" + THR.length + "</b> thresholds still have positive gain — the tree keeps growing. Raise <b>γ</b> further to see where the tree stops."
      : "<b>No threshold has positive gain left</b> — the tree stops here by itself, no pruning needed. Fighting overfitting and growing the tree are <b>one job</b>, because both read the same objective function.";
    if (slow) {
      var w = el("xbars");
      w.classList.add("pulse");
      setTimeout(function () { w.classList.remove("pulse"); }, 380);
    }
  }

  function knob(id, val, arr, set) {
    el(id).innerHTML = arr.map(function (v) {
      return '<button data-v="' + v + '"' + (v === val ? ' class="on"' : "") + ">" + fmt(v) + "</button>";
    }).join("");
    [].slice.call(el(id).querySelectorAll("button")).forEach(function (b) {
      b.onclick = function () {
        [].slice.call(el(id).querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
        set(parseFloat(b.getAttribute("data-v")));
        knob("xgam", gam, [0.5, 4, 10], function (v) { gam = v; });
        draw();
      };
    });
  }
  knob("xgam", gam, [0.5, 4, 10], function (v) { gam = v; });

  el("xrst").onclick = function () {
    gam = 0.5; cut = 4.5;
    knob("xgam", gam, [0.5, 4, 10], function (v) { gam = v; });
    draw();
  };

  draw();
})();
