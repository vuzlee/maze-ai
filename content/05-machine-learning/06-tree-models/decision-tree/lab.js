/* Lab chọn điểm chia — đoán trước, xem gain của MỌI ngưỡng, rồi so với lựa chọn của thuật toán. */
(function () {
  var el = function (id) { return document.getElementById(id); };
  if (!el("splab")) return;

  /* 12 mẫu trên một trục, hai lớp — có nhiễu để gain không đơn điệu */
  var X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  var Y = ["A", "A", "A", "B", "A", "A", "B", "B", "B", "A", "B", "B"];
  var THR = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5];

  var crit = "gini", cut = 3.5, found = false;

  function impurity(g) {
    if (!g.length) return 0;
    var a = 0;
    g.forEach(function (v) { if (v === "A") a++; });
    var p = a / g.length, q = 1 - p;
    if (crit === "gini") return 1 - p * p - q * q;
    var h = 0;
    [p, q].forEach(function (v) { if (v > 0) h -= v * Math.log2(v); });
    return h;
  }
  function split(t) {
    var L = [], R = [];
    Y.forEach(function (y, i) { (X[i] < t ? L : R).push(y); });
    return { L: L, R: R };
  }
  function gainAt(t) {
    var s = split(t), n = Y.length;
    return impurity(Y) - (s.L.length / n * impurity(s.L) + s.R.length / n * impurity(s.R));
  }
  function fmt(x) { return x.toFixed(3).replace(".", ","); }
  function cls(g) {
    var a = 0; g.forEach(function (v) { if (v === "A") a++; });
    return a + " × A · " + (g.length - a) + " × B";
  }

  /* ---------- tiêu chí ---------- */
  el("scrit").innerHTML =
    '<button data-c="gini" class="on">Gini</button><button data-c="entropy">Entropy</button>';
  [].slice.call(el("scrit").querySelectorAll("button")).forEach(function (b) {
    b.onclick = function () {
      [].slice.call(el("scrit").querySelectorAll("button")).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      crit = b.getAttribute("data-c");
      draw();
    };
  });

  /* ---------- vẽ ---------- */
  function draw() {
    /* dãy mẫu, có vạch cắt chèn đúng vị trí ngưỡng */
    var h = '<div class="strip">';
    X.forEach(function (x, i) {
      if (x > cut && X[i - 1] < cut) h += '<div class="cut"></div>';
      h += '<div class="c ' + (Y[i] === "A" ? "f" : "t") + '"><i>' + x + "</i><b>" + Y[i] + "</b></div>";
    });
    el("sview").innerHTML = h + "</div>";

    var s = split(cut), n = Y.length;
    var g = gainAt(cut);
    el("snote").innerHTML =
      "<span>trái: " + cls(s.L) + " · độ vẩn <em>" + fmt(impurity(s.L)) + "</em></span>" +
      "<span>ngưỡng <em>" + String(cut).replace(".", ",") + "</em></span>" +
      "<span>phải: " + cls(s.R) + " · độ vẩn <em>" + fmt(impurity(s.R)) + "</em></span>";

    /* gain của MỌI ngưỡng — bấm vào để chọn */
    var best = THR.reduce(function (a, b) { return gainAt(b) > gainAt(a) ? b : a; });
    var mx = gainAt(best);
    el("sgain").innerHTML =
      '<div class="explain" style="padding-bottom:6px"><h6>Gain của từng ngưỡng — bấm để xem</h6>' +
      '<div class="bars">' + THR.map(function (t) {
        var v = gainAt(t);
        var k = t === cut ? " hi" : (t === best ? "" : "");
        return '<div class="b' + k + '" data-t="' + t + '" style="cursor:pointer;margin:5px 0">' +
          "<i>" + String(t).replace(".", ",") + "</i>" +
          '<u style="width:' + (100 * v / mx).toFixed(1) + '%"></u>' +
          "<b>" + fmt(v) + (t === best ? " ★" : "") + "</b></div>";
      }).join("") + "</div></div>";
    [].slice.call(el("sgain").querySelectorAll(".b")).forEach(function (b) {
      b.onclick = function () { cut = parseFloat(b.getAttribute("data-t")); found = false; draw(); };
    });

    /* giải thích bằng số thật của ngưỡng đang chọn */
    el("sexp").innerHTML =
      "<h6>Tính gain ở ngưỡng " + String(cut).replace(".", ",") + "</h6>" +
      "<p>Nút cha " + n + " mẫu, " + cls(Y) + " → độ vẩn <b>" + fmt(impurity(Y)) + "</b>.</p>" +
      "<p>Trái " + s.L.length + " mẫu (" + cls(s.L) + ") → " + fmt(impurity(s.L)) + "<br>" +
      "Phải " + s.R.length + " mẫu (" + cls(s.R) + ") → " + fmt(impurity(s.R)) + "</p>" +
      '<p class="vals">gain = ' + fmt(impurity(Y)) + " − (" +
      (s.L.length / n).toFixed(2).replace(".", ",") + "×" + fmt(impurity(s.L)) + " + " +
      (s.R.length / n).toFixed(2).replace(".", ",") + "×" + fmt(impurity(s.R)) + ") = <b>" + fmt(g) + "</b></p>";

    el("sstat").textContent = "tiêu chí " + (crit === "gini" ? "Gini" : "Entropy") +
      " · ngưỡng tốt nhất " + String(best).replace(".", ",");

    var v = el("sverdict");
    if (found) {
      v.hidden = false;
      v.innerHTML = "Thuật toán chọn <b>ngưỡng " + String(best).replace(".", ",") + "</b>, gain <b>" + fmt(mx) + "</b>. " +
        "Đổi tiêu chí sang " + (crit === "gini" ? "Entropy" : "Gini") +
        ": con số khác hẳn nhưng <b>ngưỡng tốt nhất vẫn thế</b> — đó là lý do chọn Gini hay Entropy hiếm khi đổi cây, " +
        "và Gini được dùng mặc định vì rẻ hơn (không có logarithm).";
    } else {
      v.hidden = true;
    }
  }

  el("sbest").onclick = function () {
    cut = THR.reduce(function (a, b) { return gainAt(b) > gainAt(a) ? b : a; });
    found = true;
    draw();
  };
  el("srst").onclick = function () { cut = 3.5; found = false; draw(); };

  draw();
})();
