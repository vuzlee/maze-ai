/* Lab gain — kéo λ và γ, xem công thức tự quyết định tách hay dừng.
   8 mẫu, mỗi mẫu một cặp (g, h); thử mọi ngưỡng, tính Obj* trước và sau, gain quyết định. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("xgblab")) return;

  /* mẫu · g (độ dốc) · h (độ cong) — nhóm trái âm rõ, nhóm phải dương rõ, hai mẫu ở giữa mập mờ */
  var G = [-2.4, -2.1, -1.8, -0.4, 0.3, 1.9, 2.2, 2.5];
  var H = [1.0, 1.0, 1.0, 0.9, 0.9, 1.0, 1.0, 1.0];
  var X = [1, 2, 3, 4, 5, 6, 7, 8];
  var THR = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5];
  var N = X.length;

  var lam = 1, gam = 0.5, cut = 4.5;
  var slow = !window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function fmt(x) { return (Math.round(x * 100) / 100).toFixed(2).replace(".", ",").replace("-", "−"); }
  function sum(a, f) { var s = 0; a.forEach(function (v, i) { s += f(v, i); }); return s; }
  function score(idx) {                    /* − ½ G²/(H+λ), phần điểm của một lá */
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
    '<p class="labrow"><b>1.</b> Tám mẫu ở nút này — mỗi mẫu mang sẵn một cặp <b>(g, h)</b> tính từ loss</p>' +
    '<div id="xstrip"></div>' +
    '<p class="stripnote" id="xnote"><span></span><span></span></p>' +
    '<p class="labrow"><b>2.</b> Gain của mọi ngưỡng — bấm vào một thanh để xem chi tiết</p>' +
    '<div id="xbars"></div>';

  function draw() {
    var s = sides(cut), root = score(all()), L = score(s.L), R = score(s.R), g = gainAt(cut);

    /* dãy mẫu, vạch cắt ở đúng ngưỡng */
    var h = '<div class="strip">';
    X.forEach(function (x, i) {
      if (x > cut && X[i - 1] < cut) h += '<div class="cut"></div>';
      h += '<div class="c ' + (G[i] < 0 ? "t" : "f") + '"><i>' + x + "</i><b>" +
        (G[i] > 0 ? "+" : "−") + fmt(Math.abs(G[i])) + "</b><u>h " + fmt(H[i]) + "</u></div>";
    });
    el("xstrip").innerHTML = h + "</div>";

    el("xnote").innerHTML =
      "<span>lá trái: G " + fmt(L.g) + " · H " + fmt(L.h) + " → w* <em>" + fmt(L.w) + "</em></span>" +
      "<span>ngưỡng <em>" + fmt(cut) + "</em></span>" +
      "<span>lá phải: G " + fmt(R.g) + " · H " + fmt(R.h) + " → w* <em>" + fmt(R.w) + "</em></span>";

    /* mọi ngưỡng */
    var best = THR.reduce(function (a, b) { return gainAt(b) > gainAt(a) ? b : a; });
    var mx = Math.max(0.01, gainAt(best));
    el("xbars").innerHTML = '<div class="bars">' + THR.map(function (t) {
      var v = gainAt(t), pos = v > 0;
      return '<div class="b' + (t === cut ? " hi" : (pos ? "" : " bad")) + '" data-t="' + t +
        '" style="cursor:pointer;margin:5px 0"><i>ngưỡng ' + fmt(t) + "</i>" +
        '<u style="width:' + Math.max(1, 100 * Math.abs(v) / mx).toFixed(1) + '%"></u>' +
        "<b>" + (v > 0 ? "+" : "−") + fmt(Math.abs(v)) + (t === best ? " ★" : "") + "</b></div>";
    }).join("") + "</div>";
    [].slice.call(el("xbars").querySelectorAll(".b")).forEach(function (b) {
      b.onclick = function () { cut = parseFloat(b.getAttribute("data-t")); draw(); };
    });

    el("xexp").innerHTML = g > 0
      ? "Gain <b>" + fmt(g) + " &gt; 0</b> → <b>tách</b>. Hai lá trả về <b>" + fmt(L.w) + "</b> và <b>" + fmt(R.w) +
        "</b> — không dò, tính thẳng bằng <code>−G/(H+λ)</code>."
      : "Gain <b>" + fmt(g) + " ≤ 0</b> → <b>không tách</b>, nút này thành lá trả về <b>" + fmt(root.w) +
        "</b>. Cái giá γ = " + fmt(gam) + " của một chiếc lá mới lớn hơn phần lợi thu được.";

    el("xstat").textContent = "λ = " + fmt(lam) + " · γ = " + fmt(gam) +
      " · ngưỡng tốt nhất " + fmt(best) + " (gain " + fmt(gainAt(best)) + ")";

    var v = el("xverdict"), pos = 0;
    THR.forEach(function (t) { if (gainAt(t) > 0) pos++; });
    v.hidden = false;
    v.innerHTML = pos
      ? "Còn <b>" + pos + "/" + THR.length + "</b> ngưỡng có gain dương — cây vẫn mọc tiếp. " +
        "Tăng <b>γ</b> để tính tiền mỗi chiếc lá, hoặc tăng <b>λ</b> để ghìm giá trị lá về 0: cả hai đều nằm <b>trong công thức</b>, không phải bước cắt tỉa sau."
      : "<b>Không ngưỡng nào còn gain dương</b> — cây tự dừng ở đây. Chống overfit và mọc cây là <b>một việc</b>, vì cùng đọc một hàm mục tiêu.";
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
        knob("xlam", lam, [0, 1, 5, 20], function (v) { lam = v; });
        knob("xgam", gam, [0, 0.5, 2, 8], function (v) { gam = v; });
        draw();
      };
    });
  }
  knob("xlam", lam, [0, 1, 5, 20], function (v) { lam = v; });
  knob("xgam", gam, [0, 0.5, 2, 8], function (v) { gam = v; });

  el("xrst").onclick = function () {
    lam = 1; gam = 0.5; cut = 4.5;
    knob("xlam", lam, [0, 1, 5, 20], function (v) { lam = v; });
    knob("xgam", gam, [0, 0.5, 2, 8], function (v) { gam = v; });
    draw();
  };

  draw();
})();
