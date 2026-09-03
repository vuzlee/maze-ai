/* Lab mọc theo lá vs mọc theo tầng.
   Cùng một ngân sách lá, hai cây mọc song song: bên trái mở đều cả tầng, bên phải luôn chọn lá gain lớn nhất. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("lgblab")) return;

  var BUDGET = 8;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var timer = null;

  /* mỗi nút: gain của nó, và gain hai con sinh ra — giảm dần theo độ sâu, có nhánh giàu nhánh nghèo */
  function mk(gain, depth, rich) {
    return { g: gain, d: depth, rich: rich, kids: null, id: Math.random() };
  }
  function split(n) {
    /* nhánh "giàu" giữ được phần lớn gain khi đi sâu, nhánh nghèo tụt nhanh */
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

  /* một lượt = một lá mọc thêm ở MỖI bên, nên hai cây luôn cùng số lá.
     Bên trái chọn lá nông nhất (lấp đầy tầng trước khi xuống tầng sau); bên phải chọn lá gain lớn nhất. */
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

  /* ---------- vẽ một cây ---------- */
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
          '" x2="' + pos[k.id].x.toFixed(1) + '" y2="' + pos[k.id].y + '" stroke="#2E2822"></line>');
        walk(k);
      });
    })(root);

    leaves(root).forEach(function (n) {
      var p = pos[n.id], big = n.g > 1.2;
      var fresh = hi && n.fresh;
      out.push('<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y + '" r="9" fill="' +
        (fresh ? "rgba(237,180,74,.3)" : big ? "rgba(140,169,242,.2)" : "#241F1A") +
        '" stroke="' + (fresh ? "#EDB44A" : big ? "#8CA9F2" : "#2E2822") + '"' +
        (fresh ? ' class="pop"' : "") + "></circle>");
    });
    (function walk(n) {
      if (!n.kids) return;
      var p = pos[n.id];
      out.push('<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y +
        '" r="9" fill="rgba(91,207,160,.14)" stroke="#5BCFA0"></circle>');
      n.kids.forEach(walk);
    })(root);

    return '<svg viewBox="0 0 ' + W + " " + H + '" aria-hidden="true">' + out.join("") + "</svg>";
  }

  function draw() {
    var nl = leaves(lvl).length, nf = leaves(leaf).length;
    el("lview").innerHTML =
      '<div class="cmp two lgbcmp">' +
        '<div><h5>Mọc theo tầng — XGBoost</h5>' +
          treeSVG(lvl, false) +
          "<p>" + nl + " lá · sâu " + depth(lvl) + ' · gain thu được <b class="n">' + total(lvl).toFixed(1).replace(".", ",") + "</b></p></div>" +
        '<div><h5>Mọc theo lá — LightGBM</h5>' +
          treeSVG(leaf, true) +
          "<p>" + nf + " lá · sâu " + depth(leaf) + ' · gain thu được <b class="p">' + total(leaf).toFixed(1).replace(".", ",") + "</b></p></div>" +
      "</div>";

    el("lslider").innerHTML = '<i style="width:' + (100 * used / BUDGET) + '%"></i>';
    el("lstat").textContent = "lượt " + used + "/" + BUDGET + " · " + nl + " lá vs " + nf + " lá";

    el("lexp").innerHTML = !used
      ? "Mỗi lượt hai bên đều mọc thêm <b>đúng một lá</b> — cùng ngân sách. Bên trái luôn chọn <b>lá nông nhất</b>, bên phải luôn chọn <b>lá có gain lớn nhất</b>, bất kể nó nằm ở tầng nào."
      : "Cùng <b>" + nf + " lá</b>, nhưng bên phải sâu <b>" + depth(leaf) + "</b> tầng còn bên trái chỉ <b>" + depth(lvl) +
        "</b> — và gain thu được <b>" + total(leaf).toFixed(1).replace(".", ",") + "</b> so với <b>" +
        total(lvl).toFixed(1).replace(".", ",") + "</b>. Bên phải <b>dồn lá vào nhánh đáng giá</b>; vòng vàng là hai lá vừa mọc.";

    var v = el("lverdict");
    v.hidden = used < 3;
    if (used >= 3) {
      v.innerHTML = "Cây <b>lệch hẳn</b>: một nhánh xuống rất sâu, nhánh kia dừng sớm. Đó là lý do <code>max_depth</code> " +
        "<b>không còn phản ánh độ phức tạp</b> — phải chặn bằng <code>num_leaves</code> kèm <code>min_data_in_leaf</code>, " +
        "nếu không leaf-wise sẽ đào tới những chiếc lá chỉ còn vài mẫu.";
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
