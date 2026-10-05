/* Lab: leaf-wise vs level-wise growth.
   Same leaf budget, two trees growing side by side: the left opens a whole level evenly, the right always picks the leaf with the largest gain. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("lgblab")) return;

  var BUDGET = 8;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var timer = null;

  /* each node: its gain, and the gain of its two children — falling with depth, with rich branches and poor branches */
  function mk(gain, depth, rich) {
    return { g: gain, d: depth, rich: rich, kids: null, id: Math.random() };
  }
  function split(n) {
    /* a "rich" branch keeps most of its gain going deeper, a poor branch drops fast */
    var a = mk(n.g * (n.rich ? 0.78 : 0.30), n.d + 1, n.rich);
    var b = mk(n.g * (n.rich ? 0.34 : 0.12), n.d + 1, false);
    n.kids = [a, b];
    return [a, b];
  }
  function leaves(root) {
    var out = [];
    (function walk(n) { n.kids ? n.kids.forEach(walk) : out.push(n); })(root);
    return out;
  }
  function total(root) {
    var s = 0;
    (function walk(n) { if (n.kids) { s += n.g; n.kids.forEach(walk); } })(root);
    return s;
  }
  function depth(root) {
    var m = 0;
    leaves(root).forEach(function (l) { m = Math.max(m, l.d); });
    return m;
  }

  var lvl, leaf, used;
  function reset() {
    lvl = mk(10, 0, true);
    leaf = mk(10, 0, true);
    used = 0;
    draw();
  }

  /* one turn = one more leaf on EACH side, so both trees always have the same number of leaves.
     The left picks the shallowest leaf (fill a level before going down); the right picks the leaf with the largest gain. */
  function step() {
    if (used >= BUDGET) return;

    var ls = leaves(lvl);
    var shallow = ls.reduce(function (a, b) { return b.d < a.d ? b : a; });
    split(shallow);

    var fs = leaves(leaf);
    leaves(leaf).forEach(function (l) { l.fresh = false; });
    var best = fs.reduce(function (a, b) { return b.g > a.g ? b : a; });
    split(best).forEach(function (k) { k.fresh = true; });

    used++;
    draw();
  }

  /* ---------- draw one tree ---------- */
  function treeSVG(root, hi) {
    var W = 330, H = 210, out = [], maxd = Math.max(2, depth(root));
    var rows = {};
    (function walk(n, d) {
      (rows[d] = rows[d] || []).push(n);
      if (n.kids) n.kids.forEach(function (k) { walk(k, d + 1); });
    })(root, 0);

    var pos = {};
    Object.keys(rows).forEach(function (d) {
      var r = rows[d], y = 24 + (H - 54) * (d / maxd);
      r.forEach(function (n, i) { pos[n.id] = { x: W * (i + 1) / (r.length + 1), y: y }; });
    });

    (function walk(n) {
      if (!n.kids) return;
      n.kids.forEach(function (k) {
        out.push('<line x1="' + pos[n.id].x.toFixed(1) + '" y1="' + pos[n.id].y +
          '" x2="' + pos[k.id].x.toFixed(1) + '" y2="' + pos[k.id].y + '" stroke="var(--rule)"></line>');
        walk(k);
      });
    })(root);

    leaves(root).forEach(function (n) {
      var p = pos[n.id], big = n.g > 1.2;
      var fresh = hi && n.fresh;
      out.push('<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y + '" r="9" fill="' +
        (fresh ? "rgba(var(--amber-a),.3)" : big ? "rgba(var(--blue-a),.2)" : "var(--raise)") +
        '" stroke="' + (fresh ? "var(--probe)" : big ? "var(--filled)" : "var(--rule)") + '"' +
        (fresh ? ' class="pop"' : "") + "></circle>");
    });
    (function walk(n) {
      if (!n.kids) return;
      var p = pos[n.id];
      out.push('<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y +
        '" r="9" fill="rgba(var(--green-a),.14)" stroke="var(--ok)"></circle>');
      n.kids.forEach(walk);
    })(root);

    return '<svg viewBox="0 0 ' + W + " " + H + '" aria-hidden="true">' + out.join("") + "</svg>";
  }

  function draw() {
    var nl = leaves(lvl).length, nf = leaves(leaf).length;
    el("lview").innerHTML =
      '<div class="cmp two lgbcmp">' +
        '<div><h5>Level-wise — XGBoost</h5>' +
          treeSVG(lvl, false) +
          "<p>" + nl + " leaves · depth " + depth(lvl) + ' · total gain <b class="n">' + total(lvl).toFixed(1) + "</b></p></div>" +
        '<div><h5>Leaf-wise — LightGBM</h5>' +
          treeSVG(leaf, true) +
          "<p>" + nf + " leaves · depth " + depth(leaf) + ' · total gain <b class="p">' + total(leaf).toFixed(1) + "</b></p></div>" +
      "</div>";

    el("lslider").innerHTML = '<i style="width:' + (100 * used / BUDGET) + '%"></i>';
    el("lstat").textContent = "turn " + used + "/" + BUDGET + " · " + nl + " leaves vs " + nf + " leaves";

    el("lexp").innerHTML = !used
      ? "Each turn both sides grow <b>exactly one more leaf</b> — the same budget. The left always picks the <b>shallowest leaf</b>, the right always picks the <b>leaf with the largest gain</b>, whatever level it is on."
      : "The same <b>" + nf + " leaves</b>, but the right is <b>" + depth(leaf) + "</b> levels deep while the left is only <b>" + depth(lvl) +
        "</b> — and the total gain is <b>" + total(leaf).toFixed(1) + "</b> versus <b>" +
        total(lvl).toFixed(1) + "</b>. The right <b>puts its leaves into the branches worth it</b>; the yellow ring marks the two leaves just grown.";

    var v = el("lverdict");
    v.hidden = used < 3;
    if (used >= 3) {
      v.innerHTML = "The tree is <b>strongly lopsided</b>: one branch goes very deep, the other stops early. That is why <code>max_depth</code> " +
        "<b>no longer reflects complexity</b> — you must rein it in with <code>num_leaves</code> plus <code>min_data_in_leaf</code>, " +
        "otherwise leaf-wise growth digs down to leaves holding only a few samples.";
    }
    el("lstep").disabled = used >= BUDGET;
    el("lauto").disabled = used >= BUDGET;
  }

  el("lstep").onclick = step;
  el("lauto").onclick = function () {
    if (timer) return;
    timer = setInterval(function () {
      step();
      if (used >= BUDGET) { clearInterval(timer); timer = null; }
    }, slow ? 620 : 40);
  };
  el("lrst").onclick = function () {
    if (timer) { clearInterval(timer); timer = null; }
    reset();
  };

  reset();
})();
